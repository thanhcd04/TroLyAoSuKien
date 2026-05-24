"""Configuration management cho AI Agent"""

import json
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, asdict
from ai_agent.logger import logger
from ai_agent.exceptions import AIAgentException

# Config file path
CONFIG_DIR = Path(__file__).parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "max_iterations": 1000,
    "max_pause_count": 3,
    "log_level": "INFO",
    "enable_metrics": True,
    "enable_persistence": True,
    "persistence_format": "json",  # json or csv
    "debug_mode": False,
}

class ConfigManager:
    """Quản lý cấu hình hệ thống"""
    
    def __init__(self):
        self.config = self._load_config()
        logger.info(f"Configuration loaded: {len(self.config)} settings")
    
    def _load_config(self) -> Dict[str, Any]:
        """Tải cấu hình từ file hoặc dùng default"""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    logger.debug(f"Loaded config from {CONFIG_FILE}")
                    return {**DEFAULT_CONFIG, **config}
            else:
                logger.info("No config file found, using default config")
                return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}, using default")
            return DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """Lưu cấu hình hiện tại"""
        try:
            CONFIG_DIR.mkdir(exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Config saved to {CONFIG_FILE}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
            return False
    
    def get(self, key: str, default=None) -> Any:
        """Lấy giá trị cấu hình"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Đặt giá trị cấu hình"""
        self.config[key] = value
        logger.debug(f"Config updated: {key} = {value}")
    
    def get_all(self) -> Dict[str, Any]:
        """Lấy toàn bộ cấu hình"""
        return self.config.copy()
    
    def reset(self) -> None:
        """Reset về mặc định"""
        self.config = DEFAULT_CONFIG.copy()
        logger.info("Config reset to defaults")

# Global config instance
config_manager = ConfigManager()

def get_config() -> ConfigManager:
    """Lấy global config manager"""
    return config_manager
