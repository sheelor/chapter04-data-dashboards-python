"""01 各月销售额面积图（复现 Excel 面积图「各月销售额」）

Excel 做法：数据透视表按「月份_销售」汇总订单额（单位换算为万元），
面积图引用 统计数据!J18:K29。
Python 做法：groupby("月份_销售") 求订单额合计 ÷ 1e4，按 1–12 月排序，
与 Excel 缓存值逐项一致（1 月 145.22 万 … 12 月 146.87 万）。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_sales, save, strip_axes, PALETTE

df = load_sales()
months = [f"{i}月" for i in range(1, 13)]
sales_wan = df.groupby("月份_销售")["订单额"].sum().reindex(months) / 1e4

fig, ax = plt.subplots(figsize=(9, 4.8))
ax.fill_between(range(12), sales_wan.values, color=PALETTE[0], alpha=0.25)
ax.plot(range(12), sales_wan.values, color=PALETTE[0], linewidth=2.2, marker="o", markersize=5)
for i, v in enumerate(sales_wan.values):
    ax.text(i, v + 2.5, f"{v:.1f}", ha="center", fontsize=8.5, color="#333333")
ax.set_xticks(range(12), months)
ax.set_ylim(0, sales_wan.max() * 1.2)
ax.set_ylabel("销售额（万元）")
ax.set_title("各月销售额（2021 年）", fontsize=14, fontweight="bold")
strip_axes(ax, keep=("left", "bottom"))
save(fig, "01_各月销售额面积图", "sales")
print({m: round(v, 2) for m, v in sales_wan.items()})
