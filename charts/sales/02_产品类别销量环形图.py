"""02 产品类别销量环形图（复现 Excel 圆环图「产品类别销量」）

Excel 看板带月份选择控件，图表展示所选月份（本看板默认 9 月）的数据。
Python 做法：筛出 9 月订单后按「产品类别」计数，
与 Excel 缓存值一致：办公用品 409、家具产品 156、数码电子 186（合计 = 9 月销量 751）。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_sales, donut, save, strip_axes, MONTH

df = load_sales()
m = df[df["月份_销售"] == MONTH]
counts = m["产品类别"].value_counts().reindex(["办公用品", "家具产品", "数码电子"])
assert counts.sum() == len(m)

fig, ax = plt.subplots(figsize=(6.6, 5))
donut(ax, counts.values, list(counts.index), center_text=f"{MONTH}\n销量")
ax.set_title(f"产品类别销量（{MONTH}）", fontsize=14, fontweight="bold")
strip_axes(ax)
save(fig, "02_产品类别销量环形图", "sales")
print(dict(counts))
