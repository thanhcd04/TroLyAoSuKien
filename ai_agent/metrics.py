"""Metrics and statistics tracking"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any
from datetime import datetime
import json
from pathlib import Path
from ai_agent.logger import logger

METRICS_DIR = Path(__file__).parent.parent / "metrics"

@dataclass
class ExecutionMetrics:
    """Metrics cho một execution"""
    task_name: str
    task_type: str
    strategy: str
    start_time: str
    end_time: str = ""
    total_steps: int = 0
    total_actions: int = 0
    efficiency: float = 0.0
    completion_rate: float = 0.0
    status: str = "running"  # running, completed, failed
    error: str = ""
    duration_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def mark_completed(self, steps: int, actions: int, efficiency: float, 
                       completion_rate: float, end_time: str):
        """Mark execution as completed"""
        self.status = "completed"
        self.total_steps = steps
        self.total_actions = actions
        self.efficiency = efficiency
        self.completion_rate = completion_rate
        self.end_time = end_time
        
        # Calculate duration
        try:
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(end_time)
            self.duration_seconds = (end - start).total_seconds()
        except:
            pass
    
    def mark_failed(self, error: str, end_time: str):
        """Mark execution as failed"""
        self.status = "failed"
        self.error = error
        self.end_time = end_time

class MetricsCollector:
    """Thu thập và lưu metrics"""
    
    def __init__(self):
        self.metrics: List[ExecutionMetrics] = []
        METRICS_DIR.mkdir(exist_ok=True)
        self._load_metrics()
    
    def _load_metrics(self):
        """Tải metrics từ file"""
        try:
            metrics_file = METRICS_DIR / "metrics.json"
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        try:
                            metric = ExecutionMetrics(
                                task_name=item['task_name'],
                                task_type=item['task_type'],
                                strategy=item['strategy'],
                                start_time=item['start_time'],
                                end_time=item.get('end_time', ''),
                                total_steps=item.get('total_steps', 0),
                                total_actions=item.get('total_actions', 0),
                                efficiency=item.get('efficiency', 0.0),
                                completion_rate=item.get('completion_rate', 0.0),
                                status=item.get('status', 'running'),
                                error=item.get('error', ''),
                                duration_seconds=item.get('duration_seconds', 0.0)
                            )
                            self.metrics.append(metric)
                        except Exception as e:
                            logger.debug(f"Error loading metric item: {str(e)}")
                    logger.debug(f"Loaded {len(self.metrics)} previous metrics")
        except Exception as e:
            logger.debug(f"Error loading metrics: {str(e)}")
    
    def create_execution(self, task_name: str, task_type: str, 
                        strategy: str) -> ExecutionMetrics:
        """Tạo metrics cho execution mới"""
        metrics = ExecutionMetrics(
            task_name=task_name,
            task_type=task_type,
            strategy=strategy,
            start_time=datetime.now().isoformat()
        )
        self.metrics.append(metrics)
        logger.debug(f"Created execution metrics: {task_name}")
        return metrics
    
    def save_metrics(self):
        """Lưu metrics vào file"""
        try:
            METRICS_DIR.mkdir(exist_ok=True)
            metrics_file = METRICS_DIR / "metrics.json"
            
            data = [m.to_dict() for m in self.metrics]
            with open(metrics_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.metrics)} metrics to {metrics_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving metrics: {str(e)}")
            return False
    
    def get_stats_by_strategy(self) -> Dict[str, Dict[str, Any]]:
        """Thống kê theo strategy"""
        stats = {}
        for metric in self.metrics:
            if metric.status == "completed":
                if metric.strategy not in stats:
                    stats[metric.strategy] = {
                        "count": 0,
                        "avg_steps": 0,
                        "avg_efficiency": 0,
                        "min_steps": float('inf'),
                        "max_steps": 0,
                        "total_duration": 0
                    }
                
                s = stats[metric.strategy]
                s["count"] += 1
                s["avg_steps"] += metric.total_steps
                s["avg_efficiency"] += metric.efficiency
                s["min_steps"] = min(s["min_steps"], metric.total_steps)
                s["max_steps"] = max(s["max_steps"], metric.total_steps)
                s["total_duration"] += metric.duration_seconds
        
        # Calculate averages
        for strategy in stats:
            s = stats[strategy]
            if s["count"] > 0:
                s["avg_steps"] = round(s["avg_steps"] / s["count"], 2)
                s["avg_efficiency"] = round(s["avg_efficiency"] / s["count"], 2)
                s["avg_duration"] = round(s["total_duration"] / s["count"], 2)
        
        return stats
    
    def get_stats_by_task(self) -> Dict[str, Dict[str, Any]]:
        """Thống kê theo task type"""
        stats = {}
        for metric in self.metrics:
            if metric.status == "completed":
                if metric.task_type not in stats:
                    stats[metric.task_type] = {
                        "count": 0,
                        "avg_efficiency": 0,
                        "completed": 0,
                        "failed": 0
                    }
                
                s = stats[metric.task_type]
                s["count"] += 1
                s["avg_efficiency"] += metric.efficiency
                if metric.status == "completed":
                    s["completed"] += 1
                else:
                    s["failed"] += 1
        
        # Calculate averages
        for task_type in stats:
            s = stats[task_type]
            if s["count"] > 0:
                s["avg_efficiency"] = round(s["avg_efficiency"] / s["count"], 2)
        
        return stats
    
    def print_summary(self):
        """In tóm tắt metrics"""
        completed = [m for m in self.metrics if m.status == "completed"]
        
        if not completed:
            print("\nNo completed tasks yet.\n")
            return
        
        print("\n" + "="*60)
        print("📊 EXECUTION METRICS SUMMARY")
        print("="*60)
        
        # Overall stats
        print(f"\nTotal Executions: {len(self.metrics)}")
        print(f"Completed: {len(completed)}")
        print(f"Failed: {len([m for m in self.metrics if m.status == 'failed'])}")
        
        # By strategy
        by_strategy = self.get_stats_by_strategy()
        if by_strategy:
            print("\n📈 By Strategy:")
            for strategy, stats in by_strategy.items():
                print(f"  {strategy.upper()}:")
                print(f"    - Executions: {stats['count']}")
                print(f"    - Avg Steps: {stats['avg_steps']}")
                print(f"    - Avg Efficiency: {stats['avg_efficiency']*100:.0f}%")
                print(f"    - Avg Duration: {stats['avg_duration']:.2f}s")
        
        # By task type
        by_task = self.get_stats_by_task()
        if by_task:
            print("\n🎯 By Task Type:")
            for task_type, stats in by_task.items():
                print(f"  {task_type.upper()}:")
                print(f"    - Executions: {stats['count']}")
                print(f"    - Avg Efficiency: {stats['avg_efficiency']*100:.0f}%")
        
        print("="*60 + "\n")

# Global metrics collector
_metrics_collector = None

def get_metrics_collector() -> MetricsCollector:
    """Lấy global metrics collector"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector
