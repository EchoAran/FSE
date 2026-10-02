"""Descriptive statistics, paired non-parametric tests, and metric report generation module."""

from __future__ import annotations

import json
import shutil
from typing import Any

import numpy as np
import scipy.stats
import tiktoken

from evolution.rq1.case_artifacts import (
    read_case_csv,
    read_case_jsonl,
    resolve_case_ids,
)
from evolution.rq1.config import RQ1Config
from evolution.rq1.models import (
    ResponseRecord,
    TranscriptMetrics,
    TranscriptRecord,
)
from evolution.rq1.storage import (
    write_csv,
    write_json,
)


class ReportError(Exception):
    """Base exception for report generation failures."""


class ReportValidationError(ReportError):
    """Exception raised when metric records or matrix shapes fail validation."""


def depth_count_metric_names(metrics: list[TranscriptMetrics]) -> list[str]:
    """Return one scalar metric name for each observed exact DAG depth."""
    max_depth = max(
        (int(depth) for metric in metrics for depth in metric.depth_counts),
        default=0,
    )
    return [f"depth_{depth}_dag_count" for depth in range(1, max_depth + 1)]


def count_answer_tokens(
    responses: list[ResponseRecord],
    encoding_name: str,
) -> dict[str, int]:
    """Calculate total interviewee answer token count for each transcript."""
    encoding = tiktoken.get_encoding(encoding_name)
    token_counts: dict[str, int] = {}
    for resp in responses:
        token_count = len(encoding.encode(resp.answer))
        token_counts[resp.transcript_id] = (
            token_counts.get(resp.transcript_id, 0) + token_count
        )
    return token_counts


def build_metric_rows(
    metrics: list[TranscriptMetrics],
    transcripts: list[TranscriptRecord],
    responses: list[ResponseRecord],
    token_counts: dict[str, int],
) -> list[dict[str, object]]:
    """Assemble standardized metric evaluation rows containing quality and efficiency measures."""
    metrics_by_id = {m.transcript_id: m for m in metrics}
    depth_metrics = depth_count_metric_names(metrics)
    response_counts: dict[str, int] = {}
    for resp in responses:
        response_counts[resp.transcript_id] = (
            response_counts.get(resp.transcript_id, 0) + 1
        )

    sorted_transcripts = sorted(
        transcripts,
        key=lambda t: (t.case_id, t.method_id),
    )

    rows: list[dict[str, object]] = []
    for t in sorted_transcripts:
        if t.transcript_id not in metrics_by_id:
            raise ReportValidationError(
                f"Missing transcript metric record for {t.transcript_id}"
            )
        metric = metrics_by_id[t.transcript_id]
        resp_count = response_counts.get(t.transcript_id, 0)
        tok_count = token_counts.get(t.transcript_id, 0)

        riu_per_resp = (
            round(metric.yield_count / resp_count, 4) if resp_count > 0 else 0.0
        )
        riu_per_1k = (
            round((metric.yield_count / tok_count) * 1000.0, 4)
            if tok_count > 0
            else 0.0
        )
        breadth_per_10 = (
            round((metric.breadth / resp_count) * 10.0, 4)
            if resp_count > 0
            else 0.0
        )

        row: dict[str, object] = {
            "case_id": t.case_id,
            "method_id": t.method_id,
            "transcript_id": t.transcript_id,
            "yield": metric.yield_count,
            "breadth": metric.breadth,
            "depth_counts": json.dumps(metric.depth_counts, sort_keys=True),
            "response_count": resp_count,
            "interviewee_token_count": tok_count,
            "riu_per_response": riu_per_resp,
            "riu_per_1000_tokens": riu_per_1k,
            "breadth_per_10_responses": breadth_per_10,
        }
        for depth_metric in depth_metrics:
            depth = depth_metric.removeprefix("depth_").removesuffix("_dag_count")
            row[depth_metric] = metric.depth_counts.get(depth, 0)
        rows.append(row)

    return rows


