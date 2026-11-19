"""一键运行 charts/ 目录（含 hr/、sales/ 子目录）下全部编号脚本"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(HERE, "charts")

scripts = []
for sub in sorted(os.listdir(CHARTS)):
    d = os.path.join(CHARTS, sub)
    if os.path.isdir(d):
        scripts += [os.path.join(sub, f) for f in sorted(os.listdir(d))
                    if f.endswith(".py") and f[:2].isdigit()]

print(f"共发现 {len(scripts)} 个看板脚本\n")

failed = []
for s in scripts:
    print(f"--- 运行 {s} ---")
    r = subprocess.run([sys.executable, os.path.join(CHARTS, s)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        failed.append(s)
        print(r.stderr)
    else:
        print(r.stdout.strip())

print("\n完成！" if not failed else f"\n失败 {len(failed)} 个: {failed}")
