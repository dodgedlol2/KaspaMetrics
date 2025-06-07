"""
Price Charts View - Kaspa Analytics Pro
Advanced price charting and technical analysis
"""

import streamlit as st
import streamlit_antd_components as sac
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import utilities
from utils.auth import get_current_user, check_feature_access
from utils.data import (
    fetch_kaspa_price_data, 
    filter_data_by_subscription,
    get_technical_indicators,
    get_market_stats
)
from utils.ui import (
    render_page_header, 
    show_login_prompt,
    show_upgrade_prompt,
    apply_custom_css,
    render_chart_controls,
    render_footer
)

def main():
    """Main price charts page"""
    
    # Apply styling
    apply_custom_css()
    
    # Get current user
    user = get_current_user()
    subscription = user['subscription']
    
    # Page header
    render_page_header(
        "📈 Advanced Price Charts",
        "Professional Kaspa price analysis with technical indicators"
    )
    
    # Main content based on subscription level
    if subscription == 'public':
        render_public_charts()
    elif subscription == 'free':
        render_free_charts()
    else:
        render_premium_charts(subscription)
    
    # Footer
    render_footer()

def render_public_charts():
    """Public users see basic 7-day charts"""
    st.info("📊 Public Access - 7-day price preview available")
    
    # Fetch limited data
    df = fetch_kaspa_price_data(7)
    
    if df.empty:
        st.error("Unable to load price data")
        return
    
    # Basic chart controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox("Chart Type", ["Line"], key="public_chart_type")
    with col2:
        st.selectbox("Time Range", ["7D"], key="public_time_range")
    with col3:
        st.selectbox("Indicators", ["🔒 Login Required"], key="public_indicators")
    
    # Create basic chart
    fig = create_basic_chart(df, "7-Day Preview (Public Access)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Market stats
    stats = get_market_stats(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"${stats.get('current_price', 0):.4f}")
    with col2:
        st.metric("7D High", f"${stats.get('high_24h', 0):.4f}")
    with col3:
        st.metric("7D Low", f"${stats.get('low_24h', 0):.4f}")
    with col4:
        st.metric("7D Change", f"{stats.get('price_change_7d', 0):+.2f}%")
    
    # Feature showcase
    st.subheader("🔓 Unlock Advanced Features")
    
    feature_cols = st.columns(2)
    
    with feature_cols[0]:
        st.markdown("### 🆓 Free Account Benefits")
        st.write("• 30-day price history")
        st.write("• Basic technical indicators")
        st.write("• Multiple chart types")
        st.write("• Candlestick charts")
        st.write("• Volume analysis")
    
    with feature_cols[1]:
        st.markdown("### ⭐ Premium Features")
        st.write("• Full historical data (2+ years)")
        st.write("• Advanced technical indicators")
        st.write("• Custom overlays and studies")
        st.write("• Drawing tools")
        st.write("• Data export capabilities")
    
    # Call to action
    show_login_prompt("advanced charting features")

def render_free_charts():
    """Free users get 30-day charts with basic indicators"""
    st.success("📊 Free Account - 30-day charts with basic indicators")
    
    # Fetch data (limited to 30 days)
    df = filter_data_by_subscription(fetch_kaspa_price_data(30), 'free')
    
    if df.empty:
        st.error("Unable to load price data")
        return
    
    # Chart controls
    chart_type, timeframe, time_range = render_chart_controls()
    
    # Additional controls for free users
    col1, col2 = st.columns(2)
    
    with col1:
        show_volume = st.checkbox("Show Volume", value=True, key="free_show_volume")
    
    with col2:
        indicators = st.multiselect(
            "Basic Indicators",
            ["SMA 20", "SMA 50", "EMA 20"],
            default=["SMA 20"],
            key="free_indicators"
        )
    
    # Create chart
    fig = create_advanced_chart(df, chart_type, indicators, show_volume, "30-Day Charts (Free Account)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Technical analysis summary
    render_technical_summary(df, subscription_level='free')
    
    # Upgrade prompt
    st.markdown("---")
    show_upgrade_prompt('free', 'premium')

def render_premium_charts(subscription):
    """Premium/Pro users get full features"""
    st.success(f"🎉 {subscription.title()} Account - All charting features unlocked!")
    
    # Fetch full historical data
    df = fetch_kaspa_price_data(365 * 2)  # 2 years of data
    
    if df.empty:
        st.error("Unable to load price data")
        return
    
    # Advanced chart controls
    chart_tabs = sac.tabs([
        sac.TabsItem(label='Chart', icon='graph-up'),
        sac.TabsItem(label='Indicators', icon='sliders'),
        sac.TabsItem(label='Analysis', icon='search'),
        sac.TabsItem(label='Settings', icon='gear'),
    ], key='chart_tabs')
    
    if chart_tabs == 'Chart':
        render_main_chart_tab(df, subscription)
    elif chart_tabs == 'Indicators':
        render_indicators_tab(df)
    elif chart_tabs == 'Analysis':
        render_analysis_tab(df)
    else:
        render_settings_tab()

def create_basic_chart(df, title):
    """Create basic line chart for public users"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price'],
        mode='lines',
        name='KAS Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=500,
        template="plotly_white",
        showlegend=True
    )
    
    return fig

def create_advanced_chart(df, chart_type, indicators, show_volume, title):
    """Create advanced chart for free users"""
    fig = go.Figure()
    
    # Main price chart
    if chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            name='KAS Price',
            line=dict(color='#70C7BA', width=2)
        ))
    elif chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='KAS Price'
        ))
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            fill='tonexty',
            name='KAS Price',