def describe_metric(
    rows: list[dict[str, object]],
    metric: str,
    methods: list[str],
    bootstrap_repeats: int,
    random_seed: int,
) -> list[dict[str, object]]:
    """Compute method-level descriptive statistics with bootstrap confidence intervals."""
    rng = np.random.default_rng(random_seed)
    results: list[dict[str, object]] = []

    for method in methods:
        method_values = [
            float(row[metric])
            for row in rows
            if row["method_id"] == method and row[metric] is not None
        ]

        n = len(method_values)
        if n == 0:
            results.append(
                {
                    "metric": metric,
                    "method_id": method,
                    "n": 0,
                    "mean": None,
                    "std": None,
                    "median": None,
                    "q1": None,
                    "q3": None,
                    "min": None,
                    "max": None,
                    "ci_lower_95": None,
                    "ci_upper_95": None,
                }
            )
            continue

        arr = np.array(method_values, dtype=np.float64)
        mean_val = round(float(np.mean(arr)), 4)
        std_val = round(float(np.std(arr, ddof=1)), 4) if n > 1 else 0.0
        median_val = round(float(np.median(arr)), 4)
        q1_val = round(float(np.percentile(arr, 25)), 4)
        q3_val = round(float(np.percentile(arr, 75)), 4)
        min_val = round(float(np.min(arr)), 4)
        max_val = round(float(np.max(arr)), 4)

        boot_means: list[float] = []
        for _ in range(bootstrap_repeats):
            sample_idx = rng.choice(n, size=n, replace=True)
            boot_means.append(float(np.mean(arr[sample_idx])))

        ci_lower = round(float(np.percentile(boot_means, 2.5)), 4)
        ci_upper = round(float(np.percentile(boot_means, 97.5)), 4)

        results.append(
            {
                "metric": metric,
                "method_id": method,
                "n": n,
                "mean": mean_val,
                "std": std_val,
                "median": median_val,
                "q1": q1_val,
                "q3": q3_val,
                "min": min_val,
                "max": max_val,
                "ci_lower_95": ci_lower,
                "ci_upper_95": ci_upper,
            }
        )

    return results


def build_paired_matrix(
    rows: list[dict[str, object]],
    metric: str,
    methods: list[str],
) -> tuple[list[str], np.ndarray]:
    """Align case-level observations across methods into paired observation matrix."""
    case_groups: dict[str, dict[str, Any]] = {}
    for row in rows:
        case_id = str(row["case_id"])
        method_id = str(row["method_id"])
        case_groups.setdefault(case_id, {})[method_id] = row[metric]

    valid_cases: list[str] = []
    matrix_rows: list[list[float]] = []

    for case_id in sorted(case_groups.keys()):
        method_map = case_groups[case_id]
        if all(
            m in method_map and method_map[m] is not None for m in methods
        ):
            valid_cases.append(case_id)
            matrix_rows.append([float(method_map[m]) for m in methods])

    if not matrix_rows:
        return [], np.empty((0, len(methods)), dtype=np.float64)

    return valid_cases, np.array(matrix_rows, dtype=np.float64)


def friedman_test(matrix: np.ndarray) -> dict[str, float]:
    """Execute non-parametric Friedman omnibus test across matched treatment groups."""
    if matrix.shape[0] < 2 or matrix.shape[1] < 3:
        raise ReportValidationError(
            f"Matrix dimension insufficient for Friedman test (requires >= 2 rows and >= 3 columns): {matrix.shape}"
        )
    if np.all(matrix == matrix[0, 0]):
        return {"statistic": 0.0, "p_value": 1.0}

    samples = [matrix[:, col] for col in range(matrix.shape[1])]
    res = scipy.stats.friedmanchisquare(*samples)
    stat = float(res.statistic)
    p_val = float(res.pvalue)
    if np.isnan(stat):
        stat = 0.0
        p_val = 1.0
    return {
        "statistic": round(stat, 4),
        "p_value": p_val,
    }


def holm_adjust(p_values: list[float]) -> list[float]:
    """Perform step-down Holm correction to control family-wise error rate."""
    total_tests = len(p_values)
    if total_tests == 0:
        return []

    sorted_indices = sorted(range(total_tests), key=lambda idx: p_values[idx])
    adjusted: list[float] = [0.0] * total_tests

    running_max = 0.0
    for rank, orig_idx in enumerate(sorted_indices):
        multiplier = total_tests - rank
        raw_p = p_values[orig_idx]
        adj_val = min(1.0, multiplier * raw_p)
        running_max = max(running_max, adj_val)
        adjusted[orig_idx] = round(min(1.0, running_max), 6)

    return adjusted


