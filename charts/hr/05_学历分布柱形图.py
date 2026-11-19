"""05 学历分布柱形图（复现 Excel 柱形图「学历」）

Excel 做法：辅助表 K24:K28 用 COUNTIFS(学历, J24:J28) 计数。
注意原表 K24 的公式为 COUNTIFS(学历, J25)、K25 引用 J24（两处行列错位），
但因 COUNTIFS 按值匹配，实际计数结果不受影响；Python 按学历值正确归类即可。
结果与 Excel 一致：本科 572、硕士研究生 398、专科 282、专科以下 170、博士研究生 48。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_hr, save, strip_axes, PALETTE

df = load_hr()
edu_order = ["专科以下", "专科", "本科", "硕士研究生", "博士研究生"]
counts = df["学历"].value_counts().reindex(edu_order)
assert counts.sum() == 1470

fig, ax = plt.subplots(figsize=(7.4, 4.6))
bars = ax.bar(counts.index, counts.values, width=0.55, color=PALETTE[0], edgecolor="white")
for b, v in zip(bars, counts.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 8, str(v), ha="center",
            fontsize=11, fontweight="bold")
ax.set_ylim(0, counts.max() * 1.18)
ax.set_ylabel("人数")
ax.set_title("学历分布", fontsize=14, fontweight="bold")
strip_axes(ax, keep=("left", "bottom"))
plt.setp(ax.get_xticklabels(), rotation=15)
save(fig, "05_学历分布柱形图", "hr")
print(dict(counts))
