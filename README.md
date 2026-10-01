# Requirements Elicitation through Semi-Structured Interviews

This repository provides the methods, datasets, interview environment, and evaluation pipelines for a study of LLM-based software requirements elicitation. It brings together a study of later-stated requirement information in developer–ChatGPT conversations, a PURE-derived interview dataset, a proposed semi-structured interview method, three baseline methods, and three research-question evaluation pipelines.

The interview dataset contains **69 project cases**. Four methods have been run on every case, producing **276 completed interviews**. The evaluation pipelines examine the requirement information elicited, the quality of the interview flow, and the software implementations produced from the resulting requirements specifications.

## Study Workflow

```mermaid
flowchart TD
    D[DevGPT conversations] --> M[Motivation study: later-stated requirement information]
    M --> P[Proposed semi-structured interview method]
    S[PURE requirements documents] --> C[69 project-level interview cases]
    C --> I[Unified interview environment]
    P --> I
    B[Hashimoto / LLMREI-long / SparkMe] --> I
    I --> T[276 interview transcripts]
    T --> R1[RQ1: information yield, breadth, and depth]
    T --> R2[RQ2: interview flow quality]
    T --> R3[RQ3: requirements-to-implementation evaluation]
```

The motivation study and the interview dataset use separate sources. DevGPT supplies the conversations used to investigate later-stated requirement information; PURE supplies the project descriptions used to initiate the requirements interviews.

## Repository Modules

