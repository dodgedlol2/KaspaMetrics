"""
Kaspa Analytics Pro - Main Homepage
Entry point for the multi-page Streamlit application with sectioned navigation
"""

import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime
import pandas as pd
import numpy as np

# Try to import Plotly, fallback gracefully
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Import utilities
from utils.auth import get_current_user, is_authenticated
from utils.data import fetch_kaspa_price_data, get_market_stats
from utils.ui import (
    render_page_header, 
    show_login_prompt,
    apply_custom_css,
    render_footer
)
from utils.config import get_app_config

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro - Professional Blockchain Analysis",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://kaspa-analytics.com/help',
        'Report a bug': 'https://kaspa-analytics.com/bug-report',
        'About': "# Kaspa Analytics Pro\nProfessional blockchain analysis platform"
    }
)

# SEO and Social Media Meta Tags
st.markdown("""
<meta name="description" content="Professional Kaspa blockchain analysis platform with advanced power law models, network metrics, and real-time price tracking.">
<meta name="keywords" content="Kaspa, KAS, blockchain, cryptocurrency, analysis, power law, price prediction, technical analysis">
<meta name="author" content="Kaspa Analytics Pro">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://kaspa-analytics.com/">
<meta property="og:title" content="Kaspa Analytics Pro - Professional Blockchain Analysis">
<meta property="og:description" content="Advanced Kaspa blockchain analysis with power law models, network metrics, and professional trading tools.">
<meta property="og:image" content="https://kaspa-analytics.com/assets/social_preview.png">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://kaspa-analytics.com/">
<meta property="twitter:title" content="Kaspa Analytics Pro">
<meta property="twitter:description" content="Professional Kaspa blockchain analysis platform">
<meta property="twitter:image" content="https://kaspa-analytics.com/assets/social_preview.png">

<!-- Favicon -->
<link rel="icon" type="image/png" href="/assets/favicon.ico">
""", unsafe_allow_html=True)

# Apply custom CSS
apply_custom_css()

# Google Analytics (placeholder)
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)

# Page definitions
dashboard_page = st.Page("views/dashboard.py", title="🏠 Dashboard", icon="🏠")
price_charts_page = st.Page("views/price_charts.py", title="📈 Price Charts", icon="📈")
power_law_page = st.Page("views/power_law.py", title="📊 Power Law", icon="📊")
network_metrics_page = st.Page("views/network_metrics.py", title="🌐 Network Metrics", icon="🌐")
data_export_page = st.Page("views/data_export.py", title="📋 Data Export", icon="📋")
authentication_page = st.Page("views/authentication.py", title="⚙️ Account", icon="⚙️")
admin_panel_page = st.Page("views/admin_panel.py", title="👑 Admin Panel", icon="👑")

def get_navigation_structure():
    """Get navigation structure based on user subscription"""
    user = get_current_user()
    subscription = user['subscription']
    
    # Base navigation structure
    navigation = {
        "💎 Kaspa Analytics": [dashboard_page],
        "📊 Spot Analysis": [price_charts_page],
    }
    
    # Add On-Chain section for premium+ users
    if subscription in ['premium', 'pro']:
        navigation["🌐 On-Chain Metrics"] = [network_metrics_page]
    
    # Add Miners section for premium+ users
    if subscription in ['premium', 'pro']:
        navigation["⛏️ Miners"] = [power_law_page]
    
    # Account section
    account_pages = [authentication_page]
    
    # Add data export for premium+ users
    if subscription in ['premium', 'pro']:
        account_pages.append(data_export_page)
    
    # Add admin panel for admin user
    if user['username'] == 'admin':
        account_pages.append(admin_panel_page)
    
    navigation["👤 Account"] = account_pages
    
    return navigation

def main():
    """Main application entry point"""
    
    # Get navigation structure
    navigation = get_navigation_structure()
    
    # Set up navigation
    pg = st.navigation(navigation)
    
    # Add user info to sidebar
    user = get_current_user()
    
    with st.sidebar:
        st.markdown("---")
        
        # User status
        if user['username'] != 'public':
            st.markdown(f"**👤 {user['name']}**")
            st.markdown(f'<span class="subscription-badge badge-{user["subscription"]}">{user["subscription"].upper()}</span>', unsafe_allow_html=True)
        else:
            st.markdown("**👤 Public Access**")
            st.markdown('<span class="subscription-badge badge-public">PUBLIC</span>', unsafe_allow_html=True)
        
        # Quick stats
        render_sidebar_stats()
    
    # Run the selected page
    pg.run()

def render_sidebar_stats():
    """Render quick stats in sidebar"""
    st.markdown("---")
    st.markdown("### ⚡ Quick Stats")
    
    try:
        df = fetch_kaspa_price_data(7)  # Last 7 days for sidebar
        if not df.empty:
            stats = get_market_stats(df)
            
            st.metric(
                "KAS Price", 
                f"${stats.get('current_price', 0):.4f}",
                delta=f"{stats.get('price_change_24h', 0):+.2f}%"
            )
            
            st.metric(
                "24h Volume", 
                f"${stats.get('volume_24h', 0)/1000000:.1f}M"
            )
        else:
            st.info("Unable to load market data")
    except Exception as e:
        st.error("Market data unavailable")

if __name__ == "__main__":
    main()
