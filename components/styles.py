from __future__ import annotations

import streamlit as st

def inject_styles() -> None:
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=Barlow:wght@400;500;600;700;800&family=Barlow+Condensed:wght@600;700;800&display=swap');

:root {{
    --navy: #000568;
    --navy-2: #1b237e;
    --orange: #ff5722;
    --text: #1b1b21;
    --muted: #464652;
    --outline: #767683;
    --outline-var: #c6c5d4;
    --surface: #fbf8ff;
    --surface-low: #f5f2fb;
    --surface-container: #efecf5;
    --surface-lowest: #ffffff;
    --line: #e4e1ea;
    --sidebar: #f7f8fa;
    --input-bg: #ffffff;
    --bubble-assistant-bg: #ffffff;
    --bubble-assistant-border: rgba(198,197,212,.7);
    --bubble-user-bg: #eef1ff;
    --bubble-user-border: rgba(0,5,104,.08);
    --bubble-user-text: var(--text);
    --dock-bg: rgba(255,255,255,.88);
    --dock-border: rgba(198,197,212,.72);
}}

/* ── DARK THEME ── activated by the .theme-dark-marker sentinel emitted in app.py */
body:has(.theme-dark-marker) {{
    --text: #e8e8ee;
    --muted: #a8a8b3;
    --outline: #9a9aa6;
    --outline-var: #3a3a45;
    --surface: #0e0e14;
    --surface-low: #16161e;
    --surface-container: #1d1d27;
    --surface-lowest: #1a1a23;
    --line: #2a2a35;
    --sidebar: #13131a;
    --input-bg: #1a1a23;
    --bubble-assistant-bg: #1d1d27;
    --bubble-assistant-border: #2a2a35;
    --bubble-user-bg: #1b237e;
    --bubble-user-border: rgba(255,255,255,.08);
    --bubble-user-text: #ffffff;
    --dock-bg: rgba(26,26,35,.88);
    --dock-border: #2a2a35;
}}
/* Route hard-coded surfaces through the new variables so dark mode picks them up */
body:has(.theme-dark-marker) .stTextInput [data-baseweb="base-input"],
body:has(.theme-dark-marker) .stTextInput [data-baseweb="base-input"] > div {{
    background: var(--input-bg) !important;
    color: var(--text) !important;
}}
body:has(.theme-dark-marker) .stTextInput input,
body:has(.theme-dark-marker) .stTextInput textarea {{
    color: var(--text) !important;
    background: transparent !important;
}}
body:has(.theme-dark-marker) .msg-bubble {{
    background: var(--bubble-assistant-bg) !important;
    border-color: var(--bubble-assistant-border) !important;
    color: var(--text) !important;
}}
body:has(.theme-dark-marker) .user-msg .msg-bubble {{
    background: var(--bubble-user-bg) !important;
    border-color: var(--bubble-user-border) !important;
    color: var(--bubble-user-text) !important;
}}
body:has(.theme-dark-marker) .st-key-chat_dock_inner,
body:has(.theme-dark-marker) .st-key-chat_dock_empty_inner {{
    background: var(--dock-bg) !important;
    border-color: var(--dock-border) !important;
}}
body:has(.theme-dark-marker) .placeholder-card {{
    background: var(--surface-lowest) !important;
    border-color: var(--line) !important;
}}
body:has(.theme-dark-marker) .flash-error {{
    background: #2a1418 !important;
    border-color: #5a2a30 !important;
    color: #fda4af !important;
}}
body:has(.theme-dark-marker) .flash-success {{
    background: #14241c !important;
    border-color: #2a4a3a !important;
    color: #86efac !important;
}}
/* Toggle button styling: subtle pill that adapts to the active theme.
   Specificity raised with .st-key-top_nav prefix so it beats the generic
   .st-key-top_nav .stButton > button[kind="secondary"] rule defined later. */
.st-key-top_nav .st-key-nav_theme_toggle .stButton > button {{
    background: var(--surface-lowest) !important;
    color: var(--text) !important;
    border: 1px solid var(--line) !important;
    border-radius: 999px !important;
    height: 2.5rem !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
    padding: 0 .9rem !important;
    box-shadow: none !important;
}}
.st-key-top_nav .st-key-nav_theme_toggle .stButton > button:hover {{
    border-color: var(--outline) !important;
}}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    font-family: 'Inter', sans-serif;
    color: var(--text);
    background: var(--surface) !important;
}}

#MainMenu, header, footer, [data-testid="stDecoration"] {{ visibility: hidden; display: none; }}

[data-testid="stMainBlockContainer"] {{
    max-width: 100% !important;
    padding: 0 !important;
}}

[data-testid="stMarkdownContainer"] p {{ margin-bottom: 0; }}

/* ── LANDING PAGE ── */
body:has(.landing-page-bg),
[data-testid="stAppViewContainer"]:has(.landing-page-bg),
[data-testid="stMain"]:has(.landing-page-bg) {{
    background: #070c14 !important;
    overflow-x: hidden !important;
}}
[data-testid="stMainBlockContainer"]:has(.landing-page-bg) {{
    padding: 0 !important;
    max-width: 100% !important;
    min-height: 100vh !important;
    background:
        radial-gradient(circle at 76% 36%, rgba(30,64,175,.20), transparent 34rem),
        linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px),
        linear-gradient(180deg, rgba(255,255,255,.035) 1px, transparent 1px),
        #070c14 !important;
    background-size: auto, 4.75rem 4.75rem, 4.75rem 4.75rem, auto !important;
}}
.landing-page-bg {{
    position: fixed;
    inset: 0;
    z-index: -1;
    background:
        linear-gradient(180deg, rgba(6,20,19,.96) 0, rgba(6,20,19,.96) 4.85rem, transparent 4.85rem),
        radial-gradient(circle at 72% 35%, rgba(30,64,175,.18), transparent 26rem),
        #070c14;
    pointer-events: none;
}}
.st-key-landing_nav {{
    height: 4.85rem !important;
    padding: .72rem max(2rem, calc((100vw - 72rem) / 2)) !important;
    border-bottom: 1px solid rgba(169,190,255,.08) !important;
    background: rgba(5,18,17,.96) !important;
    box-sizing: border-box !important;
}}
.st-key-landing_nav > div[data-testid="stVerticalBlock"] {{
    height: 100% !important;
    display: flex !important;
    justify-content: center !important;
}}
.st-key-landing_nav div[data-testid="stHorizontalBlock"] {{
    align-items: center !important;
}}
.landing-brand {{
    display: flex;
    align-items: center;
    gap: .55rem;
    color: #ecf3ff;
    font-family: 'Lexend', sans-serif;
    font-weight: 800;
    font-size: .98rem;
    letter-spacing: 0;
}}
.landing-brand-mark {{
    width: 1.55rem;
    height: 1.55rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: .55rem;
    background: #1d4ed8;
    color: #fff;
    font-size: .88rem;
    box-shadow: 0 0 22px rgba(29,78,216,.28);
}}
.landing-links {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2.15rem;
    color: #7888a3;
    font-size: .82rem;
    font-weight: 600;
}}
.landing-route-link {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    text-decoration: none !important;
    line-height: 1;
    box-sizing: border-box;
}}
.landing-login-link,
.st-key-landing_login_btn .stButton > button {{
    height: 2.55rem !important;
    padding: 0 .6rem !important;
    border: none !important;
    background: transparent !important;
    color: #8592aa !important;
    box-shadow: none !important;
    font-size: .82rem !important;
    font-weight: 700 !important;
}}
.landing-start-link,
.landing-primary-link,
.st-key-landing_start_btn .stButton > button,
.st-key-landing_primary_cta .stButton > button {{
    height: 2.75rem !important;
    min-height: 2.75rem !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 999px !important;
    background: #1d4ed8 !important;
    color: #fff !important;
    box-shadow: 0 18px 38px rgba(29,78,216,.24) !important;
    font-size: .84rem !important;
    font-weight: 800 !important;
    letter-spacing: 0 !important;
}}
.landing-secondary-link,
.st-key-landing_secondary_cta .stButton > button {{
    height: 2.75rem !important;
    min-height: 2.75rem !important;
    border: 1px solid rgba(177,198,255,.22) !important;
    border-radius: 999px !important;
    background: rgba(7,12,20,.74) !important;
    color: #f5f8ff !important;
    box-shadow: none !important;
    font-size: .84rem !important;
    font-weight: 800 !important;
}}
.landing-start-link:hover,
.landing-primary-link:hover,
.st-key-landing_start_btn .stButton > button:hover,
.st-key-landing_primary_cta .stButton > button:hover {{
    background: #2563eb !important;
}}
.landing-secondary-link:hover,
.landing-login-link:hover,
.st-key-landing_secondary_cta .stButton > button:hover,
.st-key-landing_login_btn .stButton > button:hover {{
    color: #fff !important;
    border-color: rgba(177,198,255,.34) !important;
}}
.st-key-landing_hero {{
    max-width: 72rem !important;
    margin: 0 auto !important;
    padding: 5.05rem 2rem 4rem !important;
    min-height: calc(100vh - 4.85rem) !important;
    box-sizing: border-box !important;
}}
.st-key-landing_hero > div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {{
    align-items: center !important;
}}
.landing-copy {{
    padding-top: .55rem;
}}
.landing-kicker {{
    display: flex;
    align-items: center;
    gap: .55rem;
    color: #7897d6;
    font-family: 'Barlow', sans-serif;
    text-transform: uppercase;
    letter-spacing: .28em;
    font-size: .64rem;
    font-weight: 700;
    margin-bottom: 1.8rem;
}}
.landing-kicker span {{
    width: .32rem;
    height: .32rem;
    border-radius: 50%;
    background: #1d4ed8;
    box-shadow: 0 0 12px rgba(37,99,235,.72);
}}
.landing-copy h1 {{
    margin: 0;
    color: #f2f6ff;
    font-family: 'Lexend', sans-serif;
    font-size: 4.8rem;
    line-height: 1.08;
    font-weight: 500;
    letter-spacing: 0;
}}
.landing-copy h1 em {{
    color: #2f6fdd;
    font-style: normal;
}}
.landing-copy p {{
    width: min(35rem, 100%);
    margin: 1.55rem 0 1.75rem;
    color: #9eb4de;
    font-size: 1.02rem;
    line-height: 1.62;
}}
.landing-stats {{
    display: flex;
    align-items: flex-start;
    gap: 2.5rem;
    margin-top: 1.6rem;
}}
.landing-stats div {{
    display: flex;
    flex-direction: column;
    gap: .28rem;
}}
.landing-stats strong {{
    color: #fff;
    font-size: 1rem;
    font-weight: 900;
}}
.landing-stats span {{
    color: #8fa8d9;
    font-family: 'Barlow', sans-serif;
    font-size: .7rem;
    letter-spacing: .09em;
}}
.landing-visual {{
    position: relative;
    min-height: 24rem;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.plan-card {{
    width: min(31rem, 100%);
    min-height: 21rem;
    padding: 1.65rem 1.65rem 1.35rem;
    border-radius: 1.25rem;
    background:
        radial-gradient(circle at 50% 0%, rgba(30,64,175,.18), transparent 15rem),
        rgba(15,25,50,.92);
    border: 1px solid rgba(153,179,237,.26);
    box-shadow: 0 28px 80px rgba(0,0,0,.36), inset 0 1px 0 rgba(255,255,255,.05);
    box-sizing: border-box;
}}
.plan-card-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #7994cf;
    font-family: 'Barlow', sans-serif;
    text-transform: uppercase;
    letter-spacing: .16em;
    font-size: .66rem;
    font-weight: 800;
}}
.plan-card-top span {{
    color: #6ee0bf;
    background: rgba(40,155,150,.18);
    border-radius: 999px;
    padding: .24rem .55rem;
    letter-spacing: .04em;
    text-transform: none;
}}
.plan-metric {{
    display: flex;
    align-items: baseline;
    gap: .42rem;
    margin: 1.3rem 0 .85rem;
}}
.plan-metric strong {{
    color: #fff;
    font-size: 2.1rem;
    line-height: 1;
    font-family: 'Lexend', sans-serif;
    font-weight: 600;
}}
.plan-metric span {{
    color: #96acd8;
    font-size: .78rem;
    font-weight: 700;
}}
.plan-metric em {{
    margin-left: auto;
    color: #2f6fdd;
    font-style: normal;
    font-family: 'Barlow', sans-serif;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .08em;
}}
.plan-chart {{
    height: 7.6rem;
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: .52rem;
    align-items: end;
    border-bottom: 1px dashed rgba(143,168,217,.24);
}}
.plan-chart div {{
    position: relative;
    height: 100%;
    display: flex;
    align-items: end;
    justify-content: center;
    background: rgba(62,84,142,.42);
    border-radius: .34rem .34rem 0 0;
}}
.plan-chart i {{
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    display: block;
    border-radius: .34rem .34rem 0 0;
    background: linear-gradient(180deg, #2f6fdd, #1e40af);
}}
.plan-chart span {{
    position: absolute;
    bottom: -1.2rem;
    color: #58719e;
    font-family: 'Barlow', sans-serif;
    text-transform: uppercase;
    font-size: .58rem;
    letter-spacing: .16em;
}}
.plan-divider {{
    height: 1px;
    margin: 1.75rem 0 1.35rem;
    background: linear-gradient(90deg, transparent, rgba(139,166,224,.2), transparent);
}}
.plan-card-bottom {{
    display: flex;
    justify-content: space-between;
    color: #92a9d4;
    font-family: 'Barlow', sans-serif;
    font-size: .68rem;
    letter-spacing: .08em;
}}
.plan-card-bottom strong {{
    color: #fff;
}}
.plan-toast {{
    position: absolute;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: .48rem;
    height: 1.75rem;
    padding: 0 .78rem;
    border-radius: .45rem;
    color: #fff;
    font-family: 'Barlow', sans-serif;
    font-size: .7rem;
    font-weight: 800;
    letter-spacing: .05em;
    background: rgba(11,23,46,.92);
    border: 1px solid rgba(132,163,225,.28);
    box-shadow: 0 10px 26px rgba(0,0,0,.28);
}}
.plan-toast span {{
    width: .42rem;
    height: .42rem;
    border-radius: 50%;
    background: #1d4ed8;
    box-shadow: 0 0 12px rgba(37,99,235,.72);
}}
.plan-toast-top {{
    top: 3.2rem;
    right: 3.7rem;
}}
.plan-toast-left {{
    left: 1.15rem;
    top: 15rem;
}}

@media (max-width: 980px) {{
    .st-key-landing_nav {{
        height: auto !important;
        padding: .85rem 1.15rem !important;
    }}
    .landing-links {{
        display: none;
    }}
    .st-key-landing_hero {{
        padding: 3rem 1.2rem 3rem !important;
        min-height: auto !important;
    }}
    .st-key-landing_hero > div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {{
        flex-direction: column !important;
        gap: 2.4rem !important;
    }}
    .landing-copy h1 {{
        font-size: 3.4rem;
    }}
    .landing-copy p {{
        font-size: .98rem;
    }}
    .landing-stats {{
        gap: 1.5rem;
        flex-wrap: wrap;
    }}
    .landing-visual {{
        width: 100%;
        min-height: 22rem;
    }}
    .plan-toast-top {{
        right: 1rem;
    }}
    .plan-toast-left {{
        left: 0;
    }}
}}

@media (max-width: 620px) {{
    .landing-brand {{
        font-size: .9rem;
    }}
    .st-key-landing_nav div[data-testid="column"]:has(.st-key-landing_login_btn) {{
        display: none !important;
    }}
    .landing-copy h1 {{
        font-size: 2.72rem;
    }}
    .landing-kicker {{
        font-size: .58rem;
        letter-spacing: .2em;
        margin-bottom: 1.3rem;
    }}
    .plan-card {{
        padding: 1.15rem 1rem;
        min-height: 19rem;
    }}
    .plan-metric {{
        flex-wrap: wrap;
    }}
    .plan-metric em {{
        width: 100%;
        margin-left: 0;
    }}
    .plan-toast {{
        display: none;
    }}
    .plan-card-bottom {{
        flex-direction: column;
        gap: .55rem;
    }}
}}

/* ── GLOBAL INPUT ── */
.stTextInput label, .stTextInput div[data-testid="stWidgetLabel"] {{ display: none !important; }}
.stTextInput [data-baseweb="base-input"] {{
    border: 1.5px solid rgba(118,118,131,.28) !important;
    border-radius: 8px !important;
    background: #fff !important;
    box-shadow: 0 2px 10px rgba(0,5,104,.03) !important;
    overflow: hidden !important;
    min-height: 3.5rem !important;
}}
.stTextInput [data-baseweb="base-input"]:hover {{
    border-color: rgba(0,5,104,.24) !important;
}}
.stTextInput [data-baseweb="base-input"]:focus-within {{
    border-color: var(--navy) !important;
    box-shadow: 0 0 0 4px rgba(0,5,104,.08) !important;
}}
.stTextInput [data-baseweb="base-input"] > div {{ background: #fff !important; }}
.stTextInput [data-baseweb="base-input"] button {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 2.5rem !important;
    min-width: 2.5rem !important;
    height: 2.5rem !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    color: #687086 !important;
}}
.stTextInput [data-baseweb="base-input"] button:hover {{
    color: var(--navy) !important;
    background: transparent !important;
}}
.stTextInput [data-baseweb="base-input"] svg {{
    display: block !important;
    width: 1.08rem !important;
    height: 1.08rem !important;
    fill: currentColor !important;
}}
.stTextInput [data-baseweb="base-input"] > div:not(:first-child) {{
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    background: transparent !important;
    overflow: hidden !important;
}}
.stTextInput [data-baseweb="base-input"] > div:first-child {{ width: 100% !important; flex: 1 1 auto !important; display: flex !important; align-items: center !important; }}
.stTextInput [data-baseweb="base-input"] > div:last-child,
.stTextInput [data-baseweb="base-input"] > div:last-child * {{
    background: transparent !important;
}}
.stTextInput input[type="password"]::-ms-reveal,
.stTextInput input[type="password"]::-ms-clear {{ display: none !important; }}
.stTextInput input[type="password"]::-webkit-credentials-auto-fill-button,
.stTextInput input[type="password"]::-webkit-contacts-auto-fill-button {{
    visibility: hidden !important;
    display: none !important;
    pointer-events: none !important;
}}
.stTextInput input {{
    height: 3.5rem !important;
    border: none !important;
    border-radius: 0 !important;
    background: #fff !important;
    color: var(--text) !important;
    caret-color: var(--navy) !important;
    box-shadow: none !important;
    padding: 0 1.15rem !important;
    font-size: 1.02rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    line-height: 3.5rem !important;
    -webkit-appearance: none !important;
    appearance: none !important;
}}
.stTextInput input::placeholder {{ color: #9e9eae !important; opacity: .95 !important; transition: opacity .15s ease !important; }}
.stTextInput input:focus::placeholder {{ opacity: .55 !important; }}

div[data-testid="stForm"] {{ border: none !important; padding: 0 !important; background: transparent !important; }}
div[data-testid="stForm"] > div {{ border: none !important; padding: 0 !important; background: transparent !important; }}

.stButton > button, .stFormSubmitButton > button {{
    font-family: 'Lexend', sans-serif !important;
    font-weight: 800 !important;
    box-shadow: none !important;
    transition: opacity .15s ease !important;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
    opacity: 0.9 !important;
    transform: none !important;
}}

/* ── NAVBAR ── */
.st-key-top_nav {{
    padding: 1rem 3.5rem !important;
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(255,255,255,.85);
    backdrop-filter: blur(18px);
    border-bottom: 1px solid var(--line);
}}
.st-key-top_nav [data-testid="stHorizontalBlock"] {{ align-items: center; }}
.st-key-top_nav .stButton > button {{
    height: 2.8rem !important;
    border-radius: 4px !important;
    border: none !important;
    font-size: 0.92rem !important;
    padding: 0 1.3rem !important;
    min-height: unset !important;
}}
.st-key-top_nav .stButton > button[kind="secondary"] {{
    background: transparent !important;
    color: var(--navy) !important;
    box-shadow: none !important;
}}
.st-key-top_nav .stButton > button[kind="primary"] {{
    background: var(--orange) !important;
    color: #fff !important;
    box-shadow: 0 8px 24px rgba(255,87,34,.25) !important;
}}
.st-key-nav_links [data-testid="stHorizontalBlock"] {{
    justify-content: center;
    gap: 1.5rem !important;
}}
.st-key-nav_links .stButton > button {{
    height: 2.2rem !important;
    min-height: 2.2rem !important;
    padding: 0 .1rem !important;
    border: none !important;
    border-radius: 0 !important;
    background: transparent !important;
    color: var(--text) !important;
    box-shadow: none !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}}
.st-key-nav_links .stButton > button[kind="primary"] {{
    background: transparent !important;
    color: var(--text) !important;
    font-weight: 500 !important;
    border-bottom: 3px solid var(--orange) !important;
    box-shadow: none !important;
}}
.st-key-nav_links .stButton > button[kind="secondary"] {{
    color: var(--text) !important;
}}

/* ── LOGIN PAGE ── */
.st-key-login_shell {{
    padding: 3rem 5rem 2rem !important;
    min-height: calc(100vh - 80px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: var(--surface);
}}
.login-heading {{
    font-family: 'Lexend', sans-serif;
    font-size: 3.2rem;
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.05em;
    color: var(--navy);
    margin-bottom: 1rem;
}}
.login-sub {{
    font-size: 1rem;
    font-weight: 500;
    color: var(--muted);
    margin-bottom: 2rem;
}}
.login-sub a {{ color: var(--orange); font-weight: 700; text-decoration: none; }}
.field-label {{
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--outline);
    margin-bottom: 6px;
}}
.password-meta {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}}
.forgot-link {{ font-size: 0.88rem; font-weight: 700; color: rgba(0,5,104,.72); }}
.st-key-login_shell .stFormSubmitButton > button {{
    height: 4rem !important;
    border-radius: 6px !important;
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%) !important;
    color: #fff !important;
    border: none !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 32px rgba(0,5,104,.15) !important;
    margin-top: 4px !important;
}}
.alt-divider {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.8rem 0 1.2rem;
    color: var(--outline);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}}
.alt-divider::before, .alt-divider::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(198,197,212,.55);
}}
.alt-buttons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
.alt-btn {{
    display: flex;
    align-items: center;
    justify-content: center;
    height: 3rem;
    border: 2px solid rgba(198,197,212,.35);
    border-radius: 6px;
    font-family: 'Inter', sans-serif;
    font-size: 0.96rem;
    font-weight: 700;
    color: var(--text);
    background: #fff;
}}
.st-key-login_switch .stButton > button,
.st-key-register_switch .stButton > button {{
    height: auto !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
    color: var(--orange) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: auto !important;
    min-height: auto !important;
    font-family: 'Inter', sans-serif !important;
}}
.st-key-login_switch, .st-key-register_switch {{ margin-bottom: .6rem; }}
.st-key-login_switch [data-testid="stMarkdownContainer"],
.st-key-register_switch [data-testid="stMarkdownContainer"] {{
    padding-top: .08rem; white-space: nowrap;
}}
.st-key-login_switch [data-testid="stHorizontalBlock"],
.st-key-register_switch [data-testid="stHorizontalBlock"] {{
    align-items: center; justify-content: flex-start; gap: .25rem; flex-wrap: nowrap;
}}
.st-key-login_switch .stButton,
.st-key-register_switch .stButton {{ width: auto !important; flex: 0 0 auto !important; }}

