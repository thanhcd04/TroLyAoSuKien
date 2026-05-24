"""Custom exceptions cho AI Agent"""

class AIAgentException(Exception):
    """Base exception cho tất cả AI Agent errors"""
    pass

class TaskTypeError(AIAgentException):
    """Lỗi khi task type không hợp lệ"""
    pass

class StrategyError(AIAgentException):
    """Lỗi khi strategy không hợp lệ"""
    pass

class EnvironmentError(AIAgentException):
    """Lỗi liên quan đến Environment"""
    pass

class PlannerError(AIAgentException):
    """Lỗi liên quan đến Planner"""
    pass

class ExecutorError(AIAgentException):
    """Lỗi liên quan đến Executor"""
    pass

class AgentError(AIAgentException):
    """Lỗi liên quan đến Agent"""
    pass
