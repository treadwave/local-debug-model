# Local AI Debug Agent

Runs the test suite and asks a local LLM (Ollama) to explain failing tests and propose fixes.
The code never works offline.

## How it works

1. `debug_agent.py` runs the tests with pytest.
2. If pytest itself failed to run, the model is not called.
3. The source code (with line numbers) and the test output are passed to the local model through the `ollama run` command.
4. If the primary model does not answer, the agent switches to the fallback model.

## Models

| Role     | Ollama model        | Base model    | Config            |
|----------|---------------------|---------------|-------------------|
| Primary  | `debug-agent-qwen`  | `qwen3.5:9b`  | `Modelfile.qwen`  |
| Fallback | `debug-agent-llama` | `llama3.1:8b` | `Modelfile.llama` |

## Quick start (macOS)

```bash
ollama pull qwen3.5:9b
ollama pull llama3.1:8b
python3 -m venv .venv && .venv/bin/pip install pytest
make models   # build both models from the Modelfiles
make test     # 3 tests fail on purpose
make debug    # ask the local LLM to explain the failures
```

## Files

- `sensor_stats.py`: demo application with three intentional bugs
- `sensor_stats_test.py`: pytest tests that expose the bugs
- `debug_agent.py`: the agent
- `Modelfile.qwen`, `Modelfile.llama`: model configs
- `Makefile`: shortcuts for common commands