/* ── LOGIN / REGISTER HERO ── */
.login-hero {{
    position: relative;
    min-height: 100vh;
    overflow: hidden;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-color: var(--navy);
}}
.login-hero::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(0,5,104,.16) 0%, rgba(0,5,104,.55) 100%);
    z-index: 1;
}}
.login-hero-ring {{
    position: absolute;
    top: 2rem; right: -6rem;
    width: 18rem; height: 18rem;
    border: 2.5rem solid rgba(255,255,255,.06);
    border-radius: 999px;
    z-index: 2;
}}
.login-hero-content {{
    position: absolute;
    left: 4rem; bottom: 4rem;
    z-index: 3;
    max-width: 34rem;
    color: #fff;
}}
.login-hero-stripe {{
    width: 4rem; height: 0.22rem;
    background: var(--orange);
    margin-bottom: 1.8rem;
}}
.login-hero-title {{
    font-family: 'Lexend', sans-serif;
    font-size: clamp(3.2rem, 5vw, 5.5rem);
    font-weight: 900;
    line-height: 0.9;
    letter-spacing: -0.06em;
    margin-bottom: 1.5rem;
}}
.login-hero-copy {{
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 500;
    line-height: 1.75;
    max-width: 29rem;
    padding-left: 1.4rem;
    border-left: 2px solid rgba(255,87,34,.5);
    opacity: 0.9;
}}

/* ── REGISTER ── */
.st-key-auth_panel, .st-key-home_panel {{
    background: transparent;
    border: none;
    box-shadow: none;
    padding: 3rem 5rem 2rem !important;
    min-height: calc(100vh - 80px);
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.st-key-auth_panel .stFormSubmitButton > button {{
    height: 4rem !important;
    border-radius: 6px !important;
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%) !important;
    color: #fff !important;
    border: none !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 32px rgba(0,5,104,.15) !important;
}}
.panel-title {{
    font-family: 'Lexend', sans-serif;
    font-size: 3.2rem;
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.05em;
    color: var(--navy);
    margin-bottom: 1rem;
}}
.switch-copy {{ color: var(--muted); font-size: 1rem; font-weight: 500; }}
.panel-copy {{ color: var(--muted); font-size: 1rem; margin-bottom: 1.5rem; }}

/* ── FLASH ── */
.flash {{
    border-radius: 6px;
    padding: .85rem 1rem;
    margin-bottom: 1rem;
    font-size: .95rem;
    font-weight: 700;
    border: 1px solid;
}}
.flash-success {{ background: #ecfdf3; border-color: #86efac; color: #166534; }}
.flash-error {{ background: #fff1f2; border-color: #fda4af; color: #be123c; }}

/* ── BRAND / NAV ── */
.brand {{ display: flex; align-items: center; }}
.brand-logo {{ height: 2.8rem; width: auto; display: block; object-fit: contain; }}
.brand-wordmark {{
    font-family: 'Lexend', sans-serif;
    font-size: 1.9rem;
    font-style: italic;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.05em;
}}
.brand-pace {{ color: var(--navy); }}
.brand-up {{ color: var(--orange); }}
.nav-menu {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2.4rem;
    width: 100%;
    font-family: 'Lexend', sans-serif;
}}
.nav-item {{
    position: relative;
    color: #5b6473;
    font-size: .88rem;
    font-weight: 800;
    letter-spacing: .06em;
    text-transform: uppercase;
}}
.nav-item.active {{ color: var(--navy); }}
.nav-item.active::after {{
    content: "";
    position: absolute;
    left: 0; right: 0;
    bottom: -0.45rem;
    height: 3px;
    background: var(--orange);
}}

/* ── ONBOARDING ── */
.ob-wrapper {{
    display: flex;
    min-height: calc(100vh - 72px);
}}
.ob-sidebar {{
    width: 33%;
    min-width: 280px;
    background: linear-gradient(135deg, #000568 0%, #1b237e 100%);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 3rem;
    position: sticky;
    top: 72px;
    height: 100vh;
    overflow: hidden;
}}
.ob-sidebar-brand {{
    font-family: 'Lexend', sans-serif;
    font-size: 1.8rem;
    font-weight: 900;
    font-style: italic;
    letter-spacing: -0.04em;
    color: #fff;
    margin-bottom: 3rem;
}}
.ob-sidebar-title {{
    font-family: 'Lexend', sans-serif;
    font-size: clamp(1.8rem, 2.2vw, 2.6rem);
    font-weight: 700;
    line-height: 0.92;
    letter-spacing: -0.04em;
    color: #fff;
    margin-bottom: 1.5rem;
}}
.ob-sidebar-copy {{
    color: rgba(190,194,255,.85);
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 1.7;
    max-width: 260px;
}}
.ob-sidebar-footer {{
    position: relative;
    z-index: 2;
}}
.ob-phase-bar {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}}
.ob-phase-line {{
    height: 2px;
    width: 3rem;
    background: var(--orange);
}}
.ob-phase-label {{
    font-family: 'Lexend', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #fff;
}}
.ob-copyright {{
    font-size: 0.72rem;
    color: rgba(190,194,255,.5);
}}
.ob-bg-icon {{
    position: absolute;
    right: -5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20rem;
    color: rgba(255,255,255,.06);
    pointer-events: none;
    user-select: none;
    font-family: 'Material Symbols Outlined';
    z-index: 1;
}}

.ob-form-area {{
    flex: 1;
    padding: 4rem 5rem;
    background: var(--surface);
    overflow-y: auto;
}}
.ob-form-header {{ margin-bottom: 3rem; }}
.ob-form-title {{
    font-family: 'Lexend', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--navy);
    letter-spacing: -0.04em;
    margin-bottom: 0.5rem;
}}
.ob-form-sub {{
    font-size: 0.95rem;
    color: var(--muted);
}}
.ob-section-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    margin-top: 2.5rem;
}}
.ob-section-title {{
    font-family: 'Lexend', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--navy);
    white-space: nowrap;
}}
.ob-section-line {{
    flex: 1;
    height: 1px;
    background: var(--line);
}}

/* Fitness toggle buttons */
.fitness-toggle {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    background: var(--surface-low);
    padding: 4px;
    border-radius: 10px;
    margin-top: 4px;
}}
.ft-btn {{
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'Lexend', sans-serif;
    letter-spacing: 0.06em;
    text-align: center;
    cursor: pointer;
    border: none;
    transition: all .15s;
}}
.ft-btn.active {{
    background: var(--surface-lowest);
    color: var(--navy);
    box-shadow: 0 1px 4px rgba(0,0,0,.1);
}}
.ft-btn.inactive {{
    background: transparent;
    color: var(--muted);
}}

/* Day circle buttons */
.day-circles {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 4px;
}}
.day-circle {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 700;
    font-family: 'Lexend', sans-serif;
    cursor: pointer;
    border: 2px solid;
    transition: all .15s;
}}
.day-circle.selected {{
    background: var(--navy);
    border-color: var(--navy);
    color: #fff;
}}
.day-circle.unselected {{
    background: transparent;
    border-color: var(--line);
    color: var(--muted);
}}

/* Onboarding form field overrides */
.st-key-ob_form .stTextInput [data-baseweb="base-input"] {{
    border: 1px solid rgba(198,197,212,.15) !important;
    border-radius: 10px !important;
    background: var(--surface-lowest) !important;
}}
.st-key-ob_form .stTextInput input {{
    height: 3.2rem !important;
    line-height: 3.2rem !important;
    background: var(--surface-lowest) !important;
    padding: 0 1rem !important;
}}
.st-key-ob_form .stSelectbox > div > div {{
    border: 1px solid rgba(198,197,212,.15) !important;
    border-radius: 10px !important;
    background: var(--surface-lowest) !important;
    min-height: 3.2rem !important;
}}
.st-key-ob_form .stNumberInput > div > div {{
    border: 1px solid rgba(198,197,212,.15) !important;
    border-radius: 10px !important;
    background: var(--surface-lowest) !important;
}}
.st-key-ob_form label {{ font-size: 0.85rem !important; font-weight: 500 !important; color: var(--muted) !important; }}
.st-key-ob_form .stFormSubmitButton > button {{
    height: 4.2rem !important;
    border-radius: 10px !important;
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%) !important;
    color: #fff !important;
    border: none !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 36px rgba(0,5,104,.18) !important;
    margin-top: 1rem !important;
}}
.ob-terms {{
    text-align: center;
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 1rem;
}}
.ob-terms span {{ color: var(--navy); text-decoration: underline; cursor: pointer; }}

