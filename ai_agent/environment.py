from dataclasses import dataclass
from ai_agent.task_types import get_task_config, TaskType
from ai_agent.logger import env_logger
from ai_agent.exceptions import EnvironmentError
import random

@dataclass
class EnvironmentState:
    task_name: str
    task_type: str
    progress: int = 0
    max_progress: int = 5
    difficulty: int = 1
    efficiency: float = 1.0  # Hiệu suất công việc (1.0 = 100%)
    current_milestone: str = "Khởi tạo tác vụ..."

# Dữ liệu mô phỏng cho các giai đoạn sự kiện
TASK_MILESTONES = {
    TaskType.WEDDING_TIMELINE: [
        "Xác định thời gian làm lễ gia tiên và rước dâu.",
        "Sắp xếp thứ tự phát biểu và nghi thức rót rượu/cắt bánh.",
        "Lập khung giờ đón khách và khai tiệc.",
        "Điều phối lịch trình quay phim và chụp ảnh phóng sự.",
        "Hoàn tất kịch bản chạy chương trình (Timeline) chi tiết."
    ],
    TaskType.WEDDING_BUDGET: [
        "Dự toán chi phí thực đơn theo số lượng bàn tiệc.",
        "Tính toán ngân sách cho trang trí hoa tươi và cổng chào.",
        "Dự trù chi phí trang phục cưới và trang điểm.",
        "Phân bổ quỹ dự phòng cho các chi phí phát sinh (quá bàn, đồ uống).",
        "Chốt bảng ngân sách cuối cùng và danh sách nhà cung cấp."
    ],
    TaskType.BIRTHDAY_THEME: [
        "Lựa chọn chủ đề (Siêu nhân, Công chúa, Rừng xanh...).",
        "Thiết kế phông nền (Backdrop) và khu vực chụp ảnh.",
        "Lên danh sách phụ kiện trang trí (Bóng bay, bảng tên, nến).",
        "Đặt thiết kế bánh kem theo chủ đề đã chọn.",
        "Duyệt thiết kế tổng thể không gian tiệc."
    ],
    TaskType.BIRTHDAY_GAMES: [
        "Lên danh sách các trò chơi vận động nhẹ tại chỗ.",
        "Chuẩn bị danh sách quà tặng cho người thắng cuộc.",
        "Thuê chú hề tạo hình bong bóng hoặc ảo thuật gia.",
        "Sắp xếp trình tự các tiết mục hoạt náo.",
        "Sẵn sàng kịch bản giải trí cho khách mời nhí."
    ]
}

class Environment:
    def __init__(self, task_name: str, task_type: str = "search", event_data: dict = None):
        """
        Khởi tạo môi trường với loại tác vụ
        
        Args:
            task_name: Tên bài toán
            task_type: Loại tác vụ (search, processing, learning, decision, exploration)
            
        Raises:
            EnvironmentError: Nếu khởi tạo thất bại
        """
        try:
            if not task_name or not isinstance(task_name, str):
                raise EnvironmentError("Task name must be a non-empty string")
            
            task_config = get_task_config(task_type)
            
            self.state = EnvironmentState(
                task_name=task_name,
                task_type=task_type,
                progress=0,
                max_progress=task_config.max_steps,
                difficulty=task_config.difficulty,
                efficiency=1.0,
                current_milestone="Bắt đầu lập kế hoạch..."
            )
            self.task_config = task_config
            self.action_count = 0
            self.event_data = event_data or {}
            
            env_logger.info(f"Environment initialized: {task_name} ({task_type})")
        except Exception as e:
            env_logger.error(f"Failed to initialize environment: {str(e)}")
            raise EnvironmentError(f"Environment initialization failed: {str(e)}")

    def observe(self) -> dict:
        """Quan sát trạng thái hiện tại của môi trường"""
        try:
            progress_ratio = (self.state.progress / self.state.max_progress 
                             if self.state.max_progress > 0 else 0)
            
            observation = {
                "task_name": self.state.task_name,
                "task_type": self.state.task_type,
                "progress": self.state.progress,
                "remaining": self.state.max_progress - self.state.progress,
                "max_progress": self.state.max_progress,
                "progress_ratio": progress_ratio,
                "difficulty": self.state.difficulty,
                "efficiency": self.state.efficiency,
                "done": self.state.progress >= self.state.max_progress,
                "milestone": self.state.current_milestone
            }
            
            env_logger.debug(f"Observation: progress={self.state.progress}/{self.state.max_progress}")
            return observation
        except Exception as e:
            env_logger.error(f"Error observing environment: {str(e)}")
            raise EnvironmentError(f"Observation failed: {str(e)}")

    def apply_action(self, action: str) -> dict:
        """
        Thực hiện hành động và cập nhật trạng thái
        
        Args:
            action: Hành động cần thực thi (advance, pause, stop)
            
        Returns:
            Kết quả thực thi hành động
            
        Raises:
            EnvironmentError: Nếu hành động không hợp lệ
        """
        try:
            if not isinstance(action, str):
                raise EnvironmentError(f"Action must be a string, got {type(action)}")
            
            self.action_count += 1
            
            if self.state.progress >= self.state.max_progress:
                env_logger.info("Task already completed")
                return {"status": "completed", "action_count": self.action_count}

            if action == "advance":
                # Tiến hành công việc - hiệu suất giảm nếu quá khó
                efficiency_factor = 1.0 - (self.state.difficulty * 0.05)
                
                if self.state.progress % 2 == 0:
                    # Mỗi 2 bước, cập nhật efficiency
                    self.state.efficiency = max(0.5, efficiency_factor)
                
                # Mô phỏng rủi ro ngẫu nhiên (5% cơ hội gặp sự cố)
                if random.random() < 0.05 and self.state.progress > 1:
                    self.state.efficiency *= 0.8
                    env_logger.warning("Rủi ro phát sinh: Có sự thay đổi bất ngờ trong kế hoạch!")
                    return {"status": "risk_detected", "message": "Gặp sự cố nhỏ, Agent đang điều chỉnh...", "progress": self.state.progress}
                
                self.state.progress += 1
                
                # Cập nhật thông tin cột mốc dựa trên progress
                milestones = TASK_MILESTONES.get(self.task_config.task_type, [])
                if milestones:
                    # Tính toán index đảm bảo không âm và dàn trải đều
                    progress_idx = max(0, self.state.progress - 1)
                    idx = min(len(milestones) - 1, int(progress_idx / self.state.max_progress * len(milestones)))
                    self.state.current_milestone = milestones[idx]

                env_logger.debug(f"Action advance: progress={self.state.progress}")
                
                return {
                    "status": "advanced",
                    "progress": self.state.progress,
                    "milestone": self.state.current_milestone,
                    "efficiency": self.state.efficiency
                }
            
            elif action == "pause":
                # Tạm dừng để đánh giá - giữ nguyên progress
                env_logger.debug("Action pause: evaluating state")
                return {
                    "status": "paused",
                    "message": "Evaluating current state",
                    "progress": self.state.progress
                }
            
            elif action == "stop":
                env_logger.info("Action stop: terminating task")
                return {"status": "stopped"}

            else:
                env_logger.warning(f"Unknown action: {action}")
                return {"status": "idle", "progress": self.state.progress}
                
        except Exception as e:
            env_logger.error(f"Error applying action '{action}': {str(e)}")
            raise EnvironmentError(f"Action execution failed: {str(e)}")