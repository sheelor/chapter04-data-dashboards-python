"""07 销量环比图（复现 Excel 柱形图「销量环比」）

Excel 做法：引用 统计数据!J9:K10，展示 8 月、9 月销量两根柱，
L9 的「同比」列实为环比增长率 = (9 月销量 - 8 月销量) ÷ 8 月销量 = 5.18%。
Python 做法：按「月份_销售」计数取 8、9 两月，
与 Excel 缓存值一致：8 月 714、9 月 751，环比 +5.18%。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_sales, save, strip_axes, PALETTE

df = load_sales()
cnt = df.groupby("月份_销售").size().reindex([f"{i}月" for i in range(1, 13)])
aug, sep = cnt["8月"], cnt["9月"]
mom = (sep - aug) / aug
print(f"8 月 {aug}，9 月 {sep}，环比 {mom:+.2%}")

fig, ax = plt.subplots(figsize=(6.2, 4.6))
bars = ax.bar(["8月", "9月"], [aug, sep], width=0.45, color=PALETTE[:2], edgecolor="white")
for b, v in zip(bars, [aug, sep]):
    ax.text(b.get_x() + b.get_width() / 2, v + 8, str(v), ha="center",
            fontsize=12, fontweight="bold")
ax.annotate(f"环比 {mom:+.2%}", xy=(1, sep), xytext=(0.5, sep * 1.12),
            ha="center", fontsize=13, fontweight="bold", color="#C00000",
            arrowprops=dict(arrowstyle="->", color="#C00000"))
ax.set_ylim(0, sep * 1.25)
ax.set_ylabel("销量（订单数）")
ax.set_title("销量环比", fontsize=14, fontweight="bold")
strip_axes(ax, keep=("left", "bottom"))
save(fig, "07_销量环比图", "sales")
