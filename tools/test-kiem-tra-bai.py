#!/usr/bin/env python3
"""Test nhỏ cho logic phát hiện khối trùng và self-link."""
import os
import subprocess
import sys
import tempfile
from importlib.machinery import SourceFileLoader

ck = SourceFileLoader("ck", os.path.join(os.path.dirname(__file__), "kiem-tra-bai.py")).load_module()


def write(path, s5, s7="- [Khác](../khac/technique.md): bài khác.", tag="A"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = f"""# Test

## 1. Bản chất
Nội dung.

## 2. Chỉ định / Chống chỉ định
- Chỉ định: {tag}.

## 3. Chuẩn bị
- Vô cảm: {tag}.

## 4. Quy trình
- **Bước 1 — Test:** làm. Nghiệm thu: xong. Cốt lõi: đúng. Lỗi: sai.

## 5. Hậu phẫu
{s5}

## 6. Tự lượng giá
1. A?
2. B?
3. C?

## 7. Bài liên quan
{s7}
"""
    open(path, "w", encoding="utf-8").write(body)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "1-a", "technique.md")
        p2 = os.path.join(tmp, "2-b", "technique.md")
        same = "- Chăm sóc: giống.\n- Thuốc: giống.\n- Tái khám: giống.\n- Dặn quay lại ngay: đau, mờ."
        write(p1, same, tag="A")
        write(p2, same, tag="B")
        clusters = ck.duplicate_clusters([(1, p1), (2, p2)], threshold=2, min_id=1)
        assert len(clusters) == 1 and clusters[0][0] == "5" and clusters[0][2] == [1, 2], clusters
        assert ck.duplicate_clusters([(1, p1), (2, p2)], threshold=2, min_id=311) == []
        assert len(ck.duplicate_clusters([(1, p1), (2, p2)], threshold=2, any_ids={1})) == 1
        assert ck.duplicate_clusters([(1, p1), (2, p2)], threshold=2, any_ids={99}) == []

        p3 = os.path.join(tmp, "3-c", "technique.md")
        write(p3, "- Chăm sóc: khác.\n- Thuốc: khác.\n- Tái khám: khác.\n- Dặn quay lại ngay: đau, mờ.", tag="C")
        assert ck.duplicate_clusters([(1, p1), (3, p3)], threshold=2, min_id=1) == []

        p4 = os.path.join(tmp, "335-test", "technique.md")
        write(p4, same, "- [335 — Test](../335-test/technique.md): tự link.", tag="D")
        errors, _ = ck.check(p4, "")
        assert any("tự link chính bài" in e for e in errors), errors

    # CLI: --strict ID phải so với toàn repo, không chỉ tập được chọn.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ok = subprocess.run([sys.executable, os.path.join(root, "tools", "kiem-tra-bai.py"), "--strict", "332"],
                        cwd=root, capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    # 182 là cặp trùng cũ đã biết; dùng để chứng minh strict ID quét toàn repo.
    bad = subprocess.run([sys.executable, os.path.join(root, "tools", "kiem-tra-bai.py"), "--strict", "182"],
                         cwd=root, capture_output=True, text=True)
    assert bad.returncode == 1 and "trùng khối" in bad.stdout, bad.stdout + bad.stderr

    print("OK: duplicate_clusters threshold/min_id, self-link và CLI --strict ID")


if __name__ == "__main__":
    main()
