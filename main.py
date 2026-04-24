import html
import streamlit as st
import pandas as pd
import pdfplumber
from data_extractor import extract

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG & CSS
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Financial Data Extractor", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        padding-bottom: 20px;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000000; font-weight: bold; font-size: 18px; border-radius: 8px; border: none; padding: 10px 24px; width: 100%; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover { transform: translateY(-2px); box-shadow: 0px 8px 20px rgba(0, 201, 255, 0.35); }
    .stTextArea textarea { background-color: #1A1C23; color: #00C9FF; border: 1px solid #333; border-radius: 10px; font-size: 16px; }
    
    /* Metrics table */
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { background-color: #1A1C23 !important; color: #92FE9D !important; font-size: 16px; text-align: center !important; padding: 12px; border-bottom: 2px solid #00C9FF; }
    td { background-color: #0E1117 !important; color: #FFFFFF !important; font-size: 15px; text-align: center !important; padding: 12px; border-bottom: 1px solid #2a2d35; }
    
    /* Bifurcation table */
    .bif-table { width: 100%; border-collapse: collapse; margin-top: 12px; font-family: sans-serif; }
    .bif-th { background-color: #92FE9D; color: #000000; font-weight: bold; padding: 12px 14px; text-align: left; }
    .bif-td { padding: 11px 14px; color: #FFFFFF; font-size: 14px; border-bottom: 1px solid #2a2d35; }
    .bif-row-even { background-color: #0E1117; }
    .bif-row-odd  { background-color: #1A1C23; }
    .bif-total { background-color: #1e2028; font-weight: bold; color: #00C9FF; padding: 11px 14px; font-size: 14px; border-top: 2px solid #92FE9D; }
    .prog-bg  { background-color: #2a2d35; border-radius: 4px; height: 8px; width: 100%; margin-top: 5px; }
    .prog-fill { background: linear-gradient(90deg, #00C9FF, #92FE9D); border-radius: 4px; height: 8px; }

    /* Source quote & Banners */
    .source-box { background-color: #121212; border-left: 5px solid #00C9FF; padding: 16px 20px; border-radius: 8px; font-style: italic; color: #D0D0D0; font-size: 15px; line-height: 1.8; margin-top: 10px; }
    .quality-ok   { color: #92FE9D; font-weight: bold; font-size: 15px; }
    .quality-warn { color: #FFC107; font-weight: bold; font-size: 15px; }
    
    /* Upload Box Styling */
    [data-testid="stFileUploadDropzone"] {
        background-color: #1A1C23;
        border: 2px dashed #00C9FF;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════
def parse_to_float(val_str):
    if not val_str or val_str in ("N/A", ""): return None
    try:
        cleaned = val_str.replace("$", "").replace(",", "").strip()
        if cleaned.upper().endswith("B"): return float(cleaned[:-1]) * 1_000_000_000
        elif cleaned.upper().endswith("M"): return float(cleaned[:-1]) * 1_000_000
        return float(cleaned)
    except ValueError:
        return None

def format_billions(value):
    if value >= 1_000_000_000: return f"${value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000: return f"${value / 1_000_000:.1f}M"
    return f"${value:.2f}"

def beat_miss_delta(actual_str, expected_str):
    actual = parse_to_float(actual_str)
    expected = parse_to_float(expected_str)
    if actual is None or expected is None or expected == 0: return "", None
    
    diff = actual - expected
    pct  = (diff / expected) * 100
    badge = "✅ BEAT" if diff >= 0 else "❌ MISS"
    
    if abs(diff) >= 1_000_000_000: diff_str = f"{'+' if diff >= 0 else ''}{diff / 1_000_000_000:.2f}B"
    elif abs(diff) >= 1_000_000: diff_str = f"{'+' if diff >= 0 else ''}{diff / 1_000_000:.1f}M"
    else: diff_str = f"{'+' if diff >= 0 else ''}{diff:.2f}"
    
    return badge, f"${diff_str} ({pct:+.1f}%)"

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

@st.cache_data(show_spinner=False)
def cached_extract(text: str):
    return extract(text)

# ═══════════════════════════════════════════════════════════════
# RENDER BIFURCATION TABLE
# ═══════════════════════════════════════════════════════════════
def render_bifurcation(segments):
    if not segments: return
    st.markdown("---")
    st.markdown("### 🧩 Revenue Bifurcation — Segment Breakdown")
    rows_html, total_value, total_pct = "", 0.0, 0.0

    for i, seg in enumerate(segments):
        row_class = "bif-row-even" if i % 2 == 0 else "bif-row-odd"
        segment = html.escape(seg.get("segment", "—"))
        revenue = html.escape(seg.get("revenue",  "—"))
        pct_str = seg.get("percentage", "N/A")

        rev_float = parse_to_float(revenue)
        if rev_float: total_value += rev_float

        try:
            pct_float = float(pct_str.replace("%", "").strip())
            total_pct += pct_float
            progress_html = f"<div style='display:flex; align-items:center; gap:10px;'><span style='min-width:42px;'>{html.escape(pct_str)}</span><div class='prog-bg'><div class='prog-fill' style='width:{min(pct_float,100):.1f}%'></div></div></div>"
        except:
            progress_html = "<span style='color:#888'>N/A</span>"

        rows_html += f"<tr class='{row_class}'><td class='bif-td'>{segment}</td><td class='bif-td' style='text-align:right; font-weight:bold'>{revenue}</td><td class='bif-td'>{progress_html}</td></tr>"

    total_display = format_billions(total_value) if total_value else "N/A"
    pct_display = f"{total_pct:.1f}%" if total_pct > 0 else "N/A"

    table_html = f"""<table class='bif-table'><thead><tr><th class='bif-th'>Segment</th><th class='bif-th' style='text-align:right'>Revenue</th><th class='bif-th'>Share %</th></tr></thead><tbody>{rows_html}<tr><td class='bif-total'>TOTAL</td><td class='bif-total' style='text-align:right'>{total_display}</td><td class='bif-total'>{pct_display}</td></tr></tbody></table>"""
    st.markdown(table_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# MAIN DISPLAY
# ═══════════════════════════════════════════════════════════════
def display_results(data: dict):
    # Data Quality
    checks = {k: data.get(k) not in (None, "N/A", "") for k in ["revenue_actual", "revenue_expected", "eps_actual", "eps_expected", "source_quote"]}
    if data.get("revenue_yoy_growth") is not None: checks["revenue_yoy_growth"] = True
    if data.get("bifurcation"): checks["bifurcation"] = True
    
    missing = [k for k, ok in checks.items() if not ok]
    if not missing: st.markdown('<div class="quality-ok">✅ All fields extracted successfully</div>', unsafe_allow_html=True)
    else: st.markdown(f'<div class="quality-warn">⚠️ Partial extraction — {len(missing)} field(s) missing</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📈 Beat / Miss Analysis")
    col1, col2, col3 = st.columns(3)

    rev_badge, rev_delta = beat_miss_delta(data.get("revenue_actual", "N/A"), data.get("revenue_expected", "N/A"))
    eps_badge, eps_delta = beat_miss_delta(data.get("eps_actual", "N/A"), data.get("eps_expected", "N/A"))

    col1.metric(f"Revenue ({rev_badge})" if rev_badge else "Revenue", data.get("revenue_actual", "N/A"), delta=rev_delta)
    col2.metric(f"EPS ({eps_badge})" if eps_badge else "EPS", data.get("eps_actual", "N/A"), delta=eps_delta)

    yoy = data.get("revenue_yoy_growth")
    if yoy is not None: col3.metric("Revenue YoY Growth", f"{'+' if yoy >= 0 else ''}{yoy:.1f}%", delta="vs Prior Year")
    else: col3.metric("Revenue YoY Growth", "N/A", delta="Not mentioned")

    st.markdown("---")
    st.markdown("### 📊 Extracted Metrics")
    df = pd.DataFrame({"Measure": ["Revenue", "EPS"], "Estimated": [data.get("revenue_expected", "N/A"), data.get("eps_expected", "N/A")], "Actual": [data.get("revenue_actual", "N/A"), data.get("eps_actual", "N/A")]})
    st.dataframe(df.set_index("Measure"), use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Metrics as CSV", data=csv_bytes, file_name="financial_metrics.csv", mime="text/csv")

    render_bifurcation(data.get("bifurcation", []))

    source = data.get("source_quote", "N/A")
    if source and source != "N/A":
        st.markdown("---")
        st.markdown("### 🔍 AI Source Evidence")
        st.markdown(f'<div class="source-box">"{html.escape(source)}"</div>', unsafe_allow_html=True)
        with st.expander("📋 Click to copy source quote"): st.code(source, language="")

# ═══════════════════════════════════════════════════════════════
# APP ENTRY
# ═══════════════════════════════════════════════════════════════
st.title("Financial Data Extractor")

# Create Tabs for the UI
tab1, tab2 = st.tabs(["✍️ Paste Text", "📄 Upload PDF"])

# TAB 1: PASTE TEXT
with tab1:
    text_input = st.text_area("Analyze Financial Report Text:", height=180, placeholder="Paste an earnings press release here...")

    if st.button("Extract Data ⚡", key="text_btn"):
        if text_input.strip():
            with st.spinner("AI is analyzing the report..."):
                try:
                    extracted_data = cached_extract(text_input)
                    display_results(extracted_data)
                except Exception as e:
                    st.error("⚠️ Extraction failed. The AI could not parse this text.")
        else:
            st.warning("⚠️ Please paste a financial paragraph first.")

# TAB 2: UPLOAD PDF
with tab2:
    st.info("Upload an official earnings report or press release in PDF format.")
    uploaded_file = st.file_uploader("Drag and drop your PDF here", type=["pdf"])
    
    if st.button("Extract Data from PDF ⚡", key="pdf_btn"):
        if uploaded_file:
            with st.spinner(f"Reading {uploaded_file.name} and analyzing data..."):
                try:
                    # 1. Read PDF
                    raw_text = extract_text_from_pdf(uploaded_file)
                    
                    # 2. Check if text was actually found
                    if not raw_text.strip():
                        st.error("⚠️ Could not read any text from this PDF. It might be a scanned image.")
                    else:
                        # 3. Pass to the AI extractor
                        extracted_data = cached_extract(raw_text)
                        display_results(extracted_data)
                        
                except Exception as e:
                    st.error("⚠️ Extraction failed. The AI could not parse this document.")
        else:
            st.warning("⚠️ Please upload a PDF file first.")
