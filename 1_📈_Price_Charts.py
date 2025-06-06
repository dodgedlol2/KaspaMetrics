"""
Price Charts Page - Kaspa Analytics Pro
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
    render_sidebar_navigation,
    show_login_prompt,
    show_upgrade_prompt,
    apply_custom_css,
    render_chart_controls,
    render_footer
)

# Configure page
st.set_page_config(
    page_title="Price Charts - Kaspa Analytics Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Advanced Kaspa price charts with technical analysis tools, indicators, and real-time data visualization.">
<meta name="keywords" content="Kaspa price charts, KAS technical analysis, cryptocurrency charts, blockchain price data">
<meta property="og:title" content="Kaspa Price Charts - Advanced Technical Analysis">
<meta property="og:description" content="Professional Kaspa price analysis with advanced charting tools and technical indicators">
<meta property="og:type" content="website">
""", unsafe_allow_html=True)

# Apply styling
apply_custom_css()

def main():
    """Main price charts page"""
    
    # Get current user
    user = get_current_user()
    subscription = user['subscription']
    
    # Render sidebar navigation
    render_sidebar_navigation(user)
    
    # Page header
    render_page_header(
        "📈 Advanced Price Charts",
        "Professional Kaspa price analysis with technical indicators"
    )
    
    # Breadcrumb navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Dashboard", key="charts_back_to_home"):
            st.switch_page("streamlit_app.py")
    
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

