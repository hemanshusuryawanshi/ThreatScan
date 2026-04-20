import streamlit as st
import pandas as pd
import joblib
from feature_extraction import extract_features
import urllib.parse
import os

# --- Configuration ---
st.set_page_config(
    page_title="ThreatScan — URL Intelligence",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=Share+Tech+Mono&display=swap');

/* Page background */
.stApp { 
    background-color: #080C10;
    background-image: radial-gradient(circle at 50% 0%, rgba(0,212,255,0.05) 0%, transparent 60%);
}

.stApp::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 100vh;
    background: linear-gradient(180deg, rgba(0,212,255,0.04) 0%, transparent 40%);
    pointer-events: none;
    z-index: 0;
}

/* Main content block */
section.main > div { background-color: transparent; position: relative; z-index: 1; }

/* Text input */
.stTextInput > div > div > input {
    background-color: #0D1420;
    border: 1px solid #1E3A5F;
    color: #E8EDF5;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 16px;
    border-radius: 6px;
}
.stTextInput > div > div > input:focus {
    border-color: #00D4FF;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.2);
}
.stTextInput label p {
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6B8099 !important;
    font-size: 12px !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00B4D8, #00D4FF) !important;
    color: #080C10 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 16px !important;
    transition: all 0.2s ease !important;
    box-shadow: none;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 24px rgba(0,212,255,0.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="primary"]:active {
    transform: scale(0.98) !important;
}

/* Expander */
.st-emotion-cache-1vzxiuh, div[data-testid="stExpander"] {
    background-color: transparent !important;
    border: none !important;
}
div[data-testid="stExpander"] details {
    background-color: #0D1420;
    border: 1px solid #1A2535;
    border-radius: 6px;
    color: #E8EDF5;
}
div[data-testid="stExpander"] details summary p {
    font-family: 'Share Tech Mono', monospace !important;
    color: #00D4FF !important;
    font-size: 1.1rem;
}

/* Spinner text */
.stSpinner > div > div > div > p, .stSpinner > div > p, .stSpinner > div > span, div[data-testid="stSpinner"] {
    color: #00D4FF !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px;
    font-weight: bold;
    animation: blink 1.5s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
div[data-testid="stSpinner"] i {
    border-color: #00D4FF !important;
    border-top-color: transparent !important;
}

/* Hide default Streamlit branding */
#MainMenu, header, footer { visibility: hidden; }

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #080C10; }
::-webkit-scrollbar-thumb { background: #00D4FF; border-radius: 3px; }

/* Base text */
p, span, div { font-family: 'IBM Plex Mono', monospace; }

/* Header layout */
.hero-header { text-align: center; margin-bottom: 2rem; }
.hero-icon { font-size: 3rem; display: inline-block; animation: pulse 2s infinite; margin-bottom: 0.5rem; }
@keyframes pulse {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.05); opacity: 1; filter: drop-shadow(0 0 10px rgba(0,212,255,0.6)); }
    100% { transform: scale(0.95); opacity: 0.8; }
}
.hero-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2.5rem;
    color: #E8EDF5;
    margin: 0;
    letter-spacing: 2px;
}
.hero-subtitle { color: #6B8099; font-size: 1rem; margin-top: 0.5rem; }
.hero-divider { height: 1px; background: rgba(0,212,255,0.3); border: none; margin: 1.5rem auto; width: 80%; }
.cursor { animation: blinkCursor 1s step-end infinite; }
@keyframes blinkCursor { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* Stats Cards */
.stats-container { display: flex; justify-content: space-between; gap: 1rem; margin-bottom: 2rem; }
.stat-card {
    background: #0D1420;
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 4px;
    padding: 1rem;
    flex: 1;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.stat-card .icon { font-size: 1.5rem; margin-bottom: 0.5rem; display: block; }
.stat-card .label { color: #E8EDF5; font-size: 0.9rem; font-weight: 500; font-family: 'Share Tech Mono', monospace; }
.stat-card .desc { color: #6B8099; font-size: 0.75rem; margin-top: 0.3rem; }

/* Result Blocks */
.result-block { padding: 1.5rem; border-radius: 6px; margin: 2rem 0; font-family: 'JetBrains Mono', monospace; }
.result-safe {
    background: rgba(0, 230, 118, 0.05);
    border: 1px solid rgba(0, 230, 118, 0.4);
    border-left: 4px solid #00E676;
    box-shadow: 0 0 30px rgba(0,230,118,0.1);
}
.result-malicious {
    background: rgba(255, 61, 87, 0.05);
    border: 1px solid rgba(255,61,87,0.4);
    border-left: 4px solid #FF3D57;
    box-shadow: 0 0 30px rgba(255,61,87,0.12);
}
.result-title { font-size: 1.25rem; font-weight: bold; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 10px; }
.safe-text { color: #00E676; }
.malicious-text { color: #FF3D57; }
.result-desc { color: #E8EDF5; margin-bottom: 1rem; font-size: 0.95rem; }

/* Alert Animation */
.alert-icon { animation: blinkAlert 0.8s infinite alternate; }
@keyframes blinkAlert { from { opacity: 0.5; color: #FF3D57; text-shadow: none; } to { opacity: 1; color: #ff6b80; text-shadow: 0 0 10px #FF3D57; } }

/* Confidence Bar */
.confidence-wrapper { background: rgba(0,0,0,0.3); border-radius: 4px; padding: 1rem; border: 1px solid rgba(255,255,255,0.05); }
.confidence-label { display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-size: 0.85rem; color: #6B8099; }
.confidence-track { height: 8px; background: #080C10; border-radius: 4px; overflow: hidden; position: relative; }
.confidence-fill { height: 100%; border-radius: 4px; animation: fillBar 1.5s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; width: 0%; box-shadow: 0 0 10px var(--fill-color); background: var(--fill-color); }
@keyframes fillBar { to { width: var(--fill-width); } }

/* Features Table */
.feature-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; margin-bottom: 0.5rem; }
.feature-table th { text-align: left; color: #00D4FF; border-bottom: 1px solid rgba(0,212,255,0.2); padding: 0.8rem 0.5rem 0.5rem; font-family: 'Share Tech Mono', monospace; font-weight: normal; background: rgba(0,212,255,0.05); }
.feature-table td { padding: 0.6rem 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #E8EDF5; }
.feature-table tr:last-child td { border-bottom: none; }
.feature-name { color: #6B8099; text-transform: uppercase; font-size: 0.8rem; }
.badge { padding: 2px 6px; border-radius: 3px; font-size: 0.75rem; font-weight: bold; }
.badge-yes { background: rgba(255, 61, 87, 0.15); color: #FF3D57; border: 1px solid rgba(255, 61, 87, 0.3); }
.badge-no { background: rgba(255, 255, 255, 0.05); color: #6B8099; border: 1px solid rgba(255,255,255,0.1); }
.val-number { color: #00D4FF; }

/* Custom Footer */
.custom-footer { text-align: center; margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid rgba(0,212,255,0.2); color: #6B8099; font-size: 0.75rem; font-family: 'IBM Plex Mono', monospace; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
<div class="hero-header">
    <div class="hero-icon">🛡️</div>
    <h1 class="hero-title">ThreatScan</h1>
    <div class="hero-subtitle">URL Intelligence & Threat Detection<span class="cursor">|</span></div>
    <hr class="hero-divider">
    <div style="color: #6B8099; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace;">Powered by Machine Learning &nbsp;|&nbsp; v1.0</div>
</div>
""", unsafe_allow_html=True)

# --- Stats Bar ---
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <span class="icon">🔍</span>
        <div class="label">URLs Scanned</div>
        <div class="desc">Real-time</div>
    </div>
    <div class="stat-card">
        <span class="icon">☠️</span>
        <div class="label">Threats Detected</div>
        <div class="desc">ML-Powered</div>
    </div>
    <div class="stat-card">
        <span class="icon">⚡</span>
        <div class="label">Features Analyzed</div>
        <div class="desc">27 Signals</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Load Model ---
@st.cache_resource
def load_model():
    if os.path.exists('malicious_url_model.pkl'):
        return joblib.load('malicious_url_model.pkl')
    return None

model = load_model()

if not model:
    st.error("⚠️ Model file 'malicious_url_model.pkl' not found. Please run 'train_model.py' first.")
    st.stop()

# --- Input Area ---
url_input = st.text_input("ENTER TARGET URL", placeholder="https://example.com or http://suspicious-login.tk")
st.markdown("<div style='font-size: 12px; color: #6B8099; margin-top: -10px; margin-bottom: 20px;'>Supports HTTP and HTTPS. Scheme auto-added if missing.</div>", unsafe_allow_html=True)

if st.button("⚡ SCAN URL", type="primary", use_container_width=True):
    if not url_input.strip():
        st.markdown("""
        <div class="result-block result-malicious" style="padding: 1rem;">
           <div class="result-title"><span class="alert-icon">⚠</span> INPUT ERROR</div>
           <div class="result-desc">Please enter a valid URL to proceed.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("SCANNING... EXTRACTING FEATURES..."):
            # Ensure URL has scheme for accurate parsing
            if not url_input.startswith("http://") and not url_input.startswith("https://"):
                url_to_process = "http://" + url_input
            else:
                url_to_process = url_input
                
            # Extract features
            features = extract_features(url_to_process)
            
            # Predict
            features_df = pd.DataFrame([features])
            prediction = model.predict(features_df)[0]
            probability = model.predict_proba(features_df)[0]
            
            # Display Result
            if prediction == 1:
                confidence = probability[1] * 100
                st.markdown(f"""
                <div class="result-block result-malicious">
                    <div class="result-title malicious-text"><span class="alert-icon">🚨</span> VERDICT: MALICIOUS</div>
                    <div class="result-desc">WARNING — Phishing or Malware Detected</div>
                    <div class="hero-divider" style="margin: 1rem 0; width: 100%; background: rgba(255,61,87,0.3);"></div>
                    <div class="confidence-wrapper">
                        <div class="confidence-label">
                            <span>Threat Confidence</span>
                            <span style="color: #FF3D57; font-weight: bold;">{confidence:.2f}%</span>
                        </div>
                        <div class="confidence-track">
                            <div class="confidence-fill" style="--fill-width: {confidence}%; --fill-color: #FF3D57;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                confidence = probability[0] * 100
                st.markdown(f"""
                <div class="result-block result-safe">
                    <div class="result-title safe-text">✅ VERDICT: BENIGN</div>
                    <div class="result-desc">This URL appears to be safe.</div>
                    <div class="hero-divider" style="margin: 1rem 0; width: 100%; background: rgba(0,230,118,0.3);"></div>
                    <div class="confidence-wrapper">
                        <div class="confidence-label">
                            <span>Confidence Score</span>
                            <span style="color: #00E676; font-weight: bold;">{confidence:.2f}%</span>
                        </div>
                        <div class="confidence-track">
                            <div class="confidence-fill" style="--fill-width: {confidence}%; --fill-color: #00E676;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Detail Metrics
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("[ EXTRACTED SIGNAL FEATURES ]"):
                html_str = "<table class='feature-table'>"
                
                categories = {
                    "URL Structure": ["url_length", "hostname_length", "path_length"],
                    "Risk Indicators": ["is_ip_address", "uses_shortener", "is_http"],
                    "Suspicious Keywords": ["has_word_login", "has_word_verify", "has_word_secure", "has_word_account", "has_word_update"]
                }
                
                categorized_keys = set()
                for cat, keys in categories.items():
                    cat_keys = [k for k in keys if k in features]
                    if cat_keys:
                        html_str += f"<tr><th colspan='2'>[ {cat.upper()} ]</th></tr>"
                        for k in cat_keys:
                            categorized_keys.add(k)
                            val = features[k]
                            if isinstance(val, bool) or (isinstance(val, (int, float)) and val in [0, 1] and k.startswith(('is_', 'has_', 'uses_'))):
                                badge_class = "badge-yes" if val else "badge-no"
                                display_val = "YES" if val else "NO"
                                html_str += f"<tr><td class='feature-name'>{k.replace('_', ' ')}</td><td><span class='badge {badge_class}'>{display_val}</span></td></tr>"
                            else:
                                html_str += f"<tr><td class='feature-name'>{k.replace('_', ' ')}</td><td class='val-number'>{val}</td></tr>"
                
                # Remaining Features (Character Analysis etc)
                remaining_keys = [k for k in features.keys() if k not in categorized_keys]
                if remaining_keys:
                    html_str += f"<tr><th colspan='2'>[ CHARACTER ANALYSIS / EXTRAS ]</th></tr>"
                    for k in remaining_keys:
                        val = features[k]
                        if isinstance(val, bool) or (isinstance(val, (int, float)) and val in [0, 1] and k.startswith(('is_', 'has_', 'uses_'))):
                            badge_class = "badge-yes" if val else "badge-no"
                            display_val = "YES" if val else "NO"
                            html_str += f"<tr><td class='feature-name'>{k.replace('_', ' ')}</td><td><span class='badge {badge_class}'>{display_val}</span></td></tr>"
                        else:
                            html_str += f"<tr><td class='feature-name'>{k.replace('_', ' ')}</td><td class='val-number'>{val}</td></tr>"
                            
                html_str += "</table>"
                st.markdown(html_str, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div class="custom-footer">
    ThreatScan v1.0 &nbsp;|&nbsp; ML-Powered &nbsp;|&nbsp; Built with Streamlit<br>
    <span style="color: rgba(107,128,153,0.7); font-size: 0.65rem;">⚠ For educational use. Not a replacement for professional security tools.</span>
</div>
""", unsafe_allow_html=True)

