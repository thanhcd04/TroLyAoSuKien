from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from ai_agent.logger import planner_logger
from ai_agent.exceptions import PlannerError
from ai_agent.task_types import TaskType, get_task_config

@dataclass
class ActionRecord:
    action: str
    timestamp: datetime
    observation: Dict[str, object]
    
class Planner:
    VALID_STRATEGIES = ["adaptive", "aggressive", "conservative"]
    
    def __init__(self, strategy: str = "adaptive", completed_tasks: Optional[Dict[str, bool]] = None):
        """
        Khởi tạo Planner
        
        Args:
            strategy: Chiến lược lập kế hoạch
            
        Raises:
            PlannerError: Nếu strategy không hợp lệ
        """
        try:
            if strategy not in self.VALID_STRATEGIES:
                raise PlannerError(f"Invalid strategy: {strategy}. Must be one of {self.VALID_STRATEGIES}")
            
            self.history: List[ActionRecord] = []
            self.strategy = strategy
            self.pause_count = 0
            
            # Lưu trữ trạng thái hoàn thành task dưới dạng Enum để kiểm tra dependency
            self.completed_tasks: Dict[TaskType, bool] = {}
            if completed_tasks:
                for k, v in completed_tasks.items():
                    try:
                        # Map từ string ID (ví dụ: "venue") sang Enum thông qua config
                        config = get_task_config(k)
                        self.completed_tasks[config.task_type] = v
                    except Exception:
                        continue
            
            planner_logger.info(f"Planner initialized with strategy: {strategy}")
        except Exception as e:
            planner_logger.error(f"Failed to initialize planner: {str(e)}")
            raise PlannerError(f"Planner initialization failed: {str(e)}")
    
    def plan(self, observation: Dict[str, object]) -> str:
        """
        Lập kế hoạch hành động dựa trên quan sát
        - Phân tích tiến độ hiện tại
        - Đánh giá tốc độ tiến hành
        - Chọn chiến lược phù hợp
        
        Args:
            observation: Quan sát từ environment
            
        Returns:
            Hành động được chọn
            
        Raises:
            PlannerError: Nếu lập kế hoạch thất bại
        """
        try:
            if not observation or not isinstance(observation, dict):
                raise PlannerError("Observation must be a non-empty dictionary")
            
            # Nếu hoàn thành, dừng
            if observation.get("done", False):
                self.pause_count = 0
                planner_logger.info("Task completed - returning 'stop'")
                return "stop"
            
            # Lấy thông tin hiện tại
            progress = observation.get("progress", 0)
            remaining = observation.get("remaining", 0)
            max_progress = progress + remaining
            
            if not isinstance(progress, int) or not isinstance(remaining, int):
                raise PlannerError(f"Invalid progress data: progress={progress}, remaining={remaining}")
            
            # Kiểm tra ràng buộc task (Dependency Check)
            current_task_type_str = observation.get("task_type")
            if current_task_type_str:
                config = get_task_config(current_task_type_str)
                if config.required_task and not self.completed_tasks.get(config.required_task, False):
                    planner_logger.warning(f"Tác vụ {current_task_type_str} yêu cầu hoàn thành {config.required_task.value} trước.")
                    return "pause"
            
            # Phân tích lịch sử
            completion_rate = self._calculate_completion_rate()
            
            # Chọn hành động dựa trên chiến lược
            action = self._select_action(
                progress, 
                remaining, 
                max_progress, 
                completion_rate,
                current_task_type_str
            )
            
            # Track pause count to prevent infinite loops
            if action == "pause":
                self.pause_count += 1
                # Force advance if paused too many times (max 3 pauses)
                if self.pause_count > 3:
                    action = "advance"
                    self.pause_count = 0
                    planner_logger.warning("Pause count exceeded, forcing advance")
            else:
                self.pause_count = 0
            
            # Ghi lại hành động
            self.history.append(ActionRecord(
                action=action,
                timestamp=datetime.now(),
                observation=observation.copy()
            ))
            
            planner_logger.debug(f"Selected action: {action} (progress: {progress}/{max_progress})")
            return action
            
        except Exception as e:
            planner_logger.error(f"Error in plan: {str(e)}")
            raise PlannerError(f"Planning failed: {str(e)}")
    
    def _calculate_completion_rate(self) -> float:
        """Tính toán tốc độ hoàn thành trung bình"""
        try:
            if not self.history:
                return 1.0
            
            total_steps = len(self.history)
            last_progress = self.history[-1].observation.get("progress", 0)
            return last_progress / total_steps if total_steps > 0 else 1.0
        except Exception as e:
            planner_logger.warning(f"Error calculating completion rate: {str(e)}")
            return 1.0
    
    def _select_action(self, progress: int, remaining: int, 
                      max_progress: int, completion_rate: float, task_type_str: Optional[str] = None) -> str:
        """Chọn hành động dựa trên chiến lược"""
        try:
            task_config = get_task_config(task_type_str) if task_type_str else None

            if self.strategy == "adaptive":
                # Chiến lược thích ứng: thay đổi tốc độ dựa trên tiến độ
                progress_ratio = progress / max_progress if max_progress > 0 else 0
                
                # Nếu là lập ngân sách, cần kiểm tra kỹ hơn ở giai đoạn cuối
                if task_config and task_config.task_type == TaskType.WEDDING_BUDGET and progress_ratio > 0.8:
                    return "pause" if progress % 2 != 0 else "advance"

                if progress_ratio < 0.4:
                    return "advance"
                elif progress_ratio < 0.7:
                    return "advance"
                else:
                    if progress % 2 == 0:
                        return "advance"
                    else:
                        return "pause"
            
            elif self.strategy == "aggressive":
                return "advance"
            
            else:  # conservative
                if remaining <= 2:
                    return "advance"
                elif self.pause_count > 0:
                    return "advance"
                else:
                    return "pause"
                    
        except Exception as e:
            planner_logger.error(f"Error in _select_action: {str(e)}")
            return "advance"  # Default safe action
    
    def get_history(self) -> List[ActionRecord]:
        """Trả về lịch sử hành động"""
        return self.history.copy()
    
    def get_stats(self) -> Dict:
        """Thống kê hoạt động"""
        try:
            return {
                "total_actions": len(self.history),
                "strategy": self.strategy,
                "completion_rate": self._calculate_completion_rate(),
                "pause_count": self.pause_count
            }
        except Exception as e:
            planner_logger.error(f"Error getting stats: {str(e)}")
            return {"error": str(e)}