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
    ):
        self.memory_manager = MemoryManager(
            db=db.get_db(),
            model=model.get_model(),
            system_message=(
                self.load_instructions() if use_custom_instructions else None
            ),
            memory_capture_instructions=(
                self.load_capture_instructions() if use_custom_instructions else None
            ),
        )

        self.memory_manager.optimize_memories(
            strategy=MemoryOptimizationStrategyType.SUMMARIZE,
            apply=True,  # Set to False to preview without saving
        )

    def get_intructions(self):
        return self.memory_manager.get_system_message()

    def load_instructions(self) -> list[str]:
        project_root = Path(__file__).resolve().parent.parent
        prompt_path = project_root / "prompt" / "memory_system_msg.txt"

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"Memory instruction file not found. Checked: {prompt_path}"
            )

        return prompt_path.read_text(encoding="utf-8").splitlines()

    def load_capture_instructions(self) -> list[str]:
        project_root = Path(__file__).resolve().parent.parent
        prompt_path = project_root / "prompt" / "memory_capture_prompt.txt"

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"Memory capture instruction file not found. Checked: {prompt_path}"
            )

        return prompt_path.read_text(encoding="utf-8").splitlines()
