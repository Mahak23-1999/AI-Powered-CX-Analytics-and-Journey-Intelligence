import streamlit as st
import time
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI CX Analytics",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ---------- SESSION STATE ----------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "ecommerce"
if "counter_triggered" not in st.session_state:
    st.session_state.counter_triggered = False
if "show_demo" not in st.session_state:
    st.session_state.show_demo = False
if "selected_feature" not in st.session_state:
    st.session_state.selected_feature = None

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, .stApp {
    background: #f8fafc !important;
}

.main .block-container {
    padding: 0 2rem 2rem 2rem !important;
    max-width: 1200px !important;
}

/* ---- HERO ---- */
.hero-wrapper {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    margin-bottom: 56px;
    background: linear-gradient(135deg, #0052cc 0%, #0078d4 60%, #00b4d8 100%);
    padding: 80px 48px 60px;
    box-shadow: 0 20px 60px rgba(0,82,204,0.25);
}
.hero-wrapper::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
}
.hero-wrapper::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -40px;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    padding: 8px 18px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 24px;
    letter-spacing: 0.5px;
}
.hero-title {
    font-size: 56px;
    font-weight: 900;
    color: white;
    line-height: 1.1;
    letter-spacing: -2px;
    margin-bottom: 20px;
}
.hero-title span {
    background: linear-gradient(135deg, #ffd166, #ff9f1c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 18px;
    color: rgba(255,255,255,0.85);
    line-height: 1.65;
    max-width: 540px;
    margin-bottom: 36px;
    font-weight: 400;
}
.hero-stats {
    display: flex;
    gap: 40px;
    margin-top: 10px;
}
.hero-stat-item {
    text-align: left;
}
.hero-stat-num {
    font-size: 28px;
    font-weight: 800;
    color: white;
}
.hero-stat-label {
    font-size: 13px;
    color: rgba(255,255,255,0.7);
    margin-top: 2px;
}
.hero-image-panel {
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    width: 420px;
    height: 300px;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 24px 60px rgba(0,0,0,0.3);
    border: 2px solid rgba(255,255,255,0.2);
}
.hero-image-panel img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.9;
}
.hero-image-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0,82,204,0.2) 0%, rgba(0,180,216,0.1) 100%);
}

/* ---- SECTION HEADERS ---- */
.section-header {
    display: flex;
    align-items: flex-end;
    gap: 16px;
    margin: 56px 0 32px;
}
.section-label {
    font-size: 12px;
    font-weight: 700;
    color: #0052cc;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.section-title {
    font-size: 36px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -1px;
    line-height: 1.1;
}
.section-line {
    flex: 1;
    height: 2px;
    background: linear-gradient(to right, #e2e8f0, transparent);
    margin-bottom: 8px;
}

/* ---- FEATURE CARDS ---- */
.feature-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    height: 100%;
}
.feature-card:hover {
    border-color: #0052cc;
    box-shadow: 0 20px 40px rgba(0,82,204,0.12);
    transform: translateY(-6px);
}
.feature-card-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
}
.feature-card-body {
    padding: 24px;
}
.feature-card-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 14px;
}
.feature-card-title {
    font-size: 17px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 8px;
}
.feature-card-desc {
    font-size: 14px;
    color: #64748b;
    line-height: 1.6;
}
.feature-tag {
    display: inline-block;
    background: #eff6ff;
    color: #0052cc;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 100px;
    margin-top: 12px;
    letter-spacing: 0.5px;
}

