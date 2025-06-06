# pages/power_law.py - REPLACE ENTIRE FILE
"""
Power Law Analysis Page - Kaspa Analytics Pro
Mathematical price prediction models and regression analysis
"""

import streamlit as st
import streamlit_antd_components as sac
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from scipy import stats
import math

# Import utilities
from utils.auth import get_current_user, check_feature_access
from utils.data import fetch_kaspa_price_data, get_market_stats
from utils.ui import (
    render_page_header,
    show_login_prompt,
    show_upgrade_prompt,
    apply_custom_css,
    render_footer
)

def main():
    """Main power law analysis page"""
    
    # Get current user
    user = get_current_user()
    subscription = user['subscription']
    
    # Check access
    if subscription == 'public':
        show_login_prompt("Power Law analysis")
        st.stop()
    
    # Page header
    render_page_header(
        "📊 Power Law Analysis",
        "Mathematical price prediction models for Kaspa"
    )
    
    # Main content based on subscription level
    if subscription == 'free':
        render_basic_power_law()
    else:
        render_advanced_power_law(subscription)
    
    # Footer
    render_footer()

def render_basic_power_law():
    """Basic power law analysis for free users"""
    st.info("📊 Free Account - Basic Power Law Analysis")
    
    # Get data (30 days for free users)
    df = fetch_kaspa_price_data(30)
    
    if df.empty:
        st.error("Unable to load price data")
        return
    
    # Basic power law calculation
    power_law_data = calculate_basic_power_law(df)
    
    if not power_law_data:
        st.error("Unable to calculate power law")
        return
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Current Analysis")
        st.metric("Power Law Value", f"${power_law_data['current_value']:.4f}")
        st.metric("Current Price", f"${power_law_data['current_price']:.4f}")
        
        deviation = power_law_data['deviation']
        if deviation > 0:
            st.metric("vs Power Law", f"+{deviation:.1f}%", delta=f"{deviation:.1f}%")
            st.success("🟢 Price above power law trend")
        else:
            st.metric("vs Power Law", f"{deviation:.1f}%", delta=f"{deviation:.1f}%")
            st.error("🔴 Price below power law trend")
    
    with col2:
        st.markdown("### 📊 Model Statistics")
        st.metric("R-squared", f"{power_law_data['r_squared']:.3f}")
        st.metric("Data Points", len(df))
        st.metric("Time Range", "30 days")
        
        if power_law_data['r_squared'] > 0.8:
            st.success("✅ Strong correlation")
        elif power_law_data['r_squared'] > 0.6:
            st.warning("⚠️ Moderate correlation")
        else:
            st.error("❌ Weak correlation")
    
    # Basic chart
    fig = create_basic_power_law_chart(df, power_law_data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Interpretation
    st.subheader("📖 Interpretation")
    
    if deviation > 10:
        st.warning("⚠️ **Potentially Overvalued**: Price is significantly above the power law trend. Consider taking profits or waiting for a correction.")
    elif deviation < -10:
        st.success("✅ **Potentially Undervalued**: Price is significantly below the power law trend. This could be a buying opportunity.")
    else:
        st.info("📊 **Fair Value Range**: Price is close to the power law trend, suggesting fair valuation.")
    
    # Upgrade prompt
    st.markdown("---")
    show_upgrade_prompt('free', 'premium')

def render_advanced_power_law(subscription):
    """Advanced power law analysis for premium users"""
    st.success(f"🎉 {subscription.title()} Account - Advanced Power Law Analysis")
    
    # Get full historical data
    df = fetch_kaspa_price_data(730)  # 2 years of data
    
    if df.empty:
        st.error("Unable to load price data")
        return
    
    # Analysis tabs
    analysis_tabs = sac.tabs([
        sac.TabsItem(label='Power Law Model', icon='trending-up'),
        sac.TabsItem(label='Multiple Models', icon='layers'),
        sac.TabsItem(label='Predictions', icon='target'),
        sac.TabsItem(label='Statistics', icon='calculator'),
    ], key='power_law_tabs')
    
    if analysis_tabs == 'Power Law Model':
        render_main_power_law_tab(df, subscription)
    elif analysis_tabs == 'Multiple Models':
        render_multiple_models_tab(df)
    elif analysis_tabs == 'Predictions':
        render_predictions_tab(df)
    else:
        render_statistics_tab(df)

def render_main_power_law_tab(df, subscription):
    """Main power law analysis tab"""
    
    # Model configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_range = st.selectbox(
            "Analysis Period",
            ["3M", "6M", "1Y", "2Y", "All"],
            index=2,  # Default to 1Y
            key="power_law_time_range"
        )
    
    with col2:
        model_type = st.selectbox(
            "Model Type",
            ["Linear Regression", "Polynomial", "Exponential"],
            key="power_law_model_type"
        )
    
    with col3:
        confidence_level = st.selectbox(
            "Confidence Level",
            ["68%", "95%", "99%"],
            index=1,  # Default to 95%
            key="power_law_confidence"
        )
    
    # Filter data based on time range
    if time_range == "3M":
        analysis_data = df.tail(90 * 24)
    elif time_range == "6M":
        analysis_data = df.tail(180 * 24)
    elif time_range == "1Y":
        analysis_data = df.tail(365 * 24)
    elif time_range == "2Y":
        analysis_data = df.tail(730 * 24)
    else:
        analysis_data = df
    
    # Calculate advanced power law
    power_law_results = calculate_advanced_power_law(analysis_data, model_type)
    
    if not power_law_results:
        st.error("Unable to calculate power law model")
        return
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price",
            f"${power_law_results['current_price']:.4f}"
        )
    
    with col2:
        st.metric(
            "Power Law Value",
            f"${power_law_results['power_law_value']:.4f}"
        )
    
    with col3:
        deviation = power_law_results['deviation']
        st.metric(
            "Deviation",
            f"{deviation:+.1f}%",
            delta=f"{deviation:.1f}%"
        )
    
    with col4:
        st.metric(
            "R-squared",
            f"{power_law_results['r_squared']:.3f}"
        )
    
    # Advanced chart with confidence intervals
    fig = create_advanced_power_law_chart(analysis_data, power_law_results, confidence_level)
    st.plotly_chart(fig, use_container_width=True)
    
    # Model equation and parameters
    st.subheader("📐 Model Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Model Equation")
        if model_type == "Linear Regression":
            st.latex(f"y = {power_law_results['slope']:.6f} \\cdot x + {power_law_results['intercept']:.6f}")
        elif model_type == "Polynomial":
            st.latex("y = ax^2 + bx + c")
        else:
            st.latex("y = a \\cdot e^{bx}")
        
        st.write(f"**Slope:** {power_law_results.get('slope', 'N/A')}")
        st.write(f"**Intercept:** {power_law_results.get('intercept', 'N/A')}")
    
    with col2:
        st.markdown("#### Model Quality")
        r_squared = power_law_results['r_squared']
        
        if r_squared > 0.9:
            st.success(f"✅ Excellent fit (R² = {r_squared:.3f})")
        elif r_squared > 0.8:
            st.success(f"✅ Good fit (R² = {r_squared:.3f})")
        elif r_squared > 0.6:
            st.warning(f"⚠️ Moderate fit (R² = {r_squared:.3f})")
        else:
            st.error(f"❌ Poor fit (R² = {r_squared:.3f})")
        
        st.write(f"**Standard Error:** {power_law_results.get('std_error', 'N/A')}")
        st.write(f"**P-value:** {power_law_results.get('p_value', 'N/A')}")

