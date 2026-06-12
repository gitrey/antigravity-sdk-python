# GCP Terms of Service & Automated Engineering Review Agent

This directory contains advanced Python examples demonstrating how to construct, configure, and orchestrate autonomous engineering agents using the **Google Antigravity SDK** on **Agent Platform**.

Specifically, this workflow registers an autonomous Software Engineering Agent (`swe-reviewer`) provisioned with Cloud Storage data source mounts and triggers it to review remote code modifications using a rich real-time event streaming pipeline.

---

## 🏗 Directory Structure

* **`utils.py`**: A central configuration helper that automatically discovers local `.env` files, extracts environment variables, and instantiates the Agent Platform `genai.Client` with necessary billing user-project headers.
* **`swe-review-agent.py`**: Idempotently registers the `swe-reviewer` custom agent definition in the Agent Platform Agent Registry. It attaches secure Cloud Storage source mounts (`type: "gcs"`) and establishes outbound network allowlists.
* **`review-pr.py`**: Triggers a long-running, remote background review interaction and streams execution events, tool executions, and thought deltas back to your terminal in real time.

---

## ⚙️ Environment Configuration

Before executing the scripts, ensure your environment is authenticated and properly parameterized. You can export these directly or define them in a flat `.env` file located in or above this directory.

### Required Environment Variables

| Variable | Default Fallback | Description |
| :--- | :--- | :--- |
| `GOOGLE_CLOUD_PROJECT` | `YOUR_GCP_PROJECT_ID` | The Google Cloud Project ID where Agent Platform is enabled and where your Cloud Storage source bucket resides. |
| `GEMINI_API_KEY` | *(None)* | Optional API key if you are not relying exclusively on standard Google Application Default Credentials (ADC). |

### Authentication Setup

Authenticate your session by exporting your API key exactly as established in the primary SDK documentation:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Alternatively, if you are executing within an enterprise context using Google Application Default Credentials (ADC):
```bash
gcloud auth login
gcloud auth application-default login
```

---

## 🚀 Execution Guide

Follow these exact operational steps to launch the autonomous agent workflow:

### Step 1: Initialize Virtual Environment & Install Dependencies
Set up an isolated Python virtual environment and install the target SDK package:

```bash
# Create and activate local virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the Google Antigravity SDK
pip install --upgrade pip
pip install google-antigravity
```

### Step 2: Sync Source Guidelines to Cloud Storage
Because Agent Platform remote base environments rely on Cloud Storage source pointers, first ensure your custom Markdown playbooks are uploaded to your project's target bucket (e.g., `gs://<PROJECT_ID>-agents`):

```bash
# Upload your local engineering guidelines to Cloud Storage
gcloud storage cp ../../scratch/AGENTS.md gs://YOUR_GCP_PROJECT_ID-agents/.agents/AGENTS.md
```

### Step 3: Register the custom Agent
Run the registration script. This automatically deletes any pre-existing agent definition to prevent conflicts (`409 Requested entity already exists`) and registers your latest instructions:

```bash
python3 swe-review-agent.py
```
*Expected output:* `Created agent: swe-reviewer` *(or its fully qualified Agent Platform resource name)*.

### Step 4: Trigger Real-Time Streaming Review
Execute the interaction script. This establishes an unbuffered, asynchronous background stream with the secure cloud container, displaying each execution phase (`step.start`, `step.delta`, `step.stop`) and streaming the agent's textual evaluation deltas:

```bash
python3 review-pr.py
```
*Expected behavior:* The terminal will establish connection and display real-time execution steps as the agent mounts the remote repository, analyzes code changes, and presents structured engineering feedback.
