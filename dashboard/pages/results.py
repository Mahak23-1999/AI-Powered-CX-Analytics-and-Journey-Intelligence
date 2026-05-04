import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import sys
import os
from datetime import datetime

# ── PATH FIX ──────────────────────────────────────────────────────────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# ── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analysis Results · AI CX Analytics",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body, .stApp { background: #f8fafc !important; }
.main .block-container { padding: 0 2rem 2rem 2rem !important; max-width: 1300px !important; }

.page-header {
    background: linear-gradient(135deg, #0052cc 0%, #0078d4 60%, #00b4d8 100%);
    border-radius: 24px; padding: 48px 48px 40px; margin-bottom: 36px;
    position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,82,204,0.25);
}
.page-header::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:300px; height:300px; border-radius:50%;
    background:rgba(255,255,255,0.07);
}
.page-header::after {
    content:''; position:absolute; bottom:-80px; left:30%;
    width:250px; height:250px; border-radius:50%;
    background:rgba(255,255,255,0.04);
}
.page-breadcrumb { font-size:13px; color:rgba(255,255,255,0.6); margin-bottom:10px; font-weight:500; position:relative; z-index:1; }
.page-title { font-size:40px; font-weight:900; color:white; letter-spacing:-1.5px; line-height:1.1; margin-bottom:10px; position:relative; z-index:1; }
.page-subtitle { font-size:15px; color:rgba(255,255,255,0.8); line-height:1.6; position:relative; z-index:1; }

