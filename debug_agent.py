import json
import subprocess
import sys
import urllib.error
import urllib.request

MODELS = ["debug-agent-qwen", "debug-agent-llama"]
SOURCE_FILE = "sensor_stats.py"
TIMEOUT = 180

def run_tests():
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True)

    return result.returncode, result.stdout + result.stderr


def build_prompt(test_output):
    with open(SOURCE_FILE) as f:
        lines = f.read().splitlines()
    code = "\n".join(f"{n:4d}  {line}" for n, line in enumerate(lines, start=1))

    return f"Source code:\n{code}\n\nTest output:\n{test_output}"


def ask(model, prompt):
    result = subprocess.run(["ollama", "run", model], input=prompt, text=True, timeout=TIMEOUT)

    if result.returncode != 0:
        raise RuntimeError(f"ollama exited with code {result.returncode}")

code, output = run_tests()
print(output)

if code == 0:
    print("All tests passed, nothing to debug.")
    sys.exit(0)
if code != 1 or "No module named pytest" in output:
    print(f"pytest did not run properly (exit code {code}). The model is not called.")
    sys.exit(1)

prompt = build_prompt(output)
for model in MODELS:
    print(f"Asking {model}...")
    try:
        ask(model, prompt)
        break
    except (RuntimeError, subprocess.TimeoutExpired) as e:
        print(f"{model} failed: {e}. Trying the next model.")
else:
    print("No model could answer")
    sys.exit(1)
