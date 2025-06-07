"""
Kaspa Analytics Pro - Main Homepage
Entry point for the multi-page Streamlit application
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
    render_sidebar_navigation, 
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

def main():
    """Main homepage function"""
    
    # Get current user and app config
    user = get_current_user()
    config = get_app_config()
    is_auth = is_authenticated()
    
    # Render sidebar navigation
    render_sidebar_navigation(user)
    
    # Main content
    if is_auth:
        render_authenticated_homepage(user)
    else:
        render_public_homepage()
    
    # Footer
    render_footer()

def render_public_homepage():
    """Public homepage for non-authenticated users"""
    
    # Hero section
    render_page_header(
        "💎 Kaspa Analytics Pro",
        "Professional blockchain analysis platform for Kaspa (KAS)",
        show_auth_buttons=True
    )
    
    # Key metrics showcase
    st.subheader("📊 Live Market Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get market data
    df = fetch_kaspa_price_data()
    stats = get_market_stats(df) if not df.empty else {}
    
    with col1:
        st.metric(
            "KAS Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_7d', 0):+.2f}%"
        )
    
    with col2:
        st.metric(
            "24h Volume", 
            f"${stats.get('volume_24h', 0):,.0f}"
        )
    
    with col3:
        st.metric(
            "Market Cap", 
            f"${stats.get('market_cap', 0):.1f}B"
        )
    
    with col4:
        st.metric(
            "Network Hash Rate", 
            f"{stats.get('hash_rate', 0):.2f} EH/s"
        )
    
    # Quick chart preview (7 days for public)
    if not df.empty:
        st.subheader("📈 7-Day Price Preview")
        chart_data = df.tail(7)
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=chart_data['timestamp'], 
                y=chart_data['price'],
                mode='lines',
                name='KAS Price',
                line=dict(color='#70C7BA', width=3)
            ))
            
            fig.update_layout(
                title="Kaspa Price - Last 7 Days (Public Preview)",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=400,
                template="plotly_white",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback to basic line chart
            st.line_chart(chart_data.set_index('timestamp')['price'])
        
        st.info("📊 Public users see 7-day preview. Create a free account for 30+ days of data!")
    
    # Feature showcase
    st.subheader("🚀 Platform Features")
    
    feature_tabs = sac.tabs([
        sac.TabsItem(label='Analytics', icon='graph-up'),
        sac.TabsItem(label='Data Access', icon='database'),
        sac.TabsItem(label='Tools', icon='tools'),
    ], key='feature_showcase')
    
    if feature_tabs == 'Analytics':
        render_analytics_showcase()
    elif feature_tabs == 'Data Access':
        render_data_showcase()
    else:
        render_tools_showcase()
    
    # Pricing teaser
    st.subheader("💰 Choose Your Plan")
    
    pricing_cols = st.columns(3)
    
    with pricing_cols[0]:
        with st.container():
            st.markdown("### 🆓 Free")
            st.markdown("**$0/month**")
            st.write("• 30-day price history")
            st.write("• Basic power law analysis")
            st.write("• Community support")
            
            if st.button("🚀 Get Started Free", key="pricing_free", use_container_width=True, type="primary"):
                st.switch_page("pages/5_⚙️_Authentication.py")
    
    with pricing_cols[1]:
        with st.container():
            st.markdown("### ⭐ Premium")
            st.markdown("**$29/month**")
            st.write("• Full historical data")
            st.write("• Advanced analytics")
            st.write("• Data export")
            st.write("• Email support")
            
            if st.button("⭐ Upgrade to Premium", key="pricing_premium", use_container_width=True):
                st.switch_page("pages/5_⚙️_Authentication.py")
    
    with pricing_cols[2]:
        with st.container():
            st.markdown("### 👑 Pro")
            st.markdown("**$99/month**")
            st.write("• Everything in Premium")
            st.write("• API access")
            st.write("• Custom models")
            st.write("• Priority support")
            
            if st.button("👑 Go Pro", key="pricing_pro", use_container_width=True):
                st.switch_page("pages/5_⚙️_Authentication.py")
    
    # Call to action
    st.markdown("---")
    show_login_prompt("the full Kaspa Analytics platform")

def render_authenticated_homepage(user):
    """Authenticated user dashboard"""
    
    subscription = user['subscription']
    
    # Welcome header
    render_page_header(
        f"👋 Welcome back, {user['name']}!",
        f"Your {subscription.title()} Dashboard",
        show_auth_buttons=False
    )
    
    # Quick stats dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    df = fetch_kaspa_price_data()
    stats = get_market_stats(df) if not df.empty else {}
    
    with col1:
        st.metric(
            "KAS Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_24h', 0):+.2f}%"
        )
    
    with col2:
        st.metric("Your Plan", subscription.title())
    
    with col3:
        if subscription in ['premium', 'pro']:
            st.metric("Power Law Signal", "Above Trend", "+15%")
        else:
            st.metric("Power Law", "🔒 Premium Feature")
    
    with col4:
        st.metric("Active Alerts", "3 Active")
    
    # Enhanced chart for authenticated users
    if not df.empty:
        st.subheader("📈 Price Analysis Dashboard")
        
        # Chart timeframe based on subscription
        if subscription == 'free':
            chart_data = df.tail(30)
            st.info("📊 Free accounts: 30-day data. Upgrade for full historical access!")
        else:
            chart_data = df.tail(365)  # 1 year for premium+
            st.success(f"📊 {subscription.title()} account: Full historical data access")
        
        # Create advanced chart
        fig = go.Figure()
        
        # Price line
        fig.add_trace(go.Scatter(
            x=chart_data['timestamp'], 
            y=chart_data['price'],
            mode='lines',
            name='KAS Price',
            line=dict(color='#70C7BA', width=2)
        ))
        
        # Add volume for premium users
        if subscription in ['premium', 'pro'] and PLOTLY_AVAILABLE:
            fig.add_trace(go.Scatter(
                x=chart_data['timestamp'],
                y=chart_data['volume'] / 1000000,  # Scale volume
                mode='lines',
                name='Volume (M)',
                yaxis='y2',
                opacity=0.6,
                line=dict(color='orange')
            ))
            
            # Add secondary y-axis
            fig.update_layout(
                yaxis2=dict(
                    title="Volume (Millions)",
                    overlaying='y',
                    side='right',
                    showgrid=False
                )
            )
        
        if PLOTLY_AVAILABLE:
            fig.update_layout(
                title=f"Kaspa Price Analysis - {subscription.title()} View",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback to basic chart
            st.line_chart(chart_data.set_index('timestamp')['price'])
    
    # Quick actions dashboard
    st.subheader("⚡ Quick Actions")
    
    action_cols = st.columns(4)
    
    with action_cols[0]:
        if st.button("📈 Price Charts", key="dash_charts", use_container_width=True):
            st.switch_page("pages/1_📈_Price_Charts.py")
    
    with action_cols[1]:
        if st.button("📊 Power Law Analysis", key="dash_powerlaw", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")
    
    with action_cols[2]:
        if subscription in ['premium', 'pro']:
            if st.button("🌐 Network Metrics", key="dash_network", use_container_width=True):
                st.switch_page("pages/3_🌐_Network_Metrics.py")
        else:
            st.button("🔒 Network Metrics", disabled=True, use_container_width=True)
    
    with action_cols[3]:
        if subscription in ['premium', 'pro']:
            if st.button("📋 Data Export", key="dash_export", use_container_width=True):
                st.switch_page("pages/4_📋_Data_Export.py")
        else:
            st.button("🔒 Data Export", disabled=True, use_container_width=True)
    
    # Recent activity (placeholder)
    st.subheader("📋 Recent Activity")
    
    activity_data = [
        {"time": "2 hours ago", "action": "Exported price data", "status": "✅"},
        {"time": "1 day ago", "action": "Created custom alert", "status": "✅"},
        {"time": "3 days ago", "action": "Viewed power law analysis", "status": "✅"},
    ]
    
    for activity in activity_data:
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 1])
            with col1:
                st.write(activity["time"])
            with col2:
                st.write(activity["action"])
            with col3:
                st.write(activity["status"])

def render_analytics_showcase():
    """Show analytics features"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Advanced Analytics")
        st.write("• **Power Law Models**: Mathematical price predictions")
        st.write("• **Technical Indicators**: RSI, MACD, Moving averages")
        st.write("• **Trend Analysis**: Support/resistance levels")
        st.write("• **Volatility Metrics**: Price volatility tracking")
        
        if st.button("🔍 Explore Analytics", key="explore_analytics", use_container_width=True):
            st.switch_page("pages/2_📊_Power_Law.py")
    
    with col2:
        st.markdown("#### 🌐 Network Insights")
        st.write("• **Hash Rate Tracking**: Network security metrics")
        st.write("• **Address Analysis**: Active wallet tracking")
        st.write("• **Transaction Metrics**: Network usage stats")
        st.write("• **Mining Analytics**: Difficulty and rewards")
        
        if st.button("📊 View Network Data", key="explore_network", use_container_width=True):
            st.switch_page("pages/3_🌐_Network_Metrics.py")