/* Onboarding redesign */
.ob-shell {{
    display: flex;
    min-height: 100vh;
    background: var(--surface);
}}
.ob-sidebar {{
    position: sticky;
    top: 0;
    width: 100%;
    min-width: 0;
    max-width: 28rem;
    height: 100%;
    min-height: calc(100vh - 5rem);
    align-self: stretch;
    padding: 3rem 2.8rem 2.4rem;
    background: linear-gradient(135deg, #000568 0%, #1b237e 100%);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}}
.ob-sidebar-top, .ob-sidebar-footer {{
    position: relative;
    z-index: 2;
}}
.ob-sidebar-footer {{
    margin-top: auto;
    padding-top: 2rem;
}}
.ob-sidebar-brand {{
    font-family: 'Lexend', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    font-style: italic;
    letter-spacing: -0.06em;
    color: #fff;
    margin-bottom: 3.2rem;
}}
.ob-sidebar-title {{
    font-family: 'Lexend', sans-serif;
    font-size: clamp(1.8rem, 2.2vw, 2.6rem);
    font-weight: 800;
    line-height: 0.9;
    letter-spacing: -0.07em;
    color: #fff;
    max-width: 26rem;
    margin-bottom: 1.45rem;
}}
.ob-sidebar-copy {{
    color: rgba(190,194,255,.78);
    font-size: .98rem;
    line-height: 1.65;
    max-width: 20rem;
}}
.ob-phase-bar {{
    display: flex;
    align-items: center;
    gap: .8rem;
    margin-bottom: .75rem;
}}
.ob-phase-line {{
    width: 3.4rem;
    height: 2px;
    background: var(--orange);
}}
.ob-phase-label {{
    font-family: 'Lexend', sans-serif;
    font-size: .82rem;
    font-weight: 800;
    letter-spacing: .12em;
    line-height: 1.4;
    text-transform: uppercase;
    color: #fff;
    max-width: 10rem;
}}
.ob-copyright {{
    font-size: 0.8rem;
    color: rgba(190,194,255,.45);
    line-height: 1.5;
    max-width: 10rem;
}}
.ob-kinetic {{
    position: absolute;
    left: -6.5rem;
    bottom: 2.2rem;
    width: 26rem;
    height: 21rem;
    background: rgba(190,194,255,.12);
    border-radius: 48% 52% 36% 64% / 68% 34% 66% 32%;
    transform: rotate(26deg);
}}
.ob-content {{
    position: relative;
    flex: 1;
    min-height: 100vh;
    padding: 2.6rem 4.5rem 2.5rem;
    background: var(--surface);
    overflow: hidden;
}}
.ob-content-inner {{
    position: relative;
    z-index: 2;
    max-width: 44rem;
    margin: 0 auto 0 0;
}}
.ob-form-header {{
    margin-bottom: 2.1rem;
}}
.ob-form-title {{
    font-family: 'Lexend', sans-serif;
    font-size: clamp(3rem, 4vw, 4rem);
    font-weight: 900;
    color: var(--navy);
    letter-spacing: -0.06em;
    line-height: .94;
    margin-bottom: .85rem;
}}
.ob-form-sub {{
    font-size: 1.03rem;
    color: var(--text);
    opacity: .88;
    max-width: 36rem;
    line-height: 1.55;
}}
.ob-section-header {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin: 0 0 1.6rem;
}}
.ob-section-title {{
    font-family: 'Lexend', sans-serif;
    font-size: 1.18rem;
    font-weight: 800;
    color: var(--navy);
    white-space: nowrap;
}}
.ob-section-line {{
    flex: 1;
    height: 1px;
    background: var(--line);
}}
.ob-field-label {{
    font-size: 1rem;
    font-weight: 500;
    color: var(--text);
    margin-bottom: .55rem;
}}
.ob-fit-note {{
    font-size: .88rem;
    color: var(--outline);
    margin-top: .45rem;
}}
.st-key-ob_fit_toggle [data-testid="stHorizontalBlock"] {{
    gap: .45rem !important;
}}
.st-key-ob_fit_toggle .stButton > button {{
    height: 3rem !important;
    border-radius: .85rem !important;
    border: 1px solid transparent !important;
    background: var(--surface-low) !important;
    color: var(--outline) !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: .88rem !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}}
.st-key-ob_fit_toggle .stButton > button[kind="primary"] {{
    background: var(--navy) !important;
    color: #fff !important;
    border-color: var(--navy) !important;
    box-shadow: 0 10px 24px rgba(0,5,104,.24) !important;
}}
.st-key-ob_days [data-testid="stHorizontalBlock"] {{
    gap: .85rem !important;
}}
.st-key-ob_days .stButton > button {{
    width: 3.45rem !important;
    min-width: 3.45rem !important;
    height: 3.45rem !important;
    border-radius: 999px !important;
    padding: 0 !important;
    border: 2px solid #ddd9e7 !important;
    background: #fff !important;
    color: #464652 !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
}}
.st-key-ob_days .stButton > button[kind="primary"] {{
    background: var(--navy) !important;
    border-color: var(--navy) !important;
    color: #fff !important;
    box-shadow: 0 10px 24px rgba(0,5,104,.18) !important;
}}
.st-key-ob_formwrap [data-testid="stWidgetLabel"] p {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    color: var(--text) !important;
}}
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"],
.st-key-ob_formwrap .stNumberInput [data-baseweb="base-input"],
.st-key-ob_formwrap .stSelectbox > div > div,
.st-key-ob_formwrap .stDateInput > div > div {{
    border: 1px solid rgba(198,197,212,.9) !important;
    border-radius: 16px !important;
    background: #fff !important;
    box-shadow: none !important;
    overflow: hidden !important;
    clip-path: inset(0 round 16px);
    min-height: 3.5rem !important;
    height: 3.5rem !important;
}}
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"] {{
    border: 1.5px solid rgba(118,118,131,.28) !important;
    border-radius: 8px !important;
    background: #fff !important;
    box-shadow: 0 2px 10px rgba(0,5,104,.03) !important;
    height: 3.5rem !important;
    min-height: 3.5rem !important;
    overflow: hidden !important;
    padding: 0 !important;
    clip-path: none !important;
}}
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"],
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"] *,
.st-key-ob_formwrap .stNumberInput [data-baseweb="base-input"],
.st-key-ob_formwrap .stNumberInput [data-baseweb="base-input"] * {{
    background: #fff !important;
}}
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"]:focus-within,
.st-key-ob_formwrap .stNumberInput [data-baseweb="base-input"]:focus-within,
.st-key-ob_formwrap .stSelectbox > div > div:focus-within,
.st-key-ob_formwrap .stDateInput > div > div:focus-within {{
    border-color: var(--navy) !important;
    box-shadow: 0 0 0 4px rgba(0,5,104,.08) !important;
}}
.st-key-ob_formwrap [data-testid="stHorizontalBlock"] {{
    align-items: flex-start !important;
}}
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"] > div:first-child,
.st-key-ob_formwrap .stNumberInput [data-baseweb="base-input"] > div:first-child {{
    align-items: center !important;
    background: #fff !important;
}}
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"] > div:not(:first-child) {{
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    overflow: hidden !important;
}}
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"] > div:last-child,
.st-key-ob_formwrap .stTextInput [data-baseweb="base-input"] > div:last-child * {{
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    overflow: hidden !important;
}}
.st-key-ob_formwrap .stTextInput input,
.st-key-ob_formwrap .stNumberInput input,
.st-key-ob_formwrap .stDateInput input {{
    height: 3.5rem !important;
    line-height: 3.5rem !important;
    padding: 0 1.15rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 500 !important;
    background: #fff !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 16px !important;
    vertical-align: middle !important;
    -webkit-appearance: none !important;
    appearance: none !important;
}}
.st-key-ob_formwrap .stTextInput input {{
    border: none !important;
    border-radius: 0 !important;
    height: 3.5rem !important;
    background: #fff !important;
    padding: 0 1.15rem !important;
}}
.st-key-ob_formwrap .stTextInput input::placeholder,
.st-key-ob_formwrap .stNumberInput input::placeholder {{
    color: #9ea1b3 !important;
    opacity: 1 !important;
}}
.st-key-ob_formwrap .stSelectbox [data-baseweb="select"] [data-testid="stMarkdownContainer"],
.st-key-ob_formwrap .stSelectbox span,
.st-key-ob_formwrap .stSelectbox div {{
    color: var(--text) !important;
    opacity: 1 !important;
}}
.st-key-ob_formwrap .stDateInput input,
.st-key-ob_formwrap .stDateInput input::-webkit-datetime-edit,
.st-key-ob_formwrap .stDateInput input::-webkit-datetime-edit-text,
.st-key-ob_formwrap .stDateInput input::-webkit-datetime-edit-month-field,
.st-key-ob_formwrap .stDateInput input::-webkit-datetime-edit-day-field,
.st-key-ob_formwrap .stDateInput input::-webkit-datetime-edit-year-field,
.st-key-ob_formwrap .stDateInput [data-baseweb="input"],
.st-key-ob_formwrap .stDateInput [data-baseweb="input"] * {{
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    opacity: 1 !important;
}}
.st-key-ob_formwrap .stSelectbox [data-baseweb="select"] *,
.st-key-ob_formwrap .stDateInput * {{
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
}}
.st-key-ob_formwrap .stSelectbox [data-baseweb="select"],
.st-key-ob_formwrap .stDateInput [data-baseweb="input"] {{
    min-height: 3.5rem !important;
    height: 3.5rem !important;
}}
.st-key-ob_formwrap .stSelectbox [data-baseweb="select"] > div,
.st-key-ob_formwrap .stDateInput [data-baseweb="input"] > div {{
    min-height: 3.5rem !important;
    height: 3.5rem !important;
    display: flex !important;
    align-items: center !important;
}}
.st-key-ob_formwrap .stNumberInput button {{
    display: none !important;
}}
.st-key-ob_formwrap .stNumberInput [data-baseweb="base-input"] > div:not(:first-child) {{
    display: none !important;
    width: 0 !important;
    min-width: 0 !important;
    padding: 0 !important;
}}
.st-key-ob_formwrap .stDateInput button,
.st-key-ob_formwrap .stSelectbox button {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 3rem !important;
    min-width: 3rem !important;
    height: 3.5rem !important;
    color: var(--navy) !important;
    opacity: 1 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}
.st-key-ob_formwrap .stDateInput button svg,
.st-key-ob_formwrap .stSelectbox button svg,
.st-key-ob_formwrap .stDateInput svg,
.st-key-ob_formwrap .stSelectbox svg {{
    display: block !important;
    color: var(--navy) !important;
    fill: currentColor !important;
    opacity: 1 !important;
}}
.st-key-ob_submit .stButton > button {{
    height: 4.7rem !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-2) 100%) !important;
    color: #fff !important;
    border: none !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    box-shadow: 0 18px 36px rgba(0,5,104,.16) !important;
}}
.ob-map-deco {{
    display: none !important;
}}
@media (max-width: 1100px) {{
    .ob-sidebar {{
        max-width: 24rem;
        padding: 2.6rem 2.1rem;
    }}
    .ob-sidebar-title {{
        font-size: 3.3rem;
    }}
    .ob-content {{
        padding: 2.5rem 2.8rem 2.2rem;
    }}
}}
@media (max-width: 900px) {{
    .ob-shell {{
        display: block;
    }}
    .ob-sidebar {{
        position: relative;
        top: auto;
        width: 100%;
        min-width: 0;
        height: auto;
        padding: 2.5rem 1.5rem;
    }}
    .ob-sidebar-brand {{
        margin-bottom: 2.5rem;
    }}
    .ob-content {{
        padding: 2.4rem 1.25rem 2rem;
        min-height: auto;
    }}
    .ob-content-inner {{
        max-width: none;
    }}
    .ob-map-deco {{
        display: none;
    }}
}}

.placeholder-page {{
    min-height: calc(100vh - 5rem);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem 1.5rem;
}}
.placeholder-card {{
    width: min(40rem, 100%);
    padding: 3rem;
    border: 1px solid var(--line);
    border-radius: 20px;
    background: rgba(255,255,255,.92);
    box-shadow: 0 18px 48px rgba(0,5,104,.06);
    text-align: center;
}}
.placeholder-title {{
    font-family: 'Lexend', sans-serif;
    font-size: clamp(2.2rem, 4vw, 3.4rem);
    font-weight: 900;
    color: var(--navy);
    letter-spacing: -0.05em;
    margin-bottom: .75rem;
}}
.placeholder-copy {{
    font-size: 1.05rem;
    line-height: 1.65;
    color: var(--muted);
}}
.site-footer {{
    padding: 2.5rem 3.5rem;
    border-top: 1px solid var(--line);
    background: var(--surface-low);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 2rem;
}}
.footer-brand {{ font-family: 'Lexend', sans-serif; font-size: 1.1rem; font-weight: 900; color: var(--navy); font-style: italic; }}
.footer-copy {{ font-size: 0.82rem; color: var(--outline); }}
.footer-links {{ display: flex; gap: 1.5rem; }}
.footer-links a {{ font-size: 0.82rem; font-weight: 600; color: var(--outline); text-decoration: none; }}
.footer-links a:hover {{ color: var(--orange); }}

/* ── AUTH (Sign in / Sign up) ── */
body:has(.auth-page-bg),
[data-testid="stAppViewContainer"]:has(.auth-page-bg),
[data-testid="stMain"]:has(.auth-page-bg) {{
    background: #070c14 !important;
    overflow-x: hidden !important;
}}
[data-testid="stMainBlockContainer"]:has(.auth-page-bg) {{
    padding: 0 !important;
    max-width: 100% !important;
    min-height: 100vh !important;
    background:
        radial-gradient(circle at 48% 18%, rgba(55,111,213,.26), transparent 30rem),
        radial-gradient(circle at 70% 72%, rgba(16,49,116,.22), transparent 34rem),
        linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px),
        linear-gradient(180deg, rgba(255,255,255,.025) 1px, transparent 1px),
        #070c14 !important;
    background-size: auto, auto, 4.5rem 4.5rem, 4.5rem 4.5rem, auto !important;
}}
.auth-page-bg {{
    position: fixed;
    inset: 0;
    z-index: -1;
    background:
        radial-gradient(circle at 50% 20%, rgba(29,78,216,.22), transparent 30rem),
        linear-gradient(180deg, rgba(7,12,20,.2), rgba(7,12,20,.78)),
        #070c14;
    pointer-events: none;
}}

.st-key-auth_hero {{
    max-width: 34rem !important;
    margin: 0 auto !important;
    padding: clamp(1.5rem, 5vh, 3.35rem) 1.35rem 1.5rem !important;
    box-sizing: border-box !important;
}}
[data-testid="stMainBlockContainer"]:has(.auth-login-page) .st-key-auth_hero {{
    padding-top: clamp(.75rem, 2.2vh, 1.5rem) !important;
}}
[data-testid="stMainBlockContainer"]:has(.auth-login-page) .auth-sub {{
    margin-bottom: .9rem;
}}
.st-key-auth_hero > div[data-testid="stVerticalBlock"] {{
    position: relative !important;
    gap: 0 !important;
    padding: 1.45rem !important;
    border: 1px solid rgba(157,181,236,.2) !important;
    border-radius: 1.35rem !important;
    background:
        linear-gradient(180deg, rgba(18,34,68,.9), rgba(8,15,31,.9)),
        rgba(8,15,31,.78) !important;
    box-shadow:
        0 26px 80px rgba(0,0,0,.34),
        0 1px 0 rgba(255,255,255,.05) inset !important;
    backdrop-filter: blur(18px) !important;
    overflow: hidden !important;
}}
.st-key-auth_hero > div[data-testid="stVerticalBlock"]::before {{
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
        radial-gradient(circle at 18% 0%, rgba(77,141,240,.18), transparent 14rem),
        linear-gradient(90deg, rgba(255,255,255,.035), transparent 28%);
}}
.auth-brand-mini {{
    position: relative;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    gap: .55rem;
    width: fit-content;
    margin-bottom: 1.05rem;
    color: #f5f8ff;
    font-family: 'Lexend', sans-serif;
    font-size: .94rem;
    font-weight: 800;
}}
.auth-brand-mark {{
    width: 1.65rem;
    height: 1.65rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: .56rem;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: #fff;
    font-size: .86rem;
    box-shadow: 0 14px 30px rgba(37,99,235,.26);
}}
.auth-kicker {{
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: .55rem;
    color: #7897d6;
    font-family: 'Barlow', sans-serif;
    text-transform: uppercase;
    letter-spacing: .28em;
    font-size: .66rem;
    font-weight: 700;
    margin: 0 0 .7rem;
}}
.auth-kicker span {{
    width: .35rem;
    height: .35rem;
    border-radius: 50%;
    background: #1d4ed8;
    box-shadow: 0 0 12px rgba(37,99,235,.72);
}}
.auth-headline {{
    position: relative;
    z-index: 1;
    margin: 0 0 .55rem;
    color: #f5f8ff !important;
    font-family: 'Lexend', sans-serif;
    font-size: clamp(2rem, 4vw, 2.42rem);
    line-height: 1.04;
    font-weight: 600;
    letter-spacing: -.02em;
}}
.auth-sub {{
    position: relative;
    z-index: 1;
    color: #9eb4de !important;
    font-size: .95rem;
    line-height: 1.55;
    margin: 0 0 1.15rem;
}}

.auth-providers {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: .75rem;
    margin: 0 0 .25rem;
}}
.auth-provider-btn {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: .6rem;
    height: 2.6rem;
    background: rgba(15,25,50,.55);
    border: 1px solid rgba(177,198,255,.14);
    border-radius: .7rem;
    color: #ecf3ff;
    font-family: 'Inter', sans-serif;
    font-size: .88rem;
    font-weight: 600;
    cursor: pointer;
    transition: background .15s, border-color .15s;
}}
.auth-provider-btn:hover:not(:disabled) {{
    background: rgba(30,52,84,.6);
    border-color: rgba(177,198,255,.26);
}}
.auth-provider-btn:disabled {{
    cursor: not-allowed;
}}
.ap-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.2rem;
    height: 1.2rem;
    font-weight: 700;
    font-size: .92rem;
    border-radius: 50%;
}}
.ap-google {{
    background: linear-gradient(135deg, #4285f4 0%, #ea4335 50%, #fbbc05 100%);
    color: #fff;
    font-family: 'Inter', sans-serif;
}}
.ap-apple {{
    background: transparent;
    color: #f0f6fc;
    font-size: 1.05rem;
}}
.ap-apple::before {{
    content: "\\f8ff";
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI Symbol', sans-serif;
}}

.auth-divider {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: .9rem 0 .75rem;
}}
.auth-divider::before, .auth-divider::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(177,198,255,.1);
}}
.auth-divider span {{
    color: #7888a3;
    font-family: 'Barlow', sans-serif;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .28em;
    text-transform: uppercase;
}}

.st-key-auth_hero div[data-testid="stForm"] {{
    position: relative !important;
    z-index: 1 !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}}
.st-key-auth_hero div[data-testid="stForm"] > div[data-testid="stVerticalBlock"] {{
    gap: 0 !important;
}}
.st-key-auth_hero div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:has(.auth-label),
.st-key-auth_hero div[data-testid="stForm"] div[data-testid="stVerticalBlock"] > div:has(.auth-label-row) {{
    margin-bottom: .42rem !important;
}}
.st-key-auth_hero .stTextInput {{
    margin-top: .5rem !important;
    margin-bottom: .55rem !important;
}}
.auth-label {{
    display: block;
    color: #8a9bbd;
    font-family: 'Barlow', sans-serif;
    font-size: .66rem;
    font-weight: 700;
    letter-spacing: .26em;
    text-transform: uppercase;
    line-height: 1.4;
    margin: 0;
}}
.auth-label-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0;
}}
.auth-label-row .auth-label {{ margin: 0; }}
.auth-forgot {{
    color: #4d8df0;
    font-family: 'Inter', sans-serif;
    font-size: .82rem;
    font-weight: 600;
    text-decoration: none;
    text-transform: none;
    letter-spacing: 0;
}}
.auth-forgot:hover {{ text-decoration: underline; }}
.auth-hint {{
    color: #7888a3;
    font-family: 'Inter', sans-serif;
    font-size: .76rem;
    font-weight: 500;
    text-transform: none;
    letter-spacing: 0;
}}

