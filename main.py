from ai_agent.agent import AIAgent
from ai_agent.task_types import list_available_tasks
from ai_agent.logger import logger
from ai_agent.exceptions import AIAgentException
import sys
import os

# Fix encoding issue on Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def print_help():
    """In ra hướng dẫn sử dụng"""
    print("\n" + "="*60)
    print("AI Agent Task Runner - Optimized & Extended")
    print("="*60)
    
    print("\nUSAGE:")
    print("  python main.py [COMMAND] [TASK_TYPE] [STRATEGY]\n")
    
    print("COMMANDS:")
    print("  (none)           - Run task (default)")
    print("  --help, -h       - Show this help")
    print("  --metrics, -m    - Show execution metrics")
    print("  --config, -c     - Show configuration")
    print("  --version, -v    - Show version info\n")
    
    print("TASK TYPES:")
    for task_id, config in list_available_tasks().items():
        print(f"  {task_id:12} - {config.description}")
        print(f"                Max steps: {config.max_steps}, Difficulty: {config.difficulty}/5")
    
    print("\nSTRATEGIES:")
    print("  adaptive     - Thích ứng (Cân bằng)")
    print("  aggressive   - Tấn công (Nhanh)")
    print("  conservative - Bảo thủ (Cẩn trọng)")
    
    print("\nEXAMPLES:")
    print("  python main.py wedding_timeline            # Lập kịch bản đám cưới")
    print("  python main.py wedding_budget aggressive   # Lập ngân sách đám cưới nhanh")
    print("  python main.py birthday_theme              # Thiết kế chủ đề sinh nhật")
    print("  python main.py --metrics                   # Show execution metrics")
    print("  python main.py --config                    # Show configuration")
    print("="*60 + "\n")

def main():
    """Main entry point với error handling"""
    try:
        # Xử lý arguments
        task_type = "wedding_timeline"
        strategy = "adaptive"
        command = None
        
        if len(sys.argv) > 1:
            if sys.argv[1] in ["--help", "-h", "help"]:
                print_help()
                return 0
            elif sys.argv[1] in ["--metrics", "metrics", "-m"]:
                # Show metrics
                from ai_agent.metrics import get_metrics_collector
                collector = get_metrics_collector()
                collector.print_summary()
                return 0
            elif sys.argv[1] in ["--config", "config", "-c"]:
                # Show config
                from ai_agent.config import get_config
                cfg = get_config()
                print("\n" + "="*60)
                print("CONFIGURATION")
                print("="*60)
                for key, value in cfg.get_all().items():
                    print(f"{key}: {value}")
                print("="*60 + "\n")
                return 0
            elif sys.argv[1] in ["--version", "-v"]:
                print("\nAI Agent v1.0 - Optimized & Extended")
                print("Features: Multi-task, Multi-strategy, Metrics, Persistence\n")
                return 0
            else:
                task_type = sys.argv[1]
        
        if len(sys.argv) > 2:
            strategy = sys.argv[2]
        
        logger.info(f"Starting application - Task: {task_type}, Strategy: {strategy}")
        
        # Validate inputs
        from ai_agent.task_types import TASK_DEFINITIONS
        if task_type not in TASK_DEFINITIONS:
            print(f"\nError: Unknown task type '{task_type}'")
            print(f"Available tasks: {', '.join(TASK_DEFINITIONS.keys())}\n")
            logger.error(f"Invalid task type: {task_type}")
            return 1
        
        if strategy not in ["adaptive", "aggressive", "conservative"]:
            print(f"\nError: Unknown strategy '{strategy}'")
            print("Available strategies: adaptive, aggressive, conservative\n")
            logger.error(f"Invalid strategy: {strategy}")
            return 1
        
        # Khởi tạo và chạy agent
        agent = AIAgent(
            task_name=f"Hoàn thành {task_type.title()} Task",
            task_type=task_type,
            strategy=strategy
        )
        
        print(f"\n{'='*60}")
        print("AI Agent Task Runner")
        print(f"   Task: {task_type.upper()}")
        print(f"   Strategy: {strategy.upper()}")
        print(f"{'='*60}\n")
        
        agent.run()
        
        logger.info("Application completed successfully")
        return 0
        
    except AIAgentException as e:
        print(f"\nAI Agent Error: {str(e)}\n")
        logger.error(f"AI Agent Error: {str(e)}")
        return 1
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user\n")
        logger.warning("Application interrupted by user")
        return 130
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}\n")
        logger.critical(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)