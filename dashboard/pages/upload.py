import streamlit as st
import pandas as pd
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Upload Data · AI CX Analytics",
    layout="wide",
    page_icon="📤",
    initial_sidebar_state="expanded"
)

# ---------- SHARED CSS (same as homepage) ----------
st.markdown("""
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, .stApp { background: #f8fafc !important; }

.main .block-container {
    padding: 0 2rem 2rem 2rem !important;
    max-width: 1200px !important;
}

/* ---- PAGE HEADER ---- */
.page-header {
    background: linear-gradient(135deg, #0052cc 0%, #0078d4 60%, #00b4d8 100%);
    border-radius: 24px;
    padding: 48px 48px 40px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,82,204,0.25);
}
.page-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 200px;
    width: 250px; height: 250px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.page-breadcrumb {
    font-size: 13px;
    color: rgba(255,255,255,0.6);
    margin-bottom: 12px;
    font-weight: 500;
    position: relative; z-index: 1;
}
.page-title {
    font-size: 42px;
    font-weight: 900;
    color: white;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 12px;
    position: relative; z-index: 1;
}
.page-subtitle {
    font-size: 16px;
    color: rgba(255,255,255,0.8);
    font-weight: 400;
    line-height: 1.6;
    max-width: 500px;
    position: relative; z-index: 1;
}

/* ---- SECTION HEADERS ---- */
.section-header { margin: 40px 0 20px; }
.section-label {
    font-size: 11px; font-weight: 700; color: #0052cc;
    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px;
}
.section-title {
    font-size: 24px; font-weight: 800; color: #0f172a;
    letter-spacing: -0.5px; line-height: 1.2;
}

/* ---- UPLOAD ZONE ---- */
.upload-zone {
    background: white;
    border: 2px dashed #bfdbfe;
    border-radius: 20px;
    padding: 48px 32px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}
.upload-zone:hover {
    border-color: #0052cc;
    background: #f0f7ff;
}
.upload-icon { font-size: 56px; margin-bottom: 16px; line-height: 1; }
.upload-title { font-size: 20px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }
.upload-desc { font-size: 14px; color: #64748b; line-height: 1.6; margin-bottom: 20px; }
.upload-formats {
    display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 8px;
}
.format-badge {
    background: #eff6ff; color: #0052cc;
    font-size: 12px; font-weight: 600;
    padding: 5px 12px; border-radius: 100px;
    border: 1px solid #dbeafe;
}

/* ---- INFO CARDS ---- */
.info-card {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
    height: 100%;
}
.info-card:hover {
    border-color: #0052cc;
    box-shadow: 0 12px 32px rgba(0,82,204,0.1);
    transform: translateY(-3px);
}
.info-card-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; margin-bottom: 14px;
}
.info-card-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
.info-card-desc { font-size: 13px; color: #64748b; line-height: 1.6; }

/* ---- DATA PREVIEW ---- */
.preview-header {
    background: linear-gradient(135deg, #f0f7ff, #e8f4fd);
    border: 1.5px solid #bfdbfe;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 16px;
}
.preview-stat {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
    flex: 1;
}
.preview-stat-num { font-size: 26px; font-weight: 800; color: #0052cc; letter-spacing: -1px; }
.preview-stat-label { font-size: 12px; color: #94a3b8; margin-top: 2px; font-weight: 500; }

/* ---- COLUMN DETECTION ---- */
.col-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 100px;
    font-size: 12px; font-weight: 600; margin: 4px;
}
.col-badge-text { background: #dcfce7; color: #16a34a; border: 1px solid #bbf7d0; }
.col-badge-num { background: #fef3c7; color: #d97706; border: 1px solid #fde68a; }
.col-badge-other { background: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0; }
.col-badge-detected { background: #eff6ff; color: #0052cc; border: 1.5px solid #93c5fd; }

/* ---- ANALYSIS SELECTOR ---- */
.analysis-option {
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}
.analysis-option.selected {
    border-color: #0052cc;
    background: #eff6ff;
    box-shadow: 0 0 0 3px rgba(0,82,204,0.1);
}
.analysis-option:hover { border-color: #0052cc; transform: translateY(-2px); }
.analysis-option-icon { font-size: 32px; margin-bottom: 10px; }
.analysis-option-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
.analysis-option-desc { font-size: 12px; color: #64748b; }

/* ---- SUCCESS STATE ---- */
.success-banner {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    border: 1.5px solid #6ee7b7;
    border-radius: 16px;
    padding: 20px 24px;
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 24px;
}
.success-icon { font-size: 32px; }
.success-title { font-size: 16px; font-weight: 700; color: #065f46; margin-bottom: 2px; }
.success-desc { font-size: 13px; color: #047857; }

/* ---- REQUIREMENTS TABLE ---- */
.req-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f1f5f9;
    font-size: 14px; color: #374151;
}
.req-row:last-child { border-bottom: none; }
.req-check { color: #10b981; font-size: 16px; font-weight: 700; }
.req-cross { color: #ef4444; font-size: 16px; font-weight: 700; }

/* Streamlit overrides */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploader"] > div {
    background: white;
    border: 2px dashed #bfdbfe !important;
    border-radius: 16px !important;
    padding: 8px !important;
}
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1.5px solid #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ====================================================
# PAGE HEADER
# ====================================================
st.markdown("""
<div class="page-header">
    <div class="page-breadcrumb">🏠 Home &nbsp;/&nbsp; Upload Data</div>
    <div class="page-title">📤 Upload Your Dataset</div>
    <div class="page-subtitle">
        Drop in your customer feedback CSV and let our AI engine go to work. 
        Supports reviews, surveys, support tickets, and more.
    </div>
</div>
""", unsafe_allow_html=True)

# ====================================================
# HOW TO FORMAT — info cards
# ====================================================
st.markdown("""
<div class="section-header">
    <div class="section-label">Before You Start</div>
    <div class="section-title">What We Need From Your CSV</div>
</div>
""", unsafe_allow_html=True)

req_cols = st.columns(3)
reqs = [
    {"icon": "📝", "title": "Text / Review Column",
     "desc": "A column named 'review', 'text', 'feedback', or 'comment' containing the raw customer text."},
    {"icon": "📊", "title": "UTF-8 Encoding",
     "desc": "Save your CSV as UTF-8 to avoid encoding errors. Excel: Save As → CSV UTF-8."},
    {"icon": "📏", "title": "Min. 10 Rows",
     "desc": "For meaningful analysis, we recommend at least 50 rows. The more data, the richer the insights."},
]
for i, r in enumerate(reqs):
    with req_cols[i]:
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-icon">{r['icon']}</div>
            <div class="info-card-title">{r['title']}</div>
            <div class="info-card-desc">{r['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ====================================================
# FILE UPLOADER
# ====================================================
st.markdown("""
<div class="section-header">
    <div class="section-label">Step 1</div>
    <div class="section-title">Select Your File</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your CSV here or click to browse",
    type=["csv"],
    help="CSV files up to 200MB supported"
)

