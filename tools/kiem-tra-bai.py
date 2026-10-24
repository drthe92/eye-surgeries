#!/usr/bin/env python3
"""Kiểm tra chất lượng bài technique.md (mục 2, 3 và 5).

Mục tiêu: chặn lỗi template — chỉ định, chuẩn bị và hậu phẫu phải đặc thù
cho từng kỹ thuật, không dùng câu chung.

Cách dùng:
    python3 tools/kiem-tra-bai.py              # kiểm tra toàn bộ
    python3 tools/kiem-tra-bai.py 185 187      # kiểm tra vài bài
    python3 tools/kiem-tra-bai.py --fix        # thay câu hậu phẫu rỗng
    python3 tools/kiem-tra-bai.py --fix 185    # chỉ sửa bài 185

Mã thoát 1 nếu còn lỗi (ERROR).
"""
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BANNED = [
    "theo từng bước dưới đây",
    "đúng bệnh (phân biệt tuổi già-sẹo-bẩm sinh)",
    "chỉ tiêu 5-0/6-0 và chỉ không tiêu 4-0 cho neo ngang",
    "nhiễm trùng cấp, bệnh toàn thân chưa kiểm soát",
]

WEAK = [
    "như từng bước dưới đây",
    "Thay thế: xem mục 7",
    "như mô tả ở trên",
    "tùy từng trường hợp",
]

# Câu hậu phẫu rỗng — không cho phép.
BANNED_POST = [
    "các dấu hiệu trên",
    "các dấu hiệu nêu trên",
    "dấu hiệu trên",
    "như trên",
]

INSTRUMENTS = [
    "mersilene", "prolene", "supramid", "endotine", "gore-tex",
    "stent", "khoan", "bolster", "đầu đông lạnh", "triamcinolone",
    "silicone", "dải màng xương",
]

# Bằng chứng đã khâu/đóng chỉ trong quy trình.
SUTURE_RE = re.compile(
    r"\bkhâu\b|mũi chỉ|chỉ tiêu|chỉ không tiêu|\bstaples?\b|"
    r"\b(nylon|vicryl|prolene|mersilene|supramid|silk|chromic|pds|monocryl|ethibond)\b|"
    r"\b\d-\d\b",
    re.I,
)

# Dấu hiệu cần quay lại, theo nhóm. Dùng khi sửa câu rỗng.
GROUP_SIGNS = {
    "A-core": "chảy máu không cầm, sưng nóng đỏ, hở mi tăng, nhìn mờ",
    "B-ectropion/entropion": "lông quặm lại, cộm đau tăng, chảy máu, sưng nóng đỏ",
    "C-lower-lid": "vạt hoặc ghép trắng-tím-đen, chảy máu, sưng nóng đỏ, hở mi tăng",
    "D-midface": "sưng nóng đỏ, méo mặt tăng, đau tăng",
    "Brow": "sưng nóng đỏ, bất đối xứng tăng, đau tăng",
    "E-blepharo": "đau dữ dội, lồi mắt, mất thị lực, chảy máu",
    "F-palsy": "hở mi tăng, trợt giác mạc, sưng nóng đỏ, đau tăng",
    "L-lacrimal": "chảy máu mũi nhiều, sưng nóng đỏ, sốt, nhìn mờ",
    "M-medial": "chảy máu, sưng nóng đỏ, chảy nước mắt tăng",
    "N-anesthesia": "tê kéo dài, đau tăng, sưng nóng đỏ, nhìn mờ",
    "O-orbit": "lồi mắt tăng, nhìn đôi tăng, mất thị lực, chảy máu",
    "P-ptosis": "hở mi tăng, trợt giác mạc, sưng nóng đỏ",
    "R-recon": "vạt hoặc ghép trắng-tím-đen, chảy máu, sưng nóng đỏ, hở mi tăng",
    "S-strabismus": "đau dữ dội, sưng mủ, nhìn đôi tăng, giảm thị lực",
    "T-trauma": "chảy máu, sưng nóng đỏ, giảm thị lực, sốt",
    "U-upper": "cộm đau tăng, lông quặm lại, hở mi, sưng nóng đỏ",
    "U-retraction": "cộm đau tăng, hở mi, sưng nóng đỏ",
    "W-brow": "sưng nóng đỏ, bất đối xứng tăng, đau tăng, tê bì lan rộng",
    "Bx-biopsy": "chảy máu, sưng nóng đỏ, đau tăng",
    "Ca-cataract": "đau tăng, nhìn mờ đột ngột, đỏ đau, buồn nôn",
}

