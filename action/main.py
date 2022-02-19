import os
import shlex
import sys
from pathlib import Path
from subprocess import run, PIPE, STDOUT

ACTION_PATH = Path(os.environ["GITHUB_ACTION_PATH"])
ENV_PATH = ACTION_PATH / ".darker-env"
ENV_BIN = ENV_PATH / ("Scripts" if sys.platform == "win32" else "bin")
OPTIONS = os.getenv("INPUT_OPTIONS", default="")
SRC = os.getenv("INPUT_SRC", default="")
VERSION = os.getenv("INPUT_VERSION", default="")
REVISION = os.getenv(
    "INPUT_REVISION", default=os.getenv("INPUT_COMMIT_RANGE", default="HEAD^")
)

print(f"INPUT_REVISION: {os.getenv("INPUT_REVISION", default="NOT SET")}")
print(f"INPUT_COMMIT_RANGE: {os.getenv("INPUT_COMMIT_RANGE", default="NOT SET")}")

run([sys.executable, "-m", "venv", str(ENV_PATH)], check=True)

req = "darker[isort]"
if VERSION:
    req += f"=={VERSION}"
pip_proc = run(
    [str(ENV_BIN / "python"), "-m", "pip", "install", req],
    stdout=PIPE,
    stderr=STDOUT,
    encoding="utf-8",
)
if pip_proc.returncode:
    print(pip_proc.stdout)
    print("::error::Failed to install Darker.", flush=True)
    sys.exit(pip_proc.returncode)


base_cmd = [str(ENV_BIN / "darker")]
proc = run(
    [*base_cmd, *shlex.split(OPTIONS), "--revision", REVISION, *shlex.split(SRC)]
)

sys.exit(proc.returncode)
