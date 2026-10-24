# Template kỹ thuật mổ chuẩn Goal

Mỗi thư mục `surgeries/<slug>/` phải có `technique.md` gồm đủ 6 phần. `transcript.md` giữ nguyên văn. `steps.md`/`checklist.md` cũ giữ để tham khảo.

## 1. Bản chất (1 đoạn)
Kỹ thuật là gì, nguyên lý tạo kết quả, khác gì kỹ thuật lân cận.

## 2. Chỉ định / Chống chỉ định
- Chỉ định: liệt kê gạch đầu dòng, điều kiện đủ.
- Chống chỉ định tuyệt đối/tương đối + giải pháp thay thế.

## 3. Chuẩn bị
- Vô cảm: loại, vị trí tiêm, lưu ý.
- Dụng cụ + chỉ: liệt kê đủ số lượng/loại kim.
- BN: tư thế, sát khuẩn, trải khăn, marking, chụp ảnh, consent.
- Đánh giá nền: laxity, Bell, khô mắt, đông máu.

## 4. Quy trình từng bước lặp lại được
Mỗi bước theo khung:
- **Bước N — Tên:** mục tiêu.
- Thao tác: làm gì, bằng gì, ở đâu.
- **Nghiệm thu:** dấu hiệu nhìn/sờ được để qua bước tiếp.
- **Yếu tố cốt lõi:** 1-2 điểm quyết định thành công.
- **Lỗi thường gặp:** sai gì -> hậu quả gì.

## 5. Hậu phẫu
- Chăm sóc, thuốc, băng, hạn chế.
- Lịch tái khám + tiêu chí đánh giá lại.
- Dặn quay lại ngay: 3-5 dấu hiệu cụ thể (không viết “các dấu hiệu trên”).

## 6. Tự lượng giá (3 câu)

## Quy tắc chống template (bắt buộc từ 2026-10-24)
Mục 2 và mục 3 phải **đặc thù cho đúng kỹ thuật này**, không được dùng câu chung.

- Mục 2: nêu chẩn đoán cụ thể, điều kiện đủ, và **thay thế bằng bài nào** nếu không làm được.
- Mục 3: chỉ liệt kê dụng cụ/thuốc **thực sự xuất hiện ở mục 4**. Bài tiêm steroid không liệt kê dao 15, bipolar hay chỉ 5-0.
- Bài giảng (không thực hiện thủ thuật): ghi rõ “Bài giảng không thực hiện thủ thuật” ở mục 2 và “không cần dụng cụ” ở mục 3.
- Ví dụ sai: “Chỉ định: theo từng bước dưới đây” hoặc “Dụng cụ: dao 15, bipolar, chỉ 5-0/6-0, chỉ không tiêu 4-0 cho neo ngang” trong bài tiêm steroid.
- Kiểm tra trước commit: `python3 tools/kiem-tra-bai.py`

- Mục 5: câu “Dặn quay lại ngay” phải nêu dấu hiệu cụ thể; bài tiêm/đông lạnh không chườm lạnh, không vết mổ, không cắt chỉ; bài giảng ghi “Không có hậu phẫu”.
- Cấu trúc đúng 1–7, mỗi mục một lần; không trùng số mục.
- Sửa câu hậu phẫu rỗng: `python3 tools/kiem-tra-bai.py --fix` (chỉ thay câu rỗng, không thay nội dung đặc thù).
