import streamlit as st
import sys
import re
from contextlib import contextmanager

def load_css(theme_color, bg_color):
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg_color}; }}
        
        /* Header */
        .header-container {{
            padding: 1.5rem;
            background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            border-left: 4px solid {theme_color};
            display: flex; align-items: center; justify-content: space-between;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }}
        .header-title {{ font-size: 1.5rem; font-weight: 800; color: #FFF; margin: 0; letter-spacing: 1px; }}
        .header-sub {{ font-size: 0.8rem; color: #888; margin: 0; font-family: monospace; text-transform: uppercase; }}
        .user-badge {{ 
            background: {theme_color}22; color: {theme_color}; 
            padding: 6px 16px; border-radius: 30px; font-weight: 600; font-size: 0.9rem;
            border: 1px solid {theme_color}44;
        }}
        
        /* Butonlar */
        div.stButton > button:first-child {{ 
            border-color: rgba(255,255,255,0.1); color: #EEE; 
            background: rgba(255,255,255,0.02); border-radius: 8px; 
        }}
        div.stButton > button:first-child:hover {{ 
            border-color: {theme_color}; color: white; background: {theme_color}22; 
        }}
        
        /* Login Kartı */
        .login-container {{
            background: linear-gradient(180deg, rgba(30,30,30,0.8) 0%, rgba(20,20,20,0.9) 100%);
            padding: 3rem; border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            max-width: 420px; margin: 0 auto; text-align: center;
        }}
        .login-logo {{ font-size: 4rem; margin-bottom: 10px; filter: drop-shadow(0 0 10px {theme_color}66); }}
        
        /* Üye Vitrini */
        .team-showcase {{
            display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;
            padding: 20px; margin-bottom: 40px;
        }}
        .team-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 10px; width: 90px; text-align: center;
            transition: all 0.3s ease;
        }}
        .team-card:hover {{
            transform: translateY(-5px);
            background: {theme_color}11;
            border-color: {theme_color};
            box-shadow: 0 0 15px {theme_color}33;
        }}
        .team-avatar {{ font-size: 2rem; margin-bottom: 5px; }}
        .team-name {{ font-size: 0.7rem; color: #CCC; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

        .stChatMessage {{ background-color: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 12px !important; }}
        .stCodeBlock {{ border: 1px solid {theme_color}33 !important; background: #050505 !important; }}
        .mugendai-footer {{ margin-top: 60px; text-align: center; color: #555; font-size: 10px; font-family: monospace; letter-spacing: 2px; text-transform: uppercase; }}
    </style>
    """, unsafe_allow_html=True)

class StreamlitOutputStream:
    def __init__(self, c):
        self.c = c
        self.ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    def write(self, d): 
        if "terminal_logs" in st.session_state:
            st.session_state.terminal_logs += self.ansi.sub('', d)
            self.c.code(st.session_state.terminal_logs, language="yaml")
    def flush(self):
        pass

@contextmanager
def capture_output(c): 
    new = StreamlitOutputStream(c)
    old = sys.stdout
    sys.stdout = new
    try:
        yield
    finally:
        sys.stdout = old