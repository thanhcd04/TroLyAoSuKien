import sys
import os
from ai_agent.agent import AIAgent
from ai_agent.logger import logger

# Đảm bảo mã hóa UTF-8 trên Windows để hiển thị tiếng Việt chính xác
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

def run_master_event_planner():
    """
    Quy trình Master chạy toàn bộ các bước lập kế hoạch sự kiện theo trình tự logic.
    """
    # Định nghĩa luồng công việc của một sự kiện thực tế
    event_pipeline = [
        {"id": "wedding_timeline", "name": "Lập kịch bản Đám cưới"},
        {"id": "wedding_budget", "name": "Quản lý ngân sách Đám cưới"},
        {"id": "birthday_theme", "name": "Thiết kế chủ đề Sinh nhật"},
        {"id": "birthday_games", "name": "Lập kịch bản Trò chơi Sinh nhật"}
    ]
    
    print("\n" + "⭐" + "="*65 + "⭐")
    print("   HỆ THỐNG TRỢ LÝ ẢO ĐIỀU PHỐI TỔ CHỨC SỰ KIỆN TỔNG THỂ")
    print("   Trạng thái: Đang khởi động quy trình đa giai đoạn...")
    print("="*67 + "\n")

    overall_results = []
    completed_tasks_status = {} # Track completed tasks across stages
    
    for stage in event_pipeline:
        stage_id = stage["id"]
        stage_name = stage["name"]
        
        print(f"🎬 [GIAI ĐOẠN]: {stage_name.upper()}...")
        
        # Placeholder event data for master script, consistent with web_app.py
        # In a real scenario, this might come from a config file or CLI args
        default_event_data = {
            "event_name": "Sự kiện tổng thể (CLI)",
            "guest_count": 150,
            "budget_limit": 150000000
        }

        try:
            # Khởi tạo Agent cho giai đoạn hiện tại
            # Sử dụng chiến lược 'adaptive' để Agent tự điều chỉnh theo độ khó của từng task
            agent = AIAgent(
                task_name=stage_name,
                task_type=stage_id,
                strategy="adaptive",
                event_data=default_event_data, # Pass event data
                completed_tasks=completed_tasks_status # Pass the state of completed tasks
            )
            
            # Thực thi tác vụ cho đến khi hoàn thành
            final_observation = agent.run()
            
            # Update the status of completed tasks after a stage is done
            completed_tasks_status[stage_id] = True

            overall_results.append({
                "stage": stage_name,
                "result": final_observation.get("milestone", "Hoàn thành"),
                "icon": "✅"
            })
            
            print(f"✔️ Hoàn tất giai đoạn: {stage_name}\n")
            print("-" * 40)
            
        except Exception as e:
            logger.error(f"Lỗi tại giai đoạn {stage_name}: {str(e)}")
            overall_results.append({
                "stage": stage_name,
                "status": f"Gặp sự cố: {str(e)}",
                "icon": "❌"
            })
            print(f"\n⚠️ Quy trình bị gián đoạn tại bước '{stage_name}'.")
            break

    # In báo cáo tổng kết dự án
    print("\n" + "📋" + "="*65 + "📋")
    print("   BÁO CÁO TỔNG KẾT QUY TRÌNH LẬP KẾ HOẠCH SỰ KIỆN")
    print("="*67)
    for res in overall_results:
        # Lấy thông tin kết quả, ưu tiên 'result' (thành công) hoặc 'status' (lỗi)
        info = res.get('result') if 'result' in res else res.get('status', 'N/A')
        print(f"   {res['icon']} {res['stage']:<30} | {info}")
    print("="*67)
    print("   Hệ thống: Tất cả dữ liệu đã được lưu trữ vào lịch sử thực thi.")
    print("="*67 + "\n")

if __name__ == "__main__":
    run_master_event_planner()