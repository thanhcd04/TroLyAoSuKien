from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum
from ai_agent.logger import task_logger
from ai_agent.exceptions import TaskTypeError

class TaskType(Enum):
    WEDDING_TIMELINE = "wedding_timeline"  # Kịch bản đám cưới
    WEDDING_BUDGET = "wedding_budget"      # Ngân sách đám cưới
    BIRTHDAY_THEME = "birthday_theme"      # Chủ đề sinh nhật
    BIRTHDAY_GAMES = "birthday_games"      # Kịch bản trò chơi
    GENERAL_LOGISTICS = "logistics"        # Hậu cần chung

@dataclass
class TaskConfig:
    """Cấu hình cho một loại tác vụ"""
    name: str
    task_type: TaskType
    max_steps: int
    difficulty: int  # 1-5 (1=dễ, 5=rất khó)
    description: str
    required_task: TaskType = None  # Task cần hoàn thành trước đó
    
    def __post_init__(self):
        """Validate task config"""
        if not 1 <= self.difficulty <= 5:
            raise TaskTypeError(f"Difficulty must be between 1-5, got {self.difficulty}")
        if self.max_steps < 1:
            raise TaskTypeError(f"Max steps must be >= 1, got {self.max_steps}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.task_type.value,
            "max_steps": self.max_steps,
            "difficulty": self.difficulty,
            "description": self.description
        }

# Định nghĩa các loại task
TASK_DEFINITIONS = {
    "wedding_timeline": TaskConfig(
        name="Wedding Timeline",
        task_type=TaskType.WEDDING_TIMELINE,
        max_steps=6,
        difficulty=3,
        description="Lập lịch trình chi tiết từ lễ gia tiên đến tiệc chính"
    ),
    "wedding_budget": TaskConfig(
        name="Wedding Budget",
        task_type=TaskType.WEDDING_BUDGET,
        max_steps=8,
        difficulty=4,
        description="Quản lý chi phí sính lễ, nhà hàng, quay phim và chụp ảnh"
    ),
    "birthday_theme": TaskConfig(
        name="Birthday Theme",
        task_type=TaskType.BIRTHDAY_THEME,
        max_steps=5,
        difficulty=2,
        description="Thiết kế chủ đề trang trí (Concept) và lựa chọn tông màu"
    ),
    "birthday_games": TaskConfig(
        name="Birthday Games",
        task_type=TaskType.BIRTHDAY_GAMES,
        max_steps=6,
        difficulty=3,
        description="Xây dựng kịch bản trò chơi và hoạt náo viên cho trẻ nhỏ"
    )
}

def get_task_config(task_type: str) -> TaskConfig:
    """
    Lấy cấu hình task dựa trên loại
    
    Args:
        task_type: Loại task
        
    Returns:
        TaskConfig instance
        
    Raises:
        TaskTypeError: Nếu task type không hợp lệ
    """
    try:
        if task_type not in TASK_DEFINITIONS:
            first_key = list(TASK_DEFINITIONS.keys())[0]
            task_logger.warning(f"Unknown task type: {task_type}, using default ({first_key})")
            return TASK_DEFINITIONS[first_key]
        
        config = TASK_DEFINITIONS[task_type]
        task_logger.info(f"Loaded task config: {task_type}")
        return config
    except Exception as e:
        task_logger.error(f"Error getting task config for {task_type}: {str(e)}")
        raise TaskTypeError(f"Failed to get task config: {str(e)}")

def list_available_tasks() -> Dict[str, TaskConfig]:
    """Liệt kê tất cả loại task có sẵn"""
    return TASK_DEFINITIONS