def render_multiple_models_tab(df):
    """Multiple regression models comparison"""
    st.subheader("📊 Model Comparison")
    
    # Calculate multiple models
    models = ['Linear', 'Polynomial', 'Exponential', 'Logarithmic']
    model_results = {}
    
    for model in models:
        result = calculate_advanced_power_law(df, model)
        if result:
            model_results[model] = result
    
    if not model_results:
        st.error("Unable to calculate models")
        return
    
    # Model comparison table
    comparison_data = []
    for model_name, result in model_results.items():
        comparison_data.append({
            'Model': model_name,
            'R-squared': f"{result['r_squared']:.3f}",
            'Current Deviation': f"{result['deviation']:+.1f}%",
            'Predicted Value': f"${result['power_law_value']:.4f}"
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)
    
    # Best model recommendation
    best_model = max(model_results.items(), key=lambda x: x[1]['r_squared'])
    st.success(f"🏆 **Best Model:** {best_model[0]} (R² = {best_model[1]['r_squared']:.3f})")
    
    # Ensemble prediction
    ensemble_prediction = np.mean([result['power_law_value'] for result in model_results.values()])
    current_price = df['price'].iloc[-1]
    ensemble_deviation = ((current_price - ensemble_prediction) / ensemble_prediction) * 100
    
    st.info(f"🎯 **Ensemble Prediction:** ${ensemble_prediction:.4f} (Deviation: {ensemble_deviation:+.1f}%)")

def render_predictions_tab(df):
    """Price predictions based on power law"""
    st.subheader("🔮 Price Predictions")
    
    # Prediction timeframes
    timeframes = {
        "1 Week": 7,
        "1 Month": 30,
        "3 Months": 90,
        "6 Months": 180,
        "1 Year": 365
    }
    
    # Calculate predictions
    power_law_data = calculate_advanced_power_law(df, "Linear Regression")
    
    if not power_law_data:
        st.error("Unable to generate predictions")
        return
    
    predictions = []
    current_price = df['price'].iloc[-1]
    
    for timeframe, days in timeframes.items():
        # Simple linear extrapolation (in practice, you'd use more sophisticated methods)
        predicted_price = power_law_data['power_law_value'] * (1 + power_law_data['slope'] * days / 365)
        change_percent = ((predicted_price - current_price) / current_price) * 100
        
        predictions.append({
            'Timeframe': timeframe,
            'Predicted Price': f"${predicted_price:.4f}",
            'Change': f"{change_percent:+.1f}%",
            'Confidence': "Medium" if abs(change_percent) < 50 else "Low"
        })
    
    # Display predictions
    df_predictions = pd.DataFrame(predictions)
    st.dataframe(df_predictions, use_container_width=True)
    
    # Prediction chart
    fig = create_prediction_chart(df, power_law_data, timeframes)
    st.plotly_chart(fig, use_container_width=True)
    
    # Disclaimer
    st.warning("⚠️ **Disclaimer:** These predictions are based on mathematical models and should not be considered financial advice. Cryptocurrency prices are highly volatile and unpredictable.")

def render_statistics_tab(df):
    """Statistical analysis and model diagnostics"""
    st.subheader("📈 Statistical Analysis")
    
    # Calculate comprehensive statistics
    power_law_data = calculate_advanced_power_law(df, "Linear Regression")
    
    if not power_law_data:
        st.error("Unable to calculate statistics")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Model Diagnostics")
        st.metric("R-squared", f"{power_law_data['r_squared']:.4f}")
        st.metric("Adjusted R-squared", f"{power_law_data.get('adj_r_squared', 0):.4f}")
        st.metric("Standard Error", f"{power_law_data.get('std_error', 0):.6f}")
        st.metric("F-statistic", f"{power_law_data.get('f_statistic', 0):.2f}")
    
    with col2:
        st.markdown("#### Price Statistics")
        
        prices = df['price']
        st.metric("Mean Price", f"${prices.mean():.4f}")
        st.metric("Std Deviation", f"${prices.std():.4f}")
        st.metric("Min Price", f"${prices.min():.4f}")
        st.metric("Max Price", f"${prices.max():.4f}")
    
    # Residuals analysis
    st.markdown("#### 📊 Residuals Analysis")
    
    residuals = calculate_residuals(df, power_law_data)
    
    if residuals is not None:
        fig_residuals = create_residuals_chart(df, residuals)
        st.plotly_chart(fig_residuals, use_container_width=True)
        
        # Residuals statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mean Residual", f"{np.mean(residuals):.6f}")
        
        with col2:
            st.metric("Std Residuals", f"{np.std(residuals):.6f}")
        
        with col3:
            # Durbin-Watson test for autocorrelation
            dw_stat = calculate_durbin_watson(residuals)
            st.metric("Durbin-Watson", f"{dw_stat:.3f}")

# Calculation functions
def calculate_basic_power_law(df):
    """Calculate basic power law for free users"""
    try:
        # Simple linear regression on log-log scale
        prices = df['price'].values
        days = np.arange(len(prices))
        
        # Avoid log(0) by adding small value
        log_days = np.log(days + 1)
        log_prices = np.log(prices)
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_days, log_prices)
        
        # Calculate power law value for current day
        current_day = len(prices) - 1
        power_law_value = np.exp(intercept) * ((current_day + 1) ** slope)
        
        current_price = prices[-1]
        deviation = ((current_price - power_law_value) / power_law_value) * 100
        
        return {
            'current_price': current_price,
            'current_value': power_law_value,
            'deviation': deviation,
            'r_squared': r_value ** 2,
            'slope': slope,
            'intercept': intercept
        }
    
    except Exception as e:
        st.error(f"Error calculating power law: {e}")
        return None

