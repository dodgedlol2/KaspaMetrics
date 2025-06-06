import streamlit as st
from utils.auth import get_authenticator
from utils.ui import render_page_header

def main():
    render_page_header(
        "🔑 Login",
        "Sign in to your Kaspa Analytics account"
    )
    
    # Copy your login code from the old authentication.py file here
    authenticator = get_authenticator()
    
    try:
        authenticator.login()
        
        if st.session_state.get('authentication_status') == True:
            st.success(f"✅ Welcome back!")
            st.rerun()
        elif st.session_state.get('authentication_status') == False:
            st.error("❌ Incorrect credentials")
        else:
            st.info("ℹ️ Please enter your credentials")
    
    except Exception as e:
        st.error(f"Login error: {e}")

if __name__ == "__main__":
    main()
