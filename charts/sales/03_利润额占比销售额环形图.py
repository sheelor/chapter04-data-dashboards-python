"""03 利润额占比销售额环形图（复现 Excel 圆环图「利润额占比销售额」）

Excel 做法：统计数据 N3 = 利润额 ÷ 销售额（9 月 = 0.12194），
O3 为辅助列 = 1 - N3（0.87806），圆环图由 N2:O2（表头）+ N3:O3（数值）构成。
Python 做法：9 月利润额合计 ÷ 销售额合计，辅助段 = 1 - 利润率，结果与 Excel 一致。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_sales, donut, save, strip_axes, MONTH

df = load_sales()
m = df[df["月份_销售"] == MONTH]
profit_wan = m["利润额"].sum() / 1e4
sales_wan = m["订单额"].sum() / 1e4
ratio = profit_wan / sales_wan
print(f"{MONTH}：利润额 {profit_wan:.4f} 万 / 销售额 {sales_wan:.4f} 万 = 利润率 {ratio:.5f}")

fig, ax = plt.subplots(figsize=(6.2, 5))
donut(ax, [ratio, 1 - ratio], [f"利润率 {ratio:.2%}", ""], center_text=f"利润率\n{ratio:.1%}", fmt="{lab}")
ax.set_title(f"利润额占比销售额（{MONTH}）", fontsize=14, fontweight="bold")
strip_axes(ax)
save(fig, "03_利润额占比销售额环形图", "sales")
