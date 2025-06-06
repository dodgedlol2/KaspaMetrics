"""
Data management utilities for Kaspa Analytics Pro
Handles data fetching, processing, and caching
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
from typing import Optional, Dict, Any
import time

# Try to import Plotly, fallback gracefully
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_kaspa_price_data(days_back: int = 365) -> pd.DataFrame:
    """
    Fetch Kaspa price data
    In production, this would connect to real APIs like CoinGecko, CoinMarketCap, etc.
    """
    try:
        # Generate realistic mock data for demo
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        dates = pd.date_range(start=start_date, end=end_date, freq='H')  # Hourly data
        
        np.random.seed(42)
        
        # Base price and trend
        base_price = 0.025
        n_points = len(dates)
        
        # Create realistic price movement
        price_changes = np.random.normal(0, 0.02, n_points)  # 2% hourly volatility
        trend = np.linspace(0, 0.01, n_points)  # Slight upward trend
        
        # Add some cyclical patterns
        cyclical = 0.003 * np.sin(np.arange(n_points) / 24 * 2 * np.pi)  # Daily cycle
        weekly_cycle = 0.005 * np.sin(np.arange(n_points) / (24*7) * 2 * np.pi)  # Weekly cycle
        
        # Combine all price factors
        cumulative_changes = np.cumsum(price_changes + trend + cyclical + weekly_cycle)
        prices = base_price * np.exp(cumulative_changes / 10)  # Scale down changes
        
        # Ensure prices are positive
        prices = np.maximum(prices, 0.001)
        
        # Generate volume data (inversely correlated with price stability)
        volatility = np.abs(np.diff(np.concatenate([[0], price_changes])))
        base_volume = 1000000
        volumes = base_volume * (1 + 2 * volatility) * np.random.lognormal(0, 0.5, n_points)
        
        # Create DataFrame
        df = pd.DataFrame({
            'timestamp': dates,
            'price': prices,
            'volume': volumes,
            'high': prices * (1 + np.random.uniform(0, 0.02, n_points)),
            'low': prices * (1 - np.random.uniform(0, 0.02, n_points)),
            'open': np.roll(prices, 1),  # Previous price as open
            'close': prices
        })
        
        # Fix first open price
        df.loc[0, 'open'] = df.loc[0, 'close']
        
        return df
        
    except Exception as e:
        st.error(f"Error fetching price data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_real_kaspa_price() -> Optional[Dict[str, Any]]:
    """
    Fetch real Kaspa price from external API
    This is a placeholder for real API integration
    """
    try:
        # Example API call (replace with real endpoint)
        # response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=kaspa&vs_currencies=usd&include_24hr_change=true")
        # data = response.json()
        
        # Mock real-time data for demo
        df = fetch_kaspa_price_data(1)
        if not df.empty:
            current_price = df['price'].iloc[-1]
            prev_price = df['price'].iloc[-24] if len(df) > 24 else current_price
            change_24h = ((current_price - prev_price) / prev_price) * 100
            
            return {
                'price': current_price,
                'change_24h': change_24h,
                'volume_24h': df['volume'].tail(24).sum(),
                'market_cap': current_price * 18_500_000_000,  # Approximate circulating supply
                'last_updated': datetime.now().isoformat()
            }
        
        return None
        
    except Exception as e:
        st.error(f"Error fetching real-time data: {e}")
        return None

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_network_metrics() -> Dict[str, Any]:
    """
    Fetch Kaspa network metrics
    In production, this would connect to Kaspa node APIs or blockchain explorers
    """
    try:
        # Mock network data for demo
        np.random.seed(int(time.time()) // 600)  # Change every 10 minutes
        
        base_hashrate = 1.2  # EH/s
        hashrate_variation = np.random.normal(0, 0.1)
        current_hashrate = max(0.5, base_hashrate + hashrate_variation)
        
        return {
            'hash_rate': current_hashrate,
            'difficulty': current_hashrate * 2.8e15,
            'block_time': np.random.normal(1.0, 0.05),  # ~1 second blocks
            'active_addresses': np.random.randint(40000, 50000),
            'transaction_count_24h': np.random.randint(800000, 1200000),
            'mempool_size': np.random.randint(100, 5000),
            'network_fee_avg': np.random.uniform(0.0001, 0.001),
            'circulating_supply': 18_500_000_000,  # Approximate
            'last_updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        st.error(f"Error fetching network metrics: {e}")
        return {}

def get_market_stats(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate market statistics from price data"""
    if df.empty:
        return {}
    
    try:
        current_price = df['price'].iloc[-1]
        
        # Calculate various time period changes
        price_1d = df['price'].iloc[-24] if len(df) > 24 else current_price
        price_7d = df['price'].iloc[-168] if len(df) > 168 else current_price
        price_30d = df['price'].iloc[-720] if len(df) > 720 else current_price
        
        change_24h = ((current_price - price_1d) / price_1d) * 100
        change_7d = ((current_price - price_7d) / price_7d) * 100
        change_30d = ((current_price - price_30d) / price_30d) * 100
        
        # Volume statistics
        volume_24h = df['volume'].tail(24).sum()
        volume_7d_avg = df['volume'].tail(168).mean()
        
        # Price statistics
        high_24h = df['high'].tail(24).max()
        low_24h = df['low'].tail(24).min()
        
        # Market cap (approximate)
        market_cap = current_price * 18.5  # 18.5B approximate supply
        
        # Network metrics
        network_data = fetch_network_metrics()
        
        return {
            'current_price': current_price,
            'price_change_24h': change_24h,
            'price_change_7d': change_7d,
            'price_change_30d': change_30d,
            'volume_24h': volume_24h,
            'volume_7d_avg': volume_7d_avg,
            'high_24h': high_24h,
            'low_24h': low_24h,
            'market_cap': market_cap,
            'hash_rate': network_data.get('hash_rate', 0),
            'active_addresses': network_data.get('active_addresses', 0)
        }
        
    except Exception as e:
        st.error(f"Error calculating market stats: {e}")
        return {}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def calculate_power_law_models(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate power law models for price prediction
    """
    if df.empty or len(df) < 100:
        return {}
    
    try:
        # Convert timestamps to days since start
        start_date = df['timestamp'].min()
        df_calc = df.copy()
        df_calc['days_since_start'] = (df_calc['timestamp'] - start_date).dt.total_seconds() / (24 * 3600)
        
        # Remove zero and negative prices
        df_calc = df_calc[df_calc['price'] > 0]
        
        if len(df_calc) < 50:
            return {}
        
        # Calculate different power law models
        days = df_calc['days_since_start'].values
        prices = df_calc['price'].values
        
        # Model 1: Conservative (lower growth)
        conservative_model = 0.01 * np.power(days / 365 + 0.1, 1.2) + 0.008
        
        # Model 2: Base model (medium growth)
        base_model = 0.015 * np.power(days / 365 + 0.1, 1.5) + 0.01
        
        # Model 3: Aggressive (higher growth)
        aggressive_model = 0.02 * np.power(days / 365 + 0.1, 1.8) + 0.012
        
        # Calculate deviations
        current_price = prices[-1]
        conservative_deviation = (current_price / conservative_model[-1] - 1) * 100
        base_deviation = (current_price / base_model[-1] - 1) * 100
        aggressive_deviation = (current_price / aggressive_model[-1] - 1) * 100
        
        # Calculate R-squared for base model
        price_log = np.log(prices)
        days_log = np.log(days + 1)
        correlation = np.corrcoef(price_log, days_log)[0, 1]
        r_squared = correlation ** 2
        
        return {
            'timestamps': df_calc['timestamp'].tolist(),
            'actual_prices': prices.tolist(),
            'conservative_model': conservative_model.tolist(),
            'base_model': base_model.tolist(),
            'aggressive_model': aggressive_model.tolist(),
            'deviations': {
                'conservative': conservative_deviation,
                'base': base_deviation,
                'aggressive': aggressive_deviation
            },
            'statistics': {
                'r_squared': r_squared,
                'correlation': correlation,
                'data_points': len(df_calc)
            }
        }
        
    except Exception as e:
        st.error(f"Error calculating power law models: {e}")
        return {}

def filter_data_by_subscription(df: pd.DataFrame, subscription_level: str) -> pd.DataFrame:
    """Filter data based on user subscription level"""
    if df.empty:
        return df
    
    data_limits = {
        'public': 7 * 24,      # 7 days (hourly data)
        'free': 30 * 24,       # 30 days
        'premium': 0,          # Unlimited
        'pro': 0               # Unlimited
    }
    
    limit = data_limits.get(subscription_level, 7 * 24)
    
    if limit == 0:  # Unlimited
        return df
    else:
        return df.tail(limit)

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate technical indicators"""
    if df.empty or len(df) < 50:
        return {}
    
    try:
        prices = df['price'].values
        
        # Simple Moving Averages
        sma_20 = pd.Series(prices).rolling(window=20).mean().values
        sma_50 = pd.Series(prices).rolling(window=50).mean().values
        
        # Exponential Moving Average
        ema_12 = pd.Series(prices).ewm(span=12).mean().values
        ema_26 = pd.Series(prices).ewm(span=26).mean().values
        
        # MACD
        macd_line = ema_12 - ema_26
        macd_signal = pd.Series(macd_line).ewm(span=9).mean().values
        macd_histogram = macd_line - macd_signal
        
        # RSI
        price_changes = np.diff(prices)
        gains = np.where(price_changes > 0, price_changes, 0)
        losses = np.where(price_changes < 0, -price_changes, 0)
        
        avg_gains = pd.Series(gains).rolling(window=14).mean().values
        avg_losses = pd.Series(losses).rolling(window=14).mean().values
        
        rs = avg_gains / (avg_losses + 1e-10)  # Avoid division by zero
        rsi = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        bb_middle = sma_20
        bb_std = pd.Series(prices).rolling(window=20).std().values
        bb_upper = bb_middle + (bb_std * 2)
        bb_lower = bb_middle - (bb_std * 2)
        
        return {
            'sma_20': sma_20.tolist(),
            'sma_50': sma_50.tolist(),
            'ema_12': ema_12.tolist(),
            'ema_26': ema_26.tolist(),
            'macd_line': macd_line.tolist(),
            'macd_signal': macd_signal.tolist(),
            'macd_histogram': macd_histogram.tolist(),
            'rsi': rsi.tolist(),
            'bb_upper': bb_upper.tolist(),
            'bb_middle': bb_middle.tolist(),
            'bb_lower': bb_lower.tolist(),
            'current_values': {
                'rsi': rsi[-1] if len(rsi) > 0 else None,
                'macd': macd_line[-1] if len(macd_line) > 0 else None,
                'bb_position': ((prices[-1] - bb_lower[-1]) / (bb_upper[-1] - bb_lower[-1])) if len(bb_upper) > 0 else None
            }
        }
        
    except Exception as e:
        st.error(f"Error calculating technical indicators: {e}")
        return {}

def export_data_to_csv(df: pd.DataFrame, filename: str = None) -> str:
    """Export data to CSV format"""
    if filename is None:
        filename = f"kaspa_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return df.to_csv(index=False)

def export_data_to_json(df: pd.DataFrame) -> str:
    """Export data to JSON format"""
    return df.to_json(orient='records', date_format='iso')

@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_historical_events() -> list:
    """Get historical events that might affect Kaspa price"""
    # This would typically come from a database or news API
    return [
        {
            'date': '2024-01-15',
            'event': 'Major exchange listing announced',
            'impact': 'positive',
            'price_change': '+15%'
        },
        {
            'date': '2024-01-10',
            'event': 'Network upgrade completed',
            'impact': 'positive',
            'price_change': '+8%'
        },
        {
            'date': '2024-01-05',
            'event': 'Partnership announcement',
            'impact': 'positive',
            'price_change': '+12%'
        }
    ]
