from llm.llm_manager import LLM_Manager
from agno.agent import Agent
from config.setting import Setting
from db.db_manager import DbManager
from memory.user_memory import UserMemory


class FastAgent(Agent):
    def __init__(
        self,
        setting: Setting,
        db_manager: DbManager,
        memory_manager: UserMemory,
        llm_manager: LLM_Manager,
    ):
        super().__init__(setting, db_manager, memory_manager, llm_manager)
        self.name = "Fast Agent"
        self.description = (
            "A fast responder agent that provides quick answers to user queries."
        )
