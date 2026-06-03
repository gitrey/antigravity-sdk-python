# Code Review Agent Example

This folder contains a complete example of a custom **Antigravity Code Review Agent** that automates pull request reviews and links findings directly to Jira issue acceptance criteria.

The agent checks code changes for security vulnerabilities, software engineering standards, compliance, and checks for alignment with business goals by performing a strict gap analysis against the corresponding Jira ticket.

---

## Architecture & File Structure

* **`create-code-review-agent.py`**: Deletes any pre-existing code review agent and registers the new `code-review-agent` definition containing the system instructions and authorized tools.
* **`review-pr.py`**: Starts a background code-review interaction asynchronously, then polls the interaction API status until completion and outputs the final markdown report.
* **`stream-review.py`**: Triggers a real-time streamed code-review interaction, printing detailed steps, tool calls, results, and text streams to stdout as they occur.
* **`inspect-agent-tools.py`**: Queries the agent registry to print all tools configured for the code review agent.
* **`list-agents.py`**: Lists all custom agents registered in your current project scope.
* **`utils.py`**: Shared helper module that loads local variables, instantiates `genai.Client` with appropriate Vertex AI billing headers (`X-Goog-User-Project`), and handles Secret Manager retrieval.

---

## Prerequisites

1. **Google Cloud Project**: You need an active Google Cloud project with Vertex AI and Secret Manager APIs enabled.
2. **Authenticated Environment**: Authenticate your terminal with:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. **Environment Setup**:
   Copy the template `.env.sample` file from the project root into your environment and populate the values:
   ```bash
   cp ../../../.env.sample .env
   ```
   Edit the `.env` file to contain your credentials and target environment details:
   ```env
   GOOGLE_CLOUD_PROJECT=your-gcp-project-id
   JIRA_INSTANCE=https://your-domain.atlassian.net/
   JIRA_PROJECT_KEY=YOURKEY
   JIRA_CLOUD_ID=your-jira-cloud-id
   ```

---

## How to Run

### 1. Register the Agent Definition
Run the setup script to provision the agent in the registry:
```bash
python3 create-code-review-agent.py
```

### 2. (Optional) Inspect the Configured Tools
Verify that the agent was created with correct access parameters and registered tools:
```bash
python3 inspect-agent-tools.py
```

### 3. Run a Pull Request Review

#### Asynchronously (Polled)
Trigger a background review run:
```bash
python3 review-pr.py
```

#### Streaming (Real-Time Output)
Stream the step-by-step agent execution, terminal output, and tool integrations directly:
```bash
python3 stream-review.py
```
