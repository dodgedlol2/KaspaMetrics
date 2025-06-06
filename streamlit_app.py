# Replace the create_navigation_pages() function in streamlit_app.py
def create_navigation_pages():
    """Create navigation pages based on user subscription with better grouping"""
    user = get_current_user()
    subscription = user['subscription']
    
    # Start with Dashboard for everyone
    pages = {
        "🏠 Home": [
            st.Page("pages/dashboard.py", title="🏠 Dashboard", icon="🏠"),
        ],
    }
    
    # Analytics section - always show Price Charts
    analytics_pages = [
        st.Page("pages/price_charts.py", title="📈 Price Charts", icon="📈"),
    ]
    
    # Add Power Law for authenticated users
    if subscription != 'public':
        analytics_pages.append(
            st.Page("pages/power_law.py", title="📊 Power Law", icon="📊")
        )
    
    # Add Network Metrics for premium+ users
    if check_feature_access('network_metrics', subscription):
        analytics_pages.append(
            st.Page("pages/network_metrics.py", title="🌐 Network Metrics", icon="🌐")
        )
    
    # Add the analytics section
    pages["📊 Analytics"] = analytics_pages
    
    # Data section for premium+ users
    if check_feature_access('data_export', subscription):
        pages["💾 Data"] = [
            st.Page("pages/data_export.py", title="📋 Data Export", icon="📋"),
        ]
    
    # Account section
    if subscription == 'public':
        pages["👤 Account"] = [
            st.Page("pages/auth_login.py", title="🔑 Login", icon="🔑"),
            st.Page("pages/auth_register.py", title="🚀 Sign Up", icon="🚀"),
        ]
    else:
        account_pages = [
            st.Page("pages/profile.py", title="👤 Profile", icon="👤"),
            st.Page("pages/settings.py", title="⚙️ Settings", icon="⚙️"),
        ]
        
        # Add admin panel for admin users
        if user['username'] == 'admin':
            account_pages.append(
                st.Page("pages/admin_panel.py", title="👑 Admin Panel", icon="👑")
            )
        
        pages["👤 Account"] = account_pages
    
    return pages
