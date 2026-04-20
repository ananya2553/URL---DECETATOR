import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import google.generativeai as genai
from extractor import get_url_features

# --- 1. CONFIG & ENGINES ---
GEMINI_API_KEY = "AIzaSyC9keackc8bHaqP8uX0P41oJCCokzdYcTM" # Apni key yahan dalo

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

@st.cache_resource
def load_local_engine():
    return joblib.load('phish_model.pkl')

model = load_local_engine()

# --- 2. ADVANCED UI STYLING (The "Interesting" Look) ---
st.set_page_config(page_title="Forensic Dashboard", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050a14; color: #00ffcc; }
    .main-title { font-size: 45px; font-weight: 800; color: #ff00ff; text-align: center; text-shadow: 0 0 15px #ff00ff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #ff00ff, #00ffff); 
        color: black; font-weight: bold; border-radius: 10px; border: none; 
    }
    .metric-container { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 15px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DIALOG COMPONENT ---
@st.dialog("🛡️ NEURAL-SYNC FORENSIC REPORT")
def show_alert(v, s, r):
    if s > 50:
        st.error(f"## 🚨 STATUS: {v.upper()}")
    else:
        st.success(f"## ✅ STATUS: {v.upper()}")
    st.markdown(f"**Threat Index:** `{s}/100` \n\n **Forensic Reason:** {r}")
    if st.button("Close"): st.rerun()

# --- 4. HEADER ---
st.markdown("<h1 class='main-title'>⚡ PHISH-TANK: COGNITIVE DEFENSE</h1>", unsafe_allow_html=True)
st.divider()

# --- 5. INTERFACE & LOGIC ---
url_input = st.text_input("🌐 Target URL Inspection Node:", placeholder="Enter URL to scan...")
execute_btn = st.button("EXECUTE NEURAL SCAN")

# Initialize variables to avoid NameError
verdict, score, reason = None, 0, ""

if execute_btn and url_input:
    with st.status("⚡ Synchronizing Neural Nodes...", expanded=True) as status:
        # Step A: Local Model
        features = get_url_features(url_input)
        local_pred = model.predict(pd.DataFrame([features]))[0]
        
        # Fallback Logic
        if local_pred != 'benign':
            verdict, score = "Malicious", 85
            reason = "Behavioral Shield: Structural anomalies detected in URL."
        else:
            verdict, score = "Safe", 15
            reason = "Behavioral Shield: URL appears legitimate."

        # Step B: Gemini AI
        try:
            prompt = f"Analyze URL: {url_input}. Verdict|Score|Reason"
            response = gemini_model.generate_content(prompt)
            if response and response.text:
                parts = response.text.split('|')
                verdict = parts[0].strip()
                score = int([s_val for s_val in parts[1].split() if s_val.isdigit()][0])
                reason = parts[2].strip()
        except:
            reason += " (Cognitive Link Offline - Local Engine Active)"
        
        status.update(label="Scan Complete!", state="complete", expanded=False)

    # Trigger Popup
    show_alert(verdict, score, reason)

    # --- 6. VISUAL TELEMETRY DASHBOARD ---
    st.markdown("## 🛰️ Visual Telemetry Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.write("### 📊 Threat Probability")
        fig_pie = px.pie(values=[score, 100-score], names=['Threat', 'Safe'], hole=0.7, 
                         color_discrete_sequence=['#ff00ff', '#00ffcc'])
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.write("### 📉 Risk Velocity Index")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=score, 
                             gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#ff00ff"}}))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)