def pairwise_wilcoxon(
    matrix: np.ndarray,
    methods: list[str],
) -> list[dict[str, object]]:
    """Perform pairwise Wilcoxon signed-rank tests with Holm correction and rank-biserial effect sizes."""
    total_methods = len(methods)
    comparisons: list[dict[str, Any]] = []

    for i in range(total_methods):
        for j in range(i + 1, total_methods):
            method_a = methods[i]
            method_b = methods[j]
            x = matrix[:, i]
            y = matrix[:, j]
            diff = x - y

            paired_median_diff = round(float(np.median(diff)), 4)
            nonzero_diff = diff[diff != 0]

            if len(nonzero_diff) == 0:
                statistic = 0.0
                raw_p = 1.0
                rank_biserial = 0.0
            else:
                wilc_res = scipy.stats.wilcoxon(x, y, zero_method="wilcox")
                statistic = round(float(wilc_res.statistic), 4)
                raw_p = float(wilc_res.pvalue)

                abs_diff = np.abs(nonzero_diff)
                ranks = scipy.stats.rankdata(abs_diff)
                w_plus = float(np.sum(ranks[nonzero_diff > 0]))
                w_minus = float(np.sum(ranks[nonzero_diff < 0]))
                total_w = w_plus + w_minus
                rank_biserial = (
                    round((w_plus - w_minus) / total_w, 4)
                    if total_w > 0
                    else 0.0
                )

            comparisons.append(
                {
                    "method_a": method_a,
                    "method_b": method_b,
                    "sample_size": matrix.shape[0],
                    "paired_median_diff": paired_median_diff,
                    "rank_biserial_effect_size": rank_biserial,
                    "statistic": statistic,
                    "raw_p_value": raw_p,
                }
            )

    raw_p_values = [comp["raw_p_value"] for comp in comparisons]
    adjusted_p_values = holm_adjust(raw_p_values)

    for comp, adj_p in zip(comparisons, adjusted_p_values):
        comp["holm_adjusted_p_value"] = adj_p

    return comparisons


def build_depth_distribution(
    metrics: list[TranscriptMetrics],
    methods: list[str],
) -> list[dict[str, object]]:
    """Count DAGs at each exact depth for every method."""
    max_depth_seen = max(
        (int(depth) for metric in metrics for depth in metric.depth_counts),
        default=0,
    )

    results: list[dict[str, object]] = []

    for method in methods:
        method_metrics = [m for m in metrics if m.method_id == method]
        for d in range(1, max_depth_seen + 1):
            d_key = str(d)
            results.append(
                {
                    "method_id": method,
                    "depth": d,
                    "dag_count": sum(
                        metric.depth_counts.get(d_key, 0)
                        for metric in method_metrics
                    ),
                }
            )

    return results


