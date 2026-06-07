# Jira Product Owner Agent Example

This folder contains a complete example demonstrating how to define, register, and interact with an autonomous **Antigravity Jira Product Owner Agent** (`jira-product-owner-agent`) configured to securely manage backlog requirements via the **Atlassian Model Context Protocol (MCP)** server.

The agent connects to Jira via native MCP tools (specifically `atlassian__getJiraIssue`) using secure Atlassian authentication tokens to retrieve, analyze, and present comprehensive Jira ticket summaries, statuses, priorities, and acceptance criteria in real time.

---

## Architecture & File Structure

* **`create-agent.py`**: Deletes any pre-existing agent definition and registers the new `jira-product-owner-agent` containing strict MCP-only system instructions, an exact JSON schema argument invocation blueprint (`cloudId` and `issueIdOrKey`), and the configured Atlassian MCP tool connection.
* **`get-jira-issue.py`**: Triggers a real-time streaming interaction (`stream=True`) with the registered agent to retrieve issue details asynchronously. It instantly outputs step lifecycle events (`step.start`), detailed tool invocations, internal model thinking, and generated text deltas directly to standard output.
* **`utils.py`**: Shared helper module that searches parent directories for your repository root `.env` configuration, instantiates a Vertex AI configured `genai.Client` with user billing headers (`X-Goog-User-Project`), and securely fetches credentials from Google Cloud Secret Manager.

---

## Prerequisites

1. **Google Cloud Project**: You need an active Google Cloud Project with Vertex AI and Secret Manager APIs enabled.
2. **Authenticated Environment**: Authenticate your runtime session:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. **Configuration**:
   Ensure your repository root `.env` file defines your target Google Cloud Project and Jira Cloud instance identifiers:
   ```env
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   JIRA_INSTANCE=https://your-domain.atlassian.net/
   JIRA_PROJECT_KEY=GENDEV
   JIRA_CLOUD_ID=your-jira-cloud-id
   ```

---

## How to Run

### 1. Register the Agent Definition
Run the setup script to provision the locked-down MCP agent definition on Vertex AI:
```bash
python create-agent.py
```

### 2. Retrieve a Jira Issue (Real-Time Stream)
Launch an unbuffered stream to instantly inspect the agent's MCP tool calls, model thinking deltas, and retrieved ticket acceptance criteria:
```bash
PYTHONUNBUFFERED=1 python get-jira-issue.py
```
