#!/usr/bin/env python3
"""Kiểm tra chất lượng bài technique.md.

Mục tiêu: chặn tái diễn lỗi template — mục 2 (chỉ định) và mục 3 (chuẩn bị)
phải đặc thù cho từng kỹ thuật, không dùng câu chung.

Cách dùng:
    python3 tools/kiem-tra-bai.py            # quét toàn bộ
    python3 tools/kiem-tra-bai.py 185 187    # quét vài bài

Mã thoát 1 nếu có lỗi (ERROR). Cảnh báo (WARN) không chặn commit nhưng nên xem.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Câu template cũ — tuyệt đối không được xuất hiện.
BANNED = [
    "theo từng bước dưới đây",
    "đúng bệnh (phân biệt tuổi già-sẹo-bẩm sinh)",
    "chỉ tiêu 5-0/6-0 và chỉ không tiêu 4-0 cho neo ngang",
    "nhiễm trùng cấp, bệnh toàn thân chưa kiểm soát",
]

# Dấu hiệu nội dung chung chung — cảnh báo.
WEAK = [
    "Thay thế: xem mục 7",
    "như mô tả ở trên",
    "tùy từng trường hợp",
]

# Dụng cụ/thuốc cần xuất hiện lại trong phần quy trình (mục 4).
INSTRUMENTS = [
    "mersilene", "prolene", "supramid", "endotine", "gore-tex",
    "stent", "khoan", "bolster", "đầu đông lạnh", "triamcinolone",
    "silicone", "dải màng xương",
]


def sections(text):
    """Trả về dict số mục -> nội dung."""
    parts = re.split(r"\n## (\d)\. ", text)
    out = {}
    for i in range(1, len(parts), 2):
        out[parts[i]] = parts[i + 1]
    return out


def check(path):
    text = open(path, encoding="utf-8").read()
    sec = sections(text)
    errors, warns = [], []

    s2 = sec.get("2", "")
    s3 = sec.get("3", "")
    s4 = sec.get("4", "")

    for p in BANNED:
        if p in s2 or p in s3:
            errors.append(f"câu template: “{p}”")

    for p in WEAK:
        if p in s2 or p in s3:
            warns.append(f"câu chung chung: “{p}”")

    # Mục 2 phải nêu chẩn đoán cụ thể, không chỉ nói "theo từng bước".
    if len(s2.strip()) < 120:
        warns.append("mục 2 quá ngắn, khó thấy chỉ định thật")

    # Dụng cụ nêu ở mục 3 phải được dùng ở mục 4.
    low4 = s4.lower()
    for ins in INSTRUMENTS:
        if ins in s3.lower() and ins not in low4:
            warns.append(f"“{ins}” có ở Chuẩn bị nhưng không thấy trong Quy trình")

    return errors, warns


def main(argv):
    targets = []
    if argv:
        want = {int(x) for x in argv if x.isdigit()}
        for d in sorted(os.listdir(ROOT)):
            m = re.match(r"^(\d+)-", d)
            if m and os.path.isdir(os.path.join(ROOT, d)):
                if int(m.group(1)) in want:
                    targets.append(os.path.join(ROOT, d, "technique.md"))
    else:
        for d in sorted(os.listdir(ROOT)):
            m = re.match(r"^(\d+)-", d)
            if m and os.path.isdir(os.path.join(ROOT, d)):
                p = os.path.join(ROOT, d, "technique.md")
                if os.path.exists(p):
                    targets.append(p)

    n_err = n_warn = 0
    for p in targets:
        e, w = check(p)
        if e or w:
            name = os.path.basename(os.path.dirname(p))
            print(f"\n{name}")
            for x in e:
                print("  ERROR", x)
            for x in w:
                print("  WARN ", x)
            n_err += len(e)
            n_warn += len(w)

    print(f"\nĐã kiểm tra {len(targets)} bài: {n_err} lỗi, {n_warn} cảnh báo.")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
