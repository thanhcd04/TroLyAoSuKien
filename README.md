# 🤖 AI Event Planner - Trợ Lý Ảo Lập Kế Hoạch Sự Kiện

Hệ thống sử dụng AI Agent để tự động hóa quy trình lập kế hoạch cho Đám cưới và Sinh nhật, bao gồm lập kịch bản, tính toán ngân sách và quản lý rủi ro.

##  Công nghệ và Thư viện sử dụng

*   **Python 3.9+**: Ngôn ngữ lập trình chính xử lý logic AI.
*   **Streamlit**: Thư viện tạo giao diện Web trực quan.
*   **Pandas**: Xử lý dữ liệu bảng biểu và tính toán ngân sách.
*   **XlsxWriter**: Xuất báo cáo kế hoạch ra file Excel chuyên nghiệp.
*   **Logging & JSON**: Lưu trữ lịch sử hoạt động và cấu hình hệ thống.
*   **AI Agent Architecture**: Mô hình chia nhỏ logic thành Environment, Planner và Executor.

## 🚀 Cài đặt và Thiết lập

Bạn cần tải Python phiên bản mới nhất từ trang chủ python.org về máy. Khi cài đặt, bạn nhớ chọn vào ô có chữ Add Python to PATH. Bạn cũng cần cài thêm Git để tải mã nguồn.

Mở cửa sổ dòng lệnh trên máy tính (CMD hoặc PowerShell) rồi copy đoạn lệnh bên dưới để tải code về:
```bash
git clone https://github.com/ten-cua-ban/AI-Event-Planner-Pro.git
cd AI-Event-Planner-Pro
```

Tiếp theo, bạn copy lệnh này để cài đặt các thư viện cần thiết cho chương trình chạy:
```bash
pip install streamlit pandas xlsxwriter
```

Để mở ứng dụng lên, bạn gõ lệnh sau:
```bash
streamlit run web_app.py
```

## 📋 Cách sử dụng
*   Chọn loại sự kiện (Đám cưới/Sinh nhật) ở thanh bên trái.
*   Điền tên chương trình, số người tham gia và số tiền bạn dự định chi trả.
*   Bấm nút Kích hoạt AI Agent và đợi máy tự tính toán.
*   Cuối cùng, bạn có thể tải file báo cáo Excel về máy để lưu trữ.