/* ---- METRIC CARDS ---- */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 16px;
}
.metric-card {
    border-radius: 20px;
    padding: 28px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
}
.metric-card-0 { background: linear-gradient(135deg, #0052cc, #0078d4); box-shadow: 0 8px 32px rgba(0,82,204,0.2); }
.metric-card-1 { background: linear-gradient(135deg, #10b981, #059669); box-shadow: 0 8px 32px rgba(16,185,129,0.2); }
.metric-card-2 { background: linear-gradient(135deg, #f59e0b, #d97706); box-shadow: 0 8px 32px rgba(245,158,11,0.2); }
.metric-card-3 { background: linear-gradient(135deg, #8b5cf6, #7c3aed); box-shadow: 0 8px 32px rgba(139,92,246,0.2); }

.metric-card::after {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.metric-value {
    font-size: 40px;
    font-weight: 900;
    color: white;
    letter-spacing: -1.5px;
    line-height: 1;
    margin-bottom: 8px;
}
.metric-label {
    font-size: 14px;
    color: rgba(255,255,255,0.85);
    font-weight: 500;
}
.metric-trend {
    font-size: 12px;
    color: rgba(255,255,255,0.7);
    margin-top: 6px;
}

/* ---- HOW IT WORKS ---- */
.step-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 28px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.step-card:hover {
    border-color: #0052cc;
    box-shadow: 0 16px 40px rgba(0,82,204,0.1);
    transform: translateY(-4px);
}
.step-number {
    position: absolute;
    top: 20px; right: 20px;
    font-size: 64px;
    font-weight: 900;
    color: #f0f4ff;
    line-height: 1;
    pointer-events: none;
}
.step-icon-wrap {
    width: 56px; height: 56px;
    border-radius: 16px;
    background: linear-gradient(135deg, #0052cc, #0078d4);
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    margin-bottom: 18px;
    box-shadow: 0 8px 20px rgba(0,82,204,0.25);
}
.step-title {
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 10px;
}
.step-desc {
    font-size: 14px;
    color: #64748b;
    line-height: 1.6;
}

/* ---- INDUSTRY TABS ---- */
.tab-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
.industry-content {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 300px;
}
.industry-text {
    padding: 36px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.industry-label {
    font-size: 12px;
    font-weight: 700;
    color: #0052cc;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 12px;
}
.industry-title {
    font-size: 26px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
}
.industry-desc {
    font-size: 15px;
    color: #64748b;
    line-height: 1.7;
    margin-bottom: 20px;
}
.industry-bullets {
    list-style: none;
    padding: 0;
}
.industry-bullets li {
    font-size: 14px;
    color: #374151;
    padding: 5px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.industry-bullets li::before {
    content: '';
    width: 8px; height: 8px;
    background: #0052cc;
    border-radius: 50%;
    flex-shrink: 0;
}
.industry-image {
    overflow: hidden;
}
.industry-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* ---- TESTIMONIALS ---- */
.testimonial-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 28px;
    transition: all 0.3s ease;
    position: relative;
}
.testimonial-card:hover {
    border-color: #0052cc;
    box-shadow: 0 16px 40px rgba(0,82,204,0.1);
    transform: translateY(-4px);
}
.testimonial-quote-icon {
    font-size: 40px;
    color: #dbeafe;
    line-height: 1;
    margin-bottom: 12px;
}
.testimonial-text {
    font-size: 15px;
    color: #374151;
    line-height: 1.7;
    font-style: italic;
    margin-bottom: 20px;
}
.testimonial-author {
    display: flex;
    align-items: center;
    gap: 12px;
}
.testimonial-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #dbeafe;
}
.testimonial-name {
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
}
.testimonial-role {
    font-size: 13px;
    color: #94a3b8;
}
.testimonial-stars {
    position: absolute;
    top: 24px; right: 24px;
    color: #f59e0b;
    font-size: 14px;
}

/* ---- CTA SECTION ---- */
.cta-section {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    border-radius: 24px;
    padding: 64px 48px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin: 48px 0;
}
.cta-section::before {
    content: '';
    position: absolute;
    top: -100px; right: -100px;
    width: 400px; height: 400px;
    border-radius: 50%;
    background: rgba(0,82,204,0.15);
}
.cta-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    letter-spacing: -1px;
    margin-bottom: 16px;
}
.cta-title span {
    background: linear-gradient(135deg, #ffd166, #ff9f1c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.cta-subtitle {
    font-size: 17px;
    color: rgba(255,255,255,0.7);
    margin-bottom: 36px;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}

/* ---- IMPACT STRIP ---- */
.impact-strip {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 40px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 32px 0;
}
.impact-item {
    text-align: center;
}
.impact-number {
    font-size: 44px;
    font-weight: 900;
    color: #0052cc;
    letter-spacing: -2px;
    line-height: 1;
}
.impact-label {
    font-size: 14px;
    color: #94a3b8;
    margin-top: 6px;
    font-weight: 500;
}
.impact-divider {
    width: 1px;
    height: 60px;
    background: #e2e8f0;
}

/* ---- FOOTER ---- */
.footer-section {
    border-top: 1.5px solid #e2e8f0;
    padding: 40px 0 20px;
    margin-top: 60px;
    text-align: center;
    color: #94a3b8;
    font-size: 14px;
}
.footer-logo {
    font-size: 20px;
    font-weight: 800;
    color: #0052cc;
    margin-bottom: 12px;
}

/* Streamlit button overrides */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s !important;
}

/* Demo modal */
.demo-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 32px;
    margin-top: 16px;
}
.demo-bar-label { font-size: 13px; color: #374151; font-weight: 600; margin-bottom: 4px; }
.demo-bar-wrap { background: #f1f5f9; border-radius: 100px; height: 12px; overflow: hidden; margin-bottom: 14px; }
.demo-bar-pos { background: linear-gradient(90deg, #10b981, #059669); height: 100%; border-radius: 100px; }
.demo-bar-neg { background: linear-gradient(90deg, #ef4444, #dc2626); height: 100%; border-radius: 100px; }
.demo-bar-neu { background: linear-gradient(90deg, #f59e0b, #d97706); height: 100%; border-radius: 100px; }
</style>
""", unsafe_allow_html=True)

# ====================================================
# HERO SECTION
# ====================================================
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">
        ✦ AI-Powered Analytics Platform
    </div>
    <div class="hero-title">
        Turn Customer Feedback<br>Into <span>Real Growth</span>
    </div>
    <div class="hero-subtitle">
        Leverage cutting-edge AI to understand sentiment, detect issues automatically, 
        and drive meaningful improvements to your customer experience — at scale.
    </div>
    <div class="hero-stats">
        <div class="hero-stat-item">
            <div class="hero-stat-num">2M+</div>
            <div class="hero-stat-label">Feedback Analyzed</div>
        </div>
        <div class="hero-stat-item">
            <div class="hero-stat-num">94%</div>
            <div class="hero-stat-label">AI Accuracy</div>
        </div>
        <div class="hero-stat-item">
            <div class="hero-stat-num">500+</div>
            <div class="hero-stat-label">Active Users</div>
        </div>
    </div>
    <div class="hero-image-panel">
        <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80" 
             alt="Analytics Dashboard" />
        <div class="hero-image-overlay"></div>
    </div>
</div>
""", unsafe_allow_html=True)

hero_c1, hero_c2, hero_c3, _ = st.columns([1, 1, 1, 4])
with hero_c1:
    if st.button("🚀 Start Free Trial", use_container_width=True, type="primary"):
        st.success("🎉 Redirecting to signup...")
with hero_c2:
    if st.button("▶ Watch Demo", use_container_width=True):
        st.session_state.show_demo = not st.session_state.show_demo

if st.session_state.show_demo:
    with st.container():
        st.markdown("""
        <div class="demo-card">
            <h4 style="font-size:18px;font-weight:700;color:#0f172a;margin-bottom:4px;">📊 Live Sentiment Analysis Demo</h4>
            <p style="font-size:14px;color:#64748b;margin-bottom:20px;">Sample results from 1,240 e-commerce reviews analyzed in real-time</p>
            <div class="demo-bar-label">😊 Positive Sentiment — 68%</div>
            <div class="demo-bar-wrap"><div class="demo-bar-pos" style="width:68%"></div></div>
            <div class="demo-bar-label">😡 Negative Sentiment — 19%</div>
            <div class="demo-bar-wrap"><div class="demo-bar-neg" style="width:19%"></div></div>
            <div class="demo-bar-label">😐 Neutral Sentiment — 13%</div>
            <div class="demo-bar-wrap"><div class="demo-bar-neu" style="width:13%"></div></div>
            <p style="font-size:13px;color:#94a3b8;margin-top:8px;">⚡ Analyzed in 2.3 seconds · 94% confidence · 3 key issues detected</p>
        </div>
        """, unsafe_allow_html=True)

# ====================================================
# CORE FEATURES — with real Unsplash images
# ====================================================
st.markdown("""
<div class="section-header">
    <div>
        <div class="section-label">What We Offer</div>
        <div class="section-title">Core Features</div>
    </div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

features = [
    {
        "icon": "📊",
        "title": "Sentiment Analysis",
        "desc": "Auto-classify feedback into positive, negative, or neutral with 94% accuracy using state-of-the-art NLP.",
        "tag": "NLP Powered",
        "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80"
    },
    {
        "icon": "🔍",
        "title": "Issue Detection",
        "desc": "Surface recurring pain points and complaints instantly. Stop firefighting, start preventing.",
        "tag": "Real-time",
        "img": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&q=80"
    },
    {
        "icon": "💡",
        "title": "Actionable Insights",
        "desc": "AI-generated recommendations that map directly to business outcomes and satisfaction KPIs.",
        "tag": "AI Generated",
        "img": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&q=80"
    }
]

feat_cols = st.columns(3)
for i, feat in enumerate(features):
    with feat_cols[i]:
        st.markdown(f"""
        <div class="feature-card">
            <img class="feature-card-image" src="{feat['img']}" alt="{feat['title']}" />
            <div class="feature-card-body">
                <div class="feature-card-icon">{feat['icon']}</div>
                <div class="feature-card-title">{feat['title']}</div>
                <div class="feature-card-desc">{feat['desc']}</div>
                <span class="feature-tag">{feat['tag']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ====================================================
# LIVE METRICS — animated style
# ====================================================
st.markdown("""
<div class="section-header">
    <div>
        <div class="section-label">Performance</div>
        <div class="section-title">Real-Time Analytics</div>
    </div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

metrics = [
    {"value": "94%", "label": "Sentiment Accuracy", "trend": "↑ +2.1% vs last month", "cls": "metric-card-0"},
    {"value": "15K+", "label": "Feedback Analyzed", "trend": "↑ +340 this week", "cls": "metric-card-1"},
    {"value": "320", "label": "Issues Resolved", "trend": "↑ +28 today", "cls": "metric-card-2"},
    {"value": "42", "label": "Insights Generated", "trend": "↑ +5 this session", "cls": "metric-card-3"},
]

m_cols = st.columns(4)
for i, m in enumerate(metrics):
    with m_cols[i]:
        st.markdown(f"""
        <div class="metric-card {m['cls']}">
            <div class="metric-value">{m['value']}</div>
            <div class="metric-label">{m['label']}</div>
            <div class="metric-trend">{m['trend']}</div>
        </div>
        """, unsafe_allow_html=True)

# ====================================================
# HOW IT WORKS — dynamic steps
# ====================================================
st.markdown("""
<div class="section-header">
    <div>
        <div class="section-label">Process</div>
        <div class="section-title">How It Works</div>
    </div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

steps = [
    {"icon": "📤", "num": "01", "title": "Upload Your Data", 
     "desc": "Drop in a CSV of customer feedback from any channel — support tickets, reviews, surveys, chat logs."},
    {"icon": "⚡", "num": "02", "title": "AI Processes It", 
     "desc": "Our NLP engine runs sentiment scoring, topic clustering, and issue tagging in seconds."},
    {"icon": "📈", "num": "03", "title": "Explore Insights", 
     "desc": "Interact with live dashboards, drill into segments, and export reports for stakeholders."},
]

s_cols = st.columns(3)
for i, step in enumerate(steps):
    with s_cols[i]:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{step['num']}</div>
            <div class="step-icon-wrap">{step['icon']}</div>
            <div class="step-title">{step['title']}</div>
            <div class="step-desc">{step['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

# Connector line
connector_img_col1, connector_img_col2 = st.columns([2, 1])
with connector_img_col1:
    st.markdown("")  # spacer

# ====================================================
# INDUSTRY SOLUTIONS — interactive tabs
# ====================================================
st.markdown("""
<div class="section-header">
    <div>
        <div class="section-label">Use Cases</div>
        <div class="section-title">Industry Solutions</div>
    </div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

industries = {
    "ecommerce": {
        "icon": "🛍️", "name": "E-commerce",
        "label": "Retail & Shopping",
        "title": "Boost Product Ratings",
        "desc": "Analyze thousands of product reviews instantly. Identify what customers love and hate, track sentiment by SKU, and catch quality issues before they escalate.",
        "bullets": ["Product-level sentiment tracking", "Return reason analysis", "Competitor mention detection", "Review response prioritization"],
        "img": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=700&q=80"
    },
    "telecom": {
        "icon": "📱", "name": "Telecom",
        "label": "Telecommunications",
        "title": "Reduce Churn Proactively",
        "desc": "Monitor support call sentiment, detect network complaint spikes, and identify at-risk customers before they leave — all in real time.",
        "bullets": ["Call center sentiment scoring", "Churn risk prediction", "Network issue correlation", "Agent performance analysis"],
        "img": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=700&q=80"
    },
    "healthcare": {
        "icon": "🏥", "name": "Healthcare",
        "label": "Health & Wellness",
        "title": "Improve Patient Experience",
        "desc": "Turn patient feedback into care improvements. Identify departmental pain points, track satisfaction trends, and prioritize operational changes with confidence.",
        "bullets": ["Patient satisfaction trends", "Department-level benchmarking", "Staff feedback analysis", "HIPAA-compliant processing"],
        "img": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=700&q=80"
    },
    "finance": {
        "icon": "🏦", "name": "Financial",
        "label": "Banking & Finance",
        "title": "Build Customer Trust",
        "desc": "Track satisfaction across products, detect compliance-sensitive language in feedback, and monitor the impact of policy changes on customer sentiment.",
        "bullets": ["Product satisfaction by segment", "Compliance flag detection", "NPS trend analysis", "Regulatory sentiment monitoring"],
        "img": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=700&q=80"
    },
}

tab_cols = st.columns(len(industries))
for i, (key, ind) in enumerate(industries.items()):
    with tab_cols[i]:
        btn_type = "primary" if st.session_state.active_tab == key else "secondary"
        if st.button(f"{ind['icon']} {ind['name']}", use_container_width=True, key=f"tab_{key}",
                     type="primary" if st.session_state.active_tab == key else "secondary"):
            st.session_state.active_tab = key
            st.rerun()

active = industries[st.session_state.active_tab]
st.markdown(f"""
<div class="industry-content">
    <div class="industry-text">
        <div class="industry-label">{active['label']}</div>
        <div class="industry-title">{active['title']}</div>
        <div class="industry-desc">{active['desc']}</div>
        <ul class="industry-bullets">
            {''.join(f'<li>{b}</li>' for b in active['bullets'])}
        </ul>
    </div>
    <div class="industry-image">
        <img src="{active['img']}" alt="{active['name']}" style="width:100%;height:100%;object-fit:cover;" />
    </div>
</div>
""", unsafe_allow_html=True)

# ====================================================
# IMPACT STRIP
# ====================================================
st.markdown("""
<div class="impact-strip">
    <div class="impact-item">
        <div class="impact-number">500+</div>
        <div class="impact-label">Active Users</div>
    </div>
    <div class="impact-divider"></div>
    <div class="impact-item">
        <div class="impact-number">2M+</div>
        <div class="impact-label">Feedback Analyzed</div>
    </div>
    <div class="impact-divider"></div>
    <div class="impact-item">
        <div class="impact-number">98%</div>
        <div class="impact-label">Satisfaction Rate</div>
    </div>
    <div class="impact-divider"></div>
    <div class="impact-item">
        <div class="impact-number">40%</div>
        <div class="impact-label">Avg. Resolution Faster</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====================================================
# TESTIMONIALS — with real avatars
# ====================================================

# ====================================================
# CTA SECTION
# ====================================================
st.markdown("""
<div class="cta-section">
    <div style="position:relative;z-index:1;">
        <div class="cta-title">Ready to <span>Get Started?</span></div>
        <div class="cta-subtitle">
            Upload your customer feedback data and let our AI analyze it instantly. 
            No credit card required for your first 1,000 records.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

cta_c1, cta_c2, cta_c3 = st.columns([2, 1, 1])


# ====================================================
# SIDEBAR
# ====================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <div style="font-size:24px;font-weight:900;color:#0052cc;letter-spacing:-1px;">AI CX Analytics</div>
        <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Intelligence for Every Interaction</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Navigation**")
    page_selection = st.radio(
        "Select a page:",
        ["🏠 Home", "📤 Upload Data", "📊 Analytics Dashboard", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("**Live Stats**")
    st.markdown("""
    <div style="background:#f0f4ff;border-radius:12px;padding:16px;margin-top:8px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="font-size:13px;color:#64748b;">Uptime</span>
            <span style="font-size:13px;font-weight:700;color:#10b981;">99.9%</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="font-size:13px;color:#64748b;">Avg. Process Time</span>
            <span style="font-size:13px;font-weight:700;color:#0052cc;">2.3s</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="font-size:13px;color:#64748b;">Queue Status</span>
            <span style="font-size:13px;font-weight:700;color:#10b981;">● Clear</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        if st.button("📚 Docs", use_container_width=True):
            st.info("Opening docs...")
    with col_res2:
        if st.button("💬 Support", use_container_width=True):
            st.info("Opening support...")

# ====================================================
# FOOTER
# ====================================================
st.markdown(f"""
<div class="footer-section">
    <div class="footer-logo">AI CX Analytics</div>
    <p>Built with using Streamlit &nbsp;·&nbsp; © {datetime.now().year} AI CX Analytics Platform</p>
    <p style="margin-top:8px;font-size:12px;">Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
</div>
""", unsafe_allow_html=True)