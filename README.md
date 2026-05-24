# 🤖 AI Event Planner - Trợ Lý Ảo Lập Kế Hoạch Sự Kiện

Chào mừng bạn đến với hệ thống AI Event Planner. Đây là một ứng dụng thông minh sử dụng mô hình AI Agent để giúp bạn tự động hóa toàn bộ quy trình lập kế hoạch cho các sự kiện quan trọng như Đám cưới và Sinh nhật. Hệ thống không chỉ đưa ra kịch bản mà còn tính toán ngân sách và quản lý rủi ro theo thời gian thực.

## 🚀 Các công nghệ và thư viện cốt lõi

Để chạy được chương trình này, hệ thống sử dụng các nền tảng và thư viện chuyên sâu sau:
*   **Git:** Công cụ quản lý mã nguồn, dùng để tải và cập nhật dự án từ GitHub.

### 1. Ngôn ngữ lập trình
*   **Python (Phiên bản 3.9 trở lên):** Đây là ngôn ngữ chính được dùng để xây dựng bộ não cho AI.

### 2. Thư viện giao diện và hiển thị
*   **Streamlit:** Thư viện này giúp biến các kịch bản Python thành một trang web có giao diện đẹp mắt mà không cần dùng đến HTML/CSS phức tạp.

### 3. Thư viện xử lý dữ liệu và tính toán
*   **Pandas:** Dùng để xử lý các bảng biểu dữ liệu, tính toán ngân sách chi tiết và quản lý lịch sử hoạt động của AI.
*   **XlsxWriter:** Thư viện chuyên dụng để tạo ra các file báo cáo Excel chuyên nghiệp, giúp bạn tải về các kế hoạch đã lập.

### 4. Thành phần logic và hệ thống
*   **AI Agent Architecture:** Hệ thống được chia thành 3 phần: **Environment** (Môi trường sự kiện), **Planner** (Bộ lập kế hoạch) và **Executor** (Bộ thực thi) để mô phỏng cách con người suy nghĩ và làm việc.
*   **Logging & Persistence:** Sử dụng thư viện `logging` và `json` để lưu lại mọi bước đi của AI vào thư mục `logs/` và `history/`.

## 📋 Chức năng chính

*   **Tự động lập kịch bản (Timeline):** AI sẽ tự tính toán các mốc thời gian từ lúc đón khách đến khi kết thúc tiệc.
*   **Quản lý ngân sách:** Tính toán chi phí dựa trên số lượng khách mời và giới hạn ngân sách bạn nhập vào.
*   **Tùy chỉnh chiến lược:** Bạn có thể chọn AI làm việc theo kiểu "Bảo thủ" (an toàn), "Thích ứng" (cân bằng) hoặc "Tấn công" (nhanh gọn).
*   **Theo dõi trực quan:** Có biểu đồ tiến độ và nhật ký từng bước AI thực hiện để bạn dễ dàng kiểm soát.
*   **Xuất dữ liệu:** Cho phép tải toàn bộ kế hoạch về dưới dạng file Excel để in ấn hoặc gửi cho nhà cung cấp.

## 🛠 Cài đặt và Thiết lập chương trình

Bạn thực hiện theo đúng thứ tự các bước sau để cài đặt ứng dụng lên máy tính của mình:

### Bước 1: Cài đặt các phần mềm nền tảng
1.  **Cài đặt Git:** Truy cập [git-scm.com](https://git-scm.com/), tải về và cài đặt để có thể sử dụng các lệnh tải code.
2.  **Cài đặt Python:** 
Bạn truy cập vào trang chủ python.org, tải phiên bản mới nhất về và cài đặt. 
Lưu ý quan trọng: Trong lúc cài đặt, bạn phải tích vào ô **"Add Python to PATH"** để có thể chạy lệnh từ cửa sổ terminal.

### Bước 2: Tải mã nguồn dự án
Mở cửa sổ Command Prompt hoặc PowerShell trên máy tính, di chuyển đến thư mục bạn muốn lưu dự án và gõ lệnh:
```bash
git clone https://github.com/ten-cua-ban/AI-Event-Planner-Pro.git
cd AI-Event-Planner-Pro
```

### Bước 3: Cài đặt các thư viện bổ trợ
Bây giờ bạn cần cài đặt các thư viện mà chương trình yêu cầu. Hãy mở cửa sổ Terminal (hoặc CMD) ngay tại thư mục chứa code và chạy lệnh duy nhất này:
```bash
pip install streamlit pandas xlsxwriter
```

**4. Khởi chạy ứng dụng**
Sau khi cài xong, bạn chỉ cần gõ lệnh sau để mở giao diện web lên:
```bash
streamlit run web_app.py
```
Một trang web sẽ tự động mở ra trên trình duyệt của bạn.

**5. Cách sử dụng**
*   Tại cột bên trái, bạn chọn loại sự kiện (Đám cưới hoặc Sinh nhật).
*   Nhập các thông tin như tên sự kiện, số khách và ngân sách bạn có.
*   Nhấn nút "Kích hoạt AI Agent" để hệ thống bắt đầu làm việc.
*   Khi AI chạy xong, bạn có thể nhấn "Tải Báo cáo Excel" để lấy file kịch bản về máy.

Chúc bạn có những kế hoạch sự kiện tuyệt vời!