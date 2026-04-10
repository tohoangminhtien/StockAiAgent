from llm.llm_manager import LLM_Manager
from db.db_manager import DbManager
from pathlib import Path
from agno.memory import (
    MemoryManager,
    MemoryOptimizationStrategyType,
)


class UserMemory(MemoryManager):
    def __init__(
        self,
        db: DbManager,
        model: LLM_Manager,
        use_custom_instructions: bool = False,
        optimize_on_init: bool = False,
        **kwargs,
    ):
        additional_instructions = None
        memory_capture_instructions = None

        if use_custom_instructions:
            additional_instructions = self.load_file("memory_system_msg.txt")
            memory_capture_instructions = self.load_file("memory_capture_prompt.txt")

        super().__init__(
            db=db.get_db(),
            model=model.get_model(),
            additional_instructions=additional_instructions,
            memory_capture_instructions=memory_capture_instructions,
            **kwargs,
        )

        if optimize_on_init:
            self.optimize_memories(
                strategy=MemoryOptimizationStrategyType.SUMMARIZE,
                apply=True,
            )

        print("Prompts loaded successfully.")

    # -------------------
    # Helpers
    # -------------------

    def load_file(self, filename: str) -> str:
        project_root = Path(__file__).resolve().parent.parent
        path = project_root / "prompt" / filename

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        return path.read_text(encoding="utf-8")

    def get_instructions(self):
        return self.get_system_message()
