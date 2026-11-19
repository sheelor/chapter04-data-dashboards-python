"""04 本月入转调柱形图（复现 Excel 柱形图「入转调」）

Excel 做法：辅助表 N17:N19 用 COUNTIFS(本月入转调, M17:M19) 计数；
N8 的差值校验 = COUNTA(本月入转调) - SUM(N17:N19) = 0，即除入职/转入/转出外无其他取值。
Python 做法：value_counts(dropna=False) 先全量核对（1420 个空值 + 40 入职 + 5 转入 + 5 转出），
再取三类非空值绘图，与 Excel 一致。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_hr, save, strip_axes, PALETTE

df = load_hr()
full = df["本月入转调"].value_counts(dropna=False)
# 核对：非空值只包含 入职/转入/转出 三类（对应 Excel N8 差值校验 = 0）
non_null = df["本月入转调"].dropna().value_counts()
assert set(non_null.index) == {"入职", "转入", "转出"}, "本月入转调存在其他取值"
counts = non_null.reindex(["入职", "转入", "转出"])

fig, ax = plt.subplots(figsize=(6.4, 4.6))
bars = ax.bar(counts.index, counts.values, width=0.5,
              color=PALETTE[:3], edgecolor="white")
for b, v in zip(bars, counts.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.6, str(v),
            ha="center", fontsize=11, fontweight="bold")
ax.set_ylim(0, counts.max() * 1.2)
ax.set_ylabel("人数")
ax.set_title("本月入转调（2022 年 3 月）", fontsize=14, fontweight="bold")
strip_axes(ax, keep=("left", "bottom"))
save(fig, "04_入转调柱形图", "hr")
print(dict(counts))