def render_main_chart_tab(df, subscription):
    """Main charting interface for premium users"""
    
    # Chart controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        chart_type = st.selectbox(
            "Chart Type",
            ["Line", "Candlestick", "Area", "OHLC"],
            index=1,  # Default to candlestick
            key="premium_chart_type"
        )
    
    with col2:
        time_range = st.selectbox(
            "Time Range",
            ["7D", "30D", "3M", "6M", "1Y", "2Y", "All"],
            index=2,  # Default to 3M
            key="premium_time_range"
        )
    
    with col3:
        timeframe = st.selectbox(
            "Timeframe",
            ["1H", "4H", "1D", "1W"],
            index=2,  # Default to 1D
            key="premium_timeframe"
        )
    
    with col4:
        chart_style = st.selectbox(
            "Style",
            ["Light", "Dark", "Colorful"],
            key="premium_chart_style"
        )
    
    # Filter data based on time range
    if time_range == "7D":
        chart_data = df.tail(7 * 24)
    elif time_range == "30D":
        chart_data = df.tail(30 * 24)
    elif time_range == "3M":
        chart_data = df.tail(90 * 24)
    elif time_range == "6M":
        chart_data = df.tail(180 * 24)
    elif time_range == "1Y":
        chart_data = df.tail(365 * 24)
    elif time_range == "2Y":
        chart_data = df.tail(730 * 24)
    else:
        chart_data = df
    
    # Advanced indicators selection
    col1, col2 = st.columns(2)
    
    with col1:
        overlay_indicators = st.multiselect(
            "Overlay Indicators",
            ["SMA 20", "SMA 50", "EMA 12", "EMA 26", "Bollinger Bands", "VWAP"],
            default=["SMA 20", "Bollinger Bands"],
            key="premium_overlay_indicators"
        )
    
    with col2:
        oscillator_indicators = st.multiselect(
            "Oscillator Indicators",
            ["RSI", "MACD", "Stochastic", "Williams %R"],
            default=["RSI", "MACD"],
            key="premium_oscillator_indicators"
        )
    
    # Additional options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_volume = st.checkbox("Show Volume", value=True, key="premium_show_volume")
    
    with col2:
        show_events = st.checkbox("Show Events", value=False, key="premium_show_events")
    
    with col3:
        auto_scale = st.checkbox("Auto Scale", value=True, key="premium_auto_scale")
    
    # Create advanced chart
    fig = create_professional_chart(
        chart_data, 
        chart_type, 
        overlay_indicators, 
        oscillator_indicators,
        show_volume,
        show_events,
        chart_style,
        f"{time_range} Kaspa Price Analysis ({subscription.title()})"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market statistics
    render_market_statistics(chart_data)

def render_indicators_tab(df):
    """Technical indicators detailed view"""
    st.subheader("📊 Technical Indicators Analysis")
    
    # Get technical indicators
    indicators = get_technical_indicators(df)
    
    if not indicators:
        st.warning("Unable to calculate technical indicators")
        return
    
    # Current indicator values
    current_values = indicators.get('current_values', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rsi_value = current_values.get('rsi')
        if rsi_value:
            rsi_color = "red" if rsi_value > 70 else "green" if rsi_value < 30 else "orange"
            st.metric("RSI (14)", f"{rsi_value:.1f}", help="Relative Strength Index")
            st.markdown(f"<span style='color: {rsi_color}'>{'Overbought' if rsi_value > 70 else 'Oversold' if rsi_value < 30 else 'Neutral'}</span>", unsafe_allow_html=True)
    
    with col2:
        macd_value = current_values.get('macd')
        if macd_value:
            st.metric("MACD", f"{macd_value:.6f}", help="Moving Average Convergence Divergence")
    
    with col3:
        bb_position = current_values.get('bb_position')
        if bb_position:
            st.metric("BB Position", f"{bb_position:.2f}", help="Position within Bollinger Bands")
    
    # Detailed indicator charts
    indicator_tabs = sac.tabs([
        sac.TabsItem(label='RSI', icon='activity'),
        sac.TabsItem(label='MACD', icon='trending-up'),
        sac.TabsItem(label='Bollinger Bands', icon='layers'),
    ], key='indicator_detail_tabs')
    
    if indicator_tabs == 'RSI':
        render_rsi_chart(df, indicators)
    elif indicator_tabs == 'MACD':
        render_macd_chart(df, indicators)
    else:
        render_bollinger_chart(df, indicators)

def render_analysis_tab(df):
    """Market analysis and insights"""
    st.subheader("🔍 Market Analysis")
    
    # Price action analysis
    stats = get_market_stats(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Price Action")
        
        # Support and resistance levels
        recent_data = df.tail(100)
        resistance = recent_data['high'].max()
        support = recent_data['low'].min()
        current_price = df['price'].iloc[-1]
        
        st.write(f"**Resistance:** ${resistance:.4f}")
        st.write(f"**Current:** ${current_price:.4f}")
        st.write(f"**Support:** ${support:.4f}")
        
        # Price position
        position = (current_price - support) / (resistance - support)
        st.progress(position)
        st.write(f"Price position: {position:.1%} of range")
    
    with col2:
        st.markdown("#### 📊 Volume Analysis")
        
        avg_volume = df['volume'].tail(30).mean()
        current_volume = df['volume'].iloc[-1]
        volume_ratio = current_volume / avg_volume
        
        st.metric("Volume vs 30D Avg", f"{volume_ratio:.2f}x")
        
        if volume_ratio > 1.5:
            st.success("High volume - Strong interest")
        elif volume_ratio < 0.5:
            st.warning("Low volume - Weak interest")
        else:
            st.info("Normal volume levels")
    
    # Market sentiment
    st.markdown("#### 🎯 Market Sentiment")
    
    # Calculate sentiment score
    indicators = get_technical_indicators(df)
    sentiment_score = calculate_sentiment_score(indicators)
    
    sentiment_cols = st.columns(3)
    
    with sentiment_cols[0]:
        st.metric("Overall Sentiment", sentiment_score['label'])
    
    with sentiment_cols[1]:
        st.metric("Bullish Signals", sentiment_score['bullish'])
    
    with sentiment_cols[2]:
        st.metric("Bearish Signals", sentiment_score['bearish'])

def render_settings_tab():
    """Chart settings and preferences"""
    st.subheader("⚙️ Chart Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Appearance")
        
        theme = st.selectbox(
            "Chart Theme",
            ["Light", "Dark", "Auto"],
            key="chart_theme_setting"
        )
        
        color_scheme = st.selectbox(
            "Color Scheme",
            ["Default", "Colorblind Friendly", "High Contrast"],
            key="chart_color_scheme"
        )
        
        show_grid = st.checkbox("Show Grid", value=True, key="chart_show_grid")
        show_crosshair = st.checkbox("Show Crosshair", value=True, key="chart_show_crosshair")
    
    with col2:
        st.markdown("#### 📊 Data")
        
        auto_refresh = st.checkbox("Auto Refresh", value=False, key="chart_auto_refresh")
        
        if auto_refresh:
            refresh_interval = st.selectbox(
                "Refresh Interval",
                ["30 seconds", "1 minute", "5 minutes"],
                key="chart_refresh_interval"
            )
        
        data_source = st.selectbox(
            "Data Source",
            ["Primary", "Backup", "Aggregated"],
            key="chart_data_source"
        )
    
    # Save settings
    if st.button("💾 Save Settings", key="save_chart_settings"):
        st.success("Settings saved successfully!")

# Chart creation functions
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
            line=dict(color='#70C7BA')
        ))
    
    # Add basic indicators
    if "SMA 20" in indicators:
        sma_20 = df['price'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=sma_20,
            mode='lines',
            name='SMA 20',
            line=dict(color='orange', dash='dash')
        ))
    
    if "SMA 50" in indicators:
        sma_50 = df['price'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=sma_50,
            mode='lines',
            name='SMA 50',
            line=dict(color='red', dash='dash')
        ))
    
    if "EMA 20" in indicators:
        ema_20 = df['price'].ewm(span=20).mean()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=ema_20,
            mode='lines',
            name='EMA 20',
            line=dict(color='purple', dash='dot')
        ))
    
    # Add volume if requested
    if show_volume:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['volume'] / 1000000,  # Convert to millions
            mode='lines',
            name='Volume (M)',
            yaxis='y2',
            opacity=0.6,
            line=dict(color='gray')
        ))
        
        fig.update_layout(
            yaxis2=dict(
                title="Volume (Millions)",
                overlaying='y',
                side='right',
                showgrid=False
            )
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=600,
        template="plotly_white",
        showlegend=True
    )
    
    return fig

