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

/* ── CHAT STYLES ── */
.chat-sidebar-header {{ padding: 16px 16px 8px; border-bottom: 1px solid var(--line); }}
.sidebar-logo {{ font-family: 'Barlow Condensed', sans-serif; font-size: 22px; font-weight: 800; letter-spacing: -.02em; }}
.sidebar-logo .lp {{ color: var(--navy); }}
.sidebar-logo .lu {{ color: var(--orange); }}
.sidebar-section-label {{ padding: 12px 4px 4px; font-size: 11px; font-weight: 700; color: var(--outline); text-transform: uppercase; letter-spacing: .08em; }}
.user-card {{ display: flex; align-items: center; gap: 10px; padding: 12px 0 4px; }}
.user-avatar {{ width: 34px; height: 34px; border-radius: 50%; background: var(--navy); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; flex-shrink: 0; }}
.user-name {{ font-size: 13px; font-weight: 700; color: var(--text); }}
.user-email {{ font-size: 11px; color: var(--outline); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 160px; }}
.chat-header-bar {{ padding: 12px 0 10px; border-bottom: 1px solid var(--line); margin-bottom: 4px; }}
.chat-header-title {{ font-family: 'Barlow Condensed', sans-serif; font-size: 22px; font-weight: 700; color: var(--navy); }}
.chat-header-sub {{ font-size: 12px; color: var(--outline); margin-top: 1px; }}
.chat-msg-wrap {{ display: flex; flex-direction: column; gap: 18px; padding: 8px 0 16px; }}
.chat-msg {{ display: flex; gap: 10px; align-items: flex-start; }}
.chat-msg.user-msg {{ flex-direction: row-reverse; }}
.msg-av {{ width: 30px; height: 30px; border-radius: 50%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; }}
.msg-av.bot-av {{ background: var(--navy); color: #fff; }}
.msg-av.user-av {{ background: var(--orange); color: #fff; }}
.msg-inner {{ display: flex; flex-direction: column; gap: 2px; max-width: 72%; }}
.msg-sender {{ font-size: 11px; font-weight: 700; color: var(--outline); }}
.chat-msg.user-msg .msg-sender {{ text-align: right; }}
.msg-bubble {{ font-size: 14px; line-height: 1.75; color: var(--text); padding: 10px 14px; border-radius: 10px; background: #f4f5f7; white-space: pre-wrap; }}
.chat-msg.user-msg .msg-bubble {{ background: #eef0fc; }}
.empty-chat {{ padding: 48px 0; text-align: center; }}
.empty-chat-title {{ font-family: 'Barlow Condensed', sans-serif; font-size: 26px; font-weight: 700; color: var(--navy); margin-bottom: 6px; }}
.empty-chat-sub {{ font-size: 14px; color: var(--outline); line-height: 1.7; max-width: 340px; margin: 0 auto; }}
.disclaimer {{ font-size: 11px; color: #bbb; text-align: center; margin-top: 6px; }}
.st-key-new_chat_btn .stButton > button {{ background: var(--navy) !important; color: #fff !important; border-radius: 6px !important; width: 100% !important; height: 2.2rem !important; font-size: 13px !important; margin-top: 8px !important; }}
.st-key-signout_sidebar .stButton > button {{ background: transparent !important; color: var(--outline) !important; border: 1px solid var(--line) !important; border-radius: 6px !important; width: 100% !important; height: 2rem !important; font-size: 12px !important; margin-top: 6px !important; }}
.st-key-send_btn .stButton > button {{ background: var(--navy) !important; color: #fff !important; border-radius: 50% !important; width: 2.8rem !important; height: 2.8rem !important; padding: 0 !important; font-size: 16px !important; min-width: 2.8rem !important; margin-top: 2px !important; }}
.st-key-chat_input .stTextInput input {{ height: 2.8rem !important; border-radius: 24px !important; border: 1px solid var(--line) !important; background: #f7f8fa !important; padding: 0 1.2rem !important; font-size: 14px !important; }}

/* ── FOOTER ── */
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
.st-key-chat_suggestions [data-testid="stHorizontalBlock"] {{ gap: .75rem !important; margin: .5rem 0 1rem; }}
.st-key-chat_suggestions .stButton > button {{
    width: 100% !important;
    min-height: 2.9rem !important;
    height: 2.9rem !important;
    border-radius: 999px !important;
    border: 1px solid rgba(0,5,104,.08) !important;
    background: var(--navy) !important;
    color: #fff !important;
    font-size: .92rem !important;
    font-weight: 700 !important;
    box-shadow: 0 10px 24px rgba(0,5,104,.08) !important;
}}
.st-key-chat_suggestions .stButton > button:hover,
.st-key-chat_suggestions .stButton > button:focus,
.st-key-chat_suggestions .stButton > button:focus-visible {{
    background: var(--navy-2) !important;
    color: #fff !important;
    border-color: rgba(0,5,104,.12) !important;
}}
</style>
""", unsafe_allow_html=True)


# ── Navbar ────────────────────────────────────────────────────────────────────