# Tinh chỉnh trong cùng nhóm theo kỹ thuật thật.
REFINE = {
    "B-ectropion/entropion": [
        (r"lật|ectropion", "mi lật ra ngoài, hở mi tăng, chảy máu, sưng nóng đỏ"),
        (r"đông lạnh", "loét giác mạc, đau tăng, mất sắc tố lan, lông quặm lại"),
        (r"tiêm", "teo da hoặc mất sắc tố, đau tăng, nhìn mờ, sưng nóng đỏ"),
    ],
    "C-lower-lid": [
        (r"ghép da|mảnh ghép", "mảnh ghép trắng-tím-đen, chảy máu, sưng nóng đỏ, hở mi tăng"),
        (r"vạt", "đầu vạt trắng-tím-đen, chảy máu, sưng nóng đỏ, đau tăng"),
    ],
    "R-recon": [
        (r"ghép da|mảnh ghép", "mảnh ghép trắng-tím-đen, chảy máu, sưng nóng đỏ, hở mi tăng"),
        (r"vạt", "đầu vạt trắng-tím-đen, chảy máu, sưng nóng đỏ, đau tăng"),
    ],
    "S-strabismus": [
        (r"botox|botulinum", "sụp mi, nhìn đôi, đau tăng, sưng nóng đỏ"),
        (r"tiêm", "sụp mi, nhìn đôi, đau tăng, sưng nóng đỏ"),
    ],
    "N-anesthesia": [
        (r"tenon", "đau tăng, nhìn mờ, tụ máu kết mạc, sưng nóng đỏ"),
        (r"retrobulbar|cầu sau|sau nhãn cầu", "đau dữ dội, lồi mắt tăng, mất thị lực, co giật"),
        (r"dcr|túi lệ|lệ đạo", "chảy máu mũi nhiều, sưng nóng đỏ, sốt, nhìn mờ"),
    ],
    "O-orbit": [
        (r"vỡ sàn|tấm|supramid|titan", "lồi mắt tăng, nhìn đôi tăng, mất thị lực, tê môi-má"),
        (r"vật liệu|mảnh vỡ|xương", "lồi mắt tăng, nhìn đôi tăng, mất thị lực, tê môi-má"),
    ],
    "P-ptosis": [
        (r"treo trán|sling|silicone", "hở mi tăng, trợt giác mạc, lộ vật liệu, sưng nóng đỏ"),
    ],
    "F-palsy": [
        (r"tháo tạ|gỡ tạ", "hở mi tăng, trợt giác mạc, sưng nóng đỏ, đau tăng"),
        (r"\btạ\b|gold|weight", "hở mi tăng, trợt giác mạc, tạ lộ, sưng nóng đỏ"),
    ],
    "T-trauma": [
        (r"lệ quản|canalicul|stent", "chảy máu, sưng nóng đỏ, chảy nước mắt tăng, giảm thị lực"),
    ],
    "W-brow": [
        (r"endotine|neo|xuyên xương", "sưng nóng đỏ, bất đối xứng tăng, tụ máu da đầu, đau tăng"),
        (r"chân tóc|pretrichial", "sưng nóng đỏ, tê bì lan rộng, chân tóc lệch, đau tăng"),
        (r"direct|trực tiếp", "sưng nóng đỏ, bất đối xứng tăng, đau tăng, sẹo lồi"),
    ],
    "L-lacrimal": [
        (r"tuyến lệ|sa tuyến|sinh thiết.*tuyến", "chảy máu, sưng nóng đỏ, đau tăng, nhìn đôi"),
        (r"jones|ống thủy tinh|đổi ống|đặt ống|đường rò|mvr", "ống trượt, chảy máu mũi, sưng nóng đỏ, nhìn mờ"),
        (r"dcr|mở lệ đạo|nối túi lệ|mở thông túi lệ|túi lệ.*mũi", "chảy máu mũi nhiều, sưng nóng đỏ, sốt, nhìn mờ"),
        (r"cắt bỏ ống|bít lệ đạo vĩnh viễn", "đau tăng, sưng nóng đỏ, chảy máu, nhìn mờ"),
        (r"điểm lệ|punctal|cautery|bít điểm lệ", "đau tăng, sưng nóng đỏ, chảy nước mắt tăng, nhìn mờ"),
        (r"lệ quản|canalicul|sonde|nong|thông lệ|stent", "chảy máu mũi, đau tăng, sưng nóng đỏ, chảy nước mắt tăng"),
    ],
}


