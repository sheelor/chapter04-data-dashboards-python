"""05 区域销量条形图（复现 Excel 条形图「区域销量」）

Excel 做法：数据透视表按「区域」统计当月订单数，引用 统计数据!D9:E14。
Python 做法：筛出 9 月订单后按「区域」计数，
与 Excel 缓存值一致：华北 128、华南 295、东北 109、西北 51、西南 29、华东 139（合计 751）。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_sales, save, strip_axes, PALETTE, MONTH

df = load_sales()
m = df[df["月份_销售"] == MONTH]
counts = m["区域"].value_counts()
assert counts.sum() == len(m)

fig, ax = plt.subplots(figsize=(7, 4.4))
bars = ax.bar(counts.index, counts.values, width=0.55,
              color=PALETTE[: len(counts)], edgecolor="white")
for b, v in zip(bars, counts.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 5, str(v), ha="center",
            fontsize=11, fontweight="bold")
ax.set_ylim(0, counts.max() * 1.15)
ax.set_ylabel("销量（订单数）")
ax.set_title(f"区域销量（{MONTH}）", fontsize=14, fontweight="bold")
strip_axes(ax, keep=("left", "bottom"))
save(fig, "05_区域销量条形图", "sales")
print(dict(counts))
