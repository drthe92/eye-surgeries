#!/usr/bin/env python3
"""Kiểm tra semantic tối thiểu cho index.html (card Ca và nguồn)."""
import os
import re
import sys

H = open("index.html", encoding="utf-8").read()
VI = re.compile(r"[ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ]", re.I)
GENERIC = "https://eyerounds.org/video/Cataract/index.htm"
errors = []

chunks = H.split('<div class="card"')[1:]
nums = []
for ch in chunks:
    m = re.search(r'<span class="num">(\d+)</span>', ch)
    if not m:
        continue
    n = int(m.group(1)); nums.append(n)
    t = re.search(r'<span class="t">(.*?)</span>', ch, re.S)
    vi = re.search(r'<span class="vi">(.*?)</span>', ch, re.S)
    links = re.search(r'<div class="links">(.*?)</div>', ch, re.S)
    if not t or not vi:
        errors.append(f"card {n}: thiếu .t hoặc .vi")
        continue
    is_ca = 'data-g="Ca-cataract"' in ch.split('<span class="num">')[0]
    if is_ca and VI.search(t.group(1)):
        errors.append(f"card {n}: .t có tiếng Việt — có thể đảo .t/.vi")
    if not links:
        errors.append(f"card {n}: thiếu links")
        continue
    lk = links.group(1)
    if n in (346, 352) and "phaco_settings" in lk:
        errors.append(f"card {n}: nguồn còn trỏ phaco_settings")
    if n in (341, 348, 349, 350):
        if GENERIC in lk and ">Nguồn</a>" not in lk:
            errors.append(f"card {n}: nguồn tổng quan phải ghi “Nguồn”, không ghi “Video”")

if len(nums) != 353:
    errors.append(f"số card = {len(nums)}, cần 353")
if len(set(nums)) != len(nums):
    errors.append("có số card trùng")

# LEARNING-INDEX: 311-353 phải khớp URL trong technique.md
folders = {int(m.group(1)): d for d in os.listdir(".") if (m := re.match(r"^(\d+)-", d)) and os.path.isdir(d)}
rows = {}
for line in open("LEARNING-INDEX.md", encoding="utf-8"):
    if not line.startswith("|"):
        continue
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    if len(parts) >= 6 and parts[0].isdigit():
        rows[int(parts[0])] = {"url": parts[4], "group": parts[1]}
for n in range(311, 354):
    if n not in rows:
        errors.append(f"LEARNING-INDEX thiếu dòng {n}")
        continue
    d = folders.get(n)
    if not d:
        errors.append(f"thiếu folder {n}")
        continue
    tech = open(os.path.join(d, "technique.md"), encoding="utf-8").read()
    m = re.search(r"\]\((https?://[^)]+)\)", tech)
    tech_url = m.group(1) if m else ""
    if rows[n]["url"] != tech_url:
        errors.append(f"LEARNING-INDEX {n}: URL khác technique.md")
    if n in (346, 352) and "phaco_settings" in rows[n]["url"]:
        errors.append(f"LEARNING-INDEX {n}: còn nguồn phaco_settings")
if len(rows) != 353:
    errors.append(f"LEARNING-INDEX có {len(rows)} dòng, cần 353")

if errors:
    print("LỖI index:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK: {len(nums)} card, .t/.vi và nguồn nhất quán")