.st-key-auth_hero .stTextInput [data-baseweb="base-input"] {{
    border: 1px solid rgba(177,198,255,.16) !important;
    border-radius: .82rem !important;
    background: rgba(5,12,27,.74) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,.04) inset !important;
    min-height: 2.85rem !important;
    height: 2.85rem !important;
}}
.st-key-auth_hero .stTextInput [data-baseweb="base-input"]:hover {{
    border-color: rgba(177,198,255,.24) !important;
}}
.st-key-auth_hero .stTextInput [data-baseweb="base-input"]:focus-within {{
    border-color: rgba(77,141,240,.55) !important;
    box-shadow: 0 0 0 3px rgba(77,141,240,.16) !important;
}}
.st-key-auth_hero .stTextInput [data-baseweb="base-input"] > div {{
    background: transparent !important;
}}
.st-key-auth_hero .stTextInput [data-baseweb="base-input"] > div:not(:first-child) {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 2.7rem !important;
    min-width: 2.7rem !important;
    max-width: 2.7rem !important;
    height: 100% !important;
    background: transparent !important;
}}
.st-key-auth_hero .stTextInput [data-baseweb="base-input"] > div:not(:first-child) * {{
    background: transparent !important;
}}
.st-key-auth_hero .stTextInput input {{
    height: 2.85rem !important;
    line-height: 2.85rem !important;
    background: transparent !important;
    color: #ecf3ff !important;
    caret-color: #ecf3ff !important;
    font-size: .95rem !important;
    font-weight: 500 !important;
    padding: 0 1rem !important;
    border: none !important;
}}
.st-key-auth_hero .stTextInput input::placeholder {{ color: #5e6f8e !important; }}
.st-key-auth_hero .stTextInput [data-baseweb="base-input"] button {{ color: #7888a3 !important; }}
.st-key-auth_hero .stTextInput [data-baseweb="base-input"] button:hover {{ color: #ecf3ff !important; }}

.st-key-auth_hero .stCheckbox {{
    margin: .15rem 0 .15rem;
}}
.st-key-auth_hero .stCheckbox label,
.st-key-auth_hero .stCheckbox label p,
.st-key-auth_hero .stCheckbox label span {{
    color: #9eb4de !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .88rem !important;
    font-weight: 500 !important;
}}
.st-key-auth_hero .stCheckbox [data-baseweb="checkbox"] [data-checked="false"] {{
    background: transparent !important;
    border-color: rgba(177,198,255,.3) !important;
}}

.st-key-auth_hero .stFormSubmitButton {{
    margin-top: .7rem !important;
}}
.st-key-auth_hero .stFormSubmitButton > button {{
    height: 3rem !important;
    min-height: 3rem !important;
    border: none !important;
    border-radius: .95rem !important;
    background: linear-gradient(180deg, #7eb8ff 0%, #4d8df0 100%) !important;
    color: #0b1428 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0 !important;
    box-shadow: 0 18px 42px rgba(77,141,240,.28), 0 1px 0 rgba(255,255,255,.42) inset !important;
}}
.st-key-auth_hero .stFormSubmitButton > button:hover {{
    background: linear-gradient(180deg, #93c5ff 0%, #5d9cf4 100%) !important;
    opacity: 1 !important;
}}

.auth-rule-hint {{
    margin: .45rem 0 .25rem;
    color: #6e7e9c;
    font-family: 'Inter', sans-serif;
    font-size: .78rem;
    font-weight: 500;
    line-height: 1.5;
    letter-spacing: 0;
}}

.st-key-auth_hero .stCheckbox label p,
.st-key-auth_hero .stCheckbox label a {{
    color: #9eb4de !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
}}
.st-key-auth_hero .stCheckbox label a {{
    color: #4d8df0 !important;
    text-decoration: underline !important;
    text-underline-offset: .15em !important;
}}
.st-key-auth_hero .stCheckbox label a:hover {{
    color: #6ea6f5 !important;
}}

.auth-foot {{
    position: relative;
    z-index: 1;
    margin-top: .9rem;
    text-align: center;
    color: #9eb4de;
    font-size: .88rem;
    font-weight: 500;
}}
.auth-foot a {{
    color: #4d8df0;
    text-decoration: none;
    font-weight: 600;
    margin-left: .25rem;
}}
.auth-foot a:hover {{ text-decoration: underline; }}

.auth-proof {{
    position: relative;
    z-index: 1;
    margin-top: .8rem;
    padding-top: .85rem;
    border-top: 1px solid rgba(177,198,255,.1);
    color: #6f83aa;
    font-family: 'Barlow', sans-serif;
    font-size: .66rem;
    font-weight: 700;
    letter-spacing: .14em;
    text-align: center;
    text-transform: uppercase;
}}

.st-key-auth_hero .flash {{
    background: rgba(93,29,36,.35) !important;
    border-color: rgba(154,52,60,.55) !important;
    color: #ffa198 !important;
    border-radius: .65rem !important;
    padding: .65rem .85rem !important;
    font-size: .88rem !important;
    margin: 0 0 1rem !important;
}}
.st-key-auth_hero .flash-success {{
    background: rgba(15,45,26,.4) !important;
    border-color: rgba(34,102,67,.6) !important;
    color: #7ee2a8 !important;
}}

/* ── ONBOARDING WIZARD ── */
body:has(.onboarding-page-bg),
[data-testid="stAppViewContainer"]:has(.onboarding-page-bg),
[data-testid="stMain"]:has(.onboarding-page-bg) {{
    background: #070c14 !important;
    overflow-x: hidden !important;
}}
[data-testid="stMainBlockContainer"]:has(.onboarding-page-bg) {{
    padding: 0 !important;
    max-width: 100% !important;
    min-height: 100vh !important;
    background:
        radial-gradient(circle at 70% 16%, rgba(30,64,175,.18), transparent 32rem),
        #070c14 !important;
}}
.onboarding-page-bg {{
    position: fixed;
    inset: 0;
    z-index: -1;
    background:
        radial-gradient(circle at 72% 20%, rgba(30,64,175,.16), transparent 32rem),
        #070c14;
    pointer-events: none;
}}

.st-key-ob_wizard {{
    max-width: 32rem !important;
    margin: 0 auto !important;
    padding: 1.6rem 1.5rem 2rem !important;
    box-sizing: border-box !important;
}}
.st-key-ob_wizard > div[data-testid="stVerticalBlock"] {{
    gap: .9rem !important;
}}
.ob-brand {{
    display: flex;
    align-items: center;
    gap: .55rem;
    color: #ecf3ff;
    font-family: 'Lexend', sans-serif;
    font-weight: 800;
    font-size: 1rem;
    margin-bottom: 1.4rem;
}}
.ob-brand-mark {{
    width: 1.7rem;
    height: 1.7rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: .55rem;
    background: #1d4ed8;
    color: #fff;
    font-size: .92rem;
    box-shadow: 0 0 22px rgba(29,78,216,.3);
}}

.ob-progress {{
    margin: .25rem 0 1.1rem;
}}
.ob-progress-meta {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'Barlow', sans-serif;
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: #6e7e9c;
    margin-bottom: .55rem;
}}
.ob-progress-step strong {{ color: #f2f6ff; font-weight: 800; }}
.ob-progress-track {{
    position: relative;
    height: 3px;
    border-radius: 999px;
    background: rgba(177,198,255,.12);
    overflow: hidden;
}}
.ob-progress-fill {{
    position: absolute;
    inset: 0 auto 0 0;
    background: linear-gradient(90deg, #4d8df0 0%, #1d4ed8 100%);
    border-radius: 999px;
    box-shadow: 0 0 12px rgba(77,141,240,.4);
}}

.ob-kicker {{
    display: flex;
    align-items: center;
    gap: .55rem;
    color: #7897d6;
    font-family: 'Barlow', sans-serif;
    text-transform: uppercase;
    letter-spacing: .26em;
    font-size: .68rem;
    font-weight: 700;
    margin: 0 0 .8rem;
}}
.ob-kicker span {{
    width: .35rem;
    height: .35rem;
    border-radius: 50%;
    background: #1d4ed8;
    box-shadow: 0 0 12px rgba(37,99,235,.72);
}}
.ob-headline,
.st-key-ob_wizard .ob-headline,
.st-key-ob_wizard .ob-headline * {{
    margin: 0 0 .5rem;
    color: #ffffff !important;
    font-family: 'Lexend', sans-serif;
    font-size: 1.95rem;
    line-height: 1.15;
    font-weight: 600;
    letter-spacing: -.02em;
}}
.ob-sub,
.st-key-ob_wizard .ob-sub,
.st-key-ob_wizard .ob-sub * {{
    color: #b8d0ff !important;
    font-size: .92rem;
    line-height: 1.55;
    margin: 0 0 1.25rem;
}}

/* Race + fitness card grids */
.st-key-ob_race_grid div[data-testid="stHorizontalBlock"],
.st-key-ob_fit_grid div[data-testid="stHorizontalBlock"],
.st-key-ob_about_grid div[data-testid="stHorizontalBlock"] {{
    gap: .85rem !important;
}}
.st-key-ob_race_grid > div[data-testid="stVerticalBlock"] {{
    gap: .85rem !important;
}}
.st-key-ob_race_grid .stButton > button,
.st-key-ob_fit_grid .stButton > button {{
    min-height: 7rem !important;
    height: auto !important;
    padding: 1rem 1.1rem !important;
    border-radius: .85rem !important;
    border: 1px solid rgba(177,198,255,.14) !important;
    background: rgba(15,25,50,.55) !important;
    color: #ecf3ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    box-shadow: none !important;
    letter-spacing: 0 !important;
    white-space: normal !important;
    line-height: 1.45 !important;
}}
.st-key-ob_race_grid .stButton > button p,
.st-key-ob_fit_grid .stButton > button p {{
    text-align: left !important;
    margin: 0 0 .4rem !important;
}}
.st-key-ob_race_grid .stButton > button p:last-child,
.st-key-ob_fit_grid .stButton > button p:last-child {{
    margin-bottom: 0 !important;
    color: #9eb4de !important;
}}
.st-key-ob_race_grid .stButton > button p strong,
.st-key-ob_fit_grid .stButton > button p strong {{
    color: #f2f6ff !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: 1.08rem !important;
    font-weight: 700 !important;
    letter-spacing: -.01em !important;
}}
.st-key-ob_fit_grid .stButton > button {{
    min-width: 0 !important;
    padding: 1rem 1.35rem !important;
}}
.st-key-ob_fit_grid .stButton > button p:first-child {{
    white-space: nowrap !important;
    word-break: keep-all !important;
    overflow-wrap: normal !important;
}}
.st-key-ob_fit_grid .stButton > button p:first-child strong {{
    display: inline-block !important;
    white-space: nowrap !important;
    word-break: keep-all !important;
    overflow-wrap: normal !important;
    font-size: 1rem !important;
    line-height: 1.2 !important;
}}
.st-key-ob_race_grid .stButton > button:hover,
.st-key-ob_fit_grid .stButton > button:hover {{
    background: rgba(30,52,84,.6) !important;
    border-color: rgba(177,198,255,.26) !important;
    opacity: 1 !important;
}}
.st-key-ob_race_grid .stButton > button[kind="primary"],
.st-key-ob_fit_grid .stButton > button[kind="primary"] {{
    background: rgba(30,64,175,.18) !important;
    border-color: rgba(77,141,240,.65) !important;
    box-shadow: 0 0 0 1px rgba(77,141,240,.5), 0 14px 32px rgba(29,78,216,.18) !important;
}}
.st-key-ob_race_grid .stButton > button[kind="primary"]:hover,
.st-key-ob_fit_grid .stButton > button[kind="primary"]:hover {{
    background: rgba(30,64,175,.24) !important;
}}

/* About + experience inputs */
.ob-field-label {{
    color: #8a9bbd;
    font-family: 'Barlow', sans-serif;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .26em;
    text-transform: uppercase;
    margin: .9rem 0 .45rem;
    line-height: 1.4;
    display: block;
}}
.st-key-ob_wizard .stTextInput [data-baseweb="base-input"],
.st-key-ob_wizard .stSelectbox > div > div,
.st-key-ob_wizard .stDateInput > div > div {{
    border: 1px solid rgba(177,198,255,.14) !important;
    border-radius: .65rem !important;
    background: rgba(10,18,38,.85) !important;
    box-shadow: none !important;
    min-height: 2.8rem !important;
    height: 2.8rem !important;
}}
.st-key-ob_wizard .stTextInput [data-baseweb="base-input"]:focus-within,
.st-key-ob_wizard .stSelectbox > div > div:focus-within,
.st-key-ob_wizard .stDateInput > div > div:focus-within {{
    border-color: rgba(77,141,240,.55) !important;
    box-shadow: 0 0 0 3px rgba(77,141,240,.16) !important;
}}
.st-key-ob_wizard .stTextInput [data-baseweb="base-input"] > div {{
    background: transparent !important;
}}
.st-key-ob_wizard .stTextInput input,
.st-key-ob_wizard .stDateInput input {{
    height: 2.8rem !important;
    line-height: 2.8rem !important;
    background: transparent !important;
    color: #ecf3ff !important;
    caret-color: #ecf3ff !important;
    font-size: .95rem !important;
    font-weight: 500 !important;
    padding: 0 1rem !important;
    border: none !important;
}}
.st-key-ob_wizard .stTextInput input::placeholder {{ color: #5e6f8e !important; }}
.st-key-ob_wizard .stSelectbox [data-baseweb="select"] *,
.st-key-ob_wizard .stDateInput * {{
    color: #ecf3ff !important;
    font-family: 'Inter', sans-serif !important;
}}

/* Day picker */
.st-key-ob_days [data-testid="stHorizontalBlock"] {{
    gap: .5rem !important;
}}
.st-key-ob_days .stButton > button {{
    height: 2.8rem !important;
    min-height: 2.8rem !important;
    border-radius: .55rem !important;
    border: 1px solid rgba(177,198,255,.14) !important;
    background: rgba(15,25,50,.55) !important;
    color: #9eb4de !important;
    font-family: 'Lexend', sans-serif !important;
    font-size: .82rem !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    padding: 0 !important;
}}
.st-key-ob_days .stButton > button[kind="primary"] {{
    background: rgba(30,64,175,.25) !important;
    border-color: rgba(77,141,240,.55) !important;
    color: #f2f6ff !important;
}}

/* Health step checkbox */
.st-key-ob_wizard .stCheckbox label,
.st-key-ob_wizard .stCheckbox label p {{
    color: #ecf3ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .92rem !important;
    font-weight: 500 !important;
}}
.ob-disclaimer {{
    margin-top: 1rem;
    color: #6e7e9c;
    font-size: .82rem;
    line-height: 1.55;
}}

/* Errors */
.ob-error-slot {{ margin: .25rem 0; }}
.st-key-ob_wizard .flash {{
    background: rgba(93,29,36,.35) !important;
    border-color: rgba(154,52,60,.55) !important;
    color: #ffa198 !important;
    border-radius: .65rem !important;
    padding: .55rem .8rem !important;
    font-size: .85rem !important;
    margin: 0 0 .5rem !important;
}}

/* Footer: back + continue */
.st-key-ob_footer {{
    margin-top: 1.5rem !important;
}}
.st-key-ob_footer [data-testid="stHorizontalBlock"] {{
    align-items: stretch !important;
    gap: .85rem !important;
}}
.st-key-ob_footer .stButton:not(:has(button[kind="primary"])) > button {{
    height: 3rem !important;
    min-height: 3rem !important;
    background: rgba(15,25,50,.65) !important;
    border: 1px solid rgba(177,198,255,.14) !important;
    border-radius: .75rem !important;
    color: #ecf3ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .9rem !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}
.st-key-ob_footer .stButton:not(:has(button[kind="primary"])) > button:hover {{
    background: rgba(30,52,84,.7) !important;
    opacity: 1 !important;
}}
.st-key-ob_footer .stButton > button[kind="primary"] {{
    height: 3rem !important;
    min-height: 3rem !important;
    border: none !important;
    border-radius: .75rem !important;
    background: linear-gradient(180deg, #9bc5f3 0%, #6ba6e8 100%) !important;
    color: #0b1428 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .98rem !important;
    font-weight: 700 !important;
    letter-spacing: 0 !important;
    box-shadow: 0 16px 36px rgba(107,166,232,.22), 0 1px 0 rgba(255,255,255,.4) inset !important;
}}
.st-key-ob_footer .stButton > button[kind="primary"]:hover {{
    background: linear-gradient(180deg, #abd0f5 0%, #7bb1ed 100%) !important;
    opacity: 1 !important;
}}
.ob-back-spacer {{ height: 3rem; }}

/* Skip link */
.st-key-ob_skip {{
    margin-top: .85rem !important;
    display: flex !important;
    justify-content: center !important;
}}
.st-key-ob_skip .stButton > button {{
    background: transparent !important;
    border: none !important;
    color: #6e7e9c !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: .72rem !important;
    font-weight: 700 !important;
    letter-spacing: .26em !important;
    padding: .35rem .85rem !important;
    height: auto !important;
    min-height: auto !important;
    width: auto !important;
    box-shadow: none !important;
    text-transform: uppercase !important;
}}
.st-key-ob_skip .stButton > button:hover {{
    color: #ecf3ff !important;
    background: transparent !important;
    opacity: 1 !important;
}}

/* Chat screen: one fixed shell, one sidebar scroller, one message scroller. */
html:has(.chat-page-bg),
body:has(.chat-page-bg),
body:has(.chat-page-bg) #root,
body:has(.chat-page-bg) .stApp,
body:has(.chat-page-bg) [data-testid="stAppViewContainer"],
body:has(.chat-page-bg) [data-testid="stMain"],
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"],
body:has(.chat-page-bg) .block-container,
body:has(.chat-page-bg) .element-container:has(.st-key-chat_shell) {{
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: #070c14 !important;
}}
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"] > div {{
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
}}
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"] > div:has(.st-key-chat_shell) {{
    height: 100vh !important;
    height: 100dvh !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
}}

body:has(.chat-page-bg) [data-testid="stHeader"],
body:has(.chat-page-bg) [data-testid="stToolbar"] {{
    display: none !important;
}}

body:has(.chat-page-bg) [data-testid="stVerticalBlock"],
body:has(.chat-page-bg) [data-testid="stVerticalBlockBorderWrapper"],
body:has(.chat-page-bg) [data-testid="stHorizontalBlock"] {{
    background: transparent !important;
}}

.chat-page-bg {{
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    background:
        radial-gradient(circle at 18% 14%, rgba(30,64,175,.14), transparent 28rem),
        #070c14;
}}

.st-key-chat_shell {{
    --chat-sidebar-width: 22rem;
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    padding: 0 !important;
    display: flex !important;
    overflow: hidden !important;
}}

.st-key-chat_shell > div[data-testid="stVerticalBlock"],
.st-key-chat_shell > div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {{
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
    gap: 0 !important;
    overflow: hidden !important;
}}

body:has(.st-key-chat_shell) div[data-testid="column"]:has(.st-key-chat_sidebar),
body:has(.st-key-chat_shell) div[data-testid="stColumn"]:has(.st-key-chat_sidebar) {{
    flex: 0 0 var(--chat-sidebar-width) !important;
    width: var(--chat-sidebar-width) !important;
    min-width: var(--chat-sidebar-width) !important;
    max-width: var(--chat-sidebar-width) !important;
    height: 100dvh !important;
    min-height: 0 !important;
    overflow: hidden !important;
}}

body:has(.st-key-chat_shell) div[data-testid="column"]:has(.st-key-chat_main),
body:has(.st-key-chat_shell) div[data-testid="stColumn"]:has(.st-key-chat_main) {{
    flex: 1 1 calc(100vw - var(--chat-sidebar-width)) !important;
    width: calc(100vw - var(--chat-sidebar-width)) !important;
    min-width: 0 !important;
    max-width: calc(100vw - var(--chat-sidebar-width)) !important;
    height: 100dvh !important;
    min-height: 0 !important;
    overflow: hidden !important;
}}

.st-key-chat_sidebar {{
    position: relative !important;
    inset: auto !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: none !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 1rem .85rem !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    background: rgba(8,14,28,.82) !important;
    border: none !important;
    border-right: 1px solid rgba(177,198,255,.08) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}}

.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] {{
    flex: 1 1 auto !important;
    height: 100% !important;
    min-height: 0 !important;
    display: grid !important;
    grid-template-rows: auto minmax(0, 1fr) auto !important;
    gap: 0 !important;
    overflow: hidden !important;
}}

.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div {{
    min-height: 0 !important;
    overflow: hidden !important;
}}

.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sidebar_top) {{
    grid-row: 1 !important;
    overflow: visible !important;
}}

.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sessions) {{
    grid-row: 2 !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}}

.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sidebar_footer) {{
    grid-row: 3 !important;
    overflow: visible !important;
}}

.chat-brand-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: .15rem .25rem .75rem;
}}
.chat-brand {{
    display: flex;
    align-items: center;
    gap: .55rem;
    color: #ecf3ff;
    font-family: 'Lexend', sans-serif;
    font-weight: 800;
    font-size: 1rem;
}}
.chat-brand-mark {{
    width: 1.7rem;
    height: 1.7rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: .55rem;
    background: #1d4ed8;
    color: #fff;
    font-size: .92rem;
    box-shadow: 0 0 22px rgba(29,78,216,.3);
}}
.chat-brand-plus {{
    width: 1.4rem;
    height: 1.4rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: .45rem;
    border: 1px solid rgba(177,198,255,.15);
    color: #9eb4de;
    font-size: 1rem;
}}

.st-key-new_chat_btn .stButton > button {{
    background: rgba(15,25,50,.7) !important;
    border: 1px solid rgba(177,198,255,.14) !important;
    color: #ecf3ff !important;
    border-radius: .65rem !important;
    width: 100% !important;
    height: 2.45rem !important;
    min-height: 2.45rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    text-align: left !important;
    padding: 0 .8rem !important;
    justify-content: flex-start !important;
}}

.st-key-chat_search {{
    margin-top: .55rem !important;
}}
.st-key-chat_search .stTextInput [data-baseweb="base-input"] {{
    background: rgba(10,18,38,.6) !important;
    border: 1px solid rgba(177,198,255,.1) !important;
    border-radius: .65rem !important;
    box-shadow: none !important;
    min-height: 2.3rem !important;
    height: 2.3rem !important;
}}
.st-key-chat_search .stTextInput input {{
    height: 2.3rem !important;
    line-height: 2.3rem !important;
    background: transparent !important;
    color: #ecf3ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .82rem !important;
    padding: 0 .75rem !important;
    border: none !important;
}}
.st-key-chat_search .stTextInput input::placeholder {{
    color: #5e6f8e !important;
}}

.st-key-chat_sessions {{
    flex: 1 1 auto !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: none !important;
    margin-top: .75rem !important;
    padding-right: .25rem !important;
    overflow: hidden !important;
}}
.st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"],
.st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"] > div {{
    height: 100% !important;
    min-height: 0 !important;
    overflow: hidden !important;
    border: none !important;
    background: transparent !important;
}}
.st-key-chat_sessions > div[data-testid="stVerticalBlock"],
.st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] {{
    height: 100% !important;
    min-height: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    overscroll-behavior: contain !important;
    scrollbar-gutter: stable !important;
    gap: .15rem !important;
}}
.sidebar-section-label {{
    padding: .65rem .35rem .25rem !important;
    font-family: 'Barlow', sans-serif;
    font-size: .66rem;
    font-weight: 700;
    color: #6e7e9c;
    text-transform: uppercase;
    letter-spacing: .26em;
}}
.st-key-chat_sessions .stButton > button {{
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #c4d2ee !important;
    border-radius: .55rem !important;
    width: 100% !important;
    min-height: 2.4rem !important;
    height: auto !important;
    padding: .55rem .7rem !important;
    box-shadow: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    line-height: 1.4 !important;
    white-space: normal !important;
}}
.st-key-chat_sessions .stButton > button[kind="primary"] {{
    background: rgba(30,64,175,.22) !important;
    border-color: rgba(77,141,240,.3) !important;
    color: #fff !important;
}}

.st-key-chat_sidebar_footer {{
    flex: 0 0 auto !important;
    margin-top: .75rem !important;
    padding-top: .65rem !important;
    border-top: 1px solid rgba(177,198,255,.08) !important;
}}
.user-card {{
    display: flex;
    align-items: center;
    gap: .65rem;
    padding: .35rem .25rem;
}}
.user-card-text {{
    flex: 1;
    min-width: 0;
}}
.user-card-chevron {{
    color: #6e7e9c;
    font-size: 1rem;
    line-height: 1;
}}
.user-avatar {{
    width: 2.1rem;
    height: 2.1rem;
    border-radius: 999px;
    background: linear-gradient(135deg, #4d8df0 0%, #1d4ed8 100%);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Inter', sans-serif;
    font-size: .78rem;
    font-weight: 700;
    flex-shrink: 0;
}}
.user-name {{
    color: #ecf3ff;
    font-family: 'Inter', sans-serif;
    font-size: .87rem;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.user-email {{
    color: #6e7e9c;
    font-family: 'Inter', sans-serif;
    font-size: .76rem;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.st-key-signout_sidebar .stButton > button {{
    background: transparent !important;
    border: 1px solid rgba(177,198,255,.1) !important;
    color: #9eb4de !important;
    border-radius: .55rem !important;
    width: 100% !important;
    height: 2.1rem !important;
    min-height: 2.1rem !important;
    margin-top: .35rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .78rem !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}

.st-key-chat_main {{
    position: relative !important;
    inset: auto !important;
    width: 100% !important;
    max-width: none !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    margin: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    background: #070c14 !important;
}}
.st-key-chat_main > div[data-testid="stVerticalBlock"] {{
    flex: 1 1 auto !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    display: grid !important;
    grid-template-rows: auto minmax(0, 1fr) auto !important;
    gap: 0 !important;
    overflow: hidden !important;
}}

body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_header) {{
    grid-row: 1 !important;
    position: relative !important;
    inset: auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
    z-index: 3 !important;
    box-sizing: border-box !important;
}}

body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_body) {{
    grid-row: 2 !important;
    position: relative !important;
    inset: auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: hidden !important;
    z-index: 1 !important;
    box-sizing: border-box !important;
}}

body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock_empty) {{
    grid-row: 3 !important;
    position: relative !important;
    inset: auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
    z-index: 4 !important;
    box-sizing: border-box !important;
}}

.st-key-chat_header {{
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    padding: 1rem 1.75rem !important;
    border-bottom: 1px solid rgba(177,198,255,.08) !important;
    background: rgba(8,14,28,.55) !important;
    backdrop-filter: blur(8px) !important;
    box-sizing: border-box !important;
}}
.chat-header-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    width: 100%;
    min-height: 3.35rem;
    margin: 0;
}}
.chat-header-left {{
    display: flex;
    align-items: center;
    gap: .85rem;
    min-width: 0;
    margin-right: auto;
}}
.chat-header-avatar {{
    width: 2.2rem;
    height: 2.2rem;
    border-radius: .55rem;
    background: #1d4ed8;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Lexend', sans-serif;
    font-weight: 800;
    font-size: .92rem;
    flex-shrink: 0;
}}
.chat-header-title {{
    color: #ecf3ff;
    font-family: 'Lexend', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0;
}}
.chat-header-sub {{
    color: #6e7e9c;
    font-family: 'Inter', sans-serif;
    font-size: .8rem;
    font-weight: 500;
    margin-top: .15rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.chat-header-right {{
    display: flex;
    align-items: center;
    gap: .6rem;
}}
.chat-online-pill {{
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    padding: .25rem .6rem;
    border-radius: 999px;
    background: rgba(15,55,38,.55);
    border: 1px solid rgba(110,224,191,.3);
    color: #6ee0bf;
    font-family: 'Inter', sans-serif;
    font-size: .75rem;
    font-weight: 600;
}}
.pill-dot {{
    width: .42rem;
    height: .42rem;
    border-radius: 50%;
    background: #6ee0bf;
    box-shadow: 0 0 8px rgba(110,224,191,.6);
}}
.chat-header-icon {{
    width: 1.9rem;
    height: 1.9rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: .45rem;
    color: #6e7e9c;
    font-size: .7rem;
    border: 1px solid transparent;
}}

.st-key-chat_body {{
    position: relative !important;
    inset: auto !important;
    width: 100% !important;
    height: 100% !important;
    max-height: 100% !important;
    min-height: 0 !important;
    padding: 1.5rem 2.25rem 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    overscroll-behavior: contain !important;
    overflow-anchor: none !important;
    scrollbar-gutter: stable !important;
    box-sizing: border-box !important;
}}
.st-key-chat_body > div[data-testid="stVerticalBlock"],
.st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"],
.st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"] > div {{
    min-height: 100% !important;
    height: auto !important;
    overflow: visible !important;
    border: none !important;
    background: transparent !important;
}}
.st-key-chat_body_inner,
.st-key-chat_body_inner > div[data-testid="stVerticalBlock"] {{
    width: min(900px, 100%) !important;
    min-height: 100% !important;
    height: auto !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
    overflow: visible !important;
}}
.st-key-chat_body_inner .chat-msg:last-of-type {{
    scroll-margin-bottom: 1rem !important;
}}

.empty-chat {{
    flex: 1 1 auto !important;
    min-height: 100% !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    padding: 0 1rem 1.75rem !important;
    box-sizing: border-box !important;
}}
.empty-chat-copy {{
    width: min(48rem, 100%) !important;
    max-width: 48rem !important;
    margin: 0 auto !important;
    text-align: center !important;
}}
.empty-chat-kicker {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: .55rem;
    color: #7897d6;
    font-family: 'Barlow', sans-serif;
    text-transform: uppercase;
    letter-spacing: .26em;
    font-size: .68rem;
    font-weight: 700;
    margin-bottom: .9rem;
}}
.empty-chat-kicker span {{
    width: .35rem;
    height: .35rem;
    border-radius: 50%;
    background: #1d4ed8;
    box-shadow: 0 0 12px rgba(37,99,235,.72);
}}
.empty-chat-title {{
    color: #f5f8ff;
    font-family: 'Lexend', sans-serif;
    font-size: clamp(2rem, 4vw, 2.42rem);
    line-height: 1.12;
    font-weight: 600;
    letter-spacing: 0;
    max-width: 44rem;
    margin: 0 auto .8rem;
}}
.empty-chat-sub {{
    color: #9eb4de;
    font-size: 1rem;
    line-height: 1.55;
    max-width: 38rem;
    margin: 0 auto;
}}

.chat-msg {{
    display: flex;
    gap: .7rem;
    align-items: flex-start;
    min-width: 0;
    padding: .85rem 0;
    color: #ecf3ff;
}}
.chat-msg.user-msg {{
    justify-content: flex-end;
    flex-direction: row;
}}
.chat-msg.assistant-msg {{
    justify-content: flex-start;
}}
.msg-avatar {{
    width: 2rem;
    height: 2rem;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex: 0 0 auto;
    color: #fff;
    font-size: .75rem;
    font-weight: 800;
}}
.coach-avatar-sm {{
    background: #1d4ed8;
}}
.user-avatar-sm {{
    background: linear-gradient(135deg, #4d8df0, #1d4ed8);
}}
.msg-inner {{
    display: flex;
    flex-direction: column;
    gap: .28rem;
    min-width: 0;
    max-width: min(44rem, 82%);
}}
.assistant-msg .msg-inner {{
    max-width: min(52rem, 92%);
}}
.msg-bubble {{
    font-size: .96rem;
    line-height: 1.42;
    color: #ecf3ff;
    padding: .78rem .98rem;
    border-radius: .85rem;
    background: rgba(30,52,84,.58);
    border: 1px solid rgba(177,198,255,.12);
    white-space: pre-line;
    overflow-wrap: anywhere;
    max-width: 100%;
}}
.assistant-response {{
    font-size: .98rem;
    line-height: 1.5;
    color: #d8e4f8;
    padding: .2rem 0;
    background: transparent;
    border: none;
    box-shadow: none;
    white-space: pre-line;
    overflow-wrap: anywhere;
    max-width: 100%;
}}
.assistant-response p,
.msg-bubble p {{
    margin: 0 0 .35rem 0;
}}
.assistant-response p:last-child,
.msg-bubble p:last-child {{
    margin-bottom: 0;
}}

.st-key-chat_dock,
.st-key-chat_dock_empty {{
    position: relative !important;
    inset: auto !important;
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    padding: 0 2.25rem 1.25rem !important;
    overflow: visible !important;
    box-sizing: border-box !important;
    background: #070c14 !important;
}}
.st-key-chat_dock_inner,
.st-key-chat_dock_empty_inner {{
    width: min(900px, 100%) !important;
    margin: 0 auto !important;
    padding: .78rem .85rem !important;
    border-radius: .9rem !important;
    background: rgba(8,14,28,.92) !important;
    border: 1px solid rgba(177,198,255,.12) !important;
    box-shadow: 0 18px 40px rgba(0,0,0,.18) !important;
    box-sizing: border-box !important;
}}
.st-key-chat_input [data-testid="stHorizontalBlock"],
.st-key-chat_input_empty [data-testid="stHorizontalBlock"] {{
    align-items: center !important;
    gap: .5rem !important;
}}
.st-key-chat_input .stTextInput [data-baseweb="base-input"],
.st-key-chat_input_empty .stTextInput [data-baseweb="base-input"] {{
    background: rgba(15,25,50,.76) !important;
    border: 1px solid rgba(177,198,255,.12) !important;
    border-radius: .7rem !important;
    min-height: 2.7rem !important;
    height: 2.7rem !important;
    box-shadow: none !important;
}}
.st-key-chat_input .stTextInput input,
.st-key-chat_input_empty .stTextInput input {{
    height: 2.7rem !important;
    line-height: 2.7rem !important;
    background: transparent !important;
    color: #ecf3ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .92rem !important;
    padding: 0 .95rem !important;
    border: none !important;
}}
.st-key-chat_input .stTextInput input::placeholder,
.st-key-chat_input_empty .stTextInput input::placeholder {{
    color: #5e6f8e !important;
}}
.st-key-send_btn .stFormSubmitButton > button,
.st-key-send_btn_empty .stFormSubmitButton > button,
.st-key-send_btn .stButton > button,
.st-key-send_btn_empty .stButton > button {{
    background: linear-gradient(180deg, #4d8df0 0%, #1d4ed8 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: .7rem !important;
    height: 2.7rem !important;
    min-height: 2.7rem !important;
    width: 100% !important;
    min-width: 2.7rem !important;
    font-size: .9rem !important;
    font-weight: 800 !important;
    padding: 0 !important;
    box-shadow: 0 8px 18px rgba(29,78,216,.28) !important;
}}
.st-key-btn_load_older_messages .stButton > button {{
    display: block !important;
    margin: .15rem auto .6rem !important;
    width: auto !important;
    min-height: 2rem !important;
    height: 2rem !important;
    padding: 0 .85rem !important;
    border-radius: 999px !important;
    border: 1px solid rgba(177,198,255,.16) !important;
    background: rgba(15,25,50,.7) !important;
    color: #9eb4de !important;
    font-size: .74rem !important;
    font-weight: 800 !important;
    box-shadow: none !important;
}}

@media (max-width: 1100px) {{
    .st-key-chat_shell {{
        --chat-sidebar-width: 17rem;
    }}
    .st-key-chat_body,
    .st-key-chat_dock,
    .st-key-chat_dock_empty {{
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }}
}}

body:has(.chat-page-bg) [data-testid="stBottom"],
body:has(.chat-page-bg) [data-testid="stBottomBlockContainer"] {{
    display: none !important;
}}

/* Final chat layout lock.
   Restores the pre-refactor cascade: fixed viewport shell, sidebar history
   scroller, message scroller, and visible custom input dock. */
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"] > div {{
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
}}
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"] > div:has(.st-key-chat_shell) {{
    height: 100vh !important;
    height: 100dvh !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
}}
body:has(.chat-page-bg) .element-container:has(.st-key-chat_shell),
body:has(.chat-page-bg) div[data-testid="stElementContainer"]:has(.st-key-chat_shell) {{
    height: 100vh !important;
    height: 100dvh !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
}}
.st-key-chat_shell {{
    --chat-sidebar-width: 22rem;
    position: fixed !important;
    inset: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    display: flex !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
}}
.st-key-chat_shell > div[data-testid="stVerticalBlock"],
.st-key-chat_shell > div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {{
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
    gap: 0 !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) div[data-testid="column"]:has(.st-key-chat_sidebar),
body:has(.st-key-chat_shell) div[data-testid="stColumn"]:has(.st-key-chat_sidebar) {{
    position: relative !important;
    flex: 0 0 var(--chat-sidebar-width) !important;
    width: var(--chat-sidebar-width) !important;
    min-width: var(--chat-sidebar-width) !important;
    max-width: var(--chat-sidebar-width) !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) div[data-testid="column"]:has(.st-key-chat_main),
body:has(.st-key-chat_shell) div[data-testid="stColumn"]:has(.st-key-chat_main) {{
    position: relative !important;
    flex: 1 1 auto !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden !important;
}}
.st-key-chat_sidebar {{
    position: relative !important;
    inset: auto !important;
    top: auto !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: none !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    border-radius: 0 !important;
    overflow: hidden !important;
}}
.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] {{
    flex: 1 1 auto !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0 !important;
    overflow: hidden !important;
}}
.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sidebar_top) {{
    flex: 0 0 auto !important;
    overflow: visible !important;
}}
.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sessions) {{
    flex: 0 1 auto !important;
    max-height: 16rem !important;
    min-height: 0 !important;
    display: flex !important;
    overflow: hidden !important;
}}
.st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sidebar_footer) {{
    flex: 0 0 auto !important;
    margin-top: auto !important;
    overflow: visible !important;
}}
.st-key-chat_sessions {{
    flex: 1 1 auto !important;
    height: auto !important;
    max-height: 16rem !important;
    min-height: 0 !important;
    overflow: hidden !important;
}}
.st-key-chat_sessions > div[data-testid="stVerticalBlock"],
.st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"],
.st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"] > div,
.st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] {{
    height: auto !important;
    max-height: 16rem !important;
    min-height: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    overscroll-behavior: contain !important;
    scrollbar-gutter: stable !important;
}}
.st-key-chat_main {{
    position: relative !important;
    inset: auto !important;
    width: 100% !important;
    max-width: none !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}}