if not uploaded_file:
    st.markdown("""
    <div style="background:#fafbff;border:1.5px solid #e2e8f0;border-radius:16px;padding:24px;text-align:center;color:#94a3b8;">
        <div style="font-size:40px;margin-bottom:8px;">📂</div>
        <div style="font-size:14px;font-weight:500;">No file selected yet</div>
        <div style="font-size:13px;margin-top:4px;">Supported formats:</div>
        <div style="margin-top:10px;">
            <span class="format-badge">CSV</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================
# AFTER UPLOAD
# ====================================================
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, engine='python', on_bad_lines='skip')
        st.session_state["data"] = df

        # ---- SUCCESS BANNER ----
        st.markdown(f"""
        <div class="success-banner">
            <div class="success-icon">✅</div>
            <div>
                <div class="success-title">File uploaded successfully!</div>
                <div class="success-desc">{uploaded_file.name} · {len(df):,} rows · {len(df.columns)} columns · {uploaded_file.size / 1024:.1f} KB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ---- QUICK STATS ----
        stat_cols = st.columns(4)
        text_col_detected = next((c for c in df.columns if any(k in c.lower() for k in ["review","text","feedback","comment"])), None)
        null_pct = f"{df.isnull().mean().mean()*100:.1f}%"

        stats = [
            {"num": f"{len(df):,}", "label": "Total Rows"},
            {"num": str(len(df.columns)), "label": "Columns"},
            {"num": "✓ Found" if text_col_detected else "✗ None", "label": "Text Column"},
            {"num": null_pct, "label": "Missing Values"},
        ]
        for i, s in enumerate(stats):
            with stat_cols[i]:
                color = "#10b981" if "✓" in s["num"] else ("#ef4444" if "✗" in s["num"] else "#0052cc")
                st.markdown(f"""
                <div class="preview-stat">
                    <div class="preview-stat-num" style="color:{color}">{s['num']}</div>
                    <div class="preview-stat-label">{s['label']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- COLUMN ANALYSIS ----
        st.markdown("""
        <div class="section-header">
            <div class="section-label">Step 2</div>
            <div class="section-title">Column Detection</div>
        </div>
        """, unsafe_allow_html=True)

        col_html = ""
        for col in df.columns:
            dtype = df[col].dtype
            is_text_col = any(k in col.lower() for k in ["review","text","feedback","comment"])
            if is_text_col:
                col_html += f'<span class="col-badge col-badge-detected">🎯 {col}</span>'
            elif dtype == object:
                col_html += f'<span class="col-badge col-badge-text">📝 {col}</span>'
            elif dtype in ['int64','float64']:
                col_html += f'<span class="col-badge col-badge-num">🔢 {col}</span>'
            else:
                col_html += f'<span class="col-badge col-badge-other">📌 {col}</span>'

        st.markdown(f"""
        <div style="background:white;border:1.5px solid #e2e8f0;border-radius:16px;padding:20px 24px;">
            <div style="font-size:13px;color:#94a3b8;margin-bottom:12px;font-weight:500;">
                🎯 Blue = detected text column &nbsp; 📝 Green = text &nbsp; 🔢 Yellow = numeric
            </div>
            {col_html}
            {"<div style='margin-top:14px;padding-top:14px;border-top:1px solid #f1f5f9;font-size:13px;color:#10b981;font-weight:600;'>✅ Text column &quot;" + text_col_detected + "&quot; detected and ready for analysis.</div>" if text_col_detected else "<div style='margin-top:14px;padding-top:14px;border-top:1px solid #f1f5f9;font-size:13px;color:#f59e0b;font-weight:600;'>⚠️ No obvious text column found. Rename a column to &quot;review&quot; or &quot;text&quot;.</div>"}
        </div>
        """, unsafe_allow_html=True)

        # ---- DATA PREVIEW ----
        st.markdown("""
        <div class="section-header" style="margin-top:32px;">
            <div class="section-label">Step 3</div>
            <div class="section-title">Data Preview</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("👁️ Show first 10 rows", expanded=True):
            st.dataframe(df.head(10), use_container_width=True, height=300)

        # ---- ANALYSIS TYPE SELECTOR ----
        st.markdown("""
        <div class="section-header" style="margin-top:32px;">
            <div class="section-label">Step 4</div>
            <div class="section-title">Choose Analysis Type</div>
        </div>
        """, unsafe_allow_html=True)

        analysis_options = {
            "Dashboard": {"icon": "📊", "desc": "Visual charts & sentiment breakdown"},
            "Insights Report": {"icon": "📄", "desc": "Key findings & issue summary"},
            "Recommendation Report": {"icon": "💡", "desc": "AI-generated action items"},
        }

        if "analysis_type" not in st.session_state:
            st.session_state["analysis_type"] = "Dashboard"

        a_cols = st.columns(3)
        for i, (opt, meta) in enumerate(analysis_options.items()):
            with a_cols[i]:
                is_selected = st.session_state.get("analysis_type") == opt
                st.markdown(f"""
                <div class="analysis-option {'selected' if is_selected else ''}">
                    <div class="analysis-option-icon">{meta['icon']}</div>
                    <div class="analysis-option-title">{opt}</div>
                    <div class="analysis-option-desc">{meta['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {opt}", key=f"sel_{i}", use_container_width=True,
                             type="primary" if is_selected else "secondary"):
                    st.session_state["analysis_type"] = opt
                    st.rerun()

        # ---- CTA ----
        st.markdown("<br>", unsafe_allow_html=True)

        if text_col_detected:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#eff6ff,#dbeafe);border:1.5px solid #93c5fd;
                        border-radius:16px;padding:20px 24px;margin-bottom:20px;display:flex;align-items:center;gap:16px;">
                <div style="font-size:28px;">🚀</div>
                <div>
                    <div style="font-size:15px;font-weight:700;color:#1e40af;">Ready to analyze!</div>
                    <div style="font-size:13px;color:#3b82f6;margin-top:2px;">
                        {rows} rows will be processed · Analysis type: <strong>{atype}</strong>
                    </div>
                </div>
            </div>
            """.replace("{rows}", f"{len(df):,}").replace("{atype}", st.session_state.get("analysis_type","Dashboard")), unsafe_allow_html=True)

            go_col1, go_col2 = st.columns([1, 3])
            with go_col1:
                if st.button("📊 Run Analysis →", type="primary", use_container_width=True):
                    with st.spinner("Preparing your analysis..."):
                        import time; time.sleep(0.8)
                    st.success("✅ Data ready! Navigate to the **Results** page in the sidebar.")
        else:
            st.warning("⚠️ Please ensure your CSV has a column named 'review', 'text', 'feedback', or 'comment' before running analysis.")

    except Exception as e:
        st.markdown(f"""
        <div style="background:#fef2f2;border:1.5px solid #fca5a5;border-radius:16px;padding:20px 24px;">
            <div style="font-size:16px;font-weight:700;color:#991b1b;margin-bottom:4px;">❌ Error reading file</div>
            <div style="font-size:13px;color:#dc2626;">{str(e)}</div>
            <div style="font-size:13px;color:#7f1d1d;margin-top:8px;">Make sure your file is a valid UTF-8 CSV.</div>
        </div>
        """, unsafe_allow_html=True)

# ====================================================
# SIDEBAR
# ====================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <div style="font-size:22px;font-weight:900;color:#0052cc;letter-spacing:-1px;">AI CX Analytics</div>
        <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Intelligence for Every Interaction</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Navigation**")
    st.radio("Page", ["🏠 Home", "📤 Upload Data", "📊 Analysis Results", "⚙️ Settings"],
             index=1, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Upload Tips**")
    st.markdown("""
    <div style="background:#f0f4ff;border-radius:12px;padding:14px;font-size:13px;color:#374151;line-height:1.7;">
        ✅ Use UTF-8 encoding<br>
        ✅ Include a 'review' column<br>
        ✅ Remove duplicate rows<br>
        ✅ At least 50 rows recommended
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;color:#94a3b8;margin-top:48px;padding-top:24px;border-top:1.5px solid #e2e8f0;font-size:13px;">
    AI CX Analytics Platform · © {datetime.now().year}
</div>
""", unsafe_allow_html=True)