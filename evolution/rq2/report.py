from collections import Counter
from dataclasses import dataclass
import itertools
from pathlib import Path
from typing import Any, Literal
import numpy as np

from evolution.rq2.config import RQ2Config
from evolution.rq2.evaluate import build_user_payload, load_evaluation_prompt
from evolution.rq2.llm_client import build_chat_request_payload
from evolution.rq2.models import EvaluationRecord, TranscriptRecord
from evolution.rq2.ratings import (
    ALLOWED_DIMENSIONS,
    ALLOWED_RATERS,
    RatingRow,
    export_llm_ratings,
    read_rating_csv,
)
from evolution.rq2.storage import read_csv, read_json, write_csv

COVERAGE_FIELDNAMES = [
    "method_id",
    "rater_id",
    "dimension",
    "n_expected",
    "n_scored",
    "n_pending",
    "n_failed",
    "scorable_rate",
]

DISTRIBUTION_FIELDNAMES = [
    "method_id",
    "rater_id",
    "dimension",
    "score",
    "count",
    "proportion",
]

SUMMARY_FIELDNAMES = [
    "method_id",
    "rater_id",
    "dimension",
    "n",
    "mean",
    "median",
    "q1",
    "q3",
]

PAIRED_FIELDNAMES = [
    "rater_id",
    "dimension",
    "method_a",
    "method_b",
    "n_pairs",
    "mean_difference",
    "median_difference",
    "n_a_higher",
    "n_equal",
    "n_b_higher",
    "ci_low",
    "ci_high",
    "bootstrap_valid_repeats",
    "reason",
]

AGREEMENT_FIELDNAMES = [
    "rater_group",
    "dimension",
    "n_units",
    "n_cases",
    "n_ratings",
    "n_units_2_ratings",
    "n_units_3_ratings",
    "n_units_4_ratings",
    "alpha",
    "ci_low",
    "ci_high",
    "bootstrap_valid_repeats",
    "reason",
]


@dataclass(frozen=True)
class ReportSummary:
    coverage_path: Path
    distributions_path: Path
    summary_path: Path
    paired_path: Path
    agreement_path: Path
    report_md_path: Path


def compute_ordinal_krippendorff_alpha(
    units: list[list[int]],
) -> tuple[float | None, str | None]:
    valid_units = [u for u in units if len(u) >= 2]
    if len(valid_units) < 2:
        return None, "Fewer than 2 pairable units"

    categories = [1, 2, 3, 4, 5]
    num_cats = len(categories)
    c_to_idx = {c: i for i, c in enumerate(categories)}

    o_ck = np.zeros((num_cats, num_cats), dtype=float)
    for u in valid_units:
        m_u = len(u)
        counts = np.zeros(num_cats, dtype=float)
        for val in u:
            counts[c_to_idx[val]] += 1
        for c_idx in range(num_cats):
            if counts[c_idx] == 0:
                continue
            for k_idx in range(num_cats):
                identity = 1.0 if c_idx == k_idx else 0.0
                o_ck[c_idx, k_idx] += counts[c_idx] * (counts[k_idx] - identity) / (m_u - 1)

    n_c = o_ck.sum(axis=1)
    n = n_c.sum()
    if n <= 1:
        return None, "Total ratings n <= 1"

    delta_sq = np.zeros((num_cats, num_cats), dtype=float)
    for c_idx in range(num_cats):
        for k_idx in range(num_cats):
            low = min(c_idx, k_idx)
            high = max(c_idx, k_idx)
            sum_g = n_c[low : high + 1].sum()
            diff = sum_g - (n_c[c_idx] + n_c[k_idx]) / 2.0
            delta_sq[c_idx, k_idx] = diff**2

    Do = (o_ck * delta_sq).sum() / n

    denom_matrix = np.zeros((num_cats, num_cats), dtype=float)
    for c_idx in range(num_cats):
        for k_idx in range(num_cats):
            identity = 1.0 if c_idx == k_idx else 0.0
            denom_matrix[c_idx, k_idx] = n_c[c_idx] * (n_c[k_idx] - identity)

    De = (denom_matrix * delta_sq).sum() / (n * (n - 1.0))
    if De == 0.0:
        return None, "De is zero (no variance in ratings across categories)"

    alpha = 1.0 - (Do / De)
    return float(alpha), None


