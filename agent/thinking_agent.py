from pathlib import Path
from llm.llm_manager import LLM_Manager
from agno.agent import Agent
from config.setting import Setting
from db.db_manager import DbManager
from memory.user_memory import UserMemory


class ThinkingAgent(Agent):
    def __init__(
        self,
        db: DbManager,
        model: LLM_Manager,
        memory_manager: UserMemory,
        setting: Setting,
        tools: list = [],
        *args,
        **kwargs,
    ):
        super().__init__(
            db=db.get_db(),
            model=model.get_model(),
            memory_manager=memory_manager,
            tools=tools,
            name="ThinkingAgent",
            additional_context=self.load_system_message(),
            tool_call_limit=setting.TOOL_CALL_LIMIT,
            add_history_to_context=True,
            num_history_runs=setting.NUM_HISTORY_RUNS,
            # enable_agentic_memory=True,
            markdown=True,
            reasoning=True,
            reasoning_min_steps=1,
            reasoning_max_steps=8,
            *args,
            **kwargs,
        )

    def load_system_message(self):
        project_root = Path(__file__).resolve().parent.parent
        prompt_path = project_root / "prompt" / "thinking_agent_prompt.txt"

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"System message file not found. Checked: {prompt_path}"
            )

        return prompt_path.read_text(encoding="utf-8")