def group_map():
    """Đọc LEARNING-INDEX để lấy số bài -> nhóm."""
    out = {}
    path = os.path.join(ROOT, "LEARNING-INDEX.md")
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^\| (\d+) \| ([^|]+) \|", line)
        if m:
            out[int(m.group(1))] = m.group(2).strip()
    return out


def sections(text):
    parts = re.split(r"\n## (\d)\. ", text)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def signs_for(text, group):
    low = text.lower()
    for pattern, signs in REFINE.get(group, []):
        if re.search(pattern, low):
            return signs
    return GROUP_SIGNS.get(group, "đau tăng, chảy máu, sưng nóng đỏ, nhìn mờ")


def is_lecture(s1, s2):
    return "bài giảng" in s1.lower() or "không thực hiện thủ thuật" in s2.lower()


def is_nonincisional(s1, s3):
    """Thủ thuật không mở vết mổ: tiêm, đông lạnh, hoặc bài giảng."""
    low = s1.lower()
    if "đông lạnh" in low:
        return "cryo"
    if "tiêm" in low and "dao 15" not in s3.lower() and "rạch" not in low:
        return "injection"
    return ""


def check(path, group):
    text = open(path, encoding="utf-8").read()
    sec = sections(text)
    errors, warns = [], []

    s1 = sec.get("1", "")
    s2 = sec.get("2", "")
    s3 = sec.get("3", "")
    s4 = sec.get("4", "")
    s5 = sec.get("5", "")

    # Cấu trúc 1-7 phải đúng thứ tự, mỗi mục một lần.
    nums = [int(x) for x in re.findall(r"^## (\d+)\. ", text, re.M)]
    if nums != [1, 2, 3, 4, 5, 6, 7]:
        errors.append(f"cấu trúc mục sai: {nums} (cần 1-7)")

    for p in BANNED:
        if p in s2 or p in s3:
            errors.append(f"câu template: “{p}”")

    for p in WEAK:
        if p in s2 or p in s3:
            warns.append(f"câu chung chung: “{p}”")

    if len(s2.strip()) < 120:
        warns.append("mục 2 quá ngắn, khó thấy chỉ định thật")

    # --- Mục 5: hậu phẫu ---
    for p in BANNED_POST:
        if p in s5:
            errors.append(f"hậu phẫu rỗng: “{p}” (phải nêu dấu hiệu cụ thể)")

    if not s5.strip():
        errors.append("mục 5 hậu phẫu trống")

    lecture = is_lecture(s1, s2)
    noninc = is_nonincisional(s1, s3)
    nonsurgical = "không có hậu phẫu" in s5.lower()

    def says(phrase):
        """Có nhắc thật, không tính câu phủ định “không ... ”."""
        return phrase in s5.lower() and f"không {phrase}" not in s5.lower()

    if lecture and not nonsurgical and re.search(r"chăm sóc:|tái khám:|cắt chỉ|vết mổ", s5, re.I):
        errors.append("bài giảng nhưng hậu phẫu viết như ca mổ")

    if noninc == "injection" and (says("chườm lạnh") or says("vết mổ") or says("cắt chỉ")):
        errors.append("bài tiêm nhưng hậu phẫu nói chườm lạnh/vết mổ/cắt chỉ")

    if noninc == "injection" and re.search(r"kháng sinh-tra|kháng sinh \+ steroid tra|u hạt sinh mủ", s5, re.I):
        errors.append("bài tiêm nhưng hậu phẫu dùng phác đồ mổ")

    if noninc == "cryo" and (says("chườm lạnh") or says("vết mổ") or says("cắt chỉ")):
        errors.append("bài đông lạnh nhưng hậu phẫu nói chườm lạnh/vết mổ/cắt chỉ")

    # Cắt chỉ ở bài mổ hở nhưng quy trình không hề nhắc khâu/chỉ.
    if "cắt chỉ" in s5 and not SUTURE_RE.search(s4) and not noninc and not lecture:
        warns.append("hậu phẫu nhắc cắt chỉ nhưng quy trình không nêu khâu/chỉ")

    # Phải có dòng dặn dấu hiệu cụ thể, không chỉ “theo dõi”.
    if not nonsurgical:
        m = re.search(r"Dặn quay lại ngay\s*:?\s*(.+)", s5)
        if not m:
            errors.append("thiếu dòng “Dặn quay lại ngay” với dấu hiệu cụ thể")
        elif m.group(1).count(",") < 1:
            warns.append("dòng dặn quay lại ngay có quá ít dấu hiệu")

    low4 = s4.lower()
    for ins in INSTRUMENTS:
        if ins in s3.lower() and ins not in low4:
            warns.append(f"“{ins}” có ở Chuẩn bị nhưng không thấy trong Quy trình")

    return errors, warns