def create_professional_chart(df, chart_type, overlay_indicators, oscillator_indicators, 
                            show_volume, show_events, chart_style, title):
    """Create professional chart for premium users"""
    from plotly.subplots import make_subplots
    
    # Determine number of subplots
    subplot_count = 1
    if show_volume:
        subplot_count += 1
    if oscillator_indicators:
        subplot_count += len(oscillator_indicators)
    
    # Create subplots
    subplot_titles = [title]
    if show_volume:
        subplot_titles.append("Volume")
    for indicator in oscillator_indicators:
        subplot_titles.append(indicator)
    
    fig = make_subplots(
        rows=subplot_count,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=subplot_titles,
        row_heights=[0.6] + [0.2] * (subplot_count - 1)
    )
    
    # Main price chart
    if chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            name='KAS Price',
            line=dict(color='#70C7BA', width=2)
        ), row=1, col=1)
    elif chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='KAS Price'
        ), row=1, col=1)
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['price'],
            mode='lines',
            fill='tonexty',
            name='KAS Price',
            line=dict(color='#70C7BA')
        ), row=1, col=1)
    elif chart_type == "OHLC":
        fig.add_trace(go.Ohlc(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='KAS Price'
        ), row=1, col=1)
    
    # Add overlay indicators
    current_row = 1
    
    for indicator in overlay_indicators:
        if indicator == "SMA 20":
            sma_20 = df['price'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=sma_20,
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', dash='dash')
            ), row=current_row, col=1)
        
        elif indicator == "SMA 50":
            sma_50 = df['price'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=sma_50,
                mode='lines',
                name='SMA 50',
                line=dict(color='red', dash='dash')
            ), row=current_row, col=1)
        
        elif indicator == "EMA 12":
            ema_12 = df['price'].ewm(span=12).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=ema_12,
                mode='lines',
                name='EMA 12',
                line=dict(color='blue', dash='dot')
            ), row=current_row, col=1)
        
        elif indicator == "EMA 26":
            ema_26 = df['price'].ewm(span=26).mean()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=ema_26,
                mode='lines',
                name='EMA 26',
                line=dict(color='purple', dash='dot')
            ), row=current_row, col=1)
        
        elif indicator == "Bollinger Bands":
            bb_middle = df['price'].rolling(window=20).mean()
            bb_std = df['price'].rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=bb_upper,
                mode='lines',
                name='BB Upper',
                line=dict(color='gray', dash='dash'),
                showlegend=False
            ), row=current_row, col=1)
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=bb_lower,
                mode='lines',
                name='BB Lower',
                line=dict(color='gray', dash='dash'),
                fill='tonexty',
                fillcolor='rgba(128,128,128,0.1)',
                showlegend=False
            ), row=current_row, col=1)
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=bb_middle,
                mode='lines',
                name='BB Middle',
                line=dict(color='gray')
            ), row=current_row, col=1)
    
    # Add volume
    if show_volume:
        current_row += 1
        fig.add_trace(go.Bar(
            x=df['timestamp'],
            y=df['volume'],
            name='Volume',
            marker_color='lightblue',
            opacity=0.7
        ), row=current_row, col=1)
    
    # Add oscillator indicators
    indicators_data = get_technical_indicators(df)
    
    for indicator in oscillator_indicators:
        current_row += 1
        
        if indicator == "RSI" and indicators_data:
            rsi_data = indicators_data.get('rsi', [])
            if rsi_data:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=rsi_data,
                    mode='lines',
                    name='RSI',
                    line=dict(color='purple')
                ), row=current_row, col=1)
                
                # Add RSI levels
                fig.add_hline(y=70, line_dash="dash", line_color="red", 
                             annotation_text="Overbought", row=current_row, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", 
                             annotation_text="Oversold", row=current_row, col=1)
        
        elif indicator == "MACD" and indicators_data:
            macd_line = indicators_data.get('macd_line', [])
            macd_signal = indicators_data.get('macd_signal', [])
            macd_histogram = indicators_data.get('macd_histogram', [])
            
            if macd_line:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=macd_line,
                    mode='lines',
                    name='MACD',
                    line=dict(color='blue')
                ), row=current_row, col=1)
            
            if macd_signal:
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=macd_signal,
                    mode='lines',
                    name='Signal',
                    line=dict(color='red')
                ), row=current_row, col=1)
            
            if macd_histogram:
                fig.add_trace(go.Bar(
                    x=df['timestamp'],
                    y=macd_histogram,
                    name='Histogram',
                    marker_color='gray',
                    opacity=0.6
                ), row=current_row, col=1)
    
    # Apply chart style
    template = "plotly_white"
    if chart_style == "Dark":
        template = "plotly_dark"
    elif chart_style == "Colorful":
        template = "ggplot2"
    
    fig.update_layout(
        height=800,
        template=template,
        showlegend=True,
        xaxis_rangeslider_visible=False
    )
    
    return fig

