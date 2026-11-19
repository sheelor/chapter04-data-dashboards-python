"""04 成本类别占比环形图（复现 Excel 4 张迷你圆环图）

Excel 做法：对 推广/其他/人工/产品 四个成本类别各做一张圆环图，
每张图两段 = 该类别金额 ÷ 当月成本合计（F 列）与辅助列 1 - 占比（G 列），
即 4 张「单值占比圆环」；引用区域 统计数据!F27:G30，类别名取 D27:D30。
Python 做法：筛出 9 月成本后计算各类别占比与辅助段，结果与 Excel 一致：
推广 43.67%、其他 22.42%、人工 23.10%、产品 10.80%（合计 929.25）。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_cost, save, MONTH

cost = load_cost()
m = cost[cost["月份_成本"] == MONTH]
total = m["成本"].sum()
cats = ["推广", "其他", "人工", "产品"]
m = m.set_index("类别").reindex(cats)
ratios = (m["成本"] / total)

fig, axes = plt.subplots(1, 4, figsize=(13, 3.8))
colors = ["#4472C4", "#D9E2F3"]
for ax, cat, r in zip(axes, cats, ratios.values):
    ax.pie([r, 1 - r], colors=colors, startangle=90, counterclock=False,
           wedgeprops=dict(width=0.42, edgecolor="white"))
    ax.text(0, 0.08, f"{r:.1%}", ha="center", fontsize=15, fontweight="bold")
    ax.text(0, -0.28, f"{m.loc[cat, '成本']:.1f}", ha="center", fontsize=9, color="#666666")
    ax.set_title(cat, fontsize=12)
    ax.set(aspect="equal")
fig.suptitle(f"成本类别占比（{MONTH}，总成本 {total:.2f}）", fontsize=14, fontweight="bold", y=1.02)
save(fig, "04_成本类别占比环形图", "sales")
print({c: round(r, 5) for c, r in zip(cats, ratios.values)}, "合计:", round(total, 4))
