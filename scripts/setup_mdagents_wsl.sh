#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/mnt/c/Users/Danqi/Documents/New project/ARIS-paper-workspace"
BASELINE_DIR="$WORKSPACE/baselines/MDAgents"
ENV_NAME="mdagents"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found. Open the shell where your Miniconda base environment is active."
  exit 1
fi

if ! conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  conda create -n "$ENV_NAME" python=3.10 -y
fi

set +u
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
set -u

cd "$BASELINE_DIR"
python --version
python -m pip install --upgrade pip
python -m pip install "setuptools<81"
python -m pip install -r requirements.txt
python -m pip install "httpx<0.28"
python -m pip install google-generativeai

python - <<'PY'
import openai
import tqdm
import requests
import prettytable
import termcolor
import pptree
import climage
import google.generativeai
print("MDAgents dependencies import successfully.")
PY