def postop_lines(targets):
    c = Counter()
    for p in targets:
        sec = sections(open(p, encoding="utf-8").read())
        for ln in sec.get("5", "").split("\n"):
            ln = ln.strip()
            if ln.startswith("- "):
                c[ln] += 1
    return c


def selfcheck_blocks(targets):
    c = Counter()
    for p in targets:
        sec = sections(open(p, encoding="utf-8").read())
        body = sec.get("6", "").strip()
        if body:
            c[body] += 1
    return c


def fix(path, group):
    """Thay câu “các dấu hiệu trên” bằng dấu hiệu cụ thể theo kỹ thuật."""
    text = open(path, encoding="utf-8").read()
    m = re.search(r"(## 5\. Hậu phẫu\n)(.*?)(\n\n## 6\.)", text, re.S)
    if not m:
        return False
    s5 = m.group(2)
    if not any(p in s5 for p in BANNED_POST):
        return False

    sec = sections(text)
    signs = signs_for(sec.get("1", ""), group)
    new5 = re.sub(
        r"^.*(?:các dấu hiệu (?:nêu )?trên|dấu hiệu trên|như trên).*$",
        f"- Dặn quay lại ngay: {signs}.",
        s5,
        flags=re.M,
    )
    if new5 == s5:
        return False
    text = text[: m.start(2)] + new5 + text[m.end(2):]
    open(path, "w", encoding="utf-8").write(text)
    return True


def main(argv):
    do_fix = "--fix" in argv
    argv = [a for a in argv if a != "--fix"]
    want = {int(x) for x in argv if x.isdigit()}
    groups = group_map()

    targets = []
    for d in sorted(os.listdir(ROOT)):
        m = re.match(r"^(\d+)-", d)
        if not (m and os.path.isdir(os.path.join(ROOT, d))):
            continue
        n = int(m.group(1))
        if want and n not in want:
            continue
        p = os.path.join(ROOT, d, "technique.md")
        if os.path.exists(p):
            targets.append((n, p))

    if do_fix:
        fixed = 0
        for n, p in targets:
            if fix(p, groups.get(n, "")):
                fixed += 1
                print("FIX ", os.path.basename(os.path.dirname(p)))
        print(f"\nĐã sửa {fixed} bài.")

    freq = postop_lines([p for _, p in targets])
    repeated = [(ln, n) for ln, n in freq.items() if n >= 15 and "Dặn quay lại ngay" not in ln]

    n_err = n_warn = 0
    for n, p in targets:
        e, w = check(p, groups.get(n, ""))
        if e or w:
            print(f"\n{os.path.basename(os.path.dirname(p))}")
            for x in e:
                print("  ERROR", x)
            for x in w:
                print("  WARN ", x)
            n_err += len(e)
            n_warn += len(w)

    if repeated:
        print("\nCâu hậu phẫu lặp ở nhiều bài (nên xem lại):")
        for ln, n in repeated[:10]:
            print(f"  {n:3d} bài | {ln[:110]}")

    dup6 = [(b, n) for b, n in selfcheck_blocks([p for _, p in targets]).items() if n >= 5]
    if dup6:
        dup6.sort(key=lambda x: -x[1])
        print("\nKhối tự lượng giá lặp ở nhiều bài (nên cá nhân hóa):")
        for body, n in dup6[:6]:
            print(f"  {n:3d} bài | {body[:110].replace(chr(10), ' ')}")

    print(f"\nĐã kiểm tra {len(targets)} bài: {n_err} lỗi, {n_warn} cảnh báo.")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
