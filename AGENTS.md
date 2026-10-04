# AGENTS.md — Thư viện phẫu thuật mắt (Eye Surgeries)

Repo: `github.com/drthe92/eye-surgeries` — thư viện học phẫu thuật mắt từ video EyeRounds/Iowa của Richard Allen và cộng sự. Học qua GitHub Pages tại domain riêng (file `CNAME`) với `index.html` làm hub.

## Mục tiêu dài hạn
1. Mỗi kỹ thuật mổ: hiểu bản chất (chỉ định, chống chỉ định), quy trình từng bước lặp lại được, mỗi bước có tiêu chí nghiệm thu + yếu tố cốt lõi + lỗi thường gặp, checklist chuẩn bị (vô cảm, dụng cụ) và hậu phẫu (chăm sóc, thuốc, tái khám).
2. Việt hoá sâu `technique.md`: thuật ngữ tiếng Việt lên trước, tiếng Anh giữ trong ngoặc ở lần xuất hiện đầu (ví dụ: sụn mi (tarsus), góc mắt ngoài (lateral canthus)).
3. NGUỒN HỌC LIỆU CHÍNH: quét hệ thống mục lục video tại `https://eyerounds.org/video/INDEX.htm` để phát hiện nhóm video phẫu thuật chưa học, rồi triển khai theo thứ tự ưu tiên vùng mắt, đánh số tiếp nối, không bao giờ đánh lại số cũ. Link YouTube do người dùng gửi chỉ là nguồn phụ, không phải luồng chính.

## Quy ước bất biến
- Mỗi bài một folder `NN-slug/` (NN = số thứ tự 3 chữ số: `01-`, `02-`...), chứa `transcript.md` + `technique.md` chuẩn 6 mục (Bản chất, Chỉ định/Chống chỉ định, Chuẩn bị, Quy trình, Hậu phẫu, Tự lượng giá 3 câu).
- `transcript.md`: metadata (tên, tác giả, trang companion, Vimeo, ngày lấy) + transcript (ghi rõ nguyên văn hay tóm/dựng từ nguyên lý nếu trang gốc thiếu).
- `technique.md`: mở đầu bằng dòng link Video click được; cuối mỗi bước trong Quy trình có thể ghi "Dặn quay lại ngay" khi là thủ thuật lâm sàng.
- `surgeries/LEARNING-INDEX.md`: bảng Thứ tự | Nhóm | Title | Tóm tắt (~100 từ) | Link Vimeo | Xong. Thêm dòng mới khi thêm bài.
- `index.html` ở gốc repo: hub học tập (thẻ theo nhóm, search Anh-Việt, lọc nhóm, link Bài học/Transcript/Video). Sinh lại bằng script khi thêm bài hoặc đổi link. Link bài học giữ dạng blob `github.com` (KHÔNG chuyển sang domain riêng — quyết định của chủ repo).
- Nhóm mã: A góc ngoài, B lật-quặm, C tái tạo mi dưới, D nâng má, N vô cảm (N-local tê tại chỗ/thấm, N-block block kim vùng, N-systemic tiền mê/mê), U mi trên-co rút, S lác, W mày-trán, E blepharoplasty, P sụp mi, L lệ đạo, F liệt mặt, T chấn thương, O hốc mắt, R tái tạo mi trên-góc trong, Bx sinh thiết-u mi-chắp (mới từ 175).
- QUY TẮC SỐ-GHÉP NHÓM (2026-10-04): số folder = thứ tự bổ sung theo thời gian, KHÔNG BAO GIỜ đánh lại số cũ (link blob GitHub phải ổn định). Bài cùng chuyên đề nhưng đến sau vẫn lấy số tiếp nối (ví dụ vô cảm mới = 185+), chỉ gắn đúng tag nhóm (N-local/N-block/N-systemic); index.html gom hiển thị theo tag nên vẫn học gọn theo nhóm. Được tách tag con khi một nhóm phình to (mẫu: N tách 3 tag con, giữ nguyên số 24-27, đổi tag rồi sinh lại index).

## Quy trình làm việc mỗi đợt
1. Lấy transcript từ trang EyeRounds companion (ưu tiên), Vimeo, hoặc video YouTube (dùng skill `youtube-lesson-eye` khi có link YouTube).
2. Viết `transcript.md` + `technique.md` đúng khung 6 mục, Việt hoá sâu.
3. Cập nhật `LEARNING-INDEX.md` (đánh `[x]`, tóm tắt, link Vimeo thật) và sinh lại `index.html` nếu đổi link/cấu trúc.
4. Commit + push lên `main` sau MỖI đợt (SSH đã có sẵn). Kiểm tra `git status`/`git log` sau push. Nếu push bị reject (phiên khác đẩy trước), `git fetch` rồi gộp giữ nội dung mới nhất, không bao giờ force-push mất bài.

## Tiến độ (cập nhật khi xong việc)
- 184 bài (01-184) đã có transcript + technique; index đủ 184 dòng `[x]`.
- Việt hoá (2026-10-04, đợt 1): 184/184 tiêu đề technique.md đã Việt lên trước; chạy chuẩn hoá thuật ngữ script (Anh trong ngoặc ở lần đầu, BN→Bệnh nhân, epi→epinephrine, gộp ngoặc thừa) + soát mẫu bài 04 và quét không còn salad tiếng Anh trong bước mổ. Soát tay sâu tiếp tục cuốn chiếu theo nhóm khi học tới (mỗi bài học lại trau chuốt một lần).
- Khảo sát hệ thống mục lục plastics EyeRounds (2026-10-04): nhóm sinh thiết mi-u mi (7 video) đã triển khai thành 175-181; nhóm chắp chalazion (3 video) đã triển khai thành 182-184. Nhóm trống tiếp theo: sinh thiết kết mạc (7), lấy mô ghép (da/cân/sụn/niêm mạc), sinh thiết động mạch thái dương (2), orbitotomy trước-bên, ONSF (3), giải áp ổ mắt (5), khoét bỏ nhãn cầu (enucleation/evisceration/exenteration), ổ mắt vô nhãn.
- Việt hoá sâu: xong 01-02, tiếp tục từ 03 → 174.
- Bài mới: đánh số tiếp từ 175.
