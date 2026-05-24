from ai_agent.environment import Environment
from ai_agent.logger import executor_logger
from ai_agent.exceptions import ExecutorError

class Executor:
    VALID_ACTIONS = ["advance", "pause", "stop"]
    
    def execute(self, environment: Environment, action: str) -> dict:
        """
        Thực thi hành động trong môi trường
        - advance: tiến hành
        - pause: tạm dừng/đánh giá
        - stop: dừng lại
        
        Args:
            environment: Environment instance
            action: Hành động cần thực thi
            
        Returns:
            Kết quả thực thi
            
        Raises:
            ExecutorError: Nếu hành động không hợp lệ hoặc thực thi thất bại
        """
        try:
            # Validate inputs
            if not environment:
                raise ExecutorError("Environment is required")
            
            if not isinstance(action, str):
                raise ExecutorError(f"Action must be a string, got {type(action)}")
            
            action = action.lower().strip()
            
            if action not in self.VALID_ACTIONS:
                executor_logger.warning(f"Unknown action: {action}, using default behavior")
                return {"status": "unknown", "message": f"Unknown action: {action}"}
            
            executor_logger.debug(f"Executing action: {action}")
            
            if action == "pause":
                # Tạm dừng để đánh giá - không gọi apply_action
                executor_logger.info("Pausing execution for evaluation")
                return {"status": "paused", "message": "Evaluating current state"}
            
            # Gọi environment.apply_action cho advance và stop
            result = environment.apply_action(action)
            
            executor_logger.debug(f"Action result: {result}")
            return result
            
        except Exception as e:
            executor_logger.error(f"Execution failed for action '{action}': {str(e)}")
            raise ExecutorError(f"Execution failed: {str(e)}")