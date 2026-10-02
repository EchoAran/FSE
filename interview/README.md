# Interview Environment

`interview` runs requirements elicitation interviews against cases from
`dataset/cases.jsonl`. It provides one command line interface for
`proposed_method`, `hashimoto`, `llmrei-long`, and `sparkme`, with either a simulated
interviewee or a human answering the interviewer's questions. `proposed_method` is the runtime identifier for ElicitMind.

In the reported experiment, the simulator represents a stakeholder familiar with the project goals and business workflows who cooperates with the interview. It receives the project description, the most recent six question–answer pairs, and a shared role prompt. The PURE source documents establish the initial Case descriptions; they are not supplied as the simulator's full answer reference.

## Structure

```text
interview/
├── __main__.py        # Package entry point: python -m interview
├── cli.py             # Command line arguments and dispatch
├── cases/             # Case loading and validation
├── config/            # Simulated interviewee configuration
├── interviewee/       # Simulated interviewee and prompt.txt template
├── orchestrator/      # Dialogue loop and checkpoint recovery
├── adapters/          # Method registry and worker communication
├── workers/           # Isolated method execution and method-specific handlers
└── storage/           # Manifest, conversation, pending answer, and token records
```

Method implementations remain under `methods/`. The orchestrator loads a case,
starts the selected method in a separate process using the same Python
interpreter, and passes interviewee answers to it until the method signals
completion. Each method owns its interview strategy, termination rules, and
native state; the environment manages the shared dialogue and result layout.

## Setup

Use Python 3.10 or newer. Run all commands below from the repository root, rather
than from inside `interview/`, because dataset, configuration, and result paths
are resolved from the working directory.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Prepare the native configuration for the method you want to run. Copy its
template to the default path, then set the model, endpoint, credentials, and
method parameters according to its README.

| Method ID | Configuration template | Default configuration | Method guide |
| --- | --- | --- | --- |
| `proposed_method` | `methods/proposed_method/configs/default.example.yaml` | `methods/proposed_method/configs/default.yaml` | [ElicitMind](https://anonymous.4open.science/r/ElicitMind) |
| `hashimoto` | `methods/baseline/hashimoto/config/default.example.yaml` | `methods/baseline/hashimoto/config/default.yaml` | [Hashimoto](../methods/baseline/hashimoto/README.md) |
| `llmrei-long` | `methods/baseline/llmrei-long/config/default.example.yaml` | `methods/baseline/llmrei-long/config/default.yaml` | [LLMREI-long](../methods/baseline/llmrei-long/README.md) |
| `sparkme` | `methods/baseline/sparkme/.env.example` | `methods/baseline/sparkme/.env` | [SparkMe](../methods/baseline/sparkme/README.md) |

For example, to configure ElicitMind in PowerShell:

```powershell
Copy-Item methods/proposed_method/configs/default.example.yaml methods/proposed_method/configs/default.yaml
$env:LLM_API_KEY = "your-method-api-key"
```

For automated interviews, also copy `interview/config/default.example.yaml`
to `interview/config/default.yaml` if you have not configured it already:

```powershell
Copy-Item interview/config/default.example.yaml interview/config/default.yaml
```

Edit the interviewee YAML to set `model.api_url`, `model.model_name`, and
`model.api_key`. Alternatively, leave `model.api_key` empty and export the key
through the `INTERVIEWEE_API_KEY` environment variable:

```powershell
$env:INTERVIEWEE_API_KEY = "your-interviewee-api-key"
```

`history_window_pairs` controls how many recent completed
question-answer pairs the agent receives. `prompt_path` selects the stakeholder
prompt; the default is `interview/interviewee/prompt.txt`, rendered with the case's
project name and initial requirements. The method and interviewee use separate
configurations.

## Run an interview

List the available cases and command options:

```powershell
python -m interview --list-cases
python -m interview --help
```

Run an automated interview with a configured method:

```powershell
python -m interview --method proposed_method --case PURE_001
```

The CLI selects `interview/config/default.yaml` when present, otherwise
`interview/config/default.example.yaml`. To select configurations explicitly:

```powershell
python -m interview --method proposed_method --case PURE_001 --method-config methods/proposed_method/configs/default.yaml --interviewee-config interview/config/default.yaml
```

Use the same command format for the baselines after configuring them:

```powershell
python -m interview --method hashimoto --case PURE_001
python -m interview --method llmrei-long --case PURE_001
python -m interview --method sparkme --case PURE_001
```

To answer questions yourself, use interactive mode. It still requires a configured
interviewer method, but does not require an interviewee agent configuration:

```powershell
python -m interview --method proposed_method --case PURE_001 --interactive
```

Type `exit` or `quit` at the response prompt, or press `Ctrl+C`, to interrupt the
interview.

## Inspect and resume

Inspect the saved manifest without advancing the interview or starting a worker:

```powershell
python -m interview --method proposed_method --case PURE_001 --inspect
```

For `proposed_method`, `hashimoto`, and `llmrei-long`, rerun the original command
to resume from saved native state. Recovery also reconciles a pending answer with
the method checkpoint. Keep the original configurations: resume checks the method
model, method turn limit, and interviewee model for conflicts with the manifest.

SparkMe keeps its session in memory and cannot resume after its worker process
ends. An attempt to resume is rejected and recorded as interrupted.

A run whose status is `method_finished` is returned without being overwritten.
To start a fresh run for the same method and case, first move the existing
`results/<method>/<case>/` directory elsewhere. There is no CLI overwrite flag.

## Results

Each run writes to `results/<method>/<case>/`:

| Artifact | Purpose |
| --- | --- |
| `manifest.json` | Status, models, method turn limit, completed turns, and finish/error messages |
| `conversation.jsonl` | Public dialogue with turn indices, roles, and message content |
| `tokens.jsonl` | Method token usage for initialization (turn 0) and subsequent turns; excludes interviewee token usage |
| `pending_answer.json` | Temporary answer awaiting processing or recovery; removed after commit |
| `native/` | Method-owned state and logs, including `worker.log` |

The environment does not automatically generate a final requirements report.
For method-specific reports, use the explicit reporting tools described in the
method's guide. If a run fails, inspect `manifest.json` and `native/worker.log`
before resuming.