.kpi-card {
    border-radius:18px; padding:22px 24px; position:relative; overflow:hidden;
    transition:transform 0.25s ease, box-shadow 0.25s ease;
}
.kpi-card:hover { transform:translateY(-4px); }
.kpi-0 { background:linear-gradient(135deg,#0052cc,#0078d4); box-shadow:0 8px 28px rgba(0,82,204,0.22); }
.kpi-1 { background:linear-gradient(135deg,#10b981,#059669); box-shadow:0 8px 28px rgba(16,185,129,0.22); }
.kpi-2 { background:linear-gradient(135deg,#ef4444,#dc2626); box-shadow:0 8px 28px rgba(239,68,68,0.22); }
.kpi-3 { background:linear-gradient(135deg,#f59e0b,#d97706); box-shadow:0 8px 28px rgba(245,158,11,0.22); }
.kpi-4 { background:linear-gradient(135deg,#8b5cf6,#7c3aed); box-shadow:0 8px 28px rgba(139,92,246,0.22); }
.kpi-card::after {
    content:''; position:absolute; top:-20px; right:-20px;
    width:90px; height:90px; border-radius:50%;
    background:rgba(255,255,255,0.09);
}
.kpi-value { font-size:32px; font-weight:900; color:white; letter-spacing:-1px; line-height:1; margin-bottom:5px; }
.kpi-label { font-size:12px; color:rgba(255,255,255,0.85); font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }
.kpi-sub   { font-size:11px; color:rgba(255,255,255,0.6); margin-top:4px; }

.chart-card {
    background:white; border:1.5px solid #e2e8f0; border-radius:20px;
    padding:24px; transition:border-color 0.25s, box-shadow 0.25s;
}
.chart-card:hover { border-color:#bfdbfe; box-shadow:0 10px 28px rgba(0,82,204,0.07); }
.cc-title { font-size:15px; font-weight:700; color:#0f172a; margin-bottom:2px; }
.cc-sub   { font-size:12px; color:#94a3b8; margin-bottom:16px; }

.sec-label { font-size:11px; font-weight:700; color:#0052cc; text-transform:uppercase; letter-spacing:2px; margin-bottom:4px; }
.sec-title { font-size:22px; font-weight:800; color:#0f172a; letter-spacing:-0.5px; margin-bottom:20px; }

.insight-card {
    background:white; border:1.5px solid #e2e8f0; border-radius:14px;
    padding:18px 22px; display:flex; align-items:flex-start; gap:14px;
    margin-bottom:10px; transition:all 0.25s;
}
.insight-card:hover { border-color:#0052cc; box-shadow:0 6px 20px rgba(0,82,204,0.08); transform:translateX(3px); }
.i-icon { width:42px; height:42px; border-radius:11px; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:18px; }
.i-red    { background:linear-gradient(135deg,#fef2f2,#fee2e2); }
.i-green  { background:linear-gradient(135deg,#ecfdf5,#d1fae5); }
.i-yellow { background:linear-gradient(135deg,#fffbeb,#fef3c7); }
.i-blue   { background:linear-gradient(135deg,#eff6ff,#dbeafe); }
.i-title { font-size:14px; font-weight:700; color:#0f172a; margin-bottom:3px; }
.i-desc  { font-size:12px; color:#64748b; line-height:1.55; }
.badge { display:inline-block; font-size:10px; font-weight:700; padding:2px 9px; border-radius:100px; margin-top:5px; letter-spacing:0.3px; }
.b-red    { background:#fef2f2; color:#dc2626; border:1px solid #fca5a5; }
.b-yellow { background:#fffbeb; color:#d97706; border:1px solid #fde68a; }
.b-green  { background:#ecfdf5; color:#059669; border:1px solid #6ee7b7; }
.b-blue   { background:#eff6ff; color:#0052cc; border:1px solid #93c5fd; }

.rec-card {
    background:white; border:1.5px solid #e2e8f0; border-radius:18px;
    padding:26px 28px; margin-bottom:14px;
    position:relative; overflow:hidden; transition:all 0.25s;
}
.rec-card:hover { border-color:#0052cc; box-shadow:0 14px 36px rgba(0,82,204,0.09); transform:translateY(-3px); }
.rec-card::before { content:''; position:absolute; top:0; left:0; width:4px; height:100%; border-radius:18px 0 0 18px; }
.rc-critical::before { background:#ef4444; }
.rc-high::before     { background:#f59e0b; }
.rc-medium::before   { background:#10b981; }
.rc-pri   { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px; }
.rc-title { font-size:16px; font-weight:800; color:#0f172a; margin-bottom:6px; }
.rc-desc  { font-size:13px; color:#64748b; line-height:1.65; margin-bottom:12px; }
.rc-action { font-size:12px; color:#374151; font-weight:500; margin-bottom:4px; padding-left:14px; position:relative; }
.rc-action::before { content:'→'; position:absolute; left:0; color:#0052cc; font-weight:700; }
.rc-time  { font-size:11px; font-weight:600; padding:3px 10px; border-radius:100px; display:inline-block; margin-top:8px; }

.empty-state {
    background:white; border:2px dashed #e2e8f0; border-radius:24px;
    padding:64px 32px; text-align:center;
}
.es-icon  { font-size:60px; margin-bottom:14px; }
.es-title { font-size:20px; font-weight:700; color:#0f172a; margin-bottom:8px; }
.es-desc  { font-size:14px; color:#64748b; line-height:1.6; }

.stButton > button { border-radius:11px !important; font-weight:600 !important; }
.stTabs [data-baseweb="tab-list"] {
    background:white !important; border:1.5px solid #e2e8f0 !important;
    border-radius:14px !important; padding:5px !important; gap:3px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius:10px !important; font-weight:600 !important;
    font-size:13px !important; padding:8px 18px !important; color:#64748b !important;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#0052cc,#0078d4) !important; color:white !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# GUARD
# ══════════════════════════════════════════════════════════════════════
if "data" not in st.session_state:
    st.markdown("""
    <div class="empty-state">
        <div class="es-icon">📂</div>
        <div class="es-title">No Data Yet</div>
        <div class="es-desc">Upload a customer feedback CSV on the Upload page to begin your analysis.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📤 Go to Upload Page", type="primary"):
        st.info("Navigate to Upload Data in the sidebar.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════
# DATA PREPARATION
# ══════════════════════════════════════════════════════════════════════
df = st.session_state["data"].copy()

text_col = next(
    (c for c in df.columns if any(k in c.lower() for k in ["review","text","feedback","comment"])),
    None
)
if text_col is None:
    st.error("❌ No text column found. Rename a column to 'review', 'text', 'feedback', or 'comment'.")
    st.stop()

df[text_col] = df[text_col].fillna("").astype(str).str.strip()

# ── Sentiment ─────────────────────────────────────────────────────────
try:
    from backend.sentiment_analysis import get_sentiment
    results      = df[text_col].apply(get_sentiment)
    df["sentiment"] = results.apply(lambda x: x["sentiment"].lower() if isinstance(x, dict) else str(x).lower())
    df["score"]     = results.apply(lambda x: float(x["score"])      if isinstance(x, dict) else 0.0)
except Exception:
    def _mock(text):
        pos = ["good","great","love","excellent","perfect","amazing","happy","satisfied","fast","best"]
        neg = ["bad","terrible","worst","hate","awful","slow","broken","damaged","late","poor","refund"]
        t   = text.lower()
        p   = sum(w in t for w in pos)
        n   = sum(w in t for w in neg)
        return "positive" if p > n else ("negative" if n > p else "neutral")
    df["sentiment"] = df[text_col].apply(_mock)
    df["score"]     = df["sentiment"].map({"positive": 0.55, "negative": -0.55, "neutral": 0.0})

# ── Issue ─────────────────────────────────────────────────────────────
def categorize_issue(text):
    t = text.lower()
    if any(w in t for w in ["delivery","late","ship","shipping","delay","arrive","courier"]):     return "Delivery"
    if any(w in t for w in ["app","crash","bug","slow","error","loading","freeze","website"]):    return "Technical"
    if any(w in t for w in ["support","agent","staff","service","help","response","rude"]):       return "Support"
    if any(w in t for w in ["product","quality","damaged","broken","defect","packaging","item"]): return "Product"
    if any(w in t for w in ["price","expensive","cost","refund","money","charge","billing"]):     return "Pricing"
    return "General"

df["issue"]     = df[text_col].apply(categorize_issue)
df["sentiment"] = df["sentiment"].astype(str).str.lower().str.strip()
df["issue"]     = df["issue"].astype(str).str.strip()
df              = df.dropna(subset=["sentiment"])

# ── Constants ─────────────────────────────────────────────────────────
SENT_ORDER   = ["positive", "negative", "neutral"]
SENT_COLORS  = {"positive": "#10b981", "negative": "#ef4444", "neutral": "#f59e0b"}
ISSUE_COLORS = ["#0052cc","#0078d4","#00b4d8","#10b981","#f59e0b","#8b5cf6"]

sentiment_counts = df["sentiment"].value_counts().reindex(SENT_ORDER, fill_value=0)
issue_counts     = df["issue"].value_counts()
total            = len(df)
pos_pct          = sentiment_counts["positive"] / total * 100
neg_pct          = sentiment_counts["negative"] / total * 100
neu_pct          = sentiment_counts["neutral"]  / total * 100
avg_score        = df["score"].mean()
top_issue        = issue_counts.idxmax() if not issue_counts.empty else "N/A"
csat             = round(pos_pct / 10, 1)

neg_by_issue = df[df["sentiment"] == "negative"]["issue"].value_counts()

# ── Chart helper ──────────────────────────────────────────────────────
def style_ax(ax):
    ax.set_facecolor("#f8fafc")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e2e8f0")
    ax.spines["bottom"].set_color("#e2e8f0")
    ax.tick_params(colors="#64748b", labelsize=9)
    ax.xaxis.label.set_color("#94a3b8")
    ax.yaxis.label.set_color("#94a3b8")

# ══════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════
analysis_type = st.session_state.get("analysis_type", "Dashboard")
st.markdown(f"""
<div class="page-header">
    <div class="page-breadcrumb">🏠 Home &nbsp;/&nbsp; Upload &nbsp;/&nbsp; Results</div>
    <div class="page-title">📊 Analysis Results</div>
    <div class="page-subtitle">
        {total:,} records · {analysis_type} view · {datetime.now().strftime("%b %d, %Y at %I:%M %p")}
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    (k1, "kpi-0", f"{total:,}",      "Records",          f"Column: {text_col}"),
    (k2, "kpi-1", f"{pos_pct:.1f}%", "Positive",         f"{sentiment_counts['positive']:,} reviews"),
    (k3, "kpi-2", f"{neg_pct:.1f}%", "Negative",         f"{sentiment_counts['negative']:,} reviews"),
    (k4, "kpi-3", f"{csat}",         "CSAT Score (/10)", f"Avg polarity: {avg_score:+.3f}"),
    (k5, "kpi-4", top_issue,         "Top Issue",        f"{issue_counts.iloc[0]:,} mentions" if not issue_counts.empty else ""),
]
for col, cls, val, lbl, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📊  Dashboard", "📄  Insights", "💡  Recommendations"])

# ════════════════════════════════════
# TAB 1 — DASHBOARD
# ════════════════════════════════════
with tab1:

    # ── Sentiment mini-bars + pie ──────────────────────────────────────
    st.markdown('<div class="sec-label">Overview</div><div class="sec-title">Sentiment Breakdown</div>', unsafe_allow_html=True)

    sb1, sb2, sb3, pie_col = st.columns([1, 1, 1, 2])
    for col, label, pct, color, emoji in [
        (sb1, "Positive", pos_pct, "#10b981", "😊"),
        (sb2, "Negative", neg_pct, "#ef4444", "😡"),
        (sb3, "Neutral",  neu_pct, "#f59e0b", "😐"),
    ]:
        with col:
            count = sentiment_counts[label.lower()]
            st.markdown(f"""
            <div style="background:white;border:1.5px solid #e2e8f0;border-radius:16px;padding:18px 20px;">
                <div style="font-size:22px;margin-bottom:6px;">{emoji}</div>
                <div style="font-size:28px;font-weight:900;color:{color};letter-spacing:-1px;line-height:1;">{pct:.1f}%</div>
                <div style="font-size:11px;font-weight:600;color:#64748b;margin:6px 0 8px;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>
                <div style="background:#f1f5f9;border-radius:100px;height:7px;overflow:hidden;">
                    <div style="width:{pct}%;background:{color};height:100%;border-radius:100px;"></div>
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:5px;">{count:,} reviews</div>
            </div>
            """, unsafe_allow_html=True)

    # Pie chart
    with pie_col:
        st.markdown('<div class="chart-card"><div class="cc-title">Sentiment Distribution</div><div class="cc-sub">Share of positive, negative & neutral feedback</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4.5, 3.2))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        pie_vals   = [sentiment_counts[s] for s in SENT_ORDER]
        pie_colors = [SENT_COLORS[s]      for s in SENT_ORDER]
        if sum(pie_vals) > 0:
            _, _, autotexts = ax.pie(
                pie_vals, labels=None,
                autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
                colors=pie_colors, startangle=90,
                wedgeprops={"linewidth": 2, "edgecolor": "white"},
                pctdistance=0.78
            )
            for at in autotexts:
                at.set_fontsize(9); at.set_fontweight("600"); at.set_color("white")
        ax.legend(
            handles=[mpatches.Patch(color=SENT_COLORS[s], label=s.capitalize()) for s in SENT_ORDER],
            loc="lower center", ncol=3, fontsize=9, frameon=False,
            bbox_to_anchor=(0.5, -0.08)
        )
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Issue bar + Stacked sentiment-by-issue ─────────────────────────
    st.markdown('<div class="sec-label">Issue Analysis</div><div class="sec-title">Category Breakdown</div>', unsafe_allow_html=True)
    col_issue, col_stack = st.columns(2)

    with col_issue:
        st.markdown('<div class="chart-card"><div class="cc-title">Issue Frequency</div><div class="cc-sub">Volume of reviews per complaint category</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5.5, 3.8))
        fig.patch.set_facecolor("white")
        style_ax(ax)
        cats   = issue_counts.index[::-1].tolist()
        vals   = issue_counts.values[::-1].tolist()
        bclrs  = (ISSUE_COLORS * 4)[:len(cats)]
        bars   = ax.barh(cats, vals, color=bclrs, height=0.55, edgecolor="white", linewidth=1.5)
        for bar in bars:
            w = bar.get_width()
            ax.text(w + max(vals) * 0.015, bar.get_y() + bar.get_height() / 2,
                    f"{int(w):,}", va="center", ha="left", fontsize=9, color="#64748b", fontweight="600")
        ax.set_xlabel("Number of Reviews", fontsize=9)
        ax.set_xlim(0, max(vals) * 1.2)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_stack:
        st.markdown('<div class="chart-card"><div class="cc-title">Sentiment by Issue</div><div class="cc-sub">Sentiment mix within each complaint category</div>', unsafe_allow_html=True)
        pivot = pd.crosstab(df["issue"], df["sentiment"])
        for s in SENT_ORDER:
            if s not in pivot.columns:
                pivot[s] = 0
        pivot     = pivot[SENT_ORDER]
        pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

        fig, ax = plt.subplots(figsize=(5.5, 3.8))
        fig.patch.set_facecolor("white")
        style_ax(ax)
        bottom = np.zeros(len(pivot_pct))
        for s in SENT_ORDER:
            ax.bar(pivot_pct.index, pivot_pct[s].values, bottom=bottom,
                   label=s.capitalize(), color=SENT_COLORS[s],
                   edgecolor="white", linewidth=1.2)
            bottom += pivot_pct[s].values
        ax.set_ylabel("Percentage (%)", fontsize=9)
        ax.set_ylim(0, 115)
        ax.legend(loc="upper right", fontsize=9, frameon=False)
        plt.xticks(rotation=20, ha="right", fontsize=8)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Polarity histogram + Donut ─────────────────────────────────────
    st.markdown('<div class="sec-label">Deep Analysis</div><div class="sec-title">Polarity & Issue Share</div>', unsafe_allow_html=True)
    col_hist, col_donut = st.columns(2)

    with col_hist:
        st.markdown('<div class="chart-card"><div class="cc-title">Polarity Score Distribution</div><div class="cc-sub">TextBlob score per review (−1 very negative → +1 very positive)</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        fig.patch.set_facecolor("white")
        style_ax(ax)
        scores  = df["score"].dropna()
        n_bins  = min(30, max(10, len(scores) // 10))
        neg_s   = scores[scores < 0]
        neu_s   = scores[scores == 0]
        pos_s   = scores[scores > 0]
        if len(neg_s): ax.hist(neg_s, bins=max(3, n_bins//3), color="#ef4444", alpha=0.85, label="Negative", edgecolor="white")
        if len(neu_s): ax.hist(neu_s, bins=2,                  color="#f59e0b", alpha=0.85, label="Neutral",  edgecolor="white")
        if len(pos_s): ax.hist(pos_s, bins=max(3, n_bins//3), color="#10b981", alpha=0.85, label="Positive", edgecolor="white")
        ax.axvline(scores.mean(), color="#0052cc", linewidth=1.5, linestyle="--",
                   label=f"Mean: {scores.mean():+.3f}")
        ax.set_xlabel("Polarity Score", fontsize=9)
        ax.set_ylabel("Reviews", fontsize=9)
        ax.legend(fontsize=9, frameon=False)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_donut:
        st.markdown('<div class="chart-card"><div class="cc-title">Issue Share (Donut)</div><div class="cc-sub">Proportional breakdown of all complaint categories</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        d_colors = (ISSUE_COLORS * 4)[:len(issue_counts)]
        _, _, autotexts = ax.pie(
            issue_counts.values, labels=None,
            autopct=lambda p: f"{p:.1f}%" if p >= 5 else "",
            colors=d_colors, startangle=90,
            wedgeprops={"linewidth": 2.5, "edgecolor": "white", "width": 0.55},
            pctdistance=0.75
        )
        for at in autotexts:
            at.set_fontsize(8); at.set_fontweight("600"); at.set_color("white")
        ax.legend(
            handles=[mpatches.Patch(color=d_colors[i], label=f"{cat} ({issue_counts[cat]:,})")
                     for i, cat in enumerate(issue_counts.index)],
            loc="lower center", ncol=2, fontsize=8, frameon=False,
            bbox_to_anchor=(0.5, -0.15)
        )
        centre = plt.Circle((0, 0), 0.42, fc="white")
        ax.add_patch(centre)
        ax.text(0,  0.08, f"{len(issue_counts)}", ha="center", fontsize=22, fontweight="900", color="#0f172a")
        ax.text(0, -0.18, "Categories",           ha="center", fontsize=9,  fontweight="600", color="#94a3b8")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Negative rate by category (full width) ─────────────────────────
    st.markdown('<div class="sec-label">Risk Map</div><div class="sec-title">Negative Review Rate by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card"><div class="cc-title">Which Categories Drive the Most Dissatisfaction?</div><div class="cc-sub">% of reviews that are negative within each issue category vs overall average</div>', unsafe_allow_html=True)

    neg_rate = (neg_by_issue / issue_counts * 100).fillna(0).sort_values(ascending=False)
    fig, ax  = plt.subplots(figsize=(10, 2.8))
    fig.patch.set_facecolor("white")
    style_ax(ax)
    bar_c = ["#ef4444" if v >= 50 else "#f59e0b" if v >= 25 else "#10b981" for v in neg_rate.values]
    bars  = ax.bar(neg_rate.index, neg_rate.values, color=bar_c, edgecolor="white", linewidth=1.5, width=0.5)
    ax.axhline(neg_pct, color="#0052cc", linewidth=1.3, linestyle="--",
               label=f"Overall avg: {neg_pct:.1f}%")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                f"{h:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="600", color="#374151")
    ax.set_ylabel("% Negative", fontsize=9)
    ax.set_ylim(0, max(neg_rate.values) * 1.3 + 5)
    ax.legend(fontsize=9, frameon=False)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Raw data table ─────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 View Full Analyzed Data Table"):
        display_cols = [text_col, "sentiment", "score", "issue"]
        style_fn = lambda v: (
            "background-color:#ecfdf5;color:#065f46;font-weight:600" if v == "positive"
            else ("background-color:#fef2f2;color:#991b1b;font-weight:600" if v == "negative"
            else  "background-color:#fffbeb;color:#92400e;font-weight:600")
        )
        try:
            styled = df[display_cols].style.map(style_fn, subset=["sentiment"])
        except AttributeError:
            styled = df[display_cols].style.applymap(style_fn, subset=["sentiment"])
        st.dataframe(styled, use_container_width=True, height=320)

# ════════════════════════════════════
# TAB 2 — INSIGHTS
# ════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-label">Key Findings</div><div class="sec-title">Analysis Insights</div>', unsafe_allow_html=True)

    health       = "🟢 Healthy"  if pos_pct >= 60 else ("🟡 Needs Attention" if pos_pct >= 40 else "🔴 Critical")
    health_color = "#059669"     if pos_pct >= 60 else ("#d97706"            if pos_pct >= 40 else "#dc2626")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1.5px solid #93c5fd;
                border-radius:18px;padding:26px 30px;margin-bottom:24px;
                display:flex;align-items:center;gap:28px;flex-wrap:wrap;">
        <div style="text-align:center;min-width:90px;">
            <div style="font-size:44px;font-weight:900;color:#0052cc;letter-spacing:-2px;line-height:1;">{csat}</div>
            <div style="font-size:10px;color:#3b82f6;font-weight:700;margin-top:3px;text-transform:uppercase;letter-spacing:1px;">CSAT / 10</div>
        </div>
        <div style="width:1px;height:55px;background:#bfdbfe;"></div>
        <div>
            <div style="font-size:16px;font-weight:700;color:#1e40af;margin-bottom:5px;">
                Status: <span style="color:{health_color};">{health}</span>
            </div>
            <div style="font-size:13px;color:#3b82f6;line-height:1.6;">
                {total:,} reviews &nbsp;·&nbsp;
                <strong>{pos_pct:.1f}%</strong> positive &nbsp;·&nbsp;
                <strong>{neg_pct:.1f}%</strong> negative &nbsp;·&nbsp;
                <strong>{neu_pct:.1f}%</strong> neutral &nbsp;·&nbsp;
                avg polarity <strong>{avg_score:+.3f}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    top_issue_count = int(issue_counts[top_issue]) if top_issue in issue_counts else 0
    insights = [
        ("🔴","i-red",   f"Top Pain Point: {top_issue}",
         f"{top_issue_count:,} reviews ({top_issue_count/total*100:.1f}%) flag {top_issue.lower()} — most urgent area.",
         "Critical","b-red"),
        ("📉" if neg_pct > 30 else "⚠️",
         "i-red" if neg_pct > 30 else "i-yellow",
         f"Negative Rate: {neg_pct:.1f}%",
         f"{sentiment_counts['negative']:,} unhappy customers. {'Above 30% — urgent action needed.' if neg_pct > 30 else 'Manageable, monitor weekly.'}",
         "High Risk" if neg_pct > 30 else "Monitor",
         "b-red" if neg_pct > 30 else "b-yellow"),
        ("✅","i-green", f"Positive Strength: {pos_pct:.1f}%",
         f"{sentiment_counts['positive']:,} satisfied customers. {'Strong — amplify in marketing.' if pos_pct >= 60 else 'Room to grow — investigate satisfaction drivers.'}",
         "Strength" if pos_pct >= 60 else "Opportunity",
         "b-green"  if pos_pct >= 60 else "b-yellow"),
        ("📊","i-blue",  f"Issue Spread: {len(issue_counts)} Categories",
         f"{'Concentrated — fix one area for fast wins.' if len(issue_counts) <= 3 else 'Broad spread — rank by negative rate, not just volume.'}",
         "Insight","b-blue"),
        ("🎯","i-yellow", f"Avg Polarity: {avg_score:+.3f}",
         f"{'Net positive customer perception.' if avg_score > 0 else 'Net negative — customers skew dissatisfied.'} Range: {df['score'].min():.3f} → {df['score'].max():.3f}.",
         "Positive Lean" if avg_score > 0 else "Negative Lean",
         "b-green" if avg_score > 0 else "b-red"),
    ]
    for icon, icls, title, desc, badge, bcls in insights:
        st.markdown(f"""
        <div class="insight-card">
            <div class="i-icon {icls}">{icon}</div>
            <div>
                <div class="i-title">{title}</div>
                <div class="i-desc">{desc}</div>
                <span class="badge {bcls}">{badge}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Breakdown</div><div class="sec-title">Issue Frequency Table</div>', unsafe_allow_html=True)
    issue_df = issue_counts.reset_index()
    issue_df.columns = ["Issue Category", "Count"]
    issue_df["% of Total"]       = (issue_df["Count"] / total * 100).round(1).astype(str) + "%"
    issue_df["Negative Reviews"] = issue_df["Issue Category"].apply(lambda x: int(neg_by_issue.get(x, 0)))
    issue_df["Negative Rate"]    = (issue_df["Negative Reviews"] / issue_df["Count"] * 100).round(1).astype(str) + "%"
    issue_df["Priority"]         = issue_df["Count"].apply(
        lambda x: "🔴 Critical" if x/total > 0.3 else ("🟡 High" if x/total > 0.15 else "🟢 Normal")
    )
    st.dataframe(issue_df, use_container_width=True, hide_index=True)

# ════════════════════════════════════
# TAB 3 — RECOMMENDATIONS
# ════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-label">Action Plan</div><div class="sec-title">AI-Generated Recommendations</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#fffbeb;border:1.5px solid #fde68a;border-radius:12px;
                padding:14px 18px;margin-bottom:22px;font-size:13px;color:#92400e;">
        ⚡ <strong>Personalised for your data:</strong> Ranked by impact — top issue
        <strong>{top_issue}</strong>, negative rate <strong>{neg_pct:.1f}%</strong>.
    </div>
    """, unsafe_allow_html=True)

    rec_map = {
        "Delivery": {
            "critical": ("Overhaul Last-Mile Delivery",
                "Delivery is your #1 complaint. Customer loyalty erodes fast with late or missing orders.",
                ["Audit carrier SLAs and renegotiate contracts",
                 "Add real-time tracking notifications via SMS/email",
                 "Set up automated delay alerts with proactive apologies"],
                "⚡ 0–30 days", "#ef4444", "rc-critical"),
            "high": ("Improve Delivery Communication",
                "Proactive communication reduces negative reviews even when delays happen.",
                ["Send estimated delivery windows at order confirmation",
                 "Create a self-service rescheduling portal"],
                "📅 30–60 days", "#f59e0b", "rc-high"),
        },
        "Technical": {
            "critical": ("Fix Critical App/Platform Issues",
                "Technical failures are the fastest path to churn. Each crash is a lost customer.",
                ["Set up crash monitoring (Sentry / Datadog) immediately",
                 "Prioritise bug fixes in the next sprint",
                 "Implement graceful degradation for peak traffic"],
                "⚡ 0–14 days", "#ef4444", "rc-critical"),
            "high": ("Invest in Performance Infrastructure",
                "Slow load times and downtime compound into significant revenue loss.",
                ["Run load testing at 2× expected peak traffic",
                 "Implement a CDN for all static assets"],
                "📅 60–90 days", "#10b981", "rc-medium"),
        },
        "Support": {
            "critical": ("Rethink Customer Support Quality",
                "Support complaints signal a broken resolution loop.",
                ["Audit last 100 tickets for first-contact resolution rate",
                 "Train agents on empathetic, solution-first communication",
                 "Introduce tiered escalation for complex issues"],
                "⚡ 0–30 days", "#ef4444", "rc-critical"),
            "high": ("Build Self-Service Support Channels",
                "Deflect low-complexity tickets with a knowledge base and AI chat.",
                ["Create FAQ pages for top 10 support topics",
                 "Implement a Tier-1 chatbot for instant answers"],
                "📅 30–60 days", "#f59e0b", "rc-high"),
        },
        "Product": {
            "critical": ("Address Product Quality Issues",
                "Quality complaints damage brand trust and drive returns.",
                ["Review QC checkpoints throughout production",
                 "Survey customers who reported defects directly",
                 "Add 100% inspection for high-complaint SKUs"],
                "⚡ 0–21 days", "#ef4444", "rc-critical"),
            "high": ("Improve Packaging & Handling",
                "Many damage complaints originate in shipping.",
                ["Test new packaging materials for fragile products",
                 "Add 'Fragile' handling flags to fulfilment workflow"],
                "📅 30–45 days", "#10b981", "rc-medium"),
        },
        "Pricing": {
            "critical": ("Close the Value Perception Gap",
                "Pricing complaints mean customers don't feel they're getting value.",
                ["Survey churned customers on pricing expectations",
                 "Highlight value propositions more clearly in marketing",
                 "Offer flexible payment or subscription options"],
                "⚡ 0–30 days", "#ef4444", "rc-critical"),
            "high": ("Streamline Refund & Billing",
                "A smooth refund experience converts unhappy customers into repeat buyers.",
                ["Automate refund approvals under $50",
                 "Reduce processing time to under 3 business days"],
                "📅 30–60 days", "#f59e0b", "rc-high"),
        },
        "General": {
            "critical": ("Establish a Feedback Monitoring System",
                "Without categorised insights you're flying blind.",
                ["Set up a weekly sentiment review cadence",
                 "Assign issue category owners across the team",
                 "Build a live feedback dashboard for leadership"],
                "⚡ 0–14 days", "#ef4444", "rc-critical"),
            "high": ("Launch a Proactive Satisfaction Survey",
                "Structured feedback supplements organic reviews.",
                ["Deploy NPS survey post-purchase to all customers",
                 "Follow up with detractors (0–6) within 48 hours"],
                "📅 14–30 days", "#10b981", "rc-medium"),
        },
    }

    recs = rec_map.get(top_issue, rec_map["General"])
    for pri_label, key in [("🚨 Critical Priority", "critical"), ("📋 High Priority", "high")]:
        title, desc, actions, timeline, color, cls = recs[key]
        st.markdown(f"""
        <div class="rec-card {cls}">
            <div class="rc-pri" style="color:{color};">{pri_label}</div>
            <div class="rc-title">{title}</div>
            <div class="rc-desc">{desc}</div>
            {''.join(f'<div class="rc-action">{a}</div>' for a in actions)}
            <span class="rc-time" style="background:{color}18;color:{color};border:1px solid {color}35;">{timeline}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rec-card rc-medium">
        <div class="rc-pri" style="color:#10b981;">✅ Always-On Best Practice</div>
        <div class="rc-title">Track Sentiment Weekly</div>
        <div class="rc-desc">
            Positive rate: <strong>{pos_pct:.1f}%</strong> · avg polarity: <strong>{avg_score:+.3f}</strong>.
            Weekly reviews catch drops before they compound.
        </div>
        <div class="rc-action">Re-run analysis every Monday with refreshed data</div>
        <div class="rc-action">Alert if negative rate exceeds {min(neg_pct + 10, 60):.0f}%</div>
        <div class="rc-action">Share monthly trend report with leadership</div>
        <span class="rc-time" style="background:#10b98118;color:#10b981;border:1px solid #10b98135;">🔄 Ongoing</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ec1, ec2, _ = st.columns([1, 1, 3])
    with ec1:
        st.download_button(
            "⬇️ Export Results CSV",
            data=df[[text_col, "sentiment", "score", "issue"]].to_csv(index=False),
            file_name=f"cx_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    with ec2:
        if st.button("🔄 Re-run Analysis", use_container_width=True):
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:18px 0 8px;">
        <div style="font-size:20px;font-weight:900;color:#0052cc;letter-spacing:-1px;">AI CX Analytics</div>
        <div style="font-size:11px;color:#94a3b8;margin-top:3px;">Intelligence for Every Interaction</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navigation**")
    st.radio("Page", ["🏠 Home", "📤 Upload Data", "📊 Analysis Results", "⚙️ Settings"],
             index=2, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Current Analysis**")
    st.markdown(f"""
    <div style="background:#f0f4ff;border-radius:11px;padding:13px;font-size:12px;color:#374151;line-height:1.9;">
        📋 <strong>{total:,}</strong> rows<br>
        😊 <strong>{pos_pct:.1f}%</strong> positive<br>
        😡 <strong>{neg_pct:.1f}%</strong> negative<br>
        📊 CSAT <strong>{csat}/10</strong><br>
        🔍 Top: <strong>{top_issue}</strong>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;color:#94a3b8;margin-top:48px;padding-top:22px;
            border-top:1.5px solid #e2e8f0;font-size:12px;">
    AI CX Analytics Platform · © {datetime.now().year}
</div>
""", unsafe_allow_html=True)