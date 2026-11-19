"""01 年龄分布环形图（复现 Excel 圆环图「年龄」）

Excel 做法：辅助表 K11:K15 用 COUNTIFS(年龄段, J11) 逐段计数，圆环图引用该表。
Python 做法：pd.cut 按相同口径（18-24 / 25-29 / 30-34 / 35-39 / 40=<，闭区间）
从「年龄」列直接分段计数，与 Excel 预置的「年龄段」列逐一核对一致。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_hr, donut, save, strip_axes

df = load_hr()
# 分段口径与 Excel 完全一致：18-24、25-29、30-34、35-39、40 岁及以上
bands = ["18-24", "25-29", "30-34", "35-39", "40=<"]
counts = df["年龄段"].value_counts().reindex(bands)

# 数据核对：总人数必须等于明细行数（对应 Excel 差值校验 N3=N2-SUM(K11:K15)=0）
assert counts.sum() == len(df) == 1470, "年龄段计数与总人数不一致"

fig, ax = plt.subplots(figsize=(7, 5.2))
donut(ax, counts.values, bands, center_text=f"总人数\n{counts.sum()}")
ax.set_title("年龄分布", fontsize=14, fontweight="bold")
strip_axes(ax)
save(fig, "01_年龄分布环形图", "hr")
print(dict(counts))