.st-key-chat_main > div[data-testid="stVerticalBlock"] {{
    position: relative !important;
    flex: 1 1 auto !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0 !important;
    padding-bottom: 0 !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_header) {{
    position: relative !important;
    inset: auto !important;
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_body) {{
    position: relative !important;
    inset: auto !important;
    flex: 1 1 auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock_empty) {{
    position: relative !important;
    inset: auto !important;
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
    z-index: 4 !important;
}}
.st-key-chat_main,
.st-key-chat_header,
.st-key-chat_body,
.st-key-chat_body_inner,
.st-key-chat_dock,
.st-key-chat_dock_empty,
.chat-msg,
.msg-bubble,
.assistant-response,
.empty-chat {{
    visibility: visible !important;
    opacity: 1 !important;
}}
.st-key-chat_header {{
    height: auto !important;
    min-height: 0 !important;
    flex: 0 0 auto !important;
}}
.st-key-chat_body {{
    flex: 1 1 auto !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    overscroll-behavior: contain !important;
    scrollbar-gutter: stable !important;
}}
.st-key-chat_body > div[data-testid="stVerticalBlock"],
.st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"],
.st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"] > div {{
    min-height: 100% !important;
    height: auto !important;
    overflow: visible !important;
}}
.st-key-chat_body_inner,
.st-key-chat_body_inner > div[data-testid="stVerticalBlock"] {{
    min-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
}}
.st-key-chat_dock,
.st-key-chat_dock_empty {{
    position: relative !important;
    bottom: auto !important;
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
}}

/* Keep Streamlit's responsive columns from stacking or clipping the chat shell
   at normal browser zoom. The effective CSS viewport shrinks at 100% zoom on
   some displays, which can trip Streamlit's column breakpoint unless the
   exact chat columns are locked back to a single row. */
body:has(.st-key-chat_shell) .st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) {{
    width: 100vw !important;
    min-width: 100vw !important;
    max-width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    gap: 0 !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) > div[data-testid="column"]:has(.st-key-chat_sidebar),
body:has(.st-key-chat_shell) .st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) > div[data-testid="stColumn"]:has(.st-key-chat_sidebar) {{
    display: block !important;
    flex: 0 0 var(--chat-sidebar-width) !important;
    width: var(--chat-sidebar-width) !important;
    min-width: var(--chat-sidebar-width) !important;
    max-width: var(--chat-sidebar-width) !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) > div[data-testid="column"]:has(.st-key-chat_main),
body:has(.st-key-chat_shell) .st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) > div[data-testid="stColumn"]:has(.st-key-chat_main) {{
    display: block !important;
    flex: 1 1 calc(100vw - var(--chat-sidebar-width)) !important;
    width: calc(100vw - var(--chat-sidebar-width)) !important;
    min-width: 0 !important;
    max-width: calc(100vw - var(--chat-sidebar-width)) !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden !important;
}}

