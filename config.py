"""
Configuration utilities for Kaspa Analytics Pro
"""

import streamlit as st
from pathlib import Path
import yaml

def get_app_config():
    """Get application configuration"""
    return {
        'app_name': 'Kaspa Analytics Pro',
        'version': '1.0.0',
        'description': 'Professional Kaspa blockchain analysis platform',
        'support_email': 'support@kaspa-analytics.com',
        'website_url': 'https://kaspa-analytics.com',
        'social_links': {
            'twitter': 'https://twitter.com/kaspaanalytics',
            'discord': 'https://discord.gg/kaspa',
            'github': 'https://github.com/kaspa-analytics'
        }
    }
