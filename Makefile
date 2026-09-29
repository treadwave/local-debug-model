test:
	.venv/bin/python -m pytest -q

debug:
	.venv/bin/python debug_agent.py

models:
	ollama create debug-agent-qwen -f Modelfile.qwen
	ollama create debug-agent-llama -f Modelfile.llama