| Module | Purpose | Guide |
| --- | --- | --- |
| `motivation/` | Analyze Later-Stated Requirement Information (LSRI) in DevGPT conversations, retaining source evidence and producing descriptive tables. | [Motivation study](motivation/README.md) |
| `dataset/` | Provide the 69 runtime cases, original PURE documents, construction provenance, screening records, and independent reviews. | [Dataset](dataset/README.md) |
| `methods/proposed_method/` | Implement the proposed method, including interview framework generation, requirement slots, topic scheduling, question planning, and state evolution. | [Proposed method](methods/proposed_method/README.md) |
| `methods/baseline/` | Provide the Hashimoto, LLMREI-long, and SparkMe interview methods. | [Hashimoto](methods/baseline/hashimoto/README.md), [LLMREI-long](methods/baseline/llmrei-long/README.md), [SparkMe](methods/baseline/sparkme/README.md) |
| `interview/` | Run all four methods through a shared CLI with a simulated stakeholder or a human respondent, and manage conversations and checkpoints. | [Interview environment](interview/README.md) |
| `results/` | Store method-by-case interview records and method-native artifacts. | [Result format](interview/README.md#results) |
| `evolution/rq1/` | Measure elicited requirement information and produce paired statistical comparisons. | [RQ1](evolution/rq1/README.md) |
| `evolution/rq2/` | Evaluate interview flow using two LLM experts and two human experts. | [RQ2](evolution/rq2/README.md) |
| `evolution/rq3/` | Generate reviewed specifications, run coding tasks, collect implementation evidence, and evaluate delivered software. | [RQ3](evolution/rq3/README.md) |
| `visualization/` | Organize study figures and evidence materials for the motivation study and the three RQs. | |
| `docs/` | Retain supporting design and implementation documents. | |

## Dataset and Interview Methods

Each case provides a project name and an initial requirements description:

```json
{
  "case_id": "PURE_001",
  "project_name": "...",
  "initial_requirements": "..."
}
```

The descriptions establish enough context to begin an interview while leaving detailed workflows, rules, exceptions, constraints, and quality requirements open to exploration. Source documents and review records are retained separately from the runtime input. See the [dataset guide](dataset/README.md) for construction criteria and provenance.

| Method ID | Interview approach |
| --- | --- |
| `proposed_method` | Maintain a project-specific interview framework and requirement slots, select topics dynamically, and adapt questions and interview structure as new evidence is collected. |
| `hashimoto` | Fill existing slots, generate additional slots through abduction, and ask questions targeting missing information. |
| `llmrei-long` | Conduct a contextual multi-turn interview using the LLMREI-long prompt and dialogue history. |
| `sparkme` | Coordinate an Interviewer, Agenda Manager, and Exploration Planner to track coverage and explore additional requirements. |

The method guides describe their implementations and adaptations from the source papers or upstream assets. Each method retains its own interview strategy, completion rules, and native state.

The recorded interviews use `gpt-5.4-mini-2026-03-17` for both the interviewer methods and the simulated stakeholder, with a configured maximum of 100 turns per interview. All four methods have a completed record for each of the 69 cases. These settings describe the recorded experiment; model and runtime settings for new interviews are configurable.

## Quick Start

Use **Python 3.10 or newer**. Run the following commands from the repository root. The examples use PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Configure an interviewer and stakeholder

Copy the configuration template for the method you want to run and set its model, endpoint, credentials, and runtime parameters according to its guide.

| Method | Template | Local configuration |
| --- | --- | --- |
| Proposed method | `methods/proposed_method/configs/default.example.yaml` | `methods/proposed_method/configs/default.yaml` |
| Hashimoto | `methods/baseline/hashimoto/config/default.example.yaml` | `methods/baseline/hashimoto/config/default.yaml` |
| LLMREI-long | `methods/baseline/llmrei-long/config/default.example.yaml` | `methods/baseline/llmrei-long/config/default.yaml` |
| SparkMe | `methods/baseline/sparkme/.env.example` | `methods/baseline/sparkme/.env` |

For the proposed method and an automated stakeholder:

```powershell
Copy-Item methods/proposed_method/configs/default.example.yaml methods/proposed_method/configs/default.yaml
Copy-Item interview/config/default.example.yaml interview/config/default.yaml
```

Configure the proposed method's model settings in its YAML file and supply its API key through `LLM_API_KEY`. Configure the stakeholder's `model.api_url`, `model.model_name`, and `model.api_key` in `interview/config/default.yaml`. Alternatively, leave the stakeholder's `model.api_key` empty and use `INTERVIEWEE_API_KEY`.

```powershell
$env:LLM_API_KEY = "your-method-api-key"
$env:INTERVIEWEE_API_KEY = "your-interviewee-api-key"
```

The stakeholder prompt is stored at `interview/interviewee/prompt.txt` and receives the case's project name and initial requirements. The interviewer and stakeholder have separate model configurations. Local configuration files hold credentials and are excluded from version control.

### Run and inspect an interview

```powershell
python -m interview --list-cases
python -m interview --method proposed_method --case PURE_001
python -m interview --method proposed_method --case PURE_001 --inspect
```

Use `--method hashimoto`, `--method llmrei-long`, or `--method sparkme` to run a configured baseline. To answer the interview questions yourself, add `--interactive`:

```powershell
python -m interview --method proposed_method --case PURE_001 --interactive
```

Each interview writes to `results/<method_id>/<case_id>/`:

| Artifact | Contents |
| --- | --- |
| `manifest.json` | Case and method identifiers, models, completed turns, status, and completion or error messages. |
| `conversation.jsonl` | The public interviewer–stakeholder dialogue. |
| `tokens.jsonl` | Interviewer-method token usage for initialization and subsequent turns. |
| `native/` | Method-owned checkpoints and logs, including `worker.log`. |

Rerunning an unfinished interview resumes saved state for the proposed method, Hashimoto, and LLMREI-long. SparkMe sessions remain in memory and cannot resume after their worker process ends. Completed interviews are preserved when the same command is run again. The [interview guide](interview/README.md) covers explicit configuration selection, recovery, and starting a fresh run.

## Motivation Study

The motivation module investigates requirement-relevant information stated after an assistant has already supplied a concrete implementation solution. It identifies LSRI when the information is absent from the earlier conversation and classifies its requirement type, introduction mode, earlier elicitation opportunity, and response uptake.

Place the DevGPT snapshot at the location described in the [motivation guide](motivation/README.md), copy the configuration template, and configure the analysis model:

```powershell
Copy-Item motivation/config/default.example.yaml motivation/config/default.yaml
python -m motivation.cli prepare --config motivation/config/default.yaml
python -m motivation.cli analyze --config motivation/config/default.yaml
python -m motivation.cli summarize --config motivation/config/default.yaml
python -m motivation.cli inspect --config motivation/config/default.yaml
```

Prepared inputs are stored under `motivation/data/derived/`. Analysis records, summary tables, and representative-case candidates are stored under `motivation/results/`. The study retains source turns and evidence spans so individual observations can be inspected alongside aggregate counts.

## Evaluation Pipelines

All three evaluation modules read the shared interview records under `results/`. Each has its own configuration template, artifact directory, and detailed workflow. Copy the relevant `config/default.example.yaml` to `config/default.yaml` and configure the required models before running that module.

### RQ1: Requirement Information Yield, Breadth, and Depth

RQ1 extracts atomic Requirement Information Units (RIUs) from stakeholder answers, removes repeated information within each transcript, and pools the unique RIUs across methods to build a shared semantic space for each case. It measures information yield, coverage breadth, elaboration depth, and efficiency. A single reviewer checks sampled extraction, deduplication, and transcript outputs before aggregate reports are produced.

```powershell
Copy-Item evolution/rq1/config/default.example.yaml evolution/rq1/config/default.yaml
python -m evolution.rq1.cli all --case-id PURE_001 --config evolution/rq1/config/default.yaml
```

After inspecting a case, run the automatic processing across the dataset:

```powershell
python -m evolution.rq1.cli all --config evolution/rq1/config/default.yaml
```

Complete the exported review sheets, then summarize the review and produce reports:

```powershell
python -m evolution.rq1.cli audit-summarize --config evolution/rq1/config/default.yaml
python -m evolution.rq1.cli report --config evolution/rq1/config/default.yaml
python -m evolution.rq1.cli validate --config evolution/rq1/config/default.yaml
```

The default output root is `evolution/rq1/artifacts/`. Start reading aggregate results with `reports/transcript_metrics.csv`, `reports/method_descriptives.csv`, and `reports/pairwise_tests.csv`. See the [RQ1 guide](evolution/rq1/README.md) for stage commands, model and embedding configuration, review instructions, and checkpointed execution.

### RQ2: Interview Flow Quality

RQ2 evaluates three dimensions of observable interviewer behavior: **local coherence**, **transition quality**, and **contingent responsiveness**. Two independently configured LLM experts evaluate complete transcripts, and two human experts use matching review templates. Each dimension receives its own judgment and evidence; reports include score distributions, paired comparisons, and inter-rater agreement.

```powershell
Copy-Item evolution/rq2/config/default.example.yaml evolution/rq2/config/default.yaml
python -m evolution.rq2.cli prepare --config evolution/rq2/config/default.yaml
python -m evolution.rq2.cli evaluate --config evolution/rq2/config/default.yaml --judge llm_expert_1
python -m evolution.rq2.cli evaluate --config evolution/rq2/config/default.yaml --judge llm_expert_2
python -m evolution.rq2.cli export-templates --config evolution/rq2/config/default.yaml
```

The exported human templates are filled independently outside the pipeline. Generate or refresh reports from the available ratings with:

```powershell
python -m evolution.rq2.cli report --config evolution/rq2/config/default.yaml
```

The default output root is `evolution/rq2/artifacts/`. Read `reports/coverage.csv` alongside the scores and comparisons, and use `reports/report.md` as the report entry point. See the [RQ2 guide](evolution/rq2/README.md) for the rubric, expert configuration, case selection, human scoring, and rerun semantics.

### RQ3: Requirements-to-Implementation Evaluation

RQ3 studies the software delivered from interview-derived requirements specifications. The selected cases are `PURE_002`, `PURE_004`, `PURE_024`, `PURE_057`, and `PURE_069`, listed in `evolution/rq3/cases.jsonl`.

The workflow prepares transcripts, generates a draft Software Requirements Specification (SRS), applies human review, records observation scenarios, runs coding tasks in containers, collects build/run and scenario evidence, and evaluates requirements against that evidence. Judgment review and cross-run consistency tables support the final comparison.

```powershell
Copy-Item evolution/rq3/config/default.example.yaml evolution/rq3/config/default.yaml
python -m evolution.rq3.cli prepare --config evolution/rq3/config/default.yaml --case-id PURE_002
python -m evolution.rq3.cli generate-srs --config evolution/rq3/config/default.yaml --case-id PURE_002
python -m evolution.rq3.cli export-srs-review --config evolution/rq3/config/default.yaml --case-id PURE_002
```

Complete the SRS review before finalizing it and proceeding to scenario preparation and coding. RQ3 additionally requires a working Docker environment and a dedicated coding-agent Python environment. The [RQ3 guide](evolution/rq3/README.md) describes these settings and the commands for each stage, including evidence invocations and review tables.

After processing the selected implementations and reviews, generate and verify the saved artifacts:

```powershell
python -m evolution.rq3.cli report --config evolution/rq3/config/default.yaml
python -m evolution.rq3.cli verify --config evolution/rq3/config/default.yaml
```

The default output root is `evolution/rq3/artifacts/`. Start with `reports/rq3_report.md` and consult the accompanying SRS inventory, run coverage, evidence limitations, and consistency tables.

## Study Results

<!-- Add the aggregate findings and links to final reports here. -->

## Citation

<!-- Add the publication details and BibTeX entry here. -->