def build_report(config: RQ1Config) -> None:
    """Execute comprehensive statistical reporting and export tables."""
    artifacts_root = config.paths.artifacts_root
    audit_summary_src = artifacts_root / "audit" / "audit_summary.json"
    if not audit_summary_src.is_file():
        raise ReportError(
            f"Audit summary artifact not found: {audit_summary_src}. "
            f"Please complete human review and run audit-summarize before generating report."
        )

    case_ids = resolve_case_ids(config, None)
    transcripts = [
        TranscriptRecord.model_validate(row)
        for row in read_case_jsonl(
            config, "ingestion/transcripts.jsonl", case_ids
        )
    ]
    responses = [
        ResponseRecord.model_validate(row)
        for row in read_case_jsonl(config, "ingestion/responses.jsonl", case_ids)
    ]
    metrics = [
        TranscriptMetrics.model_validate(row)
        for row in read_case_jsonl(
            config, "elaboration/transcript_metrics.jsonl", case_ids
        )
    ]
    sensitivity_rows = read_case_csv(
        config, "clustering/threshold_sensitivity.csv", case_ids
    )

    token_counts = count_answer_tokens(
        responses=responses,
        encoding_name=config.statistics.tokenizer_encoding,
    )
    metric_rows = build_metric_rows(
        metrics=metrics,
        transcripts=transcripts,
        responses=responses,
        token_counts=token_counts,
    )

    reports_dir = artifacts_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    depth_metrics = depth_count_metric_names(metrics)

    transcript_fieldnames = [
        "case_id",
        "method_id",
        "transcript_id",
        "yield",
        "breadth",
        "depth_counts",
        *depth_metrics,
        "response_count",
        "interviewee_token_count",
        "riu_per_response",
        "riu_per_1000_tokens",
        "breadth_per_10_responses",
    ]
    write_csv(
        reports_dir / "transcript_metrics.csv",
        transcript_fieldnames,
        metric_rows,
    )

    efficiency_fieldnames = [
        "case_id",
        "method_id",
        "transcript_id",
        "response_count",
        "interviewee_token_count",
        "riu_per_response",
        "riu_per_1000_tokens",
        "breadth_per_10_responses",
    ]
    efficiency_rows = [
        {k: row[k] for k in efficiency_fieldnames} for row in metric_rows
    ]
    write_csv(
        reports_dir / "efficiency_metrics.csv",
        efficiency_fieldnames,
        efficiency_rows,
    )

    methods = config.methods
    bootstrap_repeats = config.statistics.bootstrap_repeats
    random_seed = config.statistics.random_seed

    descriptives: list[dict[str, object]] = []
    target_metrics = [
        "yield",
        "breadth",
        *depth_metrics,
        "riu_per_response",
        "riu_per_1000_tokens",
        "breadth_per_10_responses",
    ]
    for target in target_metrics:
        descriptives.extend(
            describe_metric(
                rows=metric_rows,
                metric=target,
                methods=methods,
                bootstrap_repeats=bootstrap_repeats,
                random_seed=random_seed,
            )
        )

    desc_fieldnames = [
        "metric",
        "method_id",
        "n",
        "mean",
        "std",
        "median",
        "q1",
        "q3",
        "min",
        "max",
        "ci_lower_95",
        "ci_upper_95",
    ]
    write_csv(
        reports_dir / "method_descriptives.csv",
        desc_fieldnames,
        descriptives,
    )

    omnibus_results: list[dict[str, object]] = []
    pairwise_results: list[dict[str, object]] = []
    paired_export_rows: list[dict[str, object]] = []

    case_ids_all = sorted({row["case_id"] for row in metric_rows})
    rows_by_case_method = {
        (row["case_id"], row["method_id"]): row for row in metric_rows
    }
    paired_metrics = ["yield", "breadth", *depth_metrics]
    for case_id in case_ids_all:
        case_dict: dict[str, object] = {"case_id": case_id}
        for target in paired_metrics:
            for m in methods:
                row_item = rows_by_case_method.get((case_id, m))
                case_dict[f"{m}_{target}"] = (
                    row_item[target] if row_item else None
                )
        paired_export_rows.append(case_dict)

    paired_fieldnames = ["case_id"] + [
        f"{m}_{target}"
        for target in paired_metrics
        for m in methods
    ]
    write_csv(
        reports_dir / "paired_metrics.csv",
        paired_fieldnames,
        paired_export_rows,
    )

    for target in paired_metrics:
        valid_cases, matrix = build_paired_matrix(
            rows=metric_rows,
            metric=target,
            methods=methods,
        )
        if matrix.shape[0] >= 2 and matrix.shape[1] >= 2:
            if matrix.shape[1] >= 3:
                friedman_res = friedman_test(matrix)
                omnibus_results.append(
                    {
                        "metric": target,
                        "sample_size": matrix.shape[0],
                        "statistic": friedman_res["statistic"],
                        "p_value": friedman_res["p_value"],
                    }
                )

            pairwise_res = pairwise_wilcoxon(matrix, methods)
            for item in pairwise_res:
                pairwise_results.append({"metric": target, **item})

    omnibus_fieldnames = ["metric", "sample_size", "statistic", "p_value"]
    write_csv(
        reports_dir / "omnibus_tests.csv",
        omnibus_fieldnames,
        omnibus_results,
    )

    pairwise_fieldnames = [
        "metric",
        "method_a",
        "method_b",
        "sample_size",
        "paired_median_diff",
        "rank_biserial_effect_size",
        "statistic",
        "raw_p_value",
        "holm_adjusted_p_value",
    ]
    write_csv(
        reports_dir / "pairwise_tests.csv",
        pairwise_fieldnames,
        pairwise_results,
    )

    depth_distribution = build_depth_distribution(
        metrics=metrics,
        methods=methods,
    )
    write_csv(
        reports_dir / "depth_distribution.csv",
        ["method_id", "depth", "dag_count"],
        depth_distribution,
    )

    sensitivity_fieldnames = [
        "threshold",
        "case_id",
        "transcript_id",
        "method_id",
        "breadth",
        "total_clusters",
    ]
    write_csv(
        reports_dir / "threshold_sensitivity.csv",
        sensitivity_fieldnames,
        sensitivity_rows,
    )
    shutil.copy2(audit_summary_src, reports_dir / "audit_summary.json")

    summary_content = {
        "total_transcripts": len(transcripts),
        "methods": methods,
        "metrics_evaluated": target_metrics,
        "omnibus_tests_count": len(omnibus_results),
        "pairwise_tests_count": len(pairwise_results),
    }
    write_json(reports_dir / "summary.json", summary_content)
