"""
Recompiles PDF and DOCX reports and synchronizes all mirrors.
"""

import os
import shutil
import subprocess

base = r"C:\Users\lenovo\.gemini\antigravity\scratch\Research_Work"

print("1. Recompiling PDF Reports...")
subprocess.run(["python", os.path.join(base, "generate_pdf_reports.py")], check=True)

print("2. Recompiling DOCX Reports...")
subprocess.run(["python", os.path.join(base, "generate_docx_reports.py")], check=True)

print("3. Mirroring complete workspace to Desktop and Home folders...")
dests = [r"C:\Users\lenovo\Desktop\Research_Work", r"C:\Users\lenovo\Research_Work"]
for d in dests:
    if os.path.exists(d):
        shutil.rmtree(d)
    shutil.copytree(base, d)
    print(f"Mirrored to: {d}")

print("=== Recompilation and Mirroring Successfully Completed ===")