def render_technical_summary(df, subscription_level):
    """Render technical analysis summary"""
    st.subheader("📊 Technical Analysis Summary")
    
    # Calculate basic indicators
    current_price = df['price'].iloc[-1]
    sma_20 = df['price'].rolling(window=20).mean().iloc[-1]
    sma_50 = df['price'].rolling(window=50).mean().iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📈 Trend Analysis")
        if current_price > sma_20 > sma_50:
            st.success("🔼 Strong Uptrend")
        elif current_price > sma_20:
            st.info("📈 Uptrend")
        elif current_price < sma_20 < sma_50:
            st.error("🔽 Strong Downtrend")
        else:
            st.warning("📊 Sideways/Mixed")
    
    with col2:
        st.markdown("#### 🎯 Price vs SMA")
        sma_20_diff = ((current_price - sma_20) / sma_20) * 100
        st.metric("vs SMA 20", f"{sma_20_diff:+.2f}%")
        
        if subscription_level != 'free':
            sma_50_diff = ((current_price - sma_50) / sma_50) * 100
            st.metric("vs SMA 50", f"{sma_50_diff:+.2f}%")
    
    with col3:
        st.markdown("#### 📊 Volume Trend")
        recent_volume = df['volume'].tail(5).mean()
        prev_volume = df['volume'].tail(10).head(5).mean()
        volume_change = ((recent_volume - prev_volume) / prev_volume) * 100
        
        if volume_change > 20:
            st.success(f"🔼 Increasing (+{volume_change:.1f}%)")
        elif volume_change < -20:
            st.error(f"🔽 Decreasing ({volume_change:.1f}%)")
        else:
            st.info("📊 Stable Volume")

