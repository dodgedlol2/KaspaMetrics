import streamlit as st
from utils.auth import get_current_user
from utils.ui import render_page_header, show_upgrade_prompt

def main():
    user = get_current_user()
    
    if user['subscription'] not in ['premium', 'pro']:
        show_upgrade_prompt(user['subscription'], 'premium')
        st.stop()
    
    render_page_header(
        "📋 Data Export",
        "Download and export your analysis data"
    )
    
    # Copy your data export content here
    st.success("📋 Data export content - copy from your existing file")

if __name__ == "__main__":
    main()
