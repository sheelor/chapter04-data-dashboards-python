"""08 商品销售额 Top3 条形图（复现 Excel 条形图「商品销售额 Top3」）

Excel 做法：按所选月份的产品销售额排序取前 3，
引用 统计数据!W3:Z5（排名 / 产品名称 / 销售额(万) / 销量）。
Python 做法：筛出 9 月订单，按「产品名称」汇总订单额取前 3，
与 Excel 缓存值一致：
  1. KI Conference Tables  16.98 万  30 件
  2. Xerox 193             16.81 万  29 件
  3. Phone 918             15.35 万  31 件

说明：Excel 图表另引用了 W10:Z13 的「辅助」数据区，其中缓存值全部为
占位数据（300/100/100），对本图无语义贡献，故不复现，详见说明文档。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_sales, save, strip_axes, PALETTE, MONTH

df = load_sales()
m = df[df["月份_销售"] == MONTH]
top3 = (m.groupby("产品名称")
          .agg(销售额=("订单额", "sum"), 销量=("订单单号", "count"))
          .sort_values("销售额", ascending=False).head(3))
print(top3.assign(销售额万=(top3["销售额"] / 1e4).round(4)))

fig, ax = plt.subplots(figsize=(7.6, 4.4))
names = [n if len(n) <= 22 else n[:21] + "…" for n in top3.index]
bars = ax.barh(range(3), top3["销售额"] / 1e4, height=0.5,
               color=PALETTE[:3], edgecolor="white")
ax.set_yticks(range(3), names)
ax.invert_yaxis()
for i, (v, (_, row)) in enumerate(zip(top3["销售额"] / 1e4, top3.iterrows())):
    ax.text(v + 0.15, i, f"{v:.2f} 万 / {int(row['销量'])} 件", va="center", fontsize=10)
ax.set_xlim(0, top3["销售额"].max() / 1e4 * 1.3)
ax.set_xlabel("销售额（万元）")
ax.set_title(f"商品销售额 Top3（{MONTH}）", fontsize=14, fontweight="bold")
strip_axes(ax, keep=("left", "bottom"))
save(fig, "08_商品销售额Top3条形图", "sales")
