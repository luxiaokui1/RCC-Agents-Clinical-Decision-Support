# Baseline Setup

## Pulled Baseline

MDAgents has been cloned as the closest baseline:

```text
ARIS-paper-workspace/
  baselines/
    MDAgents/
```

Repository:

```text
https://github.com/mitmedialab/MDAgents
```

Paper:

```text
MDAgents: An Adaptive Collaboration of LLMs for Medical Decision-Making
NeurIPS 2024 Oral
```

## Why This Baseline

MDAgents is the closest prior work because it already studies adaptive collaboration structures for medical decision-making. Our RCC paper should compare against it and then add:

- role-conditioned message schema
- evidence requirements
- sender/receiver constraints
- safety critic module
- guideline/evidence verifier module
- module add/remove ablations
- audit trace output

## Environment

MDAgents requires Python 3.9+ and these packages:

```text
openai==1.14.2
tqdm==4.66.1
requests==2.31.0
prettytable==3.9
termcolor==2.4.0
pptree==3.1
climage==0.2.0
```

Your WSL environment was checked manually:

```text
Ubuntu: 20.04.6 LTS on WSL2
Python in base: 3.13.12
Python path: /root/miniconda3/bin/python3
GPU: NVIDIA GeForce RTX 4050 Laptop GPU, CUDA 12.9 visible through nvidia-smi
```

Recommended: do not install MDAgents dependencies into the `base` conda environment. Create a separate Python 3.10 environment:

```bash
conda create -n mdagents python=3.10 -y
conda activate mdagents
cd "/mnt/c/Users/Danqi/Documents/New project/ARIS-paper-workspace/baselines/MDAgents"
pip install --upgrade pip
pip install -r requirements.txt
pip install "httpx<0.28"
pip install google-generativeai
```

It imports `google.generativeai`, but the official `requirements.txt` does not list it. Add it if running Gemini baselines:

```text
google-generativeai
```

It also uses `openai==1.14.2`, which is safer with `httpx<0.28`.

## WSL Proxy Note

Your Ubuntu prints:

```text
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
```

This means Windows has a localhost proxy, but WSL cannot automatically use `127.0.0.1` as the Windows proxy endpoint in NAT mode. If `pip install` or API calls fail, set the WSL proxy to the Windows host IP instead of localhost:

```bash
export WINDOWS_HOST=$(ip route | awk '/default/ {print $3}')
export HTTP_PROXY="http://${WINDOWS_HOST}:7890"
export HTTPS_PROXY="http://${WINDOWS_HOST}:7890"
```

Replace `7890` with your actual Windows proxy port if different. If you do not use a proxy, this warning can be ignored unless network commands fail.

## API Keys

The original code expects environment variables:

```bash
export openai_api_key="..."
export genai_api_key="..."
```

On Windows PowerShell:

```powershell
$env:openai_api_key="..."
$env:genai_api_key="..."
```

Do not put API keys into the repository or paper files.

## Data Location

MDAgents loads data using paths like:

```text
../data/<dataset>/train.jsonl
../data/<dataset>/test.jsonl
```

Because the script runs inside `baselines/MDAgents`, data should be placed here:

```text
ARIS-paper-workspace/
  baselines/
    data/
      medqa/
        train.jsonl
        test.jsonl
      pubmedqa/
        train.jsonl
        test.jsonl
```

## Example Command

From:

```text
ARIS-paper-workspace/baselines/MDAgents
```

Run:

```bash
python main.py --model gpt-4o-mini --dataset medqa --difficulty adaptive --num_samples 10
```

## CUDA Note

The official MDAgents baseline mostly calls remote LLM APIs. CUDA is not required unless we later swap in local open-source models.

For your CUDA Ubuntu environment, the recommended plan is:

1. Use your existing virtual environment if it has Python 3.9+.
2. Install MDAgents dependencies into it.
3. Run the API baseline first.
4. Later, add local-model experiments only if needed.
