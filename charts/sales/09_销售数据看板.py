"""09 销售数据看板总装（复现 Excel「数据大屏」深色整屏看板）

布局与 Excel 数据大屏一致：
- 顶部 5 张 KPI 卡片：成本 / 销量 / 销售额 / 利润额 / 利润率（均为 9 月值）；
- 中部：各月销售额面积图 + 销量环比；
- 下部：产品类别销量环形图 + 利润额占比环形图 + 商品销售额 Top3；
- 底部：区域销量 + 快递公司销量 + 成本类别占比（4 张迷你环形图）。

所有指标由明细现场计算，并设断言与 Excel 缓存值核对：
  成本 929.25 / 销量 751 / 销售额 134.29 万 / 利润额 16.37 万 / 利润率 12.19%。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib.pyplot as plt
from common import (load_sales, load_cost, donut, kpi_card, style_dark,
                    save, MONTH, DARK_BG, DARK_TEXT, DARK_ACCENT)

df = load_sales()
cost = load_cost()
m = df[df["月份_销售"] == MONTH]
mc = cost[cost["月份_成本"] == MONTH]

# ---------- 指标计算（全部来自明细，并用断言与 Excel 缓存值核对） ----------
kpi_cost = mc["成本"].sum()
kpi_qty = len(m)
kpi_sales = m["订单额"].sum() / 1e4
kpi_profit = m["利润额"].sum() / 1e4
kpi_margin = kpi_profit / kpi_sales
assert kpi_qty == 751 and round(kpi_sales, 4) == 134.2887
assert round(kpi_cost, 4) == 929.2469 and round(kpi_margin, 5) == 0.12194

months = [f"{i}月" for i in range(1, 13)]
sales_wan = df.groupby("月份_销售")["订单额"].sum().reindex(months) / 1e4
qty = df.groupby("月份_销售").size().reindex(months)
mom = (qty[MONTH] - qty["8月"]) / qty["8月"]
cat_cnt = m["产品类别"].value_counts().reindex(["办公用品", "家具产品", "数码电子"])
top3 = (m.groupby("产品名称").agg(s=("订单额", "sum"), q=("订单单号", "count"))
          .sort_values("s", ascending=False).head(3))
region = m["区域"].value_counts()
express = m["快递公司"].value_counts()
cost_cat = mc.set_index("类别").reindex(["推广", "其他", "人工", "产品"])

# ---------- 整屏布局 ----------
fig = plt.figure(figsize=(18, 13), facecolor=DARK_BG)
fig.suptitle(f"销售数据大屏（2021 年 {MONTH}）", fontsize=22, fontweight="bold",
             color=DARK_TEXT, y=0.975)
cards = [("成本", f"{kpi_cost:,.2f}"), ("销量", f"{kpi_qty:,}"),
         ("销售额", f"{kpi_sales:,.2f} 万"), ("利润额", f"{kpi_profit:,.2f} 万"),
         ("利润率", f"{kpi_margin:.2%}")]
for i, (t, v) in enumerate(cards):
    kpi_card(fig, (0.03 + i * 0.194, 0.885, 0.178, 0.065), t, v, dark=True)

gs = fig.add_gridspec(3, 3, left=0.03, right=0.97, top=0.855, bottom=0.03,
                      hspace=0.55, wspace=0.25)

# 1) 各月销售额面积图
ax = fig.add_subplot(gs[0, :2]); style_dark(ax)
ax.fill_between(range(12), sales_wan.values, color=DARK_ACCENT[0], alpha=0.3)
ax.plot(range(12), sales_wan.values, color=DARK_ACCENT[0], lw=2.2, marker="o", ms=4)
ax.set_xticks(range(12), months)
ax.set_title("各月销售额（万元）", color=DARK_TEXT, fontsize=13, fontweight="bold")

# 2) 销量环比
ax = fig.add_subplot(gs[0, 2]); style_dark(ax)
bars = ax.bar(["8月", "9月"], [qty["8月"], qty[MONTH]], width=0.45,
              color=DARK_ACCENT[1:3], edgecolor="white")
for b, v in zip(bars, [qty["8月"], qty[MONTH]]):
    ax.text(b.get_x() + b.get_width() / 2, v + 10, str(v), ha="center",
            color=DARK_TEXT, fontsize=11, fontweight="bold")
ax.text(0.5, 0.93, f"环比 {mom:+.2%}", transform=ax.transAxes, ha="center",
        color=DARK_ACCENT[1], fontsize=14, fontweight="bold")
ax.set_ylim(0, qty[MONTH] * 1.2)
ax.set_title("销量环比", color=DARK_TEXT, fontsize=13, fontweight="bold")

# 3) 产品类别销量环形图
ax = fig.add_subplot(gs[1, 0])
donut(ax, cat_cnt.values, list(cat_cnt.index), dark=True, center_text=f"销量\n{cat_cnt.sum()}")
ax.set_title(f"产品类别销量（{MONTH}）", color=DARK_TEXT, fontsize=13, fontweight="bold")

# 4) 利润额占比销售额环形图
ax = fig.add_subplot(gs[1, 1])
donut(ax, [kpi_margin, 1 - kpi_margin], [f"利润率 {kpi_margin:.2%}", ""], dark=True,
      center_text=f"利润率\n{kpi_margin:.1%}", fmt="{lab}")
ax.set_title("利润额占比销售额", color=DARK_TEXT, fontsize=13, fontweight="bold")

# 5) 商品销售额 Top3
ax = fig.add_subplot(gs[1, 2]); style_dark(ax)
names = [n if len(n) <= 20 else n[:19] + "…" for n in top3.index]
ax.barh(range(3), top3["s"] / 1e4, height=0.5, color=DARK_ACCENT[:3], edgecolor="white")
ax.set_yticks(range(3), names, color=DARK_TEXT)
ax.invert_yaxis()
for i, (_, row) in enumerate(top3.iterrows()):
    ax.text(row["s"] / 1e4 + 0.15, i, f"{row['s']/1e4:.2f} 万 / {int(row['q'])} 件",
            va="center", color=DARK_TEXT, fontsize=9.5)
ax.set_xlim(0, top3["s"].max() / 1e4 * 1.35)
ax.set_title(f"商品销售额 Top3（{MONTH}）", color=DARK_TEXT, fontsize=13, fontweight="bold")

# 6) 区域销量
ax = fig.add_subplot(gs[2, 0]); style_dark(ax)
ax.bar(region.index, region.values, color=DARK_ACCENT[0], edgecolor="white")
for i, v in enumerate(region.values):
    ax.text(i, v + 5, str(v), ha="center", color=DARK_TEXT, fontsize=9.5)
ax.set_ylim(0, region.max() * 1.15)
ax.set_title(f"区域销量（{MONTH}）", color=DARK_TEXT, fontsize=13, fontweight="bold")

# 7) 快递公司销量
ax = fig.add_subplot(gs[2, 1]); style_dark(ax)
ax.bar(express.index, express.values, color=DARK_ACCENT[3], edgecolor="white")
for i, v in enumerate(express.values):
    ax.text(i, v + 5, str(v), ha="center", color=DARK_TEXT, fontsize=9.5)
ax.set_ylim(0, express.max() * 1.15)
ax.set_title(f"快递公司销量（{MONTH}）", color=DARK_TEXT, fontsize=13, fontweight="bold")

# 8) 成本类别占比（4 张迷你环形图）
inner = gs[2, 2].subgridspec(1, 4, wspace=0.1)
for k, cat in enumerate(["推广", "其他", "人工", "产品"]):
    ax = fig.add_subplot(inner[0, k])
    r = cost_cat.loc[cat, "成本"] / kpi_cost
    ax.pie([r, 1 - r], colors=[DARK_ACCENT[1], "#1A3A66"], startangle=90,
           counterclock=False, wedgeprops=dict(width=0.42, edgecolor=DARK_BG))
    ax.text(0, 0, f"{r:.0%}", ha="center", va="center", fontsize=10,
            fontweight="bold", color=DARK_TEXT)
    ax.set_title(cat, color=DARK_TEXT, fontsize=10)
    ax.set(aspect="equal")
fig.text(0.79, 0.30, f"成本类别占比（{MONTH}）", color=DARK_TEXT,
         fontsize=13, fontweight="bold", ha="center")

save(fig, "09_销售数据看板", "sales")
print(f"看板已生成：成本 {kpi_cost:,.2f} / 销量 {kpi_qty} / 销售额 {kpi_sales:,.2f} 万 / "
      f"利润额 {kpi_profit:,.2f} 万 / 利润率 {kpi_margin:.2%}")
