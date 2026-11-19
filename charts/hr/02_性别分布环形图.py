"""02 性别分布环形图（复现 Excel 圆环图「性别」）

Excel 做法：辅助表 K19:K20 用 COUNTIFS(性别, J19/J20) 计数。
Python 做法：value_counts 直接计数，结果与 Excel 一致（男 882、女 588）。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_hr, donut, save, strip_axes

df = load_hr()
counts = df["性别"].value_counts().reindex(["男", "女"])
assert counts.sum() == 1470

fig, ax = plt.subplots(figsize=(6.4, 5))
donut(ax, counts.values, counts.index, center_text="性别占比")
ax.set_title("性别分布", fontsize=14, fontweight="bold")
strip_axes(ax)
save(fig, "02_性别分布环形图", "hr")
print(dict(counts))
