# quickstart : connect the selected agent backend
"""Agno agent exposed over AG-UI, for the CopilotKit Angular harness.

HARNESS (FINDINGS.md #1): the Angular Agno quickstart's backend step is only
`<!-- setup skipped: agent-setup is not bundled for agno -->`, so this file is
the Agno React quickstart's backend (https://docs.copilotkit.ai/agno/quickstart:
`Agent` + `AgentOS(interfaces=[AGUI(agent=agent)])`), plus the tools the Angular
guide pages call for:

* `getWeather` - the server-side tool the Frontend tools guide renders.
* `update_language` - writes Agno session state (Shared state guide).

Port 8271 (workspace port plan; the doc uses 8000).
"""
from __future__ import annotations

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.run import RunContext
from dotenv import load_dotenv

load_dotenv()


# frontend tools : server tool getWeather start
def getWeather(location: str) -> str:
    """Get the weather for a location."""
    normalized = location.strip() or "the requested location"
    return f"The weather for {normalized} is 70 degrees."
# frontend tools : server tool getWeather end


# shared state : update language tool start
def update_language(run_context: RunContext, language: str) -> str:
    """Set the user's preferred language: 'english' or 'spanish'."""
    if run_context.session_state is None:
        run_context.session_state = {}
    run_context.session_state["language"] = (language or "").strip().lower()
    return f"Language updated to {language}."
# shared state : update language tool end


# quickstart : agno agent start
agent = Agent(
    model=OpenAIChat(reasoning_effort="none", id="gpt-6-luna"),
    description="A helpful assistant that can answer questions and provide information.",
    instructions="Be helpful and friendly. Format your responses using markdown where appropriate.",
    tools=[getWeather, update_language],  # HARNESS: tools the Angular guide pages call
    # HARNESS (FINDINGS.md #18): without a db every frontend tool run dies with
    # "Frontend tool resume requires a database"; db from the Agno React frontend-tools page.
    db=SqliteDb(db_file="tmp/agno.db"),
)

agent_os = AgentOS(agents=[agent], interfaces=[AGUI(agent=agent)])
app = agent_os.get_app()
# quickstart : agno agent end

if __name__ == "__main__":
    agent_os.serve(app="main:app", port=8271, reload=True)  # HARNESS: port 8271 (doc: 8000)
