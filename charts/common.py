"""通用绘图设置与工具函数。

第四章两个看板的脚本共用：中文字体、统一配色、环形图 / KPI 卡片 / 图片保存等。
数据统一从仓库根目录的 data/ 读取，所有汇总数字均由 pandas 现场计算，
与 Excel《第四章》看板中的缓存结果逐项核对一致（见「第四章看板复现-详细说明.md」）。
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# 中文字体回退列表（Windows / macOS / Linux 均可找到可用字体）
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Noto Sans CJK JP",
    "WenQuanYi Zen Hei", "SimHei", "Arial Unicode MS",
]
plt.rcParams["axes.unicode_minus"] = False
# SVG 使用文字引用模式（体积更小，GitHub README 可直接渲染）
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "sans-serif"

# 项目统一配色（贴近 Excel 商务配色）
PALETTE = ["#4472C4", "#ED7D31", "#A5A5A5", "#FFC000", "#5B9BD5", "#70AD47", "#264478", "#9E480E"]

# 数据大屏深色主题（复现 Excel 销售看板的深色底大屏风格）
DARK_BG = "#0B1F3A"
DARK_CARD = "#12294D"
DARK_TEXT = "#E8EEF7"
DARK_GRID = "#2A4A7F"
DARK_ACCENT = ["#3FA7FF", "#FFB84D", "#7BD88F", "#FF7B9C", "#B98CFF", "#5EE0E6"]

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")
IMG_DIR = os.path.join(ROOT, "images")

# 看板当前展示月份（对应 Excel 看板的月份选择控件，默认 9 月）
# 修改此变量即可复现任意月份的销售看板。
MONTH = "9月"


def save(fig, name, subdir=""):
    """同时保存 PNG（本地查看）与 SVG（矢量，可直接在 GitHub 渲染）"""
    out = os.path.join(IMG_DIR, subdir) if subdir else IMG_DIR
    os.makedirs(out, exist_ok=True)
    for ext in ("png", "svg"):
        path = os.path.join(out, f"{name}.{ext}")
        fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"已保存 -> {path}")
    plt.close(fig)


def load_hr():
    """读取人力资源明细（1470 名员工）"""
    return pd.read_csv(os.path.join(DATA_DIR, "人力资源明细.csv"))


def load_sales():
    """读取销售明细（8564 条订单）"""
    df = pd.read_csv(os.path.join(DATA_DIR, "销售明细.csv"), parse_dates=["订单日期"])
    return df


def load_cost():
    """读取成本明细（12 个月 × 4 个成本类别）"""
    return pd.read_csv(os.path.join(DATA_DIR, "成本明细.csv"))


def donut(ax, values, labels, colors=None, center_text="", dark=False, fmt="{lab}\n{v}"):
    """环形图：wedgeprops 挖空中心，与 Excel 圆环图一致。

    fmt 控制引出线标注格式：默认「标签\n数值」；单值占比图传 fmt="{lab}" 只显示标签。
    """
    colors = colors or (DARK_ACCENT if dark else PALETTE)
    wedges, _ = ax.pie(
        values, colors=colors[: len(values)], startangle=90, counterclock=False,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.2),
    )
    text_color = DARK_TEXT if dark else "#333333"
    for w, lab, v in zip(wedges, labels, values):
        if not lab:  # 空标签的辅助段不标注
            continue
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        x, y = np.cos(ang), np.sin(ang)
        ax.annotate(fmt.format(lab=lab, v=v), xy=(x * 0.79, y * 0.79), ha="center", va="center",
                    fontsize=9, color=text_color,
                    xytext=(x * 1.28, y * 1.22), textcoords="data",
                    arrowprops=dict(arrowstyle="-", color=text_color, lw=0.7, alpha=0.6))
    if center_text:
        ax.text(0, 0, center_text, ha="center", va="center", fontsize=12,
                fontweight="bold", color=text_color)
    ax.set(aspect="equal")
    return wedges


def kpi_card(fig, pos, title, value, dark=True):
    """KPI 卡片：圆角矩形底 + 标题 + 大数字，对应 Excel 看板顶部的指标卡"""
    bg = DARK_CARD if dark else "#F5F7FA"
    tcolor = DARK_TEXT if dark else "#333333"
    scolor = "#8FB4E8" if dark else "#888888"
    box = FancyBboxPatch((pos[0], pos[1]), pos[2], pos[3],
                         boxstyle="round,pad=0.006,rounding_size=0.012",
                         transform=fig.transFigure, figure=fig,
                         linewidth=0, facecolor=bg, zorder=1)
    fig.patches.append(box)
    fig.text(pos[0] + pos[2] / 2, pos[1] + pos[3] * 0.68, title, ha="center",
             va="center", fontsize=11, color=scolor, zorder=2)
    fig.text(pos[0] + pos[2] / 2, pos[1] + pos[3] * 0.32, value, ha="center",
             va="center", fontsize=17, fontweight="bold", color=tcolor, zorder=2)


def style_dark(ax):
    """坐标轴深色主题"""
    ax.set_facecolor(DARK_BG)
    ax.tick_params(colors=DARK_TEXT, labelsize=9)
    for s in ax.spines.values():
        s.set_color(DARK_GRID)
    ax.grid(axis="y", color=DARK_GRID, linewidth=0.6, alpha=0.5)
    ax.set_axisbelow(True)


def strip_axes(ax, keep=()):
    """隐藏多余边框，仅保留 keep 指定的边"""
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(side in keep)
