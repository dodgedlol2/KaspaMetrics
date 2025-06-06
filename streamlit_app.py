# streamlit_app.py - REPLACE ENTIRE FILE WITH THIS
"""
Kaspa Analytics Pro - Main Application with Improved Navigation
"""

import streamlit as st
from utils.auth import get_current_user, check_feature_access
from utils.ui import apply_custom_css

# Configure page settings
st.set_page_config(
    page_title="Kaspa Analytics Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

def create_navigation_pages():
    """Create navigation pages based on user subscription"""
    user = get_current_user()
    subscription = user['subscription']
    
    # Define base pages that everyone can see
    pages = {
        "📊 Analytics": [
            st.Page("pages/dashboard.py", title="🏠 Dashboard", icon="🏠"),
            st.Page("pages/price_charts.py", title="📈 Price Charts", icon="📈"),
        ],
    }
    
    # Add Power Law for authenticated users
    if subscription != 'public':
        pages["📊 Analytics"].append(
            st.Page("pages/power_law.py", title="📊 Power Law", icon="📊")
        )
    
    # Add premium features
    if check_feature_access('network_metrics', subscription):
        if "💾 Data & Network" not in pages:
            pages["💾 Data & Network"] = []
        pages["💾 Data & Network"].extend([
            st.Page("pages/network_metrics.py", title="🌐 Network Metrics", icon="🌐"),
        ])
    
    if check_feature_access('data_export', subscription):
        if "💾 Data & Network" not in pages:
            pages["💾 Data & Network"] = []
        pages["💾 Data & Network"].append(
            st.Page("pages/data_export.py", title="📋 Data Export", icon="📋")
        )
    
    # Account section
    if subscription == 'public':
        pages["👤 Account"] = [
            st.Page("pages/auth_login.py", title="🔑 Login", icon="🔑"),
            st.Page("pages/auth_register.py", title="🚀 Sign Up", icon="🚀"),
        ]
    else:
        pages["👤 Account"] = [
            st.Page("pages/profile.py", title="👤 Profile", icon="👤"),
            st.Page("pages/settings.py", title="⚙️ Settings", icon="⚙️"),
        ]
        
        # Add admin panel for admin users
        if user['username'] == 'admin':
            pages["👤 Account"].append(
                st.Page("pages/admin_panel.py", title="👑 Admin Panel", icon="👑")
            )
    
    return pages

def render_custom_sidebar():
    """Render custom sidebar with user info and quick stats"""
    with st.sidebar:
        # App branding
        st.markdown("# 💎 Kaspa Analytics")
        st.markdown("*Professional Analysis Platform*")
        
        # User info
        user = get_current_user()
        
        if user['username'] == 'public':
            st.markdown("**👤 Public Access**")
            st.markdown('<span class="subscription-badge badge-public">PUBLIC</span>', unsafe_allow_html=True)
        else:
            st.markdown(f"**👤 {user['name']}**")
            st.markdown(f'<span class="subscription-badge badge-{user["subscription"]}">{user["subscription"].upper()}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick stats
        render_sidebar_quick_stats()
        
        # Plan status for authenticated users
        if user['username'] != 'public':
            render_plan_status(user)

def render_sidebar_quick_stats():
    """Render quick market stats in sidebar"""
    try:
        from utils.data import fetch_kaspa_price_data, get_market_stats
        
        # Get basic price data
        df = fetch_kaspa_price_data(7)  # Last 7 days for sidebar
        
        if not df.empty:
            stats = get_market_stats(df)
            
            st.markdown("### ⚡ Quick Stats")
            
            # Current price with 24h change
            price_change = stats.get('price_change_24h', 0)
            
            st.metric(
                "KAS Price", 
                f"${stats.get('current_price', 0):.4f}",
                delta=f"{price_change:+.2f}%"
            )
            
            st.metric(
                "24h Volume", 
                f"${stats.get('volume_24h', 0)/1000000:.1f}M"
            )
            
        else:
            st.markdown("### ⚡ Quick Stats")
            st.info("📊 Loading market data...")
            
    except Exception as e:
        st.markdown("### ⚡ Quick Stats")
        st.warning("⚠️ Stats unavailable")

def render_plan_status(user):
    """Render plan status and upgrade prompts"""
    subscription = user['subscription']
    
    st.markdown("---")
    st.markdown("### 📋 Your Plan")
    
    if subscription == 'free':
        st.info("🆓 Free Plan")
        st.write("• 30-day data access")
        st.write("• Basic analytics")
        
        if st.button("⬆️ Upgrade", key="sidebar_upgrade", use_container_width=True, type="primary"):
            st.switch_page("pages/auth_pricing.py")
    
    elif subscription == 'premium':
        st.success("⭐ Premium Plan")
        st.write("• Full data access")
        st.write("• Advanced analytics")
        st.write("• Data export")
        
        if st.button("👑 Go Pro", key="sidebar_go_pro", use_container_width=True):
            st.switch_page("pages/auth_pricing.py")
    
    else:  # pro
        st.success("👑 Pro Plan")
        st.write("• All features unlocked")
        st.write("• API access")
        st.write("• Priority support")

def main():
    """Main application entry point"""
    
    # Create navigation based on user access
    pages = create_navigation_pages()
    
    # Create navigation
    pg = st.navigation(pages)
    
    # Render custom sidebar
    render_custom_sidebar()
    
    # Run the selected page
    pg.run()

if __name__ == "__main__":
    main()