def _format_float(val: float | None, precision: int = 4) -> str:
    if val is None or np.isnan(val):
        return ""
    return f"{val:.{precision}f}"


def generate_reports(
    config: RQ2Config,
    prompt_path: Path | None = None,
) -> ReportSummary:
    artifacts_root = config.paths.artifacts_root
    inventory_path = artifacts_root / "input_inventory.csv"
    if not inventory_path.exists():
        raise FileNotFoundError(
            f"Input inventory not found at {inventory_path}. Run input preparation first."
        )

    inventory_rows = read_csv(inventory_path)
    ready_items = [r for r in inventory_rows if r.get("prepare_status") == "ready"]
    ready_case_methods = {(r["case_id"], r["method_id"]) for r in ready_items}

    # 1. Refresh LLM CSVs
    export_llm_ratings(config, "llm_expert_1", prompt_path=prompt_path)
    export_llm_ratings(config, "llm_expert_2", prompt_path=prompt_path)

    # 2. Load all transcripts to validate human ratings and compute transcript lengths
    transcripts_map: dict[tuple[str, str], TranscriptRecord] = {}
    for item in ready_items:
        c_id = item["case_id"]
        m_id = item["method_id"]
        t_path = artifacts_root / "cases" / c_id / m_id / "transcript.json"
        if not t_path.exists():
            raise FileNotFoundError(
                f"Transcript artifact missing for ready case '{c_id}', method '{m_id}' at {t_path}"
            )
        try:
            t_data = read_json(t_path)
            record = TranscriptRecord.model_validate(t_data)
        except Exception as exc:
            raise ValueError(f"Corrupt transcript artifact at {t_path}: {exc}") from exc
        transcripts_map[(c_id, m_id)] = record

    # 3. Read rating records for all four raters
    known_inventory_keys = {(r["case_id"], r["method_id"]) for r in inventory_rows}
    all_ratings: dict[str, list[RatingRow]] = {}
    unincluded_historical_rows_count = 0

    for rater_id in ALLOWED_RATERS:
        csv_path = artifacts_root / "ratings" / f"{rater_id}.csv"
        if csv_path.exists():
            rows = read_rating_csv(
                csv_path,
                expected_rater_id=rater_id,
            )
            for r in rows:
                if (r.case_id, r.method_id) not in known_inventory_keys:
                    raise ValueError(
                        f"Rating file '{csv_path}' contains unknown case/method key "
                        f"{(r.case_id, r.method_id)} not present in inventory."
                    )
                if (r.case_id, r.method_id) not in ready_case_methods:
                    unincluded_historical_rows_count += 1
            all_ratings[rater_id] = rows
        else:
            all_ratings[rater_id] = []

    # 4. Source inventory statistics
    total_cases = len({r["case_id"] for r in inventory_rows if r.get("case_id")})
    total_inventory_items = len(inventory_rows)
    status_counts = Counter(r.get("prepare_status", "") for r in inventory_rows)
    ready_count = status_counts.get("ready", 0)
    source_incomplete_count = status_counts.get("source_incomplete", 0)
    input_error_count = status_counts.get("input_error", 0)

    ending_obs_counts = Counter(r.get("ending_observation", "") for r in inventory_rows if r.get("ending_observation"))
    turn_limit_reached_count = ending_obs_counts.get("turn_limit_reached", 0)
    unknown_ending_count = ending_obs_counts.get("unknown", 0)

    method_turn_stats: dict[str, dict[str, Any]] = {}
    for method_id in config.methods:
        turns = [
            transcripts_map[(c, m)].completed_turns
            for (c, m) in ready_case_methods
            if m == method_id and (c, m) in transcripts_map
        ]
        if turns:
            method_turn_stats[method_id] = {
                "min": min(turns),
                "max": max(turns),
                "median": _format_float(float(np.median(turns))),
            }
        else:
            method_turn_stats[method_id] = {
                "min": "-",
                "max": "-",
                "median": "-",
            }

    # 4. Compute coverage
    system_prompt = load_evaluation_prompt(prompt_path)
    reports_dir = artifacts_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    coverage_rows: list[dict[str, Any]] = []

    for method_id in config.methods:
        method_ready = [r for r in ready_items if r["method_id"] == method_id]
        n_expected = len(method_ready)

        for rater_id in ALLOWED_RATERS:
            is_llm = rater_id.startswith("llm_")
            ratings_for_rater = [
                r for r in all_ratings[rater_id]
                if r.method_id == method_id and (r.case_id, r.method_id) in ready_case_methods
            ]

            for dim in ALLOWED_DIMENSIONS:
                dim_ratings = [r for r in ratings_for_rater if r.dimension == dim]
                n_scored = sum(1 for r in dim_ratings if r.status == "scored" and r.score is not None)

                n_failed = 0
                n_pending = 0

                if is_llm:
                    judge_conf = config.judges[rater_id]
                    for item in method_ready:
                        c_id = item["case_id"]
                        rec_path = artifacts_root / "cases" / c_id / method_id / f"{rater_id}.json"
                        if not rec_path.exists():
                            n_pending += 1
                            continue

                        try:
                            rec_data = read_json(rec_path)
                            eval_rec = EvaluationRecord.model_validate(rec_data)
                        except Exception:
                            n_pending += 1
                            continue

                        transcript = transcripts_map.get((c_id, method_id))
                        if transcript is None:
                            n_pending += 1
                            continue

                        u_payload = build_user_payload(transcript)
                        expected_req = build_chat_request_payload(
                            model_name=judge_conf.model_name,
                            system_prompt=system_prompt,
                            user_payload=u_payload,
                            temperature=judge_conf.temperature,
                        )

                        is_matching_call = eval_rec.call.request == expected_req

                        if not is_matching_call:
                            n_pending += 1
                        elif eval_rec.status == "failed":
                            n_failed += 1
                else:
                    # Human raters: missing or empty rows are pending, failed is always 0
                    evaluated_cases = {r.case_id for r in dim_ratings if r.status == "scored"}
                    n_pending = n_expected - len(evaluated_cases)
                    n_failed = 0

                scorable_rate = (n_scored / n_expected) if n_expected > 0 else None

                coverage_rows.append({
                    "method_id": method_id,
                    "rater_id": rater_id,
                    "dimension": dim,
                    "n_expected": n_expected,
                    "n_scored": n_scored,
                    "n_pending": n_pending,
                    "n_failed": n_failed,
                    "scorable_rate": _format_float(scorable_rate),
                })

    write_csv(reports_dir / "coverage.csv", coverage_rows, fieldnames=COVERAGE_FIELDNAMES)

    # 5. Score distributions and summary statistics
    dist_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for method_id in config.methods:
        for rater_id in ALLOWED_RATERS:
            for dim in ALLOWED_DIMENSIONS:
                scores = [
                    r.score for r in all_ratings[rater_id]
                    if r.method_id == method_id
                    and r.dimension == dim
                    and (r.case_id, r.method_id) in ready_case_methods
                    and r.status == "scored"
                    and r.score is not None
                ]
                n_scored = len(scores)

                for score_val in [1, 2, 3, 4, 5]:
                    cnt = scores.count(score_val)
                    prop = (cnt / n_scored) if n_scored > 0 else None
                    dist_rows.append({
                        "method_id": method_id,
                        "rater_id": rater_id,
                        "dimension": dim,
                        "score": score_val,
                        "count": cnt,
                        "proportion": _format_float(prop),
                    })

                if n_scored > 0:
                    arr = np.array(scores, dtype=float)
                    s_mean = float(np.mean(arr))
                    s_median = float(np.median(arr))
                    s_q1 = float(np.quantile(arr, 0.25, method="linear"))
                    s_q3 = float(np.quantile(arr, 0.75, method="linear"))
                    summary_rows.append({
                        "method_id": method_id,
                        "rater_id": rater_id,
                        "dimension": dim,
                        "n": n_scored,
                        "mean": _format_float(s_mean),
                        "median": _format_float(s_median),
                        "q1": _format_float(s_q1),
                        "q3": _format_float(s_q3),
                    })
                else:
                    summary_rows.append({
                        "method_id": method_id,
                        "rater_id": rater_id,
                        "dimension": dim,
                        "n": 0,
                        "mean": "",
                        "median": "",
                        "q1": "",
                        "q3": "",
                    })

    write_csv(reports_dir / "score_distributions.csv", dist_rows, fieldnames=DISTRIBUTION_FIELDNAMES)
    write_csv(reports_dir / "score_summary.csv", summary_rows, fieldnames=SUMMARY_FIELDNAMES)

    # 6. Paired comparisons
    rng = np.random.default_rng(config.statistics.random_seed)
    bootstrap_repeats = config.statistics.bootstrap_repeats

    paired_rows: list[dict[str, Any]] = []
    method_pairs = list(itertools.combinations(config.methods, 2))

    for rater_id in ALLOWED_RATERS:
        for dim in ALLOWED_DIMENSIONS:
            score_by_case_method: dict[tuple[str, str], int] = {
                (r.case_id, r.method_id): r.score
                for r in all_ratings[rater_id]
                if r.dimension == dim
                and (r.case_id, r.method_id) in ready_case_methods
                and r.status == "scored"
                and r.score is not None
            }

            for m_a, m_b in method_pairs:
                common_cases = [
                    item["case_id"] for item in ready_items
                    if (item["case_id"], m_a) in score_by_case_method
                    and (item["case_id"], m_b) in score_by_case_method
                ]
                # Unique cases in order
                unique_cases = sorted(set(common_cases))
                diffs = [
                    score_by_case_method[(cid, m_a)] - score_by_case_method[(cid, m_b)]
                    for cid in unique_cases
                ]
                n_pairs = len(diffs)

                if n_pairs == 0:
                    paired_rows.append({
                        "rater_id": rater_id,
                        "dimension": dim,
                        "method_a": m_a,
                        "method_b": m_b,
                        "n_pairs": 0,
                        "mean_difference": "",
                        "median_difference": "",
                        "n_a_higher": 0,
                        "n_equal": 0,
                        "n_b_higher": 0,
                        "ci_low": "",
                        "ci_high": "",
                        "bootstrap_valid_repeats": 0,
                        "reason": "No pairable cases with scores for both methods",
                    })
                elif n_pairs < 2:
                    diff_arr = np.array(diffs, dtype=float)
                    paired_rows.append({
                        "rater_id": rater_id,
                        "dimension": dim,
                        "method_a": m_a,
                        "method_b": m_b,
                        "n_pairs": 1,
                        "mean_difference": _format_float(float(np.mean(diff_arr))),
                        "median_difference": _format_float(float(np.median(diff_arr))),
                        "n_a_higher": int(np.sum(diff_arr > 0)),
                        "n_equal": int(np.sum(diff_arr == 0)),
                        "n_b_higher": int(np.sum(diff_arr < 0)),
                        "ci_low": "",
                        "ci_high": "",
                        "bootstrap_valid_repeats": 0,
                        "reason": "Fewer than 2 paired cases",
                    })
                else:
                    diff_arr = np.array(diffs, dtype=float)
                    boot_means: list[float] = []
                    for _ in range(bootstrap_repeats):
                        sample_indices = rng.integers(0, n_pairs, size=n_pairs)
                        sample_mean = float(np.mean(diff_arr[sample_indices]))
                        boot_means.append(sample_mean)

                    ci_low = float(np.percentile(boot_means, 2.5))
                    ci_high = float(np.percentile(boot_means, 97.5))

                    paired_rows.append({
                        "rater_id": rater_id,
                        "dimension": dim,
                        "method_a": m_a,
                        "method_b": m_b,
                        "n_pairs": n_pairs,
                        "mean_difference": _format_float(float(np.mean(diff_arr))),
                        "median_difference": _format_float(float(np.median(diff_arr))),
                        "n_a_higher": int(np.sum(diff_arr > 0)),
                        "n_equal": int(np.sum(diff_arr == 0)),
                        "n_b_higher": int(np.sum(diff_arr < 0)),
                        "ci_low": _format_float(ci_low),
                        "ci_high": _format_float(ci_high),
                        "bootstrap_valid_repeats": bootstrap_repeats,
                        "reason": "",
                    })

    write_csv(reports_dir / "paired_comparisons.csv", paired_rows, fieldnames=PAIRED_FIELDNAMES)

    # 7. Ordinal Krippendorff's alpha and Case-level bootstrap
    agreement_rows: list[dict[str, Any]] = []
    group_contributions_summary: list[dict[str, Any]] = []
    rater_groups: list[tuple[str, list[str]]] = [
        ("llm_pair", ["llm_expert_1", "llm_expert_2"]),
        ("human_pair", ["human_expert_1", "human_expert_2"]),
        ("all_four", ["llm_expert_1", "llm_expert_2", "human_expert_1", "human_expert_2"]),
    ]

    for group_name, raters_in_group in rater_groups:
        for dim in ALLOWED_DIMENSIONS:
            unit_ratings_map: dict[tuple[str, str], dict[str, int]] = {}
            for item in ready_items:
                c_id = item["case_id"]
                m_id = item["method_id"]
                u_key = (c_id, m_id)
                r_map: dict[str, int] = {}
                for r_id in raters_in_group:
                    match_row = next(
                        (
                            r for r in all_ratings[r_id]
                            if r.case_id == c_id
                            and r.method_id == m_id
                            and r.dimension == dim
                            and r.status == "scored"
                            and r.score is not None
                        ),
                        None,
                    )
                    if match_row is not None and match_row.score is not None:
                        r_map[r_id] = match_row.score
                unit_ratings_map[u_key] = r_map

            pairable_units_map = {
                u_key: r_map for u_key, r_map in unit_ratings_map.items() if len(r_map) >= 2
            }
            n_units = len(pairable_units_map)
            n_cases = len({k[0] for k in pairable_units_map.keys()})
            n_ratings = sum(len(m) for m in pairable_units_map.values())
            n_2 = sum(1 for m in pairable_units_map.values() if len(m) == 2)
            n_3 = sum(1 for m in pairable_units_map.values() if len(m) == 3)
            n_4 = sum(1 for m in pairable_units_map.values() if len(m) == 4)

            contributions = {
                r_id: sum(1 for m in pairable_units_map.values() if r_id in m)
                for r_id in raters_in_group
            }
            group_contributions_summary.append({
                "rater_group": group_name,
                "dimension": dim,
                **{r_id: contributions.get(r_id, 0) for r_id in ALLOWED_RATERS},
            })

            if any(cnt == 0 for cnt in contributions.values()):
                agreement_rows.append({
                    "rater_group": group_name,
                    "dimension": dim,
                    "n_units": n_units,
                    "n_cases": n_cases,
                    "n_ratings": n_ratings,
                    "n_units_2_ratings": n_2,
                    "n_units_3_ratings": n_3,
                    "n_units_4_ratings": n_4,
                    "alpha": "",
                    "ci_low": "",
                    "ci_high": "",
                    "bootstrap_valid_repeats": 0,
                    "reason": "One or more raters in group have zero valid ratings in pairable units",
                })
                continue

            if n_units < 2:
                agreement_rows.append({
                    "rater_group": group_name,
                    "dimension": dim,
                    "n_units": n_units,
                    "n_cases": n_cases,
                    "n_ratings": n_ratings,
                    "n_units_2_ratings": n_2,
                    "n_units_3_ratings": n_3,
                    "n_units_4_ratings": n_4,
                    "alpha": "",
                    "ci_low": "",
                    "ci_high": "",
                    "bootstrap_valid_repeats": 0,
                    "reason": "Fewer than 2 pairable units with m_u >= 2",
                })
                continue

            units_list = [list(r_map.values()) for r_map in pairable_units_map.values()]
            alpha_val, alpha_reason = compute_ordinal_krippendorff_alpha(units_list)

            if alpha_val is None:
                agreement_rows.append({
                    "rater_group": group_name,
                    "dimension": dim,
                    "n_units": n_units,
                    "n_cases": n_cases,
                    "n_ratings": n_ratings,
                    "n_units_2_ratings": n_2,
                    "n_units_3_ratings": n_3,
                    "n_units_4_ratings": n_4,
                    "alpha": "",
                    "ci_low": "",
                    "ci_high": "",
                    "bootstrap_valid_repeats": 0,
                    "reason": alpha_reason or "Alpha undefined",
                })
                continue

            valid_cases = sorted({k[0] for k in pairable_units_map.keys()})
            if len(valid_cases) < 2:
                agreement_rows.append({
                    "rater_group": group_name,
                    "dimension": dim,
                    "n_units": n_units,
                    "n_cases": n_cases,
                    "n_ratings": n_ratings,
                    "n_units_2_ratings": n_2,
                    "n_units_3_ratings": n_3,
                    "n_units_4_ratings": n_4,
                    "alpha": _format_float(alpha_val),
                    "ci_low": "",
                    "ci_high": "",
                    "bootstrap_valid_repeats": 0,
                    "reason": "Fewer than 2 valid cases for bootstrap",
                })
                continue

            case_to_units: dict[str, list[list[int]]] = {}
            for (cid, mid), r_map in pairable_units_map.items():
                case_to_units.setdefault(cid, []).append(list(r_map.values()))

            boot_alphas: list[float] = []
            n_valid_cases = len(valid_cases)

            for _ in range(bootstrap_repeats):
                sampled_case_indices = rng.integers(0, n_valid_cases, size=n_valid_cases)
                resampled_units: list[list[int]] = []
                for idx in sampled_case_indices:
                    cid = valid_cases[idx]
                    resampled_units.extend(case_to_units[cid])

                b_alpha, _ = compute_ordinal_krippendorff_alpha(resampled_units)
                if b_alpha is not None and not np.isnan(b_alpha):
                    boot_alphas.append(b_alpha)

            valid_boot_count = len(boot_alphas)
            if valid_boot_count < 2:
                agreement_rows.append({
                    "rater_group": group_name,
                    "dimension": dim,
                    "n_units": n_units,
                    "n_cases": n_cases,
                    "n_ratings": n_ratings,
                    "n_units_2_ratings": n_2,
                    "n_units_3_ratings": n_3,
                    "n_units_4_ratings": n_4,
                    "alpha": _format_float(alpha_val),
                    "ci_low": "",
                    "ci_high": "",
                    "bootstrap_valid_repeats": valid_boot_count,
                    "reason": "Fewer than 2 valid bootstrap replicates with non-zero De",
                })
            else:
                ci_low = float(np.percentile(boot_alphas, 2.5))
                ci_high = float(np.percentile(boot_alphas, 97.5))
                agreement_rows.append({
                    "rater_group": group_name,
                    "dimension": dim,
                    "n_units": n_units,
                    "n_cases": n_cases,
                    "n_ratings": n_ratings,
                    "n_units_2_ratings": n_2,
                    "n_units_3_ratings": n_3,
                    "n_units_4_ratings": n_4,
                    "alpha": _format_float(alpha_val),
                    "ci_low": _format_float(ci_low),
                    "ci_high": _format_float(ci_high),
                    "bootstrap_valid_repeats": valid_boot_count,
                    "reason": "",
                })

    write_csv(reports_dir / "agreement.csv", agreement_rows, fieldnames=AGREEMENT_FIELDNAMES)

    # 8. Generate report.md
    report_md_lines = [
        "# RQ2 需求访谈流程质量评估报告",
        "",
        "## 1. 来源与覆盖总览",
        "",
        "### 来源清单与就绪状态 (Source Inventory Statuses)",
        f"- 评估案例总数 (Total Cases): {total_cases}",
        f"- 来源条目总数 (Total Items): {total_inventory_items}",
        f"  - 就绪 (ready): {ready_count}",
        f"  - 来源不完整 (source_incomplete): {source_incomplete_count}",
        f"  - 输入错误 (input_error): {input_error_count}",
        "",
        "### 结束观察分布 (Ending Observations)",
        f"- 达到轮数上限 (turn_limit_reached): {turn_limit_reached_count}",
        f"- 未知/其他 (unknown): {unknown_ending_count}",
        "",
        "### 访谈轮数统计 (Interview Length / Completed Turns by Method)",
        "| 方法 | 最小轮数 (Min) | 最大轮数 (Max) | 中位数 (Median) |",
        "| --- | --- | --- | --- |",
    ]
    for mid in config.methods:
        st = method_turn_stats.get(mid, {"min": "-", "max": "-", "median": "-"})
        report_md_lines.append(f"| {mid} | {st['min']} | {st['max']} | {st['median']} |")

    report_md_lines.extend([
        "",
        "### 历史记录说明 (Historical Human Ratings)",
        f"- 人工评分表中未纳入当前评估的合法非 ready 历史行数量: {unincluded_historical_rows_count}",
        "",
        "### 覆盖情况 (Coverage)",
        "",
        "| 方法 | 评价者 | 维度 | 预期数 | 有效评分数 | 待评数 | 失败数 | 可评分率 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for r in coverage_rows:
        report_md_lines.append(
            f"| {r['method_id']} | {r['rater_id']} | {r['dimension']} | {r['n_expected']} | {r['n_scored']} | "
            f"{r['n_pending']} | {r['n_failed']} | {r['scorable_rate'] or '-'} |"
        )

    report_md_lines.extend([
        "",
        "## 2. 评分分布与中心趋势",
        "",
        "### 评分描述统计 (Score Summary)",
        "",
        "| 方法 | 评价者 | 维度 | 样本数 (N) | 均值 | 中位数 | Q1 | Q3 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for s in summary_rows:
        report_md_lines.append(
            f"| {s['method_id']} | {s['rater_id']} | {s['dimension']} | {s['n']} | "
            f"{s['mean'] or '-'} | {s['median'] or '-'} | {s['q1'] or '-'} | {s['q3'] or '-'} |"
        )

    report_md_lines.extend([
        "",
        "## 3. 同 Case 配对比较 (Paired Comparisons)",
        "",
        f"- 请求 Bootstrap 重采样次数 (Requested Repeats): {bootstrap_repeats}",
        "",
        "| 评价者 | 维度 | 方法 A | 方法 B | 配对数 | 均值差 (A-B) | 中位数差 | A较高 | 相同 | B较高 | 95% CI 低 | 95% CI 高 | 有效/请求重采样数 | 备注 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for p in paired_rows:
        valid_rep = p["bootstrap_valid_repeats"]
        rep_col = f"{valid_rep} / {bootstrap_repeats}"
        report_md_lines.append(
            f"| {p['rater_id']} | {p['dimension']} | {p['method_a']} | {p['method_b']} | {p['n_pairs']} | "
            f"{p['mean_difference'] or '-'} | {p['median_difference'] or '-'} | {p['n_a_higher']} | {p['n_equal']} | "
            f"{p['n_b_higher']} | {p['ci_low'] or '-'} | {p['ci_high'] or '-'} | {rep_col} | {p['reason']} |"
        )

    report_md_lines.extend([
        "",
        "## 4. 评价者一致性 (Ordinal Krippendorff's Alpha)",
        "",
        f"- 请求 Bootstrap 重采样次数 (Requested Repeats): {bootstrap_repeats}",
        "",
        "### 评价者在可配对单位中的有效评分贡献数 (Rater Contributions in Pairable Units)",
        "",
        "| 评价组 | 维度 | llm_expert_1 | llm_expert_2 | human_expert_1 | human_expert_2 |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for c in group_contributions_summary:
        report_md_lines.append(
            f"| {c['rater_group']} | {c['dimension']} | {c['llm_expert_1']} | {c['llm_expert_2']} | {c['human_expert_1']} | {c['human_expert_2']} |"
        )

    report_md_lines.extend([
        "",
        "### 一致性统计表 (Agreement Table)",
        "",
        "| 评价组 | 维度 | 有效单位数 | Case数 | 总评分数 | 2评价单位 | 3评价单位 | 4评价单位 | Ordinal α | 95% CI 低 | 95% CI 高 | 有效/请求重采样数 | 备注 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for a in agreement_rows:
        valid_rep = a["bootstrap_valid_repeats"]
        rep_col = f"{valid_rep} / {bootstrap_repeats}"
        report_md_lines.append(
            f"| {a['rater_group']} | {a['dimension']} | {a['n_units']} | {a['n_cases']} | {a['n_ratings']} | "
            f"{a['n_units_2_ratings']} | {a['n_units_3_ratings']} | {a['n_units_4_ratings']} | "
            f"{a['alpha'] or '-'} | {a['ci_low'] or '-'} | {a['ci_high'] or '-'} | {rep_col} | {a['reason']} |"
        )

    report_md_lines.extend([
        "",
        "## 5. 回查索引与产物路径",
        "",
        f"- 原始输入清单: `{inventory_path}`",
        f"- 评分表目录: `{artifacts_root / 'ratings'}`",
        f"- 详细评分回查: `{artifacts_root / 'cases'}/<case_id>/<method_id>/`",
        "",
    ])

    report_md_path = reports_dir / "report.md"
    report_md_path.write_text("\n".join(report_md_lines), encoding="utf-8")

    return ReportSummary(
        coverage_path=reports_dir / "coverage.csv",
        distributions_path=reports_dir / "score_distributions.csv",
        summary_path=reports_dir / "score_summary.csv",
        paired_path=reports_dir / "paired_comparisons.csv",
        agreement_path=reports_dir / "agreement.csv",
        report_md_path=report_md_path,
    )
