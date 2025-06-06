import streamlit as st
from utils.auth import get_current_user
from utils.ui import render_page_header, show_login_prompt

def main():
    user = get_current_user()
    
    if user['username'] == 'public':
        show_login_prompt("Power Law analysis")
        st.stop()
    
    render_page_header(
        "📊 Power Law Analysis",
        "Mathematical price prediction models"
    )
    
    # Copy your power law content from the old file here
    st.info("📊 Power Law analysis content - copy from your existing file")

if __name__ == "__main__":
    main()