def calculate_advanced_power_law(df, model_type):
    """Calculate advanced power law with different models"""
    try:
        prices = df['price'].values
        days = np.arange(len(prices))
        
        if model_type == "Linear Regression":
            # Log-log regression
            log_days = np.log(days + 1)
            log_prices = np.log(prices)
            slope, intercept, r_value, p_value, std_err = stats.linregress(log_days, log_prices)
            
            current_day = len(prices) - 1
            power_law_value = np.exp(intercept) * ((current_day + 1) ** slope)
            
        elif model_type == "Polynomial":
            # Polynomial regression (degree 2)
            coeffs = np.polyfit(days, prices, 2)
            poly_func = np.poly1d(coeffs)
            power_law_value = poly_func(len(prices) - 1)
            
            # Calculate R-squared for polynomial
            y_pred = poly_func(days)
            ss_res = np.sum((prices - y_pred) ** 2)
            ss_tot = np.sum((prices - np.mean(prices)) ** 2)
            r_value = np.sqrt(1 - (ss_res / ss_tot))
            slope, intercept, std_err, p_value = coeffs[0], coeffs[2], 0, 0
            
        elif model_type == "Exponential":
            # Exponential regression
            log_prices = np.log(prices)
            slope, intercept, r_value, p_value, std_err = stats.linregress(days, log_prices)
            power_law_value = np.exp(intercept + slope * (len(prices) - 1))
            
        else:  # Logarithmic
            log_days = np.log(days + 1)
            slope, intercept, r_value, p_value, std_err = stats.linregress(log_days, prices)
            power_law_value = intercept + slope * np.log(len(prices))
        
        current_price = prices[-1]
        deviation = ((current_price - power_law_value) / power_law_value) * 100
        
        return {
            'current_price': current_price,
            'power_law_value': power_law_value,
            'deviation': deviation,
            'r_squared': r_value ** 2,
            'slope': slope,
            'intercept': intercept,
            'std_error': std_err,
            'p_value': p_value
        }
    
    except Exception as e:
        st.error(f"Error calculating {model_type} model: {e}")
        return None

