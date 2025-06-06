"""
UI utilities and components for Kaspa Analytics Pro
Handles styling, common components, and layout utilities
"""

import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime
from utils.auth import get_current_user, logout_user, check_feature_access

def apply_custom_css():
    """Apply custom CSS styling for the entire application"""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --kaspa-primary: #70C7BA;
        --kaspa-secondary: #49A097;
        --kaspa-accent: #667eea;
        --kaspa-gradient: linear-gradient(135deg, #70C7BA 0%, #49A097 100%);
        --kaspa-accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Page header styling */
    .page-header {
        background: var(--kaspa-gradient);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .page-header h1 {
        margin: 0 0 0.5rem 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .page-header p {
        margin: 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Authentication container */
    .auth-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    /* Subscription badges */
    .subscription-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.25rem 0;
    }
    
    .badge-public {
        background: #28a745;
        color: white;
    }
    
    .badge-free {
        background: #6c757d;
        color: white;
    }
    
    .badge-premium {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000;
    }
    
    .badge-pro {
        background: linear-gradient(45deg, #8A2BE2, #4B0082);
        color: white;
    }
    
    /* Login prompt styling */
    .login-prompt {
        background: var(--kaspa-accent-gradient);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .login-prompt h3 {
        margin: 0 0 1rem 0;
    }
    
    /* Feature highlight boxes */
    .feature-highlight {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid var(--kaspa-primary);
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Upgrade prompt */
    .upgrade-prompt {
        background: var(--kaspa-accent-gradient);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Stats cards */
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        text-align: center;
    }
    
    /* Navigation styling */
    .nav-section {
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Footer styling */
    .footer {
        background: #f8f9fa;
        padding: 2rem;
        margin-top: 3rem;
        border-radius: 8px;
        text-align: center;
        color: #6c757d;
    }
    
    .footer a {
        color: var(--kaspa-primary);
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Error and warning styling */
    .stAlert > div {
        border-radius: 8px;
    }
    
    /* Custom metric styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Sidebar styling */
    .sidebar .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .page-header h1 {
            font-size: 2rem;
        }
        
        .page-header {
            padding: 1.5rem;
        }
        
        .auth-container {
            padding: 1rem;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--kaspa-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--kaspa-secondary);
    }
    </style>
    """, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str = "", show_auth_buttons: bool = False):
    """Render a consistent page header"""
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)
    
    if show_auth_buttons:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            auth_cols = st.columns(2)
            
            with auth_cols[0]:
                if st.button("🔑 Login", key="header_login_btn", use_container_width=True):
                    st.switch_page("pages/5_⚙️_Authentication.py")
            
            with auth_cols[1]:
                if st.button("🚀 Sign Up", key="header_signup_btn", use_container_width=True, type="primary"):
                    st.switch_page("pages/5_⚙️_Authentication.py")

def render_sidebar_navigation(user):
    """Render sidebar navigation for all pages"""
    with st.sidebar:
        # Logo and title
        st.markdown("# 💎 Kaspa Analytics")
        st.markdown(f"*Professional Analysis Platform*")
        
        # User info
        if user['username'] != 'public':
            st.markdown(f"**👤 {user['name']}**")
            st.markdown(f'<span class="subscription-badge badge-{user["subscription"]}">{user["subscription"].upper()}</span>', unsafe_allow_html=True)
        else:
            st.markdown("**👤 Public Access**")
            st.markdown('<span class="subscription-badge badge-public">PUBLIC</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### 📊 Navigation")
        
        # Home
        if st.button("🏠 Dashboard", use_container_width=True, key="nav_home"):
            st.switch_page("streamlit_app.py")
        
        # Price Charts
        if st.button("📈 Price Charts", use_container_width=True, key="nav_charts"):
            st.switch_page("pages/1_📈_Price_Charts.py")
        
        # Power Law
        if user['subscription'] == 'public':
            st.button("🔒 Power Law", disabled=True, use_container_width=True, help="Requires account")
        else:
            if st.button("📊 Power Law", use_container_width=True, key="nav_powerlaw"):
                st.switch_page("pages/2_📊_Power_Law.py")
        
        # Network Metrics (Premium+)
        if check_feature_access('network_metrics', user['subscription']):
            if st.button("🌐 Network Metrics", use_container_width=True, key="nav_network"):
                st.switch_page("pages/3_🌐_Network_Metrics.py")
        else:
            st.button("🔒 Network Metrics", disabled=True, use_container_width=True, help="Requires Premium+")
        
        # Data Export (Premium+)
        if check_feature_access('data_export', user['subscription']):
            if st.button("📋 Data Export", use_container_width=True, key="nav_export"):
                st.switch_page("pages/4_📋_Data_Export.py")
        else:
            st.button("🔒 Data Export", disabled=True, use_container_width=True, help="Requires Premium+")
        
        # Admin Panel (Admin only)
        if user['username'] == 'admin':
            if st.button("👑 Admin Panel", use_container_width=True, key="nav_admin"):
                st.switch_page("pages/6_👑_Admin_Panel.py")
        
        st.markdown("---")
        
        # Authentication section
        if user['username'] == 'public':
            st.markdown("### 🔐 Account")
            
            if st.button("🔑 Login", use_container_width=True, key="sidebar_login"):
                st.switch_page("pages/5_⚙️_Authentication.py")
            
            if st.button("🚀 Create Account", use_container_width=True, key="sidebar_signup", type="primary"):
                st.switch_page("pages/5_⚙️_Authentication.py")
        
        else:
            st.markdown("### ⚙️ Account")
            
            if st.button("👤 Profile & Settings", use_container_width=True, key="sidebar_profile"):
                st.switch_page("pages/5_⚙️_Authentication.py")
            
            if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
                logout_user()
                st.rerun()
        
        # Quick stats in sidebar
        render_sidebar_stats()

def render_sidebar_stats():
    """Render quick stats in sidebar"""
    from utils.data import get_market_stats, fetch_kaspa_price_data
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Stats")
    
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

def show_login_prompt(feature_name: str = "this feature"):
    """Show login prompt for premium features"""
    st.markdown(f"""
    <div class="login-prompt">
        <h3>🔐 Login Required</h3>
        <p>To access {feature_name}, please create a free account or login.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Create unique keys based on feature name
    safe_feature_name = feature_name.replace(" ", "_").replace("-", "_").replace(".", "_")
    
    with col1:
        if st.button("🚀 Create Account", type="primary", use_container_width=True, key=f"create_account_{safe_feature_name}"):
            st.switch_page("pages/5_⚙️_Authentication.py")
    
    with col2:
        if st.button("🔑 Login", use_container_width=True, key=f"login_{safe_feature_name}"):
            st.switch_page("pages/5_⚙️_Authentication.py")
    
    with col3:
        if st.button("ℹ️ Learn More", use_container_width=True, key=f"learn_more_{safe_feature_name}"):
            st.switch_page("streamlit_app.py")

def show_upgrade_prompt(current_subscription: str, required_subscription: str):
    """Show upgrade prompt for premium features"""
    price_map = {
        'premium': '$29/month',
        'pro': '$99/month'
    }
    
    price = price_map.get(required_subscription, '$99/month')
    
    st.markdown(f"""
    <div class="upgrade-prompt">
        <h3>⭐ {required_subscription.title()} Feature</h3>
        <p>This feature requires a {required_subscription} subscription.</p>
        <p><strong>Upgrade to {required_subscription.title()} - {price}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            f"⬆️ Upgrade to {required_subscription.title()}", 
            type="primary", 
            use_container_width=True, 
            key=f"upgrade_to_{required_subscription}_{current_subscription}"
        ):
            st.balloons()
            st.success(f"Redirecting to {required_subscription} upgrade...")
            st.switch_page("pages/5_⚙️_Authentication.py")
    
    with col2:
        if st.button(
            "📋 View All Plans", 
            use_container_width=True, 
            key=f"view_plans_{required_subscription}_{current_subscription}"
        ):
            st.switch_page("pages/5_⚙️_Authentication.py")

def render_feature_access_check(feature_name: str, required_subscription: list, current_user):
    """Check and handle feature access with appropriate prompts"""
    if current_user['username'] == 'public':
        show_login_prompt(feature_name)
        st.stop()
    
    if current_user['subscription'] not in required_subscription:
        # Determine what subscription they need
        if 'premium' in required_subscription and current_user['subscription'] == 'free':
            show_upgrade_prompt(current_user['subscription'], 'premium')
        elif 'pro' in required_subscription and current_user['subscription'] in ['free', 'premium']:
            show_upgrade_prompt(current_user['subscription'], 'pro')
        else:
            st.error(f"🔒 Access denied. Required: {', '.join(required_subscription)}")
        st.stop()

def render_subscription_comparison():
    """Render subscription comparison table"""
    st.subheader("📊 Subscription Comparison")
    
    features = [
        {"feature": "Basic Price Charts", "free": "✅", "premium": "✅", "pro": "✅"},
        {"feature": "30-day History", "free": "✅", "premium": "✅", "pro": "✅"},
        {"feature": "Full Historical Data", "free": "❌", "premium": "✅", "pro": "✅"},
        {"feature": "Power Law Analysis", "free": "Basic", "premium": "Advanced", "pro": "Advanced"},
        {"feature": "Network Metrics", "free": "❌", "premium": "✅", "pro": "✅"},
        {"feature": "Data Export", "free": "❌", "premium": "✅", "pro": "✅"},
        {"feature": "API Access", "free": "❌", "premium": "Limited", "pro": "Full"},
        {"feature": "Custom Models", "free": "❌", "premium": "❌", "pro": "✅"},
        {"feature": "Priority Support", "free": "❌", "premium": "❌", "pro": "✅"},
    ]
    
    # Create comparison table
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Feature**")
        for feature in features:
            st.write(feature["feature"])
    
    with col2:
        st.markdown("**Free**")
        for feature in features:
            st.write(feature["free"])
    
    with col3:
        st.markdown("**Premium**")
        for feature in features:
            st.write(feature["premium"])
    
    with col4:
        st.markdown("**Pro**")
        for feature in features:
            st.write(feature["pro"])

def render_loading_spinner(message: str = "Loading..."):
    """Render loading spinner with message"""
    with st.spinner(message):
        return True

def render_error_page(error_message: str, show_navigation: bool = True):
    """Render error page with navigation options"""
    st.error(f"❌ {error_message}")
    
    if show_navigation:
        st.markdown("### 🔧 What you can do:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏠 Go Home", use_container_width=True, key="error_home"):
                st.switch_page("streamlit_app.py")
        
        with col2:
            if st.button("🔄 Refresh Page", use_container_width=True, key="error_refresh"):
                st.rerun()
        
        with col3:
            if st.button("📞 Contact Support", use_container_width=True, key="error_support"):
                st.info("📧 Email: support@kaspa-analytics.com")

def render_success_message(message: str, show_confetti: bool = False):
    """Render success message with optional confetti"""
    if show_confetti:
        st.balloons()
    
    st.success(f"✅ {message}")

def render_info_box(title: str, content: str, icon: str = "ℹ️"):
    """Render information box"""
    st.markdown(f"""
    <div class="feature-highlight">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def render_stats_cards(stats: dict):
    """Render statistics as cards"""
    cols = st.columns(len(stats))
    
    for i, (label, value) in enumerate(stats.items()):
        with cols[i]:
            if isinstance(value, dict):
                st.metric(label, value.get('value', ''), delta=value.get('delta'))
            else:
                st.metric(label, value)

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>💎 Kaspa Analytics Pro</strong> - Professional blockchain analysis platform</p>
        <p>
            <a href="https://kaspa-analytics.com/about">About</a> | 
            <a href="https://kaspa-analytics.com/privacy">Privacy Policy</a> | 
            <a href="https://kaspa-analytics.com/terms">Terms of Service</a> | 
            <a href="https://kaspa-analytics.com/contact">Contact</a>
        </p>
        <p>© 2024 Kaspa Analytics Pro. All rights reserved.</p>
        <p><small>Data provided for educational and analysis purposes. Not financial advice.</small></p>
    </div>
    """, unsafe_allow_html=True)

def format_number(num: float, prefix: str = "", suffix: str = "", decimals: int = 2) -> str:
    """Format numbers for display"""
    if num >= 1e9:
        return f"{prefix}{num/1e9:.{decimals}f}B{suffix}"
    elif num >= 1e6:
        return f"{prefix}{num/1e6:.{decimals}f}M{suffix}"
    elif num >= 1e3:
        return f"{prefix}{num/1e3:.{decimals}f}K{suffix}"
    else:
        return f"{prefix}{num:.{decimals}f}{suffix}"

def format_percentage(value: float, show_sign: bool = True) -> str:
    """Format percentage values"""
    sign = "+" if value > 0 and show_sign else ""
    return f"{sign}{value:.2f}%"

def render_chart_controls():
    """Render common chart control elements"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox(
            "Chart Type",
            ["Line", "Candlestick", "Area"],
            key="chart_type_control"
        )
    
    with col2:
        timeframe = st.selectbox(
            "Timeframe",
            ["1H", "4H", "1D", "1W"],
            index=2,  # Default to 1D
            key="timeframe_control"
        )
    
    with col3:
        time_range = st.selectbox(
            "Range",
            ["7D", "30D", "3M", "1Y", "All"],
            index=1,  # Default to 30D
            key="time_range_control"
        )
    
    return chart_type, timeframe, time_range

def render_breadcrumbs(pages: list):
    """Render breadcrumb navigation"""
    breadcrumb_html = " > ".join([f'<a href="{page["url"]}">{page["name"]}</a>' for page in pages])
    st.markdown(f"**Navigation:** {breadcrumb_html}", unsafe_allow_html=True)
