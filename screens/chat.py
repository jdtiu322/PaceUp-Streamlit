from __future__ import annotations

import html

import streamlit as st

from services.firebase import build_chat_profile
from services.firestore_chat import create_chat_session, load_chat_sessions, load_messages_for_session, save_message_to_firestore
from services.gemini import get_gemini_response
from state import logout_user


def show_chat() -> None:
    user = st.session_state.user
    profile = build_chat_profile(user)
    st.session_state.user_profile = profile

    name = profile.get("display_name") or user.email.split("@", 1)[0]
    initials = "".join(word[0].upper() for word in name.split()[:2]) or "P"
    goal = profile.get("goal_distance", "Marathon Training")

    if not st.session_state.chat_sessions:
        st.session_state.chat_sessions = load_chat_sessions(user.uid)

    sidebar, main = st.columns([0.22, 0.78], gap="small")

    with sidebar:
        st.markdown('<div class="chat-sidebar-header"><div class="sidebar-logo"><span class="lp">PACE</span><span class="lu">UP</span></div></div>', unsafe_allow_html=True)
        with st.container(key="new_chat_btn"):
            if st.button("+  New Chat", key="btn_new_chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.active_session_id = None
                st.rerun()
        st.markdown('<div class="sidebar-section-label">Chat History</div>', unsafe_allow_html=True)
        sessions = st.session_state.chat_sessions
        if sessions:
            for session in sessions:
                title = session.get("title", "New conversation")
                label = f"{'> ' if session['id'] == st.session_state.active_session_id else ''}{title}"
                if st.button(label, key=f"sess_{session['id']}", use_container_width=True):
                    st.session_state.active_session_id = session["id"]
                    st.session_state.messages = load_messages_for_session(user.uid, session["id"])
                    st.rerun()
        else:
            st.markdown('<div style="font-size:12px;color:#aaa;padding:4px 0;">No chats yet</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="user-card">
            <div class="user-avatar">{initials}</div>
            <div>
                <div class="user-name">{html.escape(name)}</div>
                <div class="user-email">{html.escape(user.email)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.container(key="signout_sidebar"):
            if st.button("Sign out", key="btn_signout_chat", use_container_width=True):
                logout_user()

    with main:
        st.markdown(f"""
        <div class="chat-header-bar">
            <div class="chat-header-title">PaceUp Coach</div>
            <div class="chat-header-sub">Goal: {html.escape(str(goal))}</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.messages:
            st.markdown(f"""
            <div class="empty-chat">
                <div class="empty-chat-title">Hey {html.escape(name)}, ready to run?</div>
                <div class="empty-chat-sub">Ask me anything about your training, pace, nutrition, recovery, race prep, or just motivation to lace up today.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="chat-msg-wrap">', unsafe_allow_html=True)
            for msg in st.session_state.messages:
                role = msg["role"]
                content = msg["content"]
                is_user = role == "user"
                av_class = "user-av" if is_user else "bot-av"
                av_label = initials if is_user else "P"
                sender = "You" if is_user else "PaceUp"
                msg_class = "chat-msg user-msg" if is_user else "chat-msg"
                st.markdown(f"""
                <div class="{msg_class}">
                    <div class="msg-av {av_class}">{av_label}</div>
                    <div class="msg-inner">
                        <div class="msg-sender">{sender}</div>
                        <div class="msg-bubble">{html.escape(content)}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        prompts = ["Generate my plan", "Nutrition tips", "Recovery advice", "Pace calculator", "Race day tips"]
        triggered_prompt = None
        with st.container(key="chat_suggestions"):
            qp_cols = st.columns(5)
            for i, (col, prompt) in enumerate(zip(qp_cols, prompts)):
                with col:
                    if st.button(prompt, key=f"qp_{i}", use_container_width=True):
                        triggered_prompt = prompt

        with st.container(key="chat_input"):
            ic, bc = st.columns([0.93, 0.07], gap="small")
            with ic:
                user_input = st.text_input("msg", placeholder="Message PaceUp...", label_visibility="collapsed", key="msg_input")
            with bc:
                with st.container(key="send_btn"):
                    send = st.button("Send", key="btn_send")

        st.markdown('<div class="disclaimer">PaceUp can make mistakes. Always consult a professional for medical advice.</div>', unsafe_allow_html=True)

        final_input = triggered_prompt or (user_input.strip() if (send and user_input) else None)

        if final_input:
            if not st.session_state.active_session_id:
                sid = create_chat_session(user.uid, final_input)
                st.session_state.active_session_id = sid
                st.session_state.chat_sessions = load_chat_sessions(user.uid)
            sid = st.session_state.active_session_id
            st.session_state.messages.append({"role": "user", "content": final_input})
            save_message_to_firestore(user.uid, sid, "user", final_input)
            with st.spinner("PaceUp is thinking..."):
                reply = get_gemini_response(st.session_state.messages, profile)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            save_message_to_firestore(user.uid, sid, "assistant", reply)
            st.rerun()