/* Bottom-pinned chat input and independently scrollable messages.
   The main pane is always header / messages / input; only messages scroll. */
body:has(.st-key-chat_shell) .st-key-chat_main {{
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] {{
    flex: 1 1 auto !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: grid !important;
    grid-template-rows: auto minmax(0, 1fr) auto !important;
    gap: 0 !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_header) {{
    grid-row: 1 !important;
    min-height: 0 !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_body) {{
    grid-row: 2 !important;
    min-height: 0 !important;
    height: 100% !important;
    max-height: 100% !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock_empty) {{
    grid-row: 3 !important;
    min-height: 0 !important;
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    z-index: 20 !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_body {{
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    scroll-behavior: smooth !important;
    overscroll-behavior: contain !important;
    scrollbar-gutter: stable !important;
    padding-bottom: 1rem !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_body > div[data-testid="stVerticalBlock"],
body:has(.st-key-chat_shell) .st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"],
body:has(.st-key-chat_shell) .st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"] > div {{
    min-height: 100% !important;
    height: auto !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_body_inner,
body:has(.st-key-chat_shell) .st-key-chat_body_inner > div[data-testid="stVerticalBlock"] {{
    min-height: 100% !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_dock,
body:has(.st-key-chat_shell) .st-key-chat_dock_empty {{
    position: sticky !important;
    bottom: 0 !important;
    flex: 0 0 auto !important;
    z-index: 30 !important;
    background: #070c14 !important;
    border-top: 1px solid rgba(177,198,255,.06) !important;
}}
body:has(.chat-page-bg) [data-testid="stBottom"],
body:has(.chat-page-bg) [data-testid="stBottomBlockContainer"] {{
    display: none !important;
}}

@media (max-width: 1400px) {{
    .st-key-chat_shell {{
        --chat-sidebar-width: 17rem;
    }}
}}

@media (max-width: 1100px) {{
    .st-key-chat_shell {{
        --chat-sidebar-width: 15rem;
    }}
}}

@media (max-width: 760px) {{
    .st-key-chat_shell {{
        --chat-sidebar-width: 11rem;
    }}
    .st-key-chat_header {{
        padding: .8rem 1rem !important;
    }}
    .chat-header-right {{
        display: none !important;
    }}
    .st-key-chat_body,
    .st-key-chat_dock,
    .st-key-chat_dock_empty {{
        padding-left: .75rem !important;
        padding-right: .75rem !important;
    }}
    .st-key-chat_dock_inner,
    .st-key-chat_dock_empty_inner {{
        padding: .65rem !important;
    }}
}}

/* Final chat height lock: the app never grows taller than the viewport.
   Header and input stay fixed in the chat pane; only AI/user messages scroll. */
body:has(.chat-page-bg),
body:has(.chat-page-bg) .stApp,
body:has(.chat-page-bg) [data-testid="stAppViewContainer"],
body:has(.chat-page-bg) [data-testid="stMain"],
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"],
body:has(.chat-page-bg) .block-container {{
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
}}
.st-key-chat_shell,
.st-key-chat_shell > div[data-testid="stVerticalBlock"],
.st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) {{
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
}}
.st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    gap: 0 !important;
}}
body:has(.st-key-chat_shell) div[data-testid="column"]:has(.st-key-chat_sidebar),
body:has(.st-key-chat_shell) div[data-testid="stColumn"]:has(.st-key-chat_sidebar),
body:has(.st-key-chat_shell) div[data-testid="column"]:has(.st-key-chat_main),
body:has(.st-key-chat_shell) div[data-testid="stColumn"]:has(.st-key-chat_main) {{
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
}}
.st-key-chat_main,
.st-key-chat_main > div[data-testid="stVerticalBlock"] {{
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock_empty) {{
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_body) {{
    flex: 1 1 0 !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: hidden !important;
}}
.st-key-chat_body {{
    flex: 1 1 auto !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    overscroll-behavior: contain !important;
    scroll-behavior: smooth !important;
    padding-bottom: 1rem !important;
}}
.st-key-chat_body_inner,
.st-key-chat_body_inner > div[data-testid="stVerticalBlock"] {{
    min-height: auto !important;
    justify-content: flex-start !important;
}}
.st-key-chat_dock,
.st-key-chat_dock_empty {{
    position: relative !important;
    bottom: auto !important;
    flex: 0 0 auto !important;
    z-index: 20 !important;
    background: #070c14 !important;
}}

/* App-wide viewport lock.
   All pages fit inside the browser viewport. The only intentional internal
   scroller is the chat message transcript. */
html,
body,
body #root,
body .stApp,
body [data-testid="stAppViewContainer"],
body [data-testid="stMain"],
body [data-testid="stMainBlockContainer"],
body .block-container {{
    width: 100vw !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}}
body [data-testid="stMainBlockContainer"] > div {{
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden !important;
}}

/* Landing page: compact single-viewport hero. */
body:has(.landing-page-bg) .st-key-landing_nav {{
    height: clamp(3.4rem, 7dvh, 4.35rem) !important;
    padding: .55rem clamp(1rem, 3vw, 2rem) !important;
}}
body:has(.landing-page-bg) .st-key-landing_hero {{
    height: calc(100dvh - clamp(3.4rem, 7dvh, 4.35rem)) !important;
    min-height: 0 !important;
    max-height: calc(100dvh - clamp(3.4rem, 7dvh, 4.35rem)) !important;
    padding: clamp(1.1rem, 4dvh, 2.6rem) clamp(1rem, 3vw, 2rem) !important;
    overflow: hidden !important;
}}
body:has(.landing-page-bg) .st-key-landing_hero > div[data-testid="stVerticalBlock"],
body:has(.landing-page-bg) .st-key-landing_hero > div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {{
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: hidden !important;
}}
body:has(.landing-page-bg) .landing-kicker {{
    margin-bottom: clamp(.65rem, 2dvh, 1.15rem) !important;
}}
body:has(.landing-page-bg) .landing-copy h1 {{
    font-size: clamp(2.35rem, 7.2dvh, 4.45rem) !important;
    line-height: 1.04 !important;
}}
body:has(.landing-page-bg) .landing-copy p {{
    margin: clamp(.75rem, 2dvh, 1.15rem) 0 clamp(.8rem, 2dvh, 1.2rem) !important;
    font-size: clamp(.84rem, 1.8dvh, .98rem) !important;
    line-height: 1.45 !important;
}}
body:has(.landing-page-bg) .landing-stats {{
    margin-top: clamp(.7rem, 2dvh, 1.1rem) !important;
    gap: clamp(.9rem, 3vw, 1.8rem) !important;
}}
body:has(.landing-page-bg) .landing-visual {{
    min-height: 0 !important;
    height: min(52dvh, 24rem) !important;
}}
body:has(.landing-page-bg) .plan-card {{
    min-height: 0 !important;
    height: min(46dvh, 20rem) !important;
    padding: clamp(1rem, 2dvh, 1.4rem) !important;
}}
body:has(.landing-page-bg) .plan-chart {{
    height: min(16dvh, 6.8rem) !important;
}}

/* Auth pages: fit login/register cards without page scroll. */
body:has(.auth-page-bg) .st-key-auth_hero {{
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: clamp(.5rem, 2dvh, 1.25rem) 1rem !important;
    overflow: hidden !important;
}}
body:has(.auth-page-bg) .st-key-auth_hero > div[data-testid="stVerticalBlock"] {{
    width: min(34rem, calc(100vw - 2rem)) !important;
    max-height: calc(100dvh - 1rem) !important;
    gap: 0 !important;
    padding: clamp(.9rem, 2.1dvh, 1.35rem) !important;
    overflow: hidden !important;
}}
body:has(.auth-page-bg) .auth-brand-mini {{
    margin-bottom: clamp(.35rem, 1.2dvh, .75rem) !important;
}}
body:has(.auth-page-bg) .auth-kicker {{
    margin-bottom: .35rem !important;
    font-size: .6rem !important;
}}
body:has(.auth-page-bg) .auth-headline {{
    font-size: clamp(1.55rem, 4.4dvh, 2.45rem) !important;
    line-height: 1.05 !important;
    margin-bottom: .45rem !important;
}}
body:has(.auth-page-bg) .auth-sub {{
    font-size: clamp(.78rem, 1.8dvh, .92rem) !important;
    line-height: 1.35 !important;
    margin-bottom: .65rem !important;
}}
body:has(.auth-page-bg) .auth-label,
body:has(.auth-page-bg) .auth-label-row {{
    margin: .45rem 0 .28rem !important;
    font-size: .66rem !important;
}}
body:has(.auth-page-bg) .st-key-auth_hero .stTextInput [data-baseweb="base-input"],
body:has(.auth-page-bg) .st-key-auth_hero .stTextInput input {{
    height: clamp(2.25rem, 5.4dvh, 2.7rem) !important;
    min-height: clamp(2.25rem, 5.4dvh, 2.7rem) !important;
    line-height: clamp(2.25rem, 5.4dvh, 2.7rem) !important;
}}
body:has(.auth-page-bg) .auth-rule-hint,
body:has(.auth-page-bg) .st-key-auth_hero .stCheckbox label p {{
    font-size: .74rem !important;
    line-height: 1.3 !important;
}}
body:has(.auth-page-bg) .st-key-auth_hero .stFormSubmitButton {{
    margin-top: .45rem !important;
}}
body:has(.auth-page-bg) .st-key-auth_hero .stFormSubmitButton > button {{
    height: clamp(2.35rem, 5.4dvh, 2.75rem) !important;
    min-height: clamp(2.35rem, 5.4dvh, 2.75rem) !important;
}}
body:has(.auth-page-bg) .auth-foot {{
    margin-top: .55rem !important;
    font-size: .8rem !important;
}}

/* Onboarding: every step fits inside one viewport. */
body:has(.onboarding-page-bg) [data-testid="stMainBlockContainer"],
body:has(.onboarding-page-bg) [data-testid="stMainViewBlockContainer"] {{
    width: min(800px, 100vw) !important;
    max-width: 800px !important;
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    margin: 0 auto !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    overflow: hidden !important;
}}
body:has(.onboarding-page-bg) [data-testid="stMainBlockContainer"] > div,
body:has(.onboarding-page-bg) [data-testid="stMainViewBlockContainer"] > div {{
    width: 100% !important;
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    overflow: hidden !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard {{
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: clamp(.5rem, 2dvh, 1rem) 1rem !important;
    overflow: hidden !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard > div[data-testid="stVerticalBlock"] {{
    width: min(32rem, calc(100vw - 2rem)) !important;
    max-height: calc(100dvh - 1rem) !important;
    gap: clamp(.35rem, 1.2dvh, .7rem) !important;
    overflow: hidden !important;
}}
body:has(.onboarding-page-bg) .ob-brand {{
    margin-bottom: .45rem !important;
}}
body:has(.onboarding-page-bg) .ob-progress {{
    margin: .1rem 0 .55rem !important;
}}
body:has(.onboarding-page-bg) .ob-progress-meta,
body:has(.onboarding-page-bg) .ob-kicker,
body:has(.onboarding-page-bg) .ob-field-label {{
    font-size: .62rem !important;
}}
body:has(.onboarding-page-bg) .ob-kicker {{
    margin-bottom: .35rem !important;
}}
body:has(.onboarding-page-bg) .ob-headline {{
    font-size: clamp(1.35rem, 4dvh, 1.85rem) !important;
    line-height: 1.08 !important;
    margin-bottom: .35rem !important;
}}
body:has(.onboarding-page-bg) .ob-sub {{
    font-size: clamp(.76rem, 1.7dvh, .9rem) !important;
    line-height: 1.34 !important;
    margin-bottom: .65rem !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_race_grid > div[data-testid="stVerticalBlock"],
body:has(.onboarding-page-bg) .st-key-ob_race_grid div[data-testid="stHorizontalBlock"],
body:has(.onboarding-page-bg) .st-key-ob_fit_grid div[data-testid="stHorizontalBlock"],
body:has(.onboarding-page-bg) .st-key-ob_about_grid div[data-testid="stHorizontalBlock"] {{
    gap: .5rem !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_race_grid .stButton > button,
body:has(.onboarding-page-bg) .st-key-ob_fit_grid .stButton > button {{
    min-height: clamp(4.8rem, 12dvh, 6rem) !important;
    padding: .7rem .8rem !important;
    font-size: .78rem !important;
    line-height: 1.25 !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_race_grid .stButton > button p,
body:has(.onboarding-page-bg) .st-key-ob_fit_grid .stButton > button p {{
    margin-bottom: .22rem !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_race_grid .stButton > button p strong,
body:has(.onboarding-page-bg) .st-key-ob_fit_grid .stButton > button p strong {{
    font-size: .94rem !important;
}}
body:has(.onboarding-page-bg) .ob-field-label {{
    margin: .5rem 0 .25rem !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput [data-baseweb="base-input"],
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox > div > div,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput > div > div,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput input,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input,
body:has(.onboarding-page-bg) .st-key-ob_days .stButton > button {{
    height: clamp(2.2rem, 5.2dvh, 2.65rem) !important;
    min-height: clamp(2.2rem, 5.2dvh, 2.65rem) !important;
    line-height: clamp(2.2rem, 5.2dvh, 2.65rem) !important;
}}
body:has(.onboarding-page-bg) .ob-disclaimer {{
    margin-top: .5rem !important;
    font-size: .74rem !important;
    line-height: 1.35 !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_footer {{
    margin-top: .65rem !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_footer .stButton > button,
body:has(.onboarding-page-bg) .ob-back-spacer {{
    height: clamp(2.3rem, 5.5dvh, 2.75rem) !important;
    min-height: clamp(2.3rem, 5.5dvh, 2.75rem) !important;
}}
body:has(.onboarding-page-bg) .ob-error-slot,
body:has(.onboarding-page-bg) .st-key-ob_wizard .flash {{
    margin: .1rem 0 !important;
}}

/* Onboarding side navigation arrows */
body:has(.onboarding-page-bg) {{
    --ob-nav-size: 64px;
    --ob-nav-edge: 50px;
}}
body:has(.onboarding-page-bg) .element-container:has(.st-key-ob_nav_back),
body:has(.onboarding-page-bg) div[data-testid="stElementContainer"]:has(.st-key-ob_nav_back),
body:has(.onboarding-page-bg) .st-key-ob_nav_back,
body:has(.onboarding-page-bg) .element-container:has(.st-key-ob_nav_next),
body:has(.onboarding-page-bg) div[data-testid="stElementContainer"]:has(.st-key-ob_nav_next),
body:has(.onboarding-page-bg) .st-key-ob_nav_next {{
    position: fixed !important;
    top: 50% !important;
    width: var(--ob-nav-size) !important;
    height: var(--ob-nav-size) !important;
    min-width: var(--ob-nav-size) !important;
    min-height: var(--ob-nav-size) !important;
    margin: 0 !important;
    padding: 0 !important;
    transform: translateY(-50%) !important;
    z-index: 1000 !important;
    overflow: visible !important;
    pointer-events: auto !important;
}}
body:has(.onboarding-page-bg) .element-container:has(.st-key-ob_nav_back),
body:has(.onboarding-page-bg) div[data-testid="stElementContainer"]:has(.st-key-ob_nav_back),
body:has(.onboarding-page-bg) .st-key-ob_nav_back {{
    left: var(--ob-nav-edge) !important;
    right: auto !important;
}}
body:has(.onboarding-page-bg) .element-container:has(.st-key-ob_nav_next),
body:has(.onboarding-page-bg) div[data-testid="stElementContainer"]:has(.st-key-ob_nav_next),
body:has(.onboarding-page-bg) .st-key-ob_nav_next {{
    right: var(--ob-nav-edge) !important;
    left: auto !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back > div[data-testid="stVerticalBlock"],
body:has(.onboarding-page-bg) .st-key-ob_nav_next > div[data-testid="stVerticalBlock"] {{
    width: 100% !important;
    height: 100% !important;
    gap: 0 !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back .stButton,
body:has(.onboarding-page-bg) .st-key-ob_nav_next .stButton {{
    width: 100% !important;
    height: 100% !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back .stButton > button,
body:has(.onboarding-page-bg) .st-key-ob_nav_next .stButton > button {{
    width: var(--ob-nav-size) !important;
    min-width: var(--ob-nav-size) !important;
    height: var(--ob-nav-size) !important;
    min-height: var(--ob-nav-size) !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 999px !important;
    background: #1e63f8 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(30, 99, 248, .4), 0 18px 40px rgba(30, 99, 248, .22) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    transition: background-color .2s ease, transform .2s ease, box-shadow .2s ease !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back .stButton > button:hover,
body:has(.onboarding-page-bg) .st-key-ob_nav_next .stButton > button:hover {{
    background: #1649c1 !important;
    box-shadow: 0 6px 18px rgba(30, 99, 248, .48), 0 22px 48px rgba(30, 99, 248, .26) !important;
    opacity: 1 !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back .stButton > button p,
body:has(.onboarding-page-bg) .st-key-ob_nav_next .stButton > button p {{
    color: #ffffff !important;
    font-size: inherit !important;
    line-height: 1 !important;
    margin: 0 !important;
}}
@media (max-width: 640px) {{
    body:has(.onboarding-page-bg) {{
        --ob-nav-edge: 12px;
    }}
}}

/* Placeholder pages: full viewport, no footer-driven page growth. */
body:has(.placeholder-page) .st-key-top_nav {{
    position: relative !important;
    height: 4rem !important;
    padding: .55rem clamp(1rem, 3vw, 2rem) !important;
}}
body:has(.placeholder-page) .placeholder-page {{
    height: calc(100dvh - 4rem) !important;
    min-height: 0 !important;
    max-height: calc(100dvh - 4rem) !important;
    padding: 1rem !important;
    overflow: hidden !important;
}}
body:has(.placeholder-page) .placeholder-card {{
    padding: clamp(1.25rem, 4dvh, 2.25rem) !important;
}}
body:has(.placeholder-page) .site-footer {{
    display: none !important;
}}

/* Remove non-transcript internal scrolling. */
.ob-form-area {{
    overflow: hidden !important;
    overflow-y: hidden !important;
    scrollbar-gutter: auto !important;
}}

/* Sidebar conversation history: fixed sidebar, scroll only the history area. */
.st-key-chat_shell {{
    --chat-history-row-height: 2.15rem;
    --chat-history-height: clamp(8rem, calc(100dvh - 15.5rem), 300px);
}}
body:has(.st-key-chat_shell) .st-key-chat_sidebar,
body:has(.st-key-chat_shell) .st-key-chat_sidebar > div[data-testid="stVerticalBlock"] {{
    min-height: 0 !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) [data-testid="stSidebarUserContent"] {{
    overflow-y: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sidebar {{
    height: 100vh !important;
    height: 100dvh !important;
    max-height: 100dvh !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sidebar > div[data-testid="stVerticalBlock"] {{
    height: 100% !important;
    max-height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sidebar_top) {{
    flex: 0 0 auto !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sessions) {{
    flex: 0 0 var(--chat-history-height) !important;
    height: var(--chat-history-height) !important;
    max-height: var(--chat-history-height) !important;
    min-height: 0 !important;
    display: block !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sidebar > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_sidebar_footer) {{
    flex: 0 0 auto !important;
    margin-top: 0 !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sessions {{
    display: block !important;
    flex: 0 0 var(--chat-history-height) !important;
    height: var(--chat-history-height) !important;
    max-height: var(--chat-history-height) !important;
    min-height: 0 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    overscroll-behavior: contain !important;
    scrollbar-gutter: stable !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"],
body:has(.st-key-chat_shell) .st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"] > div {{
    display: block !important;
    height: auto !important;
    max-height: none !important;
    min-height: 0 !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sessions > div[data-testid="stVerticalBlock"],
body:has(.st-key-chat_shell) .st-key-chat_sessions > div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] {{
    display: block !important;
    height: auto !important;
    max-height: none !important;
    min-height: 0 !important;
    padding-right: .15rem !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button {{
    min-height: var(--chat-history-row-height) !important;
    height: var(--chat-history-row-height) !important;
}}
body:has(.st-key-chat_shell) [data-testid="stSidebar"] {{
    min-width: 260px !important;
    width: 260px !important;
    max-width: 260px !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton {{
    margin-bottom: .25rem !important;
}}
body:has(.st-key-chat_shell) div[key="chat_sessions"] button,
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button {{
    min-height: var(--chat-history-row-height) !important;
    height: var(--chat-history-row-height) !important;
    padding: 2px .55rem !important;
    margin-bottom: 4px !important;
    font-size: .82rem !important;
    line-height: 1.15 !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button p {{
    line-height: 1.15 !important;
    margin: 0 !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_sessions .sidebar-section-label {{
    padding: .35rem .25rem .18rem !important;
    font-size: .58rem !important;
}}

/* Nuclear chat viewport lock: the page cannot grow; only messages scroll. */
body:has(.st-key-chat_shell) .st-key-chat_shell {{
    --chat-sidebar-width: 260px;
    --chat-header-height: 5.25rem;
    --chat-dock-height: clamp(6.5rem, 14dvh, 8rem);
    --chat-body-height: calc(100dvh - var(--chat-header-height) - var(--chat-dock-height));
}}
body:has(.chat-page-bg),
body:has(.chat-page-bg) .stApp,
body:has(.chat-page-bg) [data-testid="stAppViewContainer"],
body:has(.chat-page-bg) [data-testid="stMainViewContainer"],
body:has(.chat-page-bg) [data-testid="stMain"],
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"],
body:has(.chat-page-bg) [data-testid="stMainViewBlockContainer"],
body:has(.chat-page-bg) .block-container {{
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    overflow: hidden !important;
}}
body:has(.chat-page-bg) [data-testid="stMainBlockContainer"],
body:has(.chat-page-bg) [data-testid="stMainViewBlockContainer"],
body:has(.chat-page-bg) .block-container {{
    display: flex !important;
    flex-direction: column !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_shell,
body:has(.st-key-chat_shell) .st-key-chat_shell > div[data-testid="stVerticalBlock"],
body:has(.st-key-chat_shell) .st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main),
body:has(.st-key-chat_shell) div[data-testid="column"]:has(.st-key-chat_main),
body:has(.st-key-chat_shell) div[data-testid="stColumn"]:has(.st-key-chat_main),
body:has(.st-key-chat_shell) .st-key-chat_main,
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] {{
    height: 100vh !important;
    height: 100dvh !important;
    min-height: 0 !important;
    max-height: 100dvh !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_shell div[data-testid="stHorizontalBlock"]:has(.st-key-chat_sidebar):has(.st-key-chat_main) {{
    flex-direction: row !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_header),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_header) {{
    flex: 0 0 auto !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_body),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_body) {{
    flex: 0 1 var(--chat-body-height) !important;
    height: var(--chat-body-height) !important;
    min-height: 0 !important;
    max-height: var(--chat-body-height) !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}}
body:has(.st-key-chat_shell) div[key="chat_body"],
body:has(.st-key-chat_shell) .st-key-chat_body {{
    flex: 0 1 var(--chat-body-height) !important;
    display: block !important;
    height: var(--chat-body-height) !important;
    min-height: 0 !important;
    max-height: var(--chat-body-height) !important;
    padding-bottom: 1rem !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    overscroll-behavior: contain !important;
    scroll-behavior: smooth !important;
    scrollbar-gutter: stable !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_body > div[data-testid="stVerticalBlock"],
body:has(.st-key-chat_shell) .st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"],
body:has(.st-key-chat_shell) .st-key-chat_body > div[data-testid="stVerticalBlockBorderWrapper"] > div,
body:has(.st-key-chat_shell) .st-key-chat_body_inner,
body:has(.st-key-chat_shell) .st-key-chat_body_inner > div[data-testid="stVerticalBlock"] {{
    display: block !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main > div[data-testid="stVerticalBlock"] > div:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main .element-container:has(.st-key-chat_dock_empty),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock),
body:has(.st-key-chat_shell) .st-key-chat_main div[data-testid="stElementContainer"]:has(.st-key-chat_dock_empty) {{
    flex: 0 0 0 !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin-top: 0 !important;
    overflow: visible !important;
    z-index: 100 !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"],
body:has(.st-key-chat_shell) .st-key-chat_dock,
body:has(.st-key-chat_shell) .st-key-chat_dock_empty {{
    position: fixed !important;
    bottom: 0 !important;
    left: var(--chat-sidebar-width, 0) !important;
    right: 0 !important;
    display: block !important;
    flex: 0 0 var(--chat-dock-height) !important;
    width: auto !important;
    height: var(--chat-dock-height) !important;
    min-height: 0 !important;
    max-height: var(--chat-dock-height) !important;
    padding: 0 clamp(1rem, 2.5vw, 2rem) 1rem !important;
    box-sizing: border-box !important;
    background: #070c14 !important;
    overflow: visible !important;
    z-index: 9999 !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_dock > div[data-testid="stVerticalBlock"],
body:has(.st-key-chat_shell) .st-key-chat_dock_empty > div[data-testid="stVerticalBlock"] {{
    height: 100% !important;
    min-height: 0 !important;
    max-height: 100% !important;
    overflow: visible !important;
}}
body:has(.st-key-chat_shell) .stChatInputContainer {{
    padding-bottom: 20px !important;
}}

/* Floating centered chat input pill. */
body:has(.st-key-chat_shell) .st-key-chat_shell {{
    --chat-dock-height: 5.75rem;
    --chat-body-height: calc(100dvh - var(--chat-header-height) - var(--chat-dock-height));
}}
body:has(.st-key-chat_shell) [data-testid="stBottom"],
body:has(.st-key-chat_shell) [data-testid="stBottomBlockContainer"],
body:has(.st-key-chat_shell) div:has(> div[data-testid="stChatInput"]) {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"],
body:has(.st-key-chat_shell) .st-key-chat_dock,
body:has(.st-key-chat_shell) .st-key-chat_dock_empty {{
    position: fixed !important;
    bottom: 35px !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) !important;
    width: 90% !important;
    max-width: 800px !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    padding: 0 !important;
    background-color: transparent !important;
    overflow: visible !important;
    z-index: 9999 !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_dock_inner,
body:has(.st-key-chat_shell) .st-key-chat_dock_empty_inner,
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] > div {{
    width: 100% !important;
    max-width: 800px !important;
    margin: 0 auto !important;
    border-radius: 35px !important;
    border: 1px solid #3e3e3e !important;
    padding: 5px !important;
    background-color: #1e1e1e !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, .5) !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_dock_inner,
body:has(.st-key-chat_shell) .st-key-chat_dock_empty_inner {{
    padding: 5px !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_input [data-testid="stHorizontalBlock"],
body:has(.st-key-chat_shell) .st-key-chat_input_empty [data-testid="stHorizontalBlock"] {{
    align-items: center !important;
    gap: .45rem !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_input .stTextInput [data-baseweb="base-input"],
body:has(.st-key-chat_shell) .st-key-chat_input_empty .stTextInput [data-baseweb="base-input"] {{
    height: 3rem !important;
    min-height: 3rem !important;
    border-radius: 32px !important;
    border: 1px solid transparent !important;
    background: #1e1e1e !important;
    box-shadow: none !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] textarea,
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] textarea:focus,
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] textarea:focus-visible {{
    background-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}}
body:has(.st-key-chat_shell) .st-key-chat_input .stTextInput input,
body:has(.st-key-chat_shell) .st-key-chat_input_empty .stTextInput input {{
    height: 3rem !important;
    line-height: 3rem !important;
    color: #f4f7fb !important;
    background: transparent !important;
}}
body:has(.st-key-chat_shell) .st-key-send_btn .stFormSubmitButton > button,
body:has(.st-key-chat_shell) .st-key-send_btn_empty .stFormSubmitButton > button {{
    width: 3rem !important;
    min-width: 3rem !important;
    height: 3rem !important;
    min-height: 3rem !important;
    border-radius: 999px !important;
}}
body:has(.st-key-chat_shell) div[key="chat_body"],
body:has(.st-key-chat_shell) .st-key-chat_body {{
    padding-bottom: 150px !important;
}}

/* Ghost dock: make Streamlit's bottom host click-through while the input floats. */
body:has(.st-key-chat_shell) [data-testid="stBottom"],
body:has(.st-key-chat_shell) [data-testid="stBottomBlockContainer"],
body:has(.st-key-chat_shell) div:has(> div[data-testid="stChatInput"]) {{
    display: block !important;
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    right: auto !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    flex: 0 0 0 !important;
    flex-basis: 0 !important;
    overflow: visible !important;
    background: none !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    pointer-events: none !important;
    z-index: auto !important;
}}
body:has(.st-key-chat_shell) [data-testid="stBottom"] > div,
body:has(.st-key-chat_shell) [data-testid="stBottomBlockContainer"] > div {{
    padding: 0 !important;
    margin: 0 !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: visible !important;
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    pointer-events: none !important;
}}
body:has(.st-key-chat_shell) [data-testid="stSidebar"] {{
    position: relative !important;
    z-index: 1000 !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 40px !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) !important;
    z-index: 10001 !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 85% !important;
    max-width: 800px !important;
    min-height: 0 !important;
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    background-color: transparent !important;
    pointer-events: auto !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] > div {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 100% !important;
    max-width: 800px !important;
    margin: 0 auto !important;
    background-color: #1e1e1e !important;
    border: 1px solid #3e3e3e !important;
    border-radius: 35px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, .6) !important;
    pointer-events: auto !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] textarea,
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] textarea:focus,
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] textarea:focus-visible {{
    visibility: visible !important;
    opacity: 1 !important;
    color: #f4f7fb !important;
    caret-color: #f4f7fb !important;
    background-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    pointer-events: auto !important;
}}

/* Clean slate: remove Streamlit bottom-dock paint without hiding floating controls. */
body:has(.onboarding-page-bg) [data-testid="stBottom"],
body:has(.onboarding-page-bg) [data-testid="stBottom"] > div,
body:has(.onboarding-page-bg) [data-testid="stBottomBlockContainer"],
body:has(.onboarding-page-bg) [data-testid="stBottomBlockContainer"] > div,
body:has(.st-key-chat_shell) [data-testid="stBottom"],
body:has(.st-key-chat_shell) [data-testid="stBottom"] > div,
body:has(.st-key-chat_shell) [data-testid="stBottomBlockContainer"],
body:has(.st-key-chat_shell) [data-testid="stBottomBlockContainer"] > div,
body:has(.st-key-chat_shell) .stChatInputContainer,
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] {{
    background: none !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    backdrop-filter: none !important;
}}
body:has(.onboarding-page-bg) [data-testid="stBottom"],
body:has(.onboarding-page-bg) [data-testid="stBottomBlockContainer"],
body:has(.st-key-chat_shell) [data-testid="stBottom"],
body:has(.st-key-chat_shell) [data-testid="stBottomBlockContainer"] {{
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: visible !important;
    pointer-events: none !important;
}}
body:has(.onboarding-page-bg) .element-container:has(.st-key-ob_nav_back),
body:has(.onboarding-page-bg) div[data-testid="stElementContainer"]:has(.st-key-ob_nav_back),
body:has(.onboarding-page-bg) .st-key-ob_nav_back,
body:has(.onboarding-page-bg) .element-container:has(.st-key-ob_nav_next),
body:has(.onboarding-page-bg) div[data-testid="stElementContainer"]:has(.st-key-ob_nav_next),
body:has(.onboarding-page-bg) .st-key-ob_nav_next {{
    background: none !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    pointer-events: auto !important;
    z-index: 10001 !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back .stButton > button,
body:has(.onboarding-page-bg) .st-key-ob_nav_next .stButton > button {{
    pointer-events: auto !important;
    background-color: #1e63f8 !important;
    border-radius: 50% !important;
    z-index: 10001 !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] {{
    pointer-events: auto !important;
}}
body:has(.st-key-chat_shell) div[data-testid="stChatInput"] > div {{
    background-color: #1e1e1e !important;
    border: 1px solid #3e3e3e !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, .6) !important;
}}

/* Onboarding final paint pass: one solid background and blue arrow controls. */
html:has(.onboarding-page-bg),
body:has(.onboarding-page-bg),
body:has(.onboarding-page-bg) #root,
body:has(.onboarding-page-bg) .stApp,
body:has(.onboarding-page-bg) [data-testid="stAppViewContainer"],
body:has(.onboarding-page-bg) [data-testid="stMain"],
body:has(.onboarding-page-bg) [data-testid="stMainBlockContainer"],
body:has(.onboarding-page-bg) [data-testid="stMainViewBlockContainer"],
body:has(.onboarding-page-bg) .block-container,
body:has(.onboarding-page-bg) .onboarding-page-bg {{
    background: #071426 !important;
    background-color: #071426 !important;
    background-image: none !important;
    box-shadow: none !important;
}}
body:has(.onboarding-page-bg) [data-testid="stMainBlockContainer"],
body:has(.onboarding-page-bg) [data-testid="stMainViewBlockContainer"] {{
    width: 100vw !important;
    max-width: 100vw !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back .stButton button,
body:has(.onboarding-page-bg) .st-key-ob_nav_next .stButton button,
body:has(.onboarding-page-bg) [class*="st-key-ob_nav_back_btn_"] button,
body:has(.onboarding-page-bg) [class*="st-key-ob_nav_next_btn_"] button {{
    width: 64px !important;
    min-width: 64px !important;
    height: 64px !important;
    min-height: 64px !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 50% !important;
    background: #1e63f8 !important;
    background-color: #1e63f8 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(30, 99, 248, .4), 0 18px 40px rgba(30, 99, 248, .22) !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    line-height: 1 !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_nav_back .stButton button:hover,
body:has(.onboarding-page-bg) .st-key-ob_nav_next .stButton button:hover,
body:has(.onboarding-page-bg) [class*="st-key-ob_nav_back_btn_"] button:hover,
body:has(.onboarding-page-bg) [class*="st-key-ob_nav_next_btn_"] button:hover {{
    background: #1649c1 !important;
    background-color: #1649c1 !important;
    color: #ffffff !important;
}}

/* Onboarding fields: consistent dark navy input style. */
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput [data-baseweb="base-input"],
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox > div > div,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox [data-baseweb="select"],
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox [data-baseweb="select"] > div,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput > div > div,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput [data-baseweb="input"],
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput [data-baseweb="input"] > div {{
    height: 3.1rem !important;
    min-height: 3.1rem !important;
    border: 1px solid rgba(120, 151, 214, .32) !important;
    border-radius: .85rem !important;
    background: #081226 !important;
    background-color: #081226 !important;
    box-shadow: none !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput [data-baseweb="base-input"]:focus-within,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox > div > div:focus-within,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput > div > div:focus-within {{
    border-color: rgba(77, 141, 240, .82) !important;
    box-shadow: 0 0 0 3px rgba(77, 141, 240, .18) !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput [data-baseweb="base-input"] > div,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput input,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox [data-baseweb="select"] *,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput [data-baseweb="input"] *,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput button {{
    background: transparent !important;
    background-color: transparent !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput input,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox [data-baseweb="select"] *,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox [data-testid="stMarkdownContainer"] *,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input::-webkit-datetime-edit,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input::-webkit-datetime-edit-text,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input::-webkit-datetime-edit-month-field,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input::-webkit-datetime-edit-day-field,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput input::-webkit-datetime-edit-year-field {{
    color: #ffffff !important;
    caret-color: #ffffff !important;
    line-height: 3.1rem !important;
    text-shadow: none !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput input {{
    padding: 0 1.2rem !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard .stSelectbox svg,
body:has(.onboarding-page-bg) .st-key-ob_wizard .stDateInput svg {{
    color: #ffffff !important;
    fill: #ffffff !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard .stTextInput input::placeholder {{
    color: rgba(184, 208, 255, .5) !important;
}}

/* PaceUp UI polish overrides: keep this as the final cascade layer. */
body:has(.onboarding-page-bg) [data-testid="stMainBlockContainer"],
body:has(.onboarding-page-bg) [data-testid="stMainViewBlockContainer"],
body:has(.onboarding-page-bg) .block-container {{
    min-height: 100vh !important;
    min-height: 100dvh !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 clamp(1rem, 3vw, 2rem) !important;
    box-sizing: border-box !important;
}}
body:has(.onboarding-page-bg) [data-testid="stMainBlockContainer"] > div,
body:has(.onboarding-page-bg) [data-testid="stMainViewBlockContainer"] > div {{
    width: min(800px, 100%) !important;
    min-height: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard {{
    width: min(34rem, 100%) !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_wizard > div[data-testid="stVerticalBlock"] {{
    width: 100% !important;
}}
body:has(.onboarding-page-bg) .ob-brand,
body:has(.onboarding-page-bg) .ob-kicker {{
    justify-content: center !important;
    text-align: center !important;
}}
body:has(.onboarding-page-bg) .ob-progress-meta {{
    justify-content: center !important;
    gap: .85rem !important;
    text-align: center !important;
}}
body:has(.onboarding-page-bg) .ob-headline,
body:has(.onboarding-page-bg) .ob-sub,
body:has(.onboarding-page-bg) .ob-field-label,
body:has(.onboarding-page-bg) .ob-disclaimer,
body:has(.onboarding-page-bg) .st-key-ob_wizard [data-testid="stMarkdownContainer"] p {{
    text-align: center !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_race_grid .stButton > button,
body:has(.onboarding-page-bg) .st-key-ob_fit_grid .stButton > button {{
    text-align: center !important;
    justify-content: center !important;
    align-items: center !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_race_grid .stButton > button p,
body:has(.onboarding-page-bg) .st-key-ob_fit_grid .stButton > button p {{
    text-align: center !important;
    color: #A0A0A0 !important;
}}
body:has(.onboarding-page-bg) .st-key-ob_race_grid .stButton > button p strong,
body:has(.onboarding-page-bg) .st-key-ob_fit_grid .stButton > button p strong {{
    color: #f2f6ff !important;
}}

body:has(.chat-page-bg) {{
    --chat-sidebar-width: 260px;
    --chat-input-left: calc(var(--chat-sidebar-width) + ((100vw - var(--chat-sidebar-width)) / 2));
    --chat-input-width: min(800px, calc(100vw - var(--chat-sidebar-width) - clamp(2rem, 5vw, 4rem)));
}}
body:has(.chat-page-bg) .st-key-chat_body_inner,
body:has(.chat-page-bg) .st-key-chat_body_inner > div[data-testid="stVerticalBlock"] {{
    width: min(800px, 100%) !important;
    max-width: 800px !important;
    margin-left: auto !important;
    margin-right: auto !important;
}}
body:has(.chat-page-bg) [data-testid="stBottom"],
body:has(.chat-page-bg) [data-testid="stBottomBlockContainer"],
body:has(.chat-page-bg) div:has(> div[data-testid="stChatInput"]) {{
    display: block !important;
    position: fixed !important;
    inset: auto 0 0 0 !important;
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    flex: 0 0 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    backdrop-filter: none !important;
    overflow: visible !important;
    pointer-events: none !important;
    z-index: 10000 !important;
}}
body:has(.chat-page-bg) [data-testid="stBottom"] > div,
body:has(.chat-page-bg) [data-testid="stBottomBlockContainer"] > div {{
    width: 100% !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    overflow: visible !important;
    pointer-events: none !important;
}}
body:has(.chat-page-bg) div[data-testid="stChatInput"] {{
    position: fixed !important;
    left: var(--chat-input-left) !important;
    right: auto !important;
    bottom: 2.5rem !important;
    transform: translateX(-50%) !important;
    width: var(--chat-input-width) !important;
    max-width: 800px !important;
    min-width: 0 !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    overflow: visible !important;
    pointer-events: auto !important;
    z-index: 10002 !important;
}}
body:has(.chat-page-bg) div[data-testid="stChatInput"] *,
body:has(.chat-page-bg) div[data-testid="stChatInput"] > div {{
    pointer-events: auto !important;
}}
body:has(.chat-page-bg) div[data-testid="stChatInput"] > div {{
    width: 100% !important;
    max-width: 800px !important;
    margin: 0 auto !important;
    border-radius: 35px !important;
    border: 1px solid #3e3e3e !important;
    background: #1e1e1e !important;
    background-color: #1e1e1e !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, .6) !important;
}}
body:has(.chat-page-bg) .stChatInputContainer {{
    width: 100% !important;
    max-width: 800px !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    pointer-events: none !important;
}}
body:has(.chat-page-bg) .st-key-chat_suggestions,
body:has(.chat-page-bg) .st-key-chat_suggestions_empty {{
    position: fixed !important;
    left: var(--chat-input-left) !important;
    bottom: 6.45rem !important;
    transform: translateX(-50%) !important;
    width: var(--chat-input-width) !important;
    max-width: 800px !important;
    z-index: 10001 !important;
    pointer-events: auto !important;
}}
body:has(.chat-page-bg) .st-key-chat_suggestions div[data-testid="stHorizontalBlock"],
body:has(.chat-page-bg) .st-key-chat_suggestions_empty div[data-testid="stHorizontalBlock"] {{
    gap: .45rem !important;
    flex-wrap: wrap !important;
}}
body:has(.chat-page-bg) .st-key-chat_suggestions .stButton > button,
body:has(.chat-page-bg) .st-key-chat_suggestions_empty .stButton > button {{
    min-height: 2rem !important;
    height: 2rem !important;
    padding: 0 .65rem !important;
    border-radius: 999px !important;
    border: 1px solid rgba(177, 198, 255, .16) !important;
    background: rgba(15, 25, 50, .72) !important;
    color: #A0A0A0 !important;
    font-size: .76rem !important;
    font-weight: 600 !important;
    line-height: 1 !important;
    box-shadow: none !important;
}}
body:has(.chat-page-bg) .st-key-chat_suggestions .stButton > button:hover,
body:has(.chat-page-bg) .st-key-chat_suggestions_empty .stButton > button:hover {{
    background: rgba(30, 52, 84, .74) !important;
    border-color: rgba(177, 198, 255, .28) !important;
    color: #f4f7fb !important;
    opacity: 1 !important;
}}

@media (max-width: 720px) {{
    body:has(.chat-page-bg) {{
        --chat-sidebar-width: 0px;
        --chat-input-left: 50%;
        --chat-input-width: calc(100vw - 2rem);
    }}
    body:has(.chat-page-bg) div[data-testid="stChatInput"] {{
        bottom: 1.25rem !important;
    }}
    body:has(.chat-page-bg) .st-key-chat_suggestions,
    body:has(.chat-page-bg) .st-key-chat_suggestions_empty {{
        bottom: 5.25rem !important;
    }}
}}

[data-testid="stSidebarNav"] ul li {{
    height: auto !important;
    margin-bottom: 10px !important;
}}
body:has(.chat-page-bg) .st-key-chat_sessions .stButton > button,
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button {{
    min-height: 2.45rem !important;
    height: 2.45rem !important;
    padding: .42rem .72rem .58rem !important;
    align-items: center !important;
    line-height: 1.35 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}}
body:has(.chat-page-bg) .st-key-chat_sessions .stButton > button [data-testid="stMarkdownContainer"],
body:has(.chat-page-bg) .st-key-chat_sessions .stButton > button p,
body:has(.chat-page-bg) .st-key-chat_sessions .stButton > button span,
body:has(.chat-page-bg) .st-key-chat_sessions .stButton > button strong,
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button [data-testid="stMarkdownContainer"],
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button p,
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button span,
body:has(.st-key-chat_shell) .st-key-chat_sessions .stButton > button strong {{
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding-bottom: .04rem !important;
    line-height: 1.35 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}}

/* Visible Voice: keep live and completed chat responses readable. */
body:has(.chat-page-bg) .chat-msg,
body:has(.chat-page-bg) .chat-msg *,
body:has(.chat-page-bg) .msg-bubble,
body:has(.chat-page-bg) .msg-bubble *,
body:has(.chat-page-bg) .assistant-response,
body:has(.chat-page-bg) .assistant-response *,
body:has(.chat-page-bg) .st-key-streaming_msg,
body:has(.chat-page-bg) .st-key-streaming_msg *,
body:has(.chat-page-bg) .st-key-streaming_bubble,
body:has(.chat-page-bg) .st-key-streaming_bubble *,
body:has(.chat-page-bg) [data-testid="stChatMessage"],
body:has(.chat-page-bg) [data-testid="stChatMessage"] *,
body:has(.chat-page-bg) div[data-testid="stChatMessageContent"],
body:has(.chat-page-bg) div[data-testid="stChatMessageContent"] * {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    filter: none !important;
    text-shadow: none !important;
}}
body:has(.chat-page-bg) .assistant-response p,
body:has(.chat-page-bg) .assistant-response li,
body:has(.chat-page-bg) .assistant-response strong,
body:has(.chat-page-bg) .assistant-response em,
body:has(.chat-page-bg) .assistant-response code,
body:has(.chat-page-bg) .msg-bubble p,
body:has(.chat-page-bg) .msg-bubble li,
body:has(.chat-page-bg) .st-key-streaming_bubble [data-testid="stMarkdownContainer"],
body:has(.chat-page-bg) .st-key-streaming_bubble [data-testid="stMarkdownContainer"] *,
body:has(.chat-page-bg) [data-testid="stChatMessage"] p,
body:has(.chat-page-bg) [data-testid="stChatMessage"] li,
body:has(.chat-page-bg) [data-testid="stChatMessage"] strong,
body:has(.chat-page-bg) [data-testid="stChatMessage"] em,
body:has(.chat-page-bg) [data-testid="stChatMessage"] code {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
}}
body:has(.chat-page-bg) .st-key-chat_body_inner .chat-msg:last-of-type,
body:has(.chat-page-bg) .st-key-chat_body_inner .chat-msg:last-of-type *,
body:has(.chat-page-bg) .st-key-streaming_msg,
body:has(.chat-page-bg) .st-key-streaming_msg *,
body:has(.chat-page-bg) .stChatInputContainer + div .stChatMessage:last-child,
body:has(.chat-page-bg) .stChatInputContainer + div .stChatMessage:last-child * {{
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
    filter: none !important;
}}

</style>
""", unsafe_allow_html=True)


# ── Navbar ────────────────────────────────────────────────────────────────────


