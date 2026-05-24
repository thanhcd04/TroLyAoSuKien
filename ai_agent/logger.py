"""Logging configuration cho AI Agent"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# Tạo thư mục logs nếu chưa tồn tại
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Log file names
LOG_FILE = LOGS_DIR / f"ai_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
ERROR_LOG_FILE = LOGS_DIR / "errors.log"

# Định dạng log
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DETAILED_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"

class ColoredFormatter(logging.Formatter):
    """Custom formatter với màu sắc cho console"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        if sys.stdout.isatty():  # Only use colors if terminal supports it
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        return super().format(record)

def setup_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    """
    Thiết lập logger với console và file handlers
    
    Args:
        name: Tên logger
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Tránh duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler (INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # File handler (DEBUG level - ghi tất cả)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(DETAILED_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # Error file handler (ERROR level trở lên)
    error_handler = logging.FileHandler(ERROR_LOG_FILE)
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(DETAILED_FORMAT)
    error_handler.setFormatter(error_formatter)
    
    # Thêm handlers vào logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    return logger

# Tạo global logger instances
logger = setup_logger("ai_agent")
task_logger = setup_logger("ai_agent.task")
env_logger = setup_logger("ai_agent.environment")
planner_logger = setup_logger("ai_agent.planner")
executor_logger = setup_logger("ai_agent.executor")
agent_logger = setup_logger("ai_agent.agent")

def get_logger(name: str) -> logging.Logger:
    """Lấy logger với tên cụ thể"""
    return logging.getLogger(name)
