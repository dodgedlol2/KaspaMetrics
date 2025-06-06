"""
Admin Panel Page - Kaspa Analytics Pro
Simple placeholder for now
"""

import streamlit as st
from utils.auth import get_current_user
from utils.ui import render_page_header, render_sidebar_navigation, apply_custom_css

# Configure page
st.set_page_config(
    page_title="Admin Panel - Kaspa Analytics Pro",
    page_icon="👑",
    layout="wide"
)

apply_custom_css()

def main():
    user = get_current_user()
    render_sidebar_navigation(user)
    
    # Check admin access
    if user['username'] != 'admin':
        st.error("🔒 Access denied. Admin only.")
        st.info("This page is restricted to administrators.")
        if st.button("← Back to Dashboard", key="admin_denied_back"):
            st.switch_page("streamlit_app.py")
        return
    
    render_page_header("👑 Admin Panel", "System administration and user management")
    
    # Back button
    if st.button("← Dashboard", key="admin_back"):
        st.switch_page("streamlit_app.py")
    
    # Simple admin content
    st.success("👑 Administrator Access Granted")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "156")
    with col2:
        st.metric("Free Users", "98")
    with col3:
        st.metric("Premium Users", "42")
    with col4:
        st.metric("Pro Users", "16")
    
    # Simple admin actions
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(3)
    
    with action_cols[0]:
        if st.button("👥 Manage Users", use_container_width=True):
            st.info("User management interface would go here")
    
    with action_cols[1]:
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("System analytics would go here")
    
    with action_cols[2]:
        if st.button("⚙️ System Settings", use_container_width=True):
            st.info("System settings would go here")
    
    # Placeholder content
    st.subheader("🚧 Coming Soon")
    st.write("Full admin panel features will be implemented here.")

if __name__ == "__main__":
    main()
