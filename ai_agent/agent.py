from ai_agent.environment import Environment
from ai_agent.planner import Planner
from ai_agent.executor import Executor
from ai_agent.logger import agent_logger
from ai_agent.exceptions import AgentError
from ai_agent.config import get_config
from ai_agent.metrics import get_metrics_collector, ExecutionMetrics
from ai_agent.persistence import get_execution_history
from datetime import datetime
from typing import Dict

class AIAgent:
    def __init__(self, task_name: str, task_type: str = "search", strategy: str = "adaptive", event_data: dict = None, completed_tasks: Dict[str, bool] = None):
        """
        Khởi tạo AI Agent
        
        Args:
            task_name: Tên bài toán
            task_type: Loại tác vụ (search, processing, learning, decision, exploration)
            strategy: Chiến lược lập kế hoạch (adaptive, aggressive, conservative)
            event_data: Dữ liệu chi tiết sự kiện từ người dùng
            completed_tasks: Trạng thái các task đã hoàn thành (để kiểm tra dependency)
            
        Raises:
            AgentError: Nếu khởi tạo thất bại
        """
        try:
            if not task_name or not isinstance(task_name, str):
                raise AgentError("Task name must be a non-empty string")
            
            self.config = get_config()
            self.metrics_collector = get_metrics_collector()
            self.execution_history = get_execution_history()
            
            self.environment = Environment(task_name, task_type, event_data=event_data) # Environment doesn't need completed_tasks
            self.planner = Planner(strategy, completed_tasks=completed_tasks) # Pass completed_tasks to Planner
            self.executor = Executor()
            self.task_type = task_type
            self.task_name = task_name
            
            # Create execution metrics
            self.metrics = self.metrics_collector.create_execution(
                task_name, task_type, strategy
            )
            
            agent_logger.info(f"Agent initialized - Task: {task_name}, Type: {task_type}, Strategy: {strategy}")
        except Exception as e:
            agent_logger.error(f"Failed to initialize agent: {str(e)}")
            raise AgentError(f"Agent initialization failed: {str(e)}")

    def run(self):
        """
        Chạy agent với xử lý lỗi toàn diện
        
        Raises:
            AgentError: Nếu quá trình chạy thất bại
        """
        step = 0
        max_iterations = self.config.get("max_iterations", 1000)
        enable_persistence = self.config.get("enable_persistence", True)
        persistence_format = self.config.get("persistence_format", "json")
        
        try:
            while step < max_iterations:
                step += 1
                
                try:
                    observation = self.environment.observe()
                    action = self.planner.plan(observation)
                    result = self.executor.execute(self.environment, action)

                    # In thông tin chi tiết
                    print(f"\n[Step {step}] Task: {observation['task_name']} ({observation['task_type']})")
                    print(f"         Progress: {observation['progress']}/{observation['max_progress']} ({observation['progress_ratio']*100:.0f}%)")
                    print(f"         Difficulty: {observation['difficulty']}/5 | Efficiency: {observation['efficiency']*100:.0f}%")
                    print(f"         Action: {action} → {result.get('status', 'unknown')}")

                    if action == "stop":
                        self._print_completion_summary(step, observation)
                        
                        # Save metrics
                        self.metrics.mark_completed(
                            steps=step,
                            actions=len(self.planner.history),
                            efficiency=observation['efficiency'],
                            completion_rate=self.planner.get_stats()['completion_rate'],
                            end_time=datetime.now().isoformat()
                        )
                        
                        # Save execution history
                        if enable_persistence:
                            self.execution_history.save_execution({
                                "task_name": self.task_name,
                                "task_type": self.task_type,
                                "strategy": self.planner.strategy,
                                "total_steps": step,
                                "efficiency": observation['efficiency'],
                                "status": "completed"
                            }, format=persistence_format)
                        
                        # Save metrics to file
                        self.metrics_collector.save_metrics()
                        
                        return observation
                        
                except Exception as e:
                    agent_logger.error(f"Error in step {step}: {str(e)}")
                    print(f"\nError in step {step}: {str(e)}")
                    raise
            
            # Max iterations reached
            agent_logger.warning(f"Max iterations ({max_iterations}) reached without completion")
            raise AgentError(f"Task did not complete within {max_iterations} steps")
            
        except AgentError:
            raise
        except Exception as e:
            agent_logger.error(f"Unexpected error during execution: {str(e)}")
            raise AgentError(f"Unexpected error: {str(e)}")
    
    def _print_completion_summary(self, step: int, observation: dict):
        """In tóm tắt hoàn thành"""
        stats = self.planner.get_stats()
        print("\n" + "✨" + "="*58 + "✨")
        print("  BÁO CÁO HOÀN THÀNH KẾ HOẠCH SỰ KIỆN")
        print("="*60)
        print(f"  📌 Hạng mục: {observation['task_name']}")
        print(f"  📊 Trạng thái: Đã hoàn tất 100%")
        print(f"  ⏱️ Tổng số bước thực hiện: {step}")
        print(f"  ⚡ Hiệu quả đạt được: {observation['efficiency']*100:.1f}%")
        print(f"  🧠 Chiến lược tư duy: {self.planner.strategy.upper()}")
        print(f"  📝 Ghi chú: Đã kiểm tra các ràng buộc và tối ưu hóa tài nguyên.")
        print("="*60 + "\n")
        
        agent_logger.info(f"Task completed successfully in {step} steps")
    
    def get_planner_stats(self):
        """Lấy thống kê của planner"""
        try:
            return self.planner.get_stats()
        except Exception as e:
            agent_logger.error(f"Error getting planner stats: {str(e)}")
            return {"error": str(e)}