def calculate_residuals(df, power_law_data):
    """Calculate residuals for model diagnostics"""
    try:
        prices = df['price'].values
        days = np.arange(len(prices))
        
        # Calculate predicted values
        predicted_values = []
        for day in days:
            predicted = np.exp(power_law_data['intercept']) * ((day + 1) ** power_law_data['slope'])
            predicted_values.append(predicted)
        
        residuals = prices - np.array(predicted_values)
        return residuals
    
    except Exception:
        return None

def calculate_durbin_watson(residuals):
    """Calculate Durbin-Watson statistic for autocorrelation"""
    try:
        diff = np.diff(residuals)
        dw = np.sum(diff**2) / np.sum(residuals**2)
        return dw
    except Exception:
        return 0

# Chart creation functions
def create_basic_power_law_chart(df, power_law_data):
    """Create basic power law chart for free users"""
    fig = go.Figure()
    
    # Actual price
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price'],
        mode='lines',
        name='Actual Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    # Power law trend
    days = np.arange(len(df))
    power_law_line = [
        np.exp(power_law_data['intercept']) * ((day + 1) ** power_law_data['slope'])
        for day in days
    ]
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=power_law_line,
        mode='lines',
        name='Power Law Trend',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title="Basic Power Law Analysis (30 Days)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=500,
        template="plotly_white"
    )
    
    return fig

