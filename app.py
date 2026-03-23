import html
from typing import Optional, Tuple
import folium
import ollama
import pandas as pd
import pdfplumber
import streamlit as st
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="WB College Market Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #dff3ef 0%, #edf8f6 55%, #f9fcfc 100%);
    }

    .block-container {
        max-width: 1380px;
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    html, body, p, div, span, label, li {
        color: #111111 !important;
    }

    h1, h2, h3, h4 {
        color: #111111 !important;
        font-weight: 800 !important;
    }

    .app-header {
        background: rgba(255,255,255,0.72);
        border: 1px solid #d8e6e2;
        border-radius: 22px;
        padding: 18px 22px;
        box-shadow: 0 10px 28px rgba(20, 40, 60, 0.06);
        margin-bottom: 18px;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 800;
        color: #111111 !important;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        font-size: 1rem;
        color: #2d2d2d !important;
    }

    .panel {
        background: rgba(255,255,255,0.96);
        border: 1px solid #d9e7e3;
        border-radius: 22px;
        padding: 18px 20px;
        box-shadow: 0 10px 26px rgba(20, 40, 60, 0.07);
        margin-bottom: 16px;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #111111 !important;
        margin-bottom: 0.25rem;
    }

    .section-note {
        font-size: 0.95rem;
        color: #333333 !important;
        margin-bottom: 0.8rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.98);
        border: 1px solid #d9e7e3;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 8px 22px rgba(20, 40, 60, 0.06);
        min-height: 116px;
    }

    .metric-label {
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #0a8b80 !important;
        margin-bottom: 0.45rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #111111 !important;
        line-height: 1.1;
    }

    .metric-sub {
        margin-top: 0.35rem;
        font-size: 0.95rem;
        color: #333333 !important;
    }

    .college-box {
        background: #ffffff;
        border: 1px solid #dbe7e4;
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 6px 16px rgba(20, 40, 60, 0.05);
    }

    .college-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #111111 !important;
        margin-bottom: 0.25rem;
    }

    .college-address {
        font-size: 0.95rem;
        color: #222222 !important;
        line-height: 1.4;
    }

    .result-box {
        background: #ffffff;
        border: 1px solid #dbe7e4;
        border-radius: 16px;
        padding: 16px;
        margin-top: 10px;
    }

    .stButton > button {
        width: 100%;
        background: #111111 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 18px rgba(0,0,0,0.16) !important;
    }

    .stButton > button:hover {
        background: #000000 !important;
        color: #ffffff !important;
    }

    .stButton > button * {
        color: #ffffff !important;
    }

    .stSelectbox label {
        color: #111111 !important;
        font-weight: 700 !important;
    }

    [data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #cfd8d5 !important;
        border-radius: 14px !important;
        min-height: 48px !important;
        box-shadow: none !important;
    }

    [data-baseweb="select"] input {
        color: #111111 !important;
        caret-color: #111111 !important;
    }

    [data-baseweb="select"] span {
        color: #111111 !important;
    }

    [data-baseweb="select"] svg {
        fill: #111111 !important;
    }

    div[data-baseweb="popover"] {
        z-index: 99999 !important;
    }

    div[data-baseweb="popover"] * {
        color: #111111 !important;
    }

    div[data-baseweb="popover"] ul {
        background: #ffffff !important;
        border: 1px solid #cfd8d5 !important;
        border-radius: 14px !important;
        box-shadow: 0 12px 28px rgba(20, 40, 60, 0.14) !important;
    }

    div[data-baseweb="popover"] li {
        background: #ffffff !important;
        color: #111111 !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="popover"] li:hover {
        background: #e7f6f2 !important;
        color: #111111 !important;
    }

    div[role="option"] {
        background: #ffffff !important;
        color: #111111 !important;
    }

    div[role="option"]:hover {
        background: #e7f6f2 !important;
        color: #111111 !important;
    }

    .stRadio label {
        color: #111111 !important;
        font-weight: 700 !important;
    }

    div[role="radiogroup"] > label {
        background: #ffffff;
        border: 1px solid #dbe7e4;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 8px;
        display: block;
    }

    div[role="radiogroup"] > label:hover {
        border-color: #0a8b80;
        box-shadow: 0 4px 12px rgba(10, 139, 128, 0.10);
    }

    [data-testid="stAlert"] {
        border-radius: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown("""
<div class="app-header">
    <div class="app-title">mobilAIze</div>
    <div class="app-subtitle">
        Powering Student Mobilisation through Intelligence
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
PDF_PATH = "wb_46_colleges.pdf"
OLLAMA_MODEL = "tinyllama"

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def safe_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()

def html_escape(value) -> str:
    return html.escape(safe_text(value))

@st.cache_resource
def get_geolocator():
    return Nominatim(user_agent="wb_college_market_app_clean")

def ask_ollama(prompt: str) -> str:
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return (
            "AI analysis could not be generated.\n\n"
            "Check these:\n"
            "1. Ollama is installed and running\n"
            f"2. Model '{OLLAMA_MODEL}' is installed\n"
            "3. If hosted in cloud, Ollama service may not be available there\n\n"
            f"Technical error: {e}"
        )

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data_from_pdf(pdf_path: str) -> pd.DataFrame:
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table and len(table) > 1:
                for row in table[1:]:
                    if not row or len(row) < 4:
                        continue

                    college = safe_text(row[0])
                    address = safe_text(row[1])
                    district = safe_text(row[2])
                    pin = safe_text(row[3])

                    if college and address and district and pin:
                        rows.append({
                            "College": college,
                            "Address": address,
                            "District": district,
                            "PIN": pin
                        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    return df.dropna().drop_duplicates().reset_index(drop=True)

@st.cache_data(show_spinner=False)
def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    geolocator = get_geolocator()
    query = f"{address}, West Bengal, India"
    try:
        loc = geolocator.geocode(query, timeout=10)
        if loc:
            return (loc.latitude, loc.longitude)
    except (GeocoderTimedOut, GeocoderServiceError):
        return None
    except Exception:
        return None
    return None

def run_market_analysis(pin: str, district: str, colleges: list[str]) -> str:
    prompt = f"""
You are a professional market analyst.

Analyze the business potential of this location based on student presence.

Location Details:
PIN Code: {pin}
District: {district}
Nearby Colleges: {", ".join(colleges)}

Provide analysis in this format:
1. Student Population Potential
2. Business Opportunities (hostel, PG, coaching, food, stationery, transport, etc.)
3. Market Demand Level (Low/Medium/High with reason)
4. Startup Ideas (practical suggestions)

Keep it simple, practical, and structured.
"""
    return ask_ollama(prompt)

def run_industry_analysis(pin: str, district: str, colleges: list[str]) -> str:
    prompt = f"""
You are a local industrial and business opportunity analyst.

Analyze the local industrial/company potential of this location in West Bengal.

Location Details:
PIN Code: {pin}
District: {district}
Nearby Colleges: {", ".join(colleges)}

Give a practical structured response in this format:
1. Possible Local Industry Presence
2. Types of Companies/Factories/Business Segments that may grow here
3. Employment & Internship Potential for Students
4. Supply/Service Business Opportunities
5. Overall Industrial Potential (Low/Medium/High with reason)

Important:
- Keep it practical and realistic
- Focus on local business, SME, factory, service sector, warehouse, logistics, training center, IT support, manufacturing support, food processing, retail distribution, healthcare support, education support, and transport-related opportunities
- Write in simple language
"""
    return ask_ollama(prompt)

# ---------------------------------------------------
# MAIN LOAD
# ---------------------------------------------------
try:
    df = load_data_from_pdf(PDF_PATH)
except FileNotFoundError:
    st.error("PDF file not found. Keep 'wb_46_colleges.pdf' in the same folder as app.py.")
    st.stop()
except Exception as e:
    st.error(f"Failed to load PDF data: {e}")
    st.stop()

if df.empty:
    st.error("No data found in the PDF.")
    st.stop()

# ---------------------------------------------------
# FILTER BAR
# ---------------------------------------------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
f1, f2 = st.columns([1.1, 2.6])

with f1:
    pin_options = sorted(df["PIN"].astype(str).unique().tolist())
    selected_pin = st.selectbox("Select PIN Code", pin_options, index=0)

with f2:
    st.markdown(
        """
        <div style="padding-top: 33px; font-size: 0.98rem; color: #222;">
            Choose a PIN code to view matching colleges, map location, and AI-based market analysis.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

filtered = df[df["PIN"].astype(str) == str(selected_pin)].reset_index(drop=True)

if filtered.empty:
    st.warning("No colleges found for the selected PIN code.")
    st.stop()

district = safe_text(filtered.iloc[0]["District"])
college_count = len(filtered)

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">District</div>
        <div class="metric-value">{html_escape(district)}</div>
        <div class="metric-sub">Selected area district</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">PIN Code</div>
        <div class="metric-value">{html_escape(selected_pin)}</div>
        <div class="metric-sub">Active market location</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Colleges Found</div>
        <div class="metric-value">{college_count}</div>
        <div class="metric-sub">Institutions in this PIN</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------
# COLLEGE + MAP
# ---------------------------------------------------
left_col, right_col = st.columns([1, 1], gap="large")

college_options = filtered["College"].tolist()

with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎓 Colleges</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-note">Select a college to view its address and map location.</div>',
        unsafe_allow_html=True
    )

    selected_college = st.radio(
        "Choose College",
        options=college_options,
        label_visibility="collapsed"
    )

    selected_row = filtered[filtered["College"] == selected_college].iloc[0]

    st.markdown(f"""
    <div class="college-box">
        <div class="college-name">{html_escape(selected_row['College'])}</div>
        <div class="college-address">📍 {html_escape(selected_row['Address'])}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗺️ College Map</div>', unsafe_allow_html=True)

    coords = geocode_address(safe_text(selected_row["Address"]))

    if coords:
        lat, lon = coords
        fmap = folium.Map(location=[lat, lon], zoom_start=15, control_scale=True)
        folium.Marker(
            [lat, lon],
            popup=safe_text(selected_row["College"]),
            tooltip=safe_text(selected_row["College"])
        ).add_to(fmap)
        st_folium(fmap, width=None, height=430)
    else:
        st.warning("Map location could not be found for this address.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# MARKET ANALYSIS
# ---------------------------------------------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Market Analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Generate PIN-wise business and student market analysis using TinyLlama.</div>',
    unsafe_allow_html=True
)

all_college_names = filtered["College"].tolist()

if st.button("Run Market Analysis"):
    with st.spinner("Generating market analysis..."):
        analysis_result = run_market_analysis(selected_pin, district, all_college_names)
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("#### Analysis Result")
        st.write(analysis_result)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# INDUSTRIAL ANALYSIS
# ---------------------------------------------------
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏭 Local Industrial / Company Analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Generate a practical industrial and company opportunity analysis for this PIN using TinyLlama.</div>',
    unsafe_allow_html=True
)

if st.button("Run Local Industrial Analysis"):
    with st.spinner("Generating local industrial/company analysis..."):
        industry_result = run_industry_analysis(selected_pin, district, all_college_names)
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("#### Industrial / Company Analysis Result")
        st.write(industry_result)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)