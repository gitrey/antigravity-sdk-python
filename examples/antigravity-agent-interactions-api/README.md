# Google Antigravity Agent Interactions API Examples

This directory contains Python examples demonstrating how to use the **Google Antigravity Agent Interactions API** to register custom agents, provision sandboxed developer environments, and execute complex workflows.

---

## Example Directory Structure

This repository contains two sets of examples depending on your target complexity:

### 1. Basic Agent Verification & Lifecycle Examples
These scripts demonstrate core client capabilities like agent creation, deletion, and direct interaction:
* **`agent.py`**: Directly initiates a prompt interaction with the base model, saving findings to a file.
* **`create-agent.py`**: Registers a custom developer agent (`swe`) with inline playbook rules and clones a public repository into its sandbox.
* **`review-pr.py`**: Invokes the custom `swe` agent to synchronously execute a prompt.
* **`list-agents.py`**: Lists all custom agents currently registered in your project context.
* **`delete-agent.py`**: Deletes the custom developer agent from the registry.
* **`test_agent.py`**: A self-contained script executing a full cleanup-creation-interaction lifecycle test.

### 2. Advanced Code Review Agent Integration
Located in the [code-review/](code-review/) subdirectory, this example shows a production-like agent integration that:
* Integrates with **GitHub** and **Jira** MCP servers.
* Automatically evaluates pull request code changes.
* Maps code implementation against Jira acceptance criteria and posts markup feedback.
* Supports real-time **streaming** of agent steps, tool executions, and delta text chunks.

---

## Setup & Prerequisites

Before running any scripts, ensure your environment is configured:

1. **Google Cloud Authentication**:
   Authenticate your terminal to grant billing and service access:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Environment Variables**:
   Copy the `.env.sample` template from the project root directory and fill out the parameters:
   ```bash
   cp ../../.env.sample .env
   ```
   For details on JIRA and GitHub server configurations, refer to the advanced [code-review/README.md](code-review/README.md).

---

## Running the Basic Examples

To test a quick end-to-end flow using the default model and workspace:

```bash
# Register a simple developer agent
python3 create-agent.py

# List active agents to confirm registration
python3 list-agents.py

# Run a sample pull request review query
python3 review-pr.py

# Clean up the agent definition
python3 delete-agent.py
```
For the comprehensive Code Review agent walkthrough, see [code-review/README.md](code-review/README.md).
