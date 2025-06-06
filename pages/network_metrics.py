import streamlit as st
from utils.auth import get_current_user
from utils.ui import render_page_header, show_upgrade_prompt

def main():
    user = get_current_user()
    
    if user['subscription'] not in ['premium', 'pro']:
        show_upgrade_prompt(user['subscription'], 'premium')
        st.stop()
    
    render_page_header(
        "🌐 Network Metrics",
        "Kaspa network health and statistics"
    )
    
    # Copy your network metrics content here
    st.success("🌐 Network metrics content - copy from your existing file")

if __name__ == "__main__":
    main()
