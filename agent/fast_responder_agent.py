from pathlib import Path
from llm.llm_manager import LLM_Manager
from agno.agent import Agent
from config.setting import Setting
from db.db_manager import DbManager
from memory.user_memory import UserMemory


class FastAgent(Agent):
    def __init__(
        self,
        db: DbManager | None = None,
        model: LLM_Manager | None = None,
        memory_manager: UserMemory | None = None,
        setting: Setting | None = None,
        tools: list | None = None,
        *args,
        **kwargs,
    ):
        # Support two init flows:
        # 1) App bootstrap passes wrapper objects (DbManager/LLM_Manager/Setting).
        # 2) agno deep_copy passes raw Agent fields back into __init__(**fields).
        if db is not None:
            kwargs.setdefault("db", db.get_db() if hasattr(db, "get_db") else db)
        if model is not None:
            kwargs.setdefault(
                "model", model.get_model() if hasattr(model, "get_model") else model
            )
        if memory_manager is not None:
            kwargs.setdefault("memory_manager", memory_manager)
        if tools is not None:
            kwargs.setdefault("tools", tools)

        kwargs.setdefault("name", "FastResponderAgent")
        kwargs.setdefault("additional_context", self.load_system_message())
        kwargs.setdefault("add_history_to_context", True)
        kwargs.setdefault("markdown", True)

        if setting is not None:
            kwargs.setdefault("tool_call_limit", setting.TOOL_CALL_LIMIT)
            kwargs.setdefault("num_history_runs", setting.NUM_HISTORY_RUNS)

        super().__init__(*args, **kwargs)

    def load_system_message(self):
        project_root = Path(__file__).resolve().parent.parent
        prompt_path = project_root / "prompt" / "fast_agent_prompt.txt"

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"System message file not found. Checked: {prompt_path}"
            )

        return prompt_path.read_text(encoding="utf-8")
