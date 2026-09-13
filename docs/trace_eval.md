# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Trịnh Xuân Huy]  
> **Mã Sinh Viên / Mã Học viên:** [2A202602995]  
> **Chủ đề Lựa chọn:** [Trợ lý Đặt Phòng họp & Thiết bị (Facilities Agent)]  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4/ 5 | Quá trình đặt phòng đòi hỏi chuỗi suy luận nhiều bước có điều kiện: Trích xuất ý định. Phân tích điều kiện tiên quyết (ngày, giờ, số người)  Quyết định tra cứu phòng trống trước khi thực hiện hành động ghi nhận/đặt phòng hoặc báo lỗi xung đột. |
| **2. Tool Interaction** | 5/ 5 | LLM không thể tự suy diễn trạng thái phòng theo thời gian thực nếu không có dữ liệu ngoại cảnh. Bắt buộc phải kết nối với MCP Server để gọi 2 công cụ: check_room_availability (tra cứu lịch phòng trống) và book_meeting_room (tạo giao dịch đặt phòng). |
| **3. Dynamic Decision** | 4/ 5 | Phản hồi kế tiếp phụ thuộc hoàn toàn vào quan sát (Observation) từ MCP Server: Nếu phòng còn trống rightarrow cho phép đặt; nếu phòng đã kín lịch rightarrow đề xuất khung giờ/phòng khác; nếu câu hỏi thiếu tham số rightarrow tự động chuyển nhánh hỏi làm rõ thông tin. |
| **4. Long Horizon Goal** | 4/ 5 | Duy trì mục tiêu xuyên suốt từ bước tiếp nhận nhu cầu ban đầu của người dùng đến khi xuất được mã xác nhận giao dịch (booking_id) và danh sách thiết bị đi kèm hoàn tất mà không bị lạc ngữ cảnh.|
| **TỔNG ĐIỂM AGENTIC FIT** | **17/ 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "ngày mai phòng 1",
    "action_type": "FINAL_ANSWER",
    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Chào bạn, câu hỏi của bạn (\"ngày mai phòng 1\") chưa rõ mục đích chi tiết. Bạn có thể cho biết cụ thể hơn yêu cầu của mình không?\n\n1. **Nếu bạn muốn kiểm tra phòng họp còn trống:** Vui lòng cung cấp **ngày cụ thể**, **khung giờ họp** (ví dụ: `09:00-11:00`) và **số lượng người tham gia tối thiểu**.\n2. **Nếu bạn muốn đặt phòng họp:** Vui lòng cung cấp **họ tên người đặt**, **mã phòng** (ví dụ: P301, P101...), **ngày đặt**, **khung giờ** và **thiết bị cần thêm** (nếu có). \n\nRất sẵn lòng hỗ trợ bạn!",
    "latency_ms": 24832.89
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt.
- **Kết quả đẩy Repo nộp bài:** [ x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
