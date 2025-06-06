"""
Network Metrics Page - Kaspa Analytics Pro
Simple placeholder for now
"""

import streamlit as st
from utils.auth import get_current_user, check_feature_access
from utils.ui import render_page_header, render_sidebar_navigation, show_upgrade_prompt, apply_custom_css

# Configure page
st.set_page_config(
    page_title="Network Metrics - Kaspa Analytics Pro",
    page_icon="🌐",
    layout="wide"
)

apply_custom_css()

def main():
    user = get_current_user()
    render_sidebar_navigation(user)
    
    render_page_header("🌐 Network Metrics", "Kaspa blockchain network analysis")
    
    # Back button
    if st.button("← Dashboard", key="network_back"):
        st.switch_page("streamlit_app.py")
    
    # Check access (Premium+ only)
    if user['subscription'] not in ['premium', 'pro']:
        st.error("🔒 This feature requires Premium or Pro subscription")
        show_upgrade_prompt(user['subscription'], 'premium')
        return
    
    # Simple content for premium users
    st.success(f"🎉 {user['subscription'].title()} Account - Network Metrics Available!")
    
    # Placeholder metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Hash Rate", "1.23 EH/s", "+5.2%")
    with col2:
        st.metric("Difficulty", "3.45E+15", "+2.1%")
    with col3:
        st.metric("Block Time", "1.02s", "-0.02s")
    with col4:
        st.metric("Active Addresses", "45,231", "+12.5%")
    
    # Placeholder content
    st.subheader("🚧 Coming Soon")
    st.write("Detailed network metrics analysis will be implemented here.")

if __name__ == "__main__":
    main()
