import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai
import json
import base64
import os
import time
from extractor import get_url_features

# --- 1. CORE ENGINE CONFIGURATION ---
GEMINI_API_KEY = "" 
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-flash-latest')

@st.cache_resource
def load_neural_core():
    return joblib.load('phish_model.pkl')

model = load_neural_core()

# Helper for Image Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

BG_IMAGE_PATH = r"C:\Users\anany\.gemini\antigravity\brain\312db8a1-560e-4a1a-b360-5d606edadaaf\neural_scan_background_1776714503412.png"
bg_base64 = get_base64_image(BG_IMAGE_PATH)

# Session State for Scan sequencing
if 'scan_phase' not in st.session_state:
    st.session_state.scan_phase = "IDLE"
if 'scan_result' not in st.session_state:
    st.session_state.scan_result = None

# --- 2. PREMIUM ENTERPRISE CSS ---
st.set_page_config(page_title="Sentinel Blue | Neural-Sync Engine", page_icon="🛡️", layout="wide")

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* COMPLETE HEADER OVERRIDE */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0) !important;
    }}
    header {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    #MainMenu {{ visibility: hidden; }}

    /* Global Viewport: Total Crimson-Black Immersion */
    .stApp {{
        background: linear-gradient(180deg, #4d0f1a 0%, #1a0a0d 100%) !important;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Split Layout Containers */
    .main .block-container {{
        padding-top: 1rem;
        max-width: 95%;
        margin: 0 auto;
    }}

    /* Global Branding Header */
    .branding-bar {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 60px;
    }}
    .brand-title {{ font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 28px; margin: 0; letter-spacing: 1px; }}
    .brand-sub {{ color: #ccc; font-size: 14px; margin: 0; text-transform: uppercase; letter-spacing: 3px; font-weight: 300; }}

    /* Hero Text & Inputs (Left) */
    .hero-title {{ font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 52px; line-height: 1.1; margin-bottom: 15px; }}
    .hero-tagline {{ color: #bbb; font-size: 20px; margin-bottom: 40px; font-weight: 300; }}

    /* Laptop Visualizer (Right) */
    .laptop-container {{ position: relative; width: 100%; max-width: 750px; margin: 0 auto; }}
    .laptop-frame {{
        width: 100%;
        aspect-ratio: 16/10;
        background: #111;
        border-radius: 25px;
        padding: 12px;
        position: relative;
        box-shadow: 0 40px 100px rgba(0,0,0,0.9);
        border: 1px solid #333;
    }}
    .laptop-screen {{
        width: 100%;
        height: 100%;
        background: url('data:image/png;base64,{bg_base64}') center/cover no-repeat;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        transition: filter 0.8s ease;
    }}
    .is-scanning .laptop-screen {{
        filter: blur(8px);
    }}

    /* Address Bar Overlay */
    .address-bar-overlay {{
        background: #ff3344;
        width: 80%;
        height: 30px;
        margin: 15px auto;
        border-radius: 15px;
        display: flex;
        align-items: center;
        padding: 0 15px;
        gap: 10px;
        color: white;
        font-size: 11px;
        z-index: 10;
        box-shadow: 0 4px 15px rgba(255,0,0,0.3);
    }}

    /* Execute Button: GLOWING CYAN */
    .stButton>button {{
        background: linear-gradient(90deg, #0cebeb 0%, #20e3b2 100%);
        color: #000;
        font-weight: 700 !important;
        font-family: 'Montserrat', sans-serif !important;
        padding: 14px 40px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 20px;
        box-shadow: 0 0 20px rgba(12, 235, 235, 0.4);
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .stButton>button:hover {{
        transform: scale(1.05) translateY(-3px);
        box-shadow: 0 0 35px rgba(12, 235, 235, 0.8);
    }}

    /* Floating Result Card (Glassmorphism) */
    .floating-result {{
        position: absolute;
        right: -60px;
        top: 80px;
        width: 320px;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        z-index: 100;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        animation: slideIn 0.6s cubic-bezier(0.19, 1, 0.22, 1);
    }}
    @keyframes slideIn {{
        from {{ transform: translateX(50px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}

    /* Pulsing Status Text */
    .status-pulse {{
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        letter-spacing: 2px;
        color: #0cebeb;
        animation: pulseFade 2s infinite ease-in-out;
    }}
    @keyframes pulseFade {{
        0%, 100% {{ opacity: 0.3; }}
        50% {{ opacity: 1; }}
    }}

    .shield-icon {{ width: 24px; height: 24px; margin-bottom: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- 3. TOP BRANDING BAR ---
st.markdown("""
<div class='branding-bar'>
    <div class='brand-left'>
        <p class='brand-title'>Sentinel Blue</p>
        <p class='brand-sub'>Neural-Sync Engine</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. ENGINE CORE LAYOUT ---
col_left, col_space, col_right = st.columns([1, 0.1, 1.2])

with col_left:
    st.markdown("<h1 class='hero-title'>URL Phishing Defense</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-tagline'>Neutralize new threats instantly with Hybrid AI reasoning.</p>", unsafe_allow_html=True)
    
    url_input = st.text_input("Address", placeholder="https://suspicious-node.xyz/verify", label_visibility="collapsed")
    
    if st.button("EXECUTE SCAN"):
        st.session_state.scan_phase = "SCANNING"
        st.rerun()

with col_right:
    # State-based styling class
    laptop_class = "is-scanning" if st.session_state.scan_phase == "SCANNING" else ""
    
    st.markdown(f"""
    <div class='laptop-container {laptop_class}'>
        <div class='laptop-frame'>
            <div class='laptop-screen'>
                <div class='address-bar-overlay'>
                    <span>🔒</span>
                    <span>https://[Target Inspection Active]</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Render Floating Result Overlay if available
    if st.session_state.scan_phase == "RESULT" and st.session_state.scan_result:
        res = st.session_state.scan_result
        res_verdict = res['verdict'].lower()
        color = "#00ff88" if res_verdict in ["safe", "benign"] else "#ff3344"
        shield_svg = f'<svg class="shield-icon" viewBox="0 0 24 24" fill="{color}"><path d="M12 2L3 7V12C3 17.5 6.8 22.3 12 24C17.2 22.3 21 17.5 21 12V7L12 2ZM12 22C8.3 20.6 5 16.5 5 12V8.4L12 4.5L19 8.4V12C19 16.5 15.7 20.6 12 22Z"/></svg>'
        
        st.markdown(f"""
        <div class='floating-result'>
            {shield_svg}
            <p style='color: #888; font-size: 10px; text-transform: uppercase; margin-bottom: 5px;'>System Verdict</p>
            <h3 style='color: {color}; margin-top: 0; font-family: Montserrat;'>{res['verdict'].upper()}</h3>
            <div style='height: 1px; background: rgba(255,255,255,0.1); margin: 15px 0;'></div>
            <p style='color: #888; font-size: 10px; text-transform: uppercase; margin-bottom: 5px;'>AI Insight</p>
            <p style='font-size: 13px; line-height: 1.5; color: #eee;'>{res['reasoning']}</p>
            <p style='font-size: 11px; color: {color}; margin-top: 15px; font-weight: 700;'>CONFIDENCE: {res['confidence']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. SCANNING & STATUS LOGIC ---
if st.session_state.scan_phase == "SCANNING":
    with st.empty():
        # Perform logical scan
        features = get_url_features(url_input)
        f_df = pd.DataFrame([features])
        ml_pred = model.predict(f_df)[0]
        ml_proba = round(model.predict_proba(f_df)[0].max() * 100, 1)
        
        try:
            prompt = f"Analyze URL intent: {url_input}. Verdict: <Safe/Malicious> | Confidence: <%> | Reasoning: <brief>"
            ai_res = gemini_model.generate_content(prompt)
            import re
            txt = ai_res.text
            v_match = re.search(r"Verdict:\s*(\w+)", txt, re.I)
            c_match = re.search(r"Confidence:\s*(\d+)", txt, re.I)
            r_match = re.search(r"Reasoning:\s*(.*)", txt, re.I)
            
            st.session_state.scan_result = {
                "verdict": v_match.group(1) if v_match else ml_pred,
                "confidence": int(c_match.group(1)) if c_match else ml_proba,
                "reasoning": r_match.group(1) if r_match else f"Pattern matches {ml_pred} profile."
            }
        except Exception as e:
             st.sidebar.error(f"AI Sync Error: {str(e)}")
             st.session_state.scan_result = {"verdict": ml_pred, "confidence": ml_proba, "reasoning": "AI Link Offline. Local Engine Active."}
        
        # Simulate scanning time for visuals
        time.sleep(2) 
        st.session_state.scan_phase = "RESULT"
        st.rerun()

# --- 6. FOOTER / STATUS BAR ---
bottom_status = "SYSTEM IDLE | STANDBY" if st.session_state.scan_phase == "IDLE" else "ENGINE ACTIVE: ANALYZING NEURAL PATTERNS..."
status_class = "status-pulse" if st.session_state.scan_phase == "SCANNING" else ""

st.markdown(f"""
<div style='position: fixed; bottom: 30px; left: 50%; translate: -50%;'>
    <p class='{status_class}' style='margin: 0; opacity: 0.5;'>{bottom_status}</p>
</div>
""", unsafe_allow_html=True)
