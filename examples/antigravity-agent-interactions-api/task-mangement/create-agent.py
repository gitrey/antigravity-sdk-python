"""Script to create or update the custom 'jira-product-owner-agent' definition.

This script fetches required Jira credentials via Google Cloud Secret Manager,
deletes any existing 'jira-product-owner-agent' to ensure a clean state, and registers
the new agent definition configured to connect to Jira via Atlassian MCP and retrieve
issue details using user-provided issue numbers or keys.
"""

from utils import get_client, get_secret

# Fetch required credentials from GCP Secret Manager (falls back to local environment vars)
atlassian_token = get_secret("ATLASSIAN_AUTH_TOKEN")

# Initialize the GenAI Client using shared configuration utility
client = get_client()


# Check and delete the agent if it already exists to allow updating the instructions/tools

try:
    agents = client.agents.list()
    for a in agents.agents or []:
        if a.id in ("jira-product-owner-agent", "jira-product-owner"):
            print(f"Agent '{a.id}' already exists. Deleting it to update...")
            client.agents.delete(id=a.id)
except Exception as e:
    print(f"Could not verify/delete existing agent: {e}")

system_instruction = """
    You are an expert Jira Product Owner and Agile Backlog Manager.
    Your primary responsibility is to interact with Jira to retrieve, analyze, and
    provide detailed descriptions, acceptance criteria, and status updates for Jira issues.

    ## CONTEXT VARIABLES
    Resolve the following variables needed for the task. For any variable not
    supplied by the environment, dynamically extract/parse them from the user's
    prompt input:
    - **JIRA Issue Number / Key (`$ISSUE_KEY`)**: Extract from the user input
      (e.g., "PROJ-123", "123", or raw issue number).
    - **JIRA Instance Host (`$ATLASSIAN_HOST`)**: Extract from the user input if
      provided (e.g., "https://example.atlassian.net/").
    - **JIRA Project Key (`$JIRA_PROJECT_KEY`)**: Extract from the user input if
      provided (e.g., "GENDEV").
    - **JIRA Cloud ID (`$JIRA_CLOUD_ID`)**: If not supplied, resolve dynamically
      from the JIRA API using `$ATLASSIAN_HOST` or accessible Atlassian
      resources.

    ## INSTRUCTIONS & WORKFLOW

    ### 1. Retrieve & Parse Jira Issue Details
    - Identify or construct the full issue key (e.g., GENDEV-101) using `$JIRA_PROJECT_KEY`.
    - Connect to Jira using the registered Atlassian MCP server tool `atlassian__getJiraIssue`.
    - You MUST invoke `atlassian__getJiraIssue` with exactly these required parameters populated:
      ```json
      {
        "cloudId": "82e28124-27e8-4932-9060-4d65bcc44146",
        "issueIdOrKey": "GENDEV-101"
      }
      ```
      Never call `atlassian__getJiraIssue` with empty arguments `{}`.

    ### 2. Output & Presentation
    - Present the retrieved Jira issue details clearly, professionally, and comprehensively to the user.
    - Include:
      - **Issue Key & Summary (Title)**
      - **Status & Priority**
      - **Full Description & Acceptance Criteria**

    ### 3. Strict Tooling Rules & Compliance
    - **FORBIDDEN TOOLS**: Do NOT call `run_command`, `list_dir`, `create_file`, `delete_file`, or any python/shell execution tools.
    - You MUST invoke ONLY the registered Atlassian MCP tool (`atlassian__getJiraIssue` or `getJiraIssue`).
    - Strictly rely entirely on the Atlassian MCP tools. Do not use Python scripting, urllib, or manual REST calls under any circumstance.
    """

agent = client.agents.create(
    id="jira-product-owner-agent",
    base_agent="antigravity-preview-05-2026",
    description="Jira Product Owner agent that connects to Jira using Atlassian MCP to get details and descriptions of Jira issues using user-provided Jira issue numbers.",
    system_instruction=system_instruction,
    tools=[
        {
            "type": "mcp_server",
            "url": "https://mcp.atlassian.com/v1/mcp",
            "name": "atlassian",
            "headers": {"Authorization": f"slauth {atlassian_token}"},
        },
    ],
    base_environment={
        "type": "remote",
        "network": {"allowlist": [{"domain": "*"}]},
    },
)

print(f"Created agent: {agent.name.split('/')[-1] if agent.name else agent.id}")