def create_advanced_power_law_chart(df, power_law_data, confidence_level):
    """Create advanced power law chart with confidence intervals"""
    fig = go.Figure()
    
    # Actual price
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price'],
        mode='lines',
        name='Actual Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    # Power law trend
    days = np.arange(len(df))
    power_law_line = []
    
    for day in days:
        if 'slope' in power_law_data and 'intercept' in power_law_data:
            value = np.exp(power_law_data['intercept']) * ((day + 1) ** power_law_data['slope'])
            power_law_line.append(value)
        else:
            power_law_line.append(df['price'].iloc[day])
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=power_law_line,
        mode='lines',
        name='Power Law Trend',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Confidence intervals (simplified)
    if confidence_level == "95%":
        multiplier = 1.96
    elif confidence_level == "99%":
        multiplier = 2.58
    else:
        multiplier = 1.0
    
    std_error = power_law_data.get('std_error', 0.1)
    upper_bound = [val * (1 + multiplier * std_error) for val in power_law_line]
    lower_bound = [val * (1 - multiplier * std_error) for val in power_law_line]
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=upper_bound,
        mode='lines',
        name=f'{confidence_level} Upper',
        line=dict(color='rgba(255,0,0,0.3)', width=1),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=lower_bound,
        mode='lines',
        name=f'{confidence_level} Lower',
        line=dict(color='rgba(255,0,0,0.3)', width=1),
        fill='tonexty',
        fillcolor='rgba(255,0,0,0.1)',
        showlegend=False
    ))
    
    fig.update_layout(
        title=f"Advanced Power Law Analysis - {confidence_level} Confidence Interval",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=600,
        template="plotly_white"
    )
    
    return fig

def create_prediction_chart(df, power_law_data, timeframes):
    """Create prediction chart showing future projections"""
    fig = go.Figure()
    
    # Historical price
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['price'],
        mode='lines',
        name='Historical Price',
        line=dict(color='#70C7BA', width=2)
    ))
    
    # Predictions (simplified)
    last_date = df['timestamp'].iloc[-1]
    last_price = df['price'].iloc[-1]
    
    future_dates = []
    future_prices = []
    
    for days in [7, 30, 90, 180, 365]:
        future_date = last_date + timedelta(days=days)
        # Simple linear extrapolation
        future_price = last_price * (1 + power_law_data['slope'] * days / 365)
        future_dates.append(future_date)
        future_prices.append(future_price)
    
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=future_prices,
        mode='lines+markers',
        name='Predictions',
        line=dict(color='red', width=2, dash='dot'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Price Predictions Based on Power Law",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=500,
        template="plotly_white"
    )
    
    return fig

def create_residuals_chart(df, residuals):
    """Create residuals analysis chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=residuals,
        mode='markers',
        name='Residuals',
        marker=dict(color='blue', opacity=0.6)
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    
    fig.update_layout(
        title="Residuals Analysis",
        xaxis_title="Date",
        yaxis_title="Residuals",
        height=400,
        template="plotly_white"
    )
    
    return fig

if __name__ == "__main__":
    main()
