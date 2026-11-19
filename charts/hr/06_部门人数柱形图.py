"""06 部门人数柱形图（复现 Excel 柱形图「部门」）

Excel 做法：辅助表 N24:N29 用 COUNTIFS(部门, M24:M29) 计数，按人数降序排列。
Python 做法：value_counts 本身就是降序结果，与 Excel 一致：
研发部 799、销售部 437、信息技术部 162、人力资源部 46、财务部 17、行政部 9。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_hr, save, strip_axes, PALETTE

df = load_hr()
counts = df["部门"].value_counts()
assert counts.sum() == 1470

fig, ax = plt.subplots(figsize=(7.4, 4.6))
bars = ax.bar(counts.index, counts.values, width=0.55,
              color=PALETTE[: len(counts)], edgecolor="white")
for b, v in zip(bars, counts.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 10, str(v), ha="center",
            fontsize=11, fontweight="bold")
ax.set_ylim(0, counts.max() * 1.15)
ax.set_ylabel("人数")
ax.set_title("各部门人数", fontsize=14, fontweight="bold")
strip_axes(ax, keep=("left", "bottom"))
plt.setp(ax.get_xticklabels(), rotation=15)
save(fig, "06_部门人数柱形图", "hr")
print(dict(counts))
