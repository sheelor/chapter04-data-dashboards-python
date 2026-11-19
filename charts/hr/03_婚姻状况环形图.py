"""03 婚姻状况环形图（复现 Excel 圆环图「婚姻状况」）

Excel 做法：辅助表 N11:N13 用 COUNTIFS(婚姻状况, M11:M13) 计数。
Python 做法：value_counts 直接计数，结果与 Excel 一致（已婚 673、单身 470、离异 327）。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_hr, donut, save, strip_axes

df = load_hr()
counts = df["婚姻状况"].value_counts().reindex(["单身", "已婚", "离异"])
assert counts.sum() == 1470

fig, ax = plt.subplots(figsize=(6.4, 5))
donut(ax, counts.values, counts.index, center_text="婚姻状况")
ax.set_title("婚姻状况分布", fontsize=14, fontweight="bold")
strip_axes(ax)
save(fig, "03_婚姻状况环形图", "hr")
print(dict(counts))