def render_data_showcase():
    """Show data access features"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Real-time Data")
        st.write("• **Live Price Feeds**: Real-time KAS pricing")
        st.write("• **Historical Data**: Complete price history")
        st.write("• **High Frequency**: Minute-by-minute updates")
        st.write("• **Multiple Exchanges**: Aggregated pricing data")
    
    with col2:
        st.markdown("#### 📋 Export Options")
        st.write("• **CSV/JSON Export**: Download your data")
        st.write("• **API Access**: Programmatic data access")
        st.write("• **Custom Reports**: Automated reporting")
        st.write("• **Webhooks**: Real-time notifications")
        
        if st.button("📥 Export Data", key="explore_export", use_container_width=True):
            st.switch_page("pages/4_📋_Data_Export.py")

def render_tools_showcase():
    """Show tools and utilities"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛠️ Analysis Tools")
        st.write("• **Custom Dashboards**: Personalized views")
        st.write("• **Alert System**: Price and volume alerts")
        st.write("• **Portfolio Tracking**: Track your holdings")
        st.write("• **Comparison Tools**: Compare with other assets")
    
    with col2:
        st.markdown("#### ⚙️ Advanced Features")
        st.write("• **API Integration**: Connect your tools")
        st.write("• **White-label Reports**: Branded analysis")
        st.write("• **Team Collaboration**: Share insights")
        st.write("• **Mobile App**: Access anywhere")

if __name__ == "__main__":
    main()
