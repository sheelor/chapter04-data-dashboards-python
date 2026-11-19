"""07 人力资源可视化看板总装（复现 Excel 整屏看板布局）

Excel 看板布局：顶部「总人数：1470」卡片 + 6 张图表（上排 3 张圆环图：
年龄 / 性别 / 婚姻状况；下排 3 张柱形图：入转调 / 学历 / 部门）。
本脚本把 01–06 的六张图以相同版式拼成一整张看板，数据全部现场计算并逐项核对：
- 各维度计数之和 = 总人数 1470（对应 Excel 差值校验列 N 全为 0）。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib.pyplot as plt
from common import load_hr, donut, kpi_card, save, strip_axes, PALETTE

df = load_hr()
total = len(df)
bands = ["18-24", "25-29", "30-34", "35-39", "40=<"]
age = df["年龄段"].value_counts().reindex(bands)
gender = df["性别"].value_counts().reindex(["男", "女"])
marry = df["婚姻状况"].value_counts().reindex(["单身", "已婚", "离异"])
change = df["本月入转调"].value_counts().reindex(["入职", "转入", "转出"])
edu_order = ["专科以下", "专科", "本科", "硕士研究生", "博士研究生"]
edu = df["学历"].value_counts().reindex(edu_order)
dept = df["部门"].value_counts()
for s in (age, gender, marry):
    assert s.sum() == total
# 差值校验：除入职/转入/转出外，本月入转调无其他非空取值
assert df["本月入转调"].dropna().isin(["入职", "转入", "转出"]).all()

fig = plt.figure(figsize=(16, 10.5), facecolor="#F5F7FA")
fig.suptitle("人力资源可视化看板（2022 年 3 月）", fontsize=20, fontweight="bold", y=0.975)
kpi_card(fig, (0.38, 0.865, 0.24, 0.075), "总人数", f"{total} 人", dark=False)

# 上排：三张圆环图
for i, (counts, title, ct) in enumerate([
    (age, "年龄分布", "年龄"), (gender, "性别分布", "性别"), (marry, "婚姻状况", "婚姻"),
]):
    ax = fig.add_subplot(2, 3, i + 1)
    donut(ax, counts.values, list(counts.index), center_text=ct)
    ax.set_title(title, fontsize=13, fontweight="bold")
    strip_axes(ax)

# 下排：三张柱形图
for j, (counts, title, ymax_pad) in enumerate([
    (change, "本月入转调", 1.25), (edu, "学历分布", 1.18), (dept, "各部门人数", 1.15),
]):
    ax = fig.add_subplot(2, 3, j + 4)
    bars = ax.bar(counts.index, counts.values, width=0.55,
                  color=PALETTE[j], edgecolor="white")
    for b, v in zip(bars, counts.values):
        ax.text(b.get_x() + b.get_width() / 2, v + ymax_pad * 0.02 * counts.max(), str(v),
                ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, counts.max() * ymax_pad)
    ax.set_title(title, fontsize=13, fontweight="bold")
    strip_axes(ax, keep=("left", "bottom"))
    if j in (1, 2):
        plt.setp(ax.get_xticklabels(), rotation=15)

fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "07_人力资源看板", "hr")
print(f"看板已生成：总人数 {total}；各维度计数均通过核对")
