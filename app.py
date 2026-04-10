from llm.llm_manager import LLM_Manager
from config.setting import Setting
from db.db_manager import DbManager
from memory.user_memory import UserMemory
from agent.fast_responder_agent import FastAgent
from agno.tools.reasoning import ReasoningTools
from utils.metrics import print_response_summary


if __name__ == "__main__":
    setting = Setting()
    # Initialize the LLM manager with the settings
    llm_manager = LLM_Manager(setting)

    # Initialize the database manager and memory manager
    db_manager = DbManager(setting)
    user_memory = UserMemory(db_manager, llm_manager, use_custom_instructions=True)

    # Initialize the reasoning tools
    reasoning_tools = ReasoningTools(enable_analyze=False)

    # Create an instance of the FastAgent
    agent = FastAgent(
        db=db_manager,
        model=llm_manager,
        memory_manager=user_memory,
        setting=setting,
        # tools=[reasoning_tools],
        debug_mode=True,
        debug_level=2,
    )

    question = "Thủ đô của Việt Nam ở đâu? Tại sao bạn biết điều đó? Bạn có thể giải thích không?"
    # Lấy RunOutput object
    response = agent.run(question, debug_mode=True, debug_level=2)
    # print_response_summary(response)
