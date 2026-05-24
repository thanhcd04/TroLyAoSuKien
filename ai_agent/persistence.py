"""Persistence layer for execution history"""

import json
import csv
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from ai_agent.logger import logger

HISTORY_DIR = Path(__file__).parent.parent / "history"

class ExecutionHistory:
    """Quản lý lịch sử execution"""
    
    def __init__(self):
        HISTORY_DIR.mkdir(exist_ok=True)
        self.history_file = HISTORY_DIR / f"history_{datetime.now().strftime('%Y%m%d')}.json"
    
    def save_execution(self, execution_data: Dict[str, Any], format: str = "json") -> bool:
        """
        Lưu chi tiết execution
        
        Args:
            execution_data: Dữ liệu execution
            format: Định dạng lưu (json hoặc csv)
        """
        try:
            if format == "json":
                return self._save_json(execution_data)
            elif format == "csv":
                return self._save_csv(execution_data)
            else:
                logger.warning(f"Unknown format: {format}")
                return False
        except Exception as e:
            logger.error(f"Error saving execution: {str(e)}")
            return False
    
    def _save_json(self, data: Dict[str, Any]) -> bool:
        """Lưu dưới định dạng JSON"""
        try:
            history = []
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            
            history.append({
                "timestamp": datetime.now().isoformat(),
                **data
            })
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            logger.debug(f"Saved execution to {self.history_file}")
            return True
        except Exception as e:
            logger.error(f"Error in _save_json: {str(e)}")
            return False
    
    def _save_csv(self, data: Dict[str, Any]) -> bool:
        """Lưu dưới định dạng CSV"""
        try:
            csv_file = HISTORY_DIR / f"history_{datetime.now().strftime('%Y%m%d')}.csv"
            
            file_exists = csv_file.exists()
            
            with open(csv_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data.keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(data)
            
            logger.debug(f"Saved execution to {csv_file}")
            return True
        except Exception as e:
            logger.error(f"Error in _save_csv: {str(e)}")
            return False
    
    def load_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Tải lịch sử execution gần đây"""
        try:
            if not self.history_file.exists():
                return []
            
            with open(self.history_file, 'r') as f:
                history = json.load(f)
            
            return history[-limit:]  # Return last N items
        except Exception as e:
            logger.error(f"Error loading history: {str(e)}")
            return []

# Global history instance
_history = None

def get_execution_history() -> ExecutionHistory:
    """Lấy global execution history"""
    global _history
    if _history is None:
        _history = ExecutionHistory()
    return _history