def render_market_statistics(df):
    """Render comprehensive market statistics"""
    st.subheader("📊 Market Statistics")
    
    stats = get_market_stats(df)
    
    # Main statistics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Current Price", 
            f"${stats.get('current_price', 0):.4f}",
            delta=f"{stats.get('price_change_24h', 0):+.2f}%"
        )
    
    with col2:
        st.metric("24h High", f"${stats.get('high_24h', 0):.4f}")
    
    with col3:
        st.metric("24h Low", f"${stats.get('low_24h', 0):.4f}")
    
    with col4:
        st.metric("24h Volume", f"${stats.get('volume_24h', 0)/1000000:.1f}M")
    
    with col5:
        st.metric("Market Cap", f"${stats.get('market_cap', 0):.1f}B")
    
    # Additional statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Performance")
        st.metric("7-Day Change", f"{stats.get('price_change_7d', 0):+.2f}%")
        st.metric("30-Day Change", f"{stats.get('price_change_30d', 0):+.2f}%")
    
    with col2:
        st.markdown("#### 🌐 Network")
        st.metric("Hash Rate", f"{stats.get('hash_rate', 0):.2f} EH/s")
        st.metric("Active Addresses", f"{stats.get('active_addresses', 0):,}")

def render_rsi_chart(df, indicators):
    """Render RSI indicator chart"""
    st.markdown("#### RSI (Relative Strength Index)")
    
    rsi_data = indicators.get('rsi', [])
    if not rsi_data:
        st.warning("RSI data not available")
        return
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=rsi_data,
        mode='lines',
        name='RSI',
        line=dict(color='purple', width=2)
    ))
    
    # Add reference lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig.add_hline(y=50, line_dash="dash", line_color="gray", annotation_text="Neutral (50)")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    
    # Color areas
    fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1)
    fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1)
    
    fig.update_layout(
        title="RSI Indicator",
        xaxis_title="Date",
        yaxis_title="RSI",
        height=300,
        yaxis=dict(range=[0, 100])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # RSI interpretation
    current_rsi = rsi_data[-1] if rsi_data else 0
    if current_rsi > 70:
        st.warning(f"⚠️ RSI at {current_rsi:.1f} - Potentially overbought")
    elif current_rsi < 30:
        st.success(f"✅ RSI at {current_rsi:.1f} - Potentially oversold")
    else:
        st.info(f"📊 RSI at {current_rsi:.1f} - Neutral territory")

def render_macd_chart(df, indicators):
    """Render MACD indicator chart"""
    st.markdown("#### MACD (Moving Average Convergence Divergence)")
    
    macd_line = indicators.get('macd_line', [])
    macd_signal = indicators.get('macd_signal', [])
    macd_histogram = indicators.get('macd_histogram', [])
    
    if not macd_line:
        st.warning("MACD data not available")
        return
    
    fig = go.Figure()
    
    # MACD line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=macd_line,
        mode='lines',
        name='MACD',
        line=dict(color='blue', width=2)
    ))
    
    # Signal line
    if macd_signal:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=macd_signal,
            mode='lines',
            name='Signal',
            line=dict(color='red', width=2)
        ))
    
    # Histogram
    if macd_histogram:
        colors = ['green' if h > 0 else 'red' for h in macd_histogram]
        fig.add_trace(go.Bar(
            x=df['timestamp'],
            y=macd_histogram,
            name='Histogram',
            marker_color=colors,
            opacity=0.6
        ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    fig.update_layout(
        title="MACD Indicator",
        xaxis_title="Date",
        yaxis_title="MACD",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # MACD interpretation
    if macd_line and macd_signal:
        current_macd = macd_line[-1]
        current_signal = macd_signal[-1]
        
        if current_macd > current_signal:
            st.success("✅ MACD above signal line - Bullish momentum")
        else:
            st.warning("⚠️ MACD below signal line - Bearish momentum")

def render_bollinger_chart(df, indicators):
    """Render Bollinger Bands chart"""
    st.markdown("#### Bollinger Bands")
    
    bb_upper = indicators.get('bb_upper', [])
    bb_middle = indicators.get('bb_middle', [])
    bb_lower = indicators.get('bb_lower', [])
    
    if not bb_upper:
        st.warning("Bollinger Bands data not available")
        return
    
    fig = go.Figure()
    
    # Price
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price'],
        mode='lines',
        name='Price',
        line=dict(color='blue', width=2)
    ))
    
    # Upper band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=bb_upper,
        mode='lines',
        name='Upper Band',
        line=dict(color='red', dash='dash')
    ))
    
    # Lower band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=bb_lower,
        mode='lines',
        name='Lower Band',
        line=dict(color='green', dash='dash'),
        fill='tonexty',
        fillcolor='rgba(128,128,128,0.1)'
    ))
    
    # Middle band
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=bb_middle,
        mode='lines',
        name='Middle Band (SMA 20)',
        line=dict(color='orange')
    ))
    
    fig.update_layout(
        title="Bollinger Bands",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Bollinger Bands interpretation
    current_price = df['price'].iloc[-1]
    current_upper = bb_upper[-1] if bb_upper else 0
    current_lower = bb_lower[-1] if bb_lower else 0
    
    if current_price > current_upper:
        st.warning("⚠️ Price above upper band - Potentially overbought")
    elif current_price < current_lower:
        st.success("✅ Price below lower band - Potentially oversold")
    else:
        st.info("📊 Price within normal range")

def calculate_sentiment_score(indicators):
    """Calculate overall market sentiment score"""
    bullish_signals = 0
    bearish_signals = 0
    
    current_values = indicators.get('current_values', {})
    
    # RSI analysis
    rsi = current_values.get('rsi')
    if rsi:
        if rsi < 30:
            bullish_signals += 1  # Oversold = potential buy
        elif rsi > 70:
            bearish_signals += 1  # Overbought = potential sell
    
    # MACD analysis
    macd = current_values.get('macd')
    if macd:
        if macd > 0:
            bullish_signals += 1
        else:
            bearish_signals += 1
    
    # Bollinger Bands analysis
    bb_position = current_values.get('bb_position')
    if bb_position:
        if bb_position < 0.2:
            bullish_signals += 1  # Near lower band
        elif bb_position > 0.8:
            bearish_signals += 1  # Near upper band
    
    # Determine overall sentiment
    if bullish_signals > bearish_signals:
        sentiment_label = "🟢 Bullish"
    elif bearish_signals > bullish_signals:
        sentiment_label = "🔴 Bearish"
    else:
        sentiment_label = "🟡 Neutral"
    
    return {
        'label': sentiment_label,
        'bullish': bullish_signals,
        'bearish': bearish_signals
    }

if __name__ == "__main__":
    main()
