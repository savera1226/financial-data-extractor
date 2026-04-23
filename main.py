import streamlit as st
import pandas as pd
from data_extractor import extract
# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="AI Financial Extractor", page_icon="📊", layout="centered")

# 2. Injecting Custom CSS for a "Stunning" Look
st.markdown("""
    <style>
    /* Dark professional background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }

    /* Make the Title pop with a gradient color */
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        padding-bottom: 20px;
    }

    /* Style the Text Area box */
    .stTextArea textarea {
        background-color: #1A1C23;
        color: #00C9FF;
        border: 1px solid #333;
        border-radius: 10px;
        font-size: 16px;
    }

    /* Stunning Gradient Button with Hover Effect */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #000000;
        font-weight: bold;
        font-size: 18px;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 15px rgba(0, 201, 255, 0.3);
    }

    /* Clean, professional table styling */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    th {
        background-color: #1A1C23 !important;
        color: #92FE9D !important;
        font-size: 18px;
        text-align: center !important;
        padding: 12px;
        border-bottom: 2px solid #00C9FF;
    }
    td {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
        font-size: 16px;
        text-align: center !important;
        padding: 12px;
        border-bottom: 1px solid #333;
    }
    tr:hover td {
        background-color: #1A1C23 !important;
        transition: 0.2s;
    }
    /* Professional Insight Box */
    .insight-box {
        background-color: #1A1C23;
        border-left: 5px solid #92FE9D; /* Mint Green accent */
        padding: 20px;
        border-radius: 10px;
        color: #FFFFFF;
        font-size: 16px;
        line-height: 1.6;
    }
    .insight-title {
        color: #00C9FF; /* Cyan title */
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)




# 4. App UI Elements
st.title("Financial Data Extraction")

text_input = st.text_area("Analyze Financial Report:", height=150,
                          placeholder="Paste your Q3 earnings paragraph here...")

if st.button("Extract Data ⚡"):
    if text_input:
        with st.spinner('AI is analyzing the text...'):
            # Call the function
            extracted_data = extract(text_input)

            # Map the JSON data using .get() for safety in case a key is missing
            data = {
                "Measure": ["Revenue", "EPS"],
                "Estimated": [extracted_data.get('revenue_expected', 'N/A'), extracted_data.get('eps_expected', 'N/A')],
                "Actual": [extracted_data.get('revenue_actual', 'N/A'), extracted_data.get('eps_actual', 'N/A')]
            }

            df = pd.DataFrame(data)

            # Display the styled table
            # Display the Styled Table
            st.markdown("### 📊 Extracted Metrics")
            st.dataframe(df, use_container_width=True)

            # NEW: Professional Bifurcation Display
            bifurcation_insight = extracted_data.get('bifurcation', 'N/A')
            if bifurcation_insight != 'N/A':
                st.markdown("---")
                # Using custom HTML for the "Stunning" look
                st.markdown(f"""
                                <div class="insight-box">
                                    <div class="insight-title">🧩 Financial Bifurcation (Revenue Split)</div>
                                    {bifurcation_insight}
                                </div>
                            """, unsafe_allow_html=True)
