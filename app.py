from llm.llm_manager import LLM_Manager
from config.setting import Setting
from db.db_manager import DbManager
from memory.user_memory import UserMemory
from agent.fast_responder_agent import FastAgent
from agno.tools.reasoning import ReasoningTools
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI


setting = Setting()
# Initialize the LLM manager with the settings
llm_manager = LLM_Manager(setting)

# Initialize the database manager and memory manager
db_manager = DbManager(setting)
user_memory = UserMemory(db_manager, llm_manager)

# Initialize the reasoning tools
reasoning_tools = ReasoningTools(enable_analyze=False)

# Create an instance of the FastAgent
agent = FastAgent(
    db=db_manager,
    model=llm_manager,
    memory_manager=user_memory,
    setting=setting,
    tools=[reasoning_tools],
)
agent_os = AgentOS(agents=[agent], interfaces=[AGUI(agent=agent)])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="basic:app", reload=True)
