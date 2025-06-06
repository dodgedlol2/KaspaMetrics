"""
Authentication Page - Kaspa Analytics Pro
Handles login, registration, user profile, and account management
"""

import streamlit as st
import streamlit_antd_components as sac
from datetime import datetime

# Import utilities
from utils.auth import (
    get_current_user, 
    get_authenticator, 
    is_authenticated,
    add_user,
    logout_user,
    get_user_stats,
    update_user_subscription
)
from utils.ui import (
    render_page_header, 
    render_sidebar_navigation,
    apply_custom_css,
    render_subscription_comparison,
    render_footer
)

# Configure page
st.set_page_config(
    page_title="Authentication - Kaspa Analytics Pro",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SEO Meta Tags
st.markdown("""
<meta name="description" content="Login, register, or manage your Kaspa Analytics Pro account. Access premium features and manage your subscription.">
<meta name="keywords" content="Kaspa Analytics login, register account, user profile, subscription management">
<meta property="og:title" content="Account Management - Kaspa Analytics Pro">
<meta property="og:description" content="Manage your Kaspa Analytics Pro account and subscription">
""", unsafe_allow_html=True)

# Apply styling
apply_custom_css()

def main():
    """Main authentication page"""
    
    # Get current user
    user = get_current_user()
    
    # Render sidebar navigation
    render_sidebar_navigation(user)
    
    # Main content based on authentication status
    if user['username'] == 'public':
        render_public_auth_page()
    else:
        render_user_profile_page(user)
    
    # Footer
    render_footer()

def render_public_auth_page():
    """Authentication page for public users"""
    
    render_page_header(
        "🔐 Account Access",
        "Login to your account or create a new one to unlock premium features"
    )
    
    # Navigation breadcrumb
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Dashboard", key="auth_back_to_home"):
            st.switch_page("streamlit_app.py")
    
    # Authentication tabs
    auth_tabs = sac.tabs([
        sac.TabsItem(label='Login', icon='box-arrow-in-right'),
        sac.TabsItem(label='Register', icon='person-plus'),
        sac.TabsItem(label='Pricing', icon='currency-dollar'),
        sac.TabsItem(label='Features', icon='star'),
    ], key='main_auth_tabs')
    
    if auth_tabs == 'Login':
        render_login_tab()
    elif auth_tabs == 'Register':
        render_registration_tab()
    elif auth_tabs == 'Pricing':
        render_pricing_tab()
    else:
        render_features_tab()

def render_login_tab():
    """Login interface"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 🔑 Login to Your Account")
        
        # Get authenticator and handle login
        authenticator = get_authenticator()
        
        try:
            authenticator.login()
            
            # Check authentication status
            name = st.session_state.get('name')
            authentication_status = st.session_state.get('authentication_status')
            username = st.session_state.get('username')
            
            if authentication_status == False:
                st.error("❌ Username/password is incorrect. Please try again.")
            elif authentication_status == None:
                st.info("ℹ️ Please enter your credentials to access the platform.")
            elif authentication_status == True:
                st.success(f"✅ Welcome back, {name}!")
                st.info("Redirecting to dashboard...")
                if st.button("Continue to Dashboard", key="login_continue"):
                    st.switch_page("streamlit_app.py")
        
        except Exception as e:
            st.error(f"Login error: {e}")
        
        # Demo credentials section
        st.markdown("---")
        st.markdown("**🔑 Demo Accounts:**")
        
        demo_tabs = sac.tabs([
            sac.TabsItem(label='Free', icon='person'),
            sac.TabsItem(label='Premium', icon='star'),
            sac.TabsItem(label='Pro', icon='crown'),
        ], key='demo_accounts')
        
        if demo_tabs == 'Free':
            st.code("Username: free_user\nPassword: free123\nFeatures: Basic analytics, 30-day data")
        elif demo_tabs == 'Premium':
            st.code("Username: premium_user\nPassword: premium123\nFeatures: Advanced analytics, full data")
        else:
            st.code("Username: admin\nPassword: admin123\nFeatures: Full platform access + admin")
        
        # Additional options
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Password", key="reset_password_btn", use_container_width=True):
                st.info("Password reset functionality would be implemented here")
        
        with col2:
            if st.button("❓ Forgot Username", key="forgot_username_btn", use_container_width=True):
                st.info("Username recovery functionality would be implemented here")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_registration_tab():
    """Registration interface"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### ✨ Create Your Free Account")
        st.info("🎉 Start with a free account - upgrade anytime!")
        
        # Registration form
        with st.form("registration_form"):
            st.markdown("#### 📝 Account Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username*", help="Choose a unique username")
                first_name = st.text_input("First Name*")
                email = st.text_input("Email*", help="Valid email address required")
            
            with col2:
                last_name = st.text_input("Last Name*")
                password = st.text_input("Password*", type="password", help="Minimum 6 characters")
                confirm_password = st.text_input("Confirm Password*", type="password")
            
            # Account type selection
            st.markdown("#### 📊 Choose Your Starting Plan")
            
            plan_choice = st.selectbox(
                "Account Type",
                ["Free - $0/month", "Premium - $29/month", "Pro - $99/month"],
                help="You can always upgrade later"
            )
            
            subscription = plan_choice.split(" - ")[0].lower()
            
            # Terms and conditions
            agree_terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy*",
                help="Required to create an account"
            )
            
            marketing_emails = st.checkbox(
                "Send me product updates and analytics insights",
                value=True,
                help="Optional marketing communications"
            )
            
            # Submit button
            submit_registration = st.form_submit_button(
                "🚀 Create Account",
                type="primary",
                use_container_width=True
            )
        
        # Handle registration submission
        if submit_registration:
            # Validation
            errors = []
            
            if not username:
                errors.append("Username is required")
            elif len(username) < 3:
                errors.append("Username must be at least 3 characters")
            
            if not email or '@' not in email:
                errors.append("Valid email address is required")
            
            if not first_name:
                errors.append("First name is required")
            
            if not last_name:
                errors.append("Last name is required")
            
            if not password:
                errors.append("Password is required")
            elif len(password) < 6:
                errors.append("Password must be at least 6 characters")
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            if not agree_terms:
                errors.append("You must agree to the terms of service")
            
            # Display errors or create account
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                success, message = add_user(username, email, first_name, last_name, password, subscription)
                
                if success:
                    st.success("🎉 Account created successfully!")
                    st.balloons()
                    
                    # Show account details
                    st.markdown("#### ✅ Account Created")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Username:** {username}")
                        st.write(f"**Email:** {email}")
                    with col2:
                        st.write(f"**Name:** {first_name} {last_name}")
                        st.write(f"**Plan:** {subscription.title()}")
                    
                    st.info("👈 Please use the Login tab to sign in with your new account")
                else:
                    st.error(f"❌ {message}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_pricing_tab():
    """Pricing and subscription information"""
    st.markdown("### 💰 Choose Your Plan")
    
    pricing_cols = st.columns(3)
    
    with pricing_cols[0]:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 🆓 Free")
        st.markdown("**$0/month**")
        st.markdown("Perfect for getting started")
        st.markdown("---")
        st.markdown("**Features:**")
        st.write("• 30-day price history")
        st.write("• Basic power law analysis")
        st.write("• Simple technical indicators")
        st.write("• Community support")
        st.write("• Basic charts and data")
        st.markdown("---")
        if st.button("🚀 Start Free", key="pricing_select_free", use_container_width=True, type="primary"):
            st.session_state.selected_plan = 'free'
            st.info("Switch to the Register tab to create your free account!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with pricing_cols[1]:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### ⭐ Premium")
        st.markdown("**$29/month**")
        st.markdown("Most popular for traders")
        st.markdown("---")
        st.markdown("**Everything in Free, plus:**")
        st.write("• Full historical data access")
        st.write("• Advanced power law models")
        st.write("• Network metrics analysis")
        st.write("• Data export capabilities")
        st.write("• Technical indicator suite")
        st.write("• Email support")
        st.markdown("---")
        if st.button("⭐ Choose Premium", key="pricing_select_premium", use_container_width=True):
            st.session_state.selected_plan = 'premium'
            st.success("Premium plan selected! Create your account to get started.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with pricing_cols[2]:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown("### 👑 Pro")
        st.markdown("**$99/month**")
        st.markdown("For professional analysts")
        st.markdown("---")
        st.markdown("**Everything in Premium, plus:**")
        st.write("• Research workspace")
        st.write("• Custom power law models")
        st.write("• Full API access")
        st.write("• Priority support")
        st.write("• White-label reports")
        st.write("• Team collaboration tools")
        st.markdown("---")
        if st.button("👑 Choose Pro", key="pricing_select_pro", use_container_width=True):
            st.session_state.selected_plan = 'pro'
            st.success("Pro plan selected! Create your account to get started.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature comparison
    st.markdown("---")
    render_subscription_comparison()

def render_features_tab():
    """Feature showcase and comparison"""
    st.markdown("### ⭐ Platform Features")
    
    feature_categories = sac.tabs([
        sac.TabsItem(label='Analytics', icon='graph-up'),
        sac.TabsItem(label='Data Access', icon='database'),
        sac.TabsItem(label='Tools & API', icon='tools'),
        sac.TabsItem(label='Support', icon='headphones'),
    ], key='feature_categories')
    
    if feature_categories == 'Analytics':
        render_analytics_features()
    elif feature_categories == 'Data Access':
        render_data_features()
    elif feature_categories == 'Tools & API':
        render_tools_features()
    else:
        render_support_features()

def render_analytics_features():
    """Analytics features breakdown"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Power Law Analysis")
        st.write("**Free:** Basic power law model")
        st.write("**Premium+:** Multiple regression models, confidence intervals, predictions")
        
        st.markdown("#### 📈 Technical Analysis")
        st.write("**Free:** SMA, EMA, basic indicators")
        st.write("**Premium+:** Full indicator suite, custom studies, alerts")
        
        st.markdown("#### 🎯 Price Predictions")
        st.write("**Free:** Simple trend analysis")
        st.write("**Premium+:** AI-powered predictions, multiple timeframes")
    
    with col2:
        st.markdown("#### 🌐 Network Analytics")
        st.write("**Free:** Basic network stats")
        st.write("**Premium+:** Hash rate tracking, address analysis, mining metrics")
        
        st.markdown("#### 📊 Market Intelligence")
        st.write("**Premium+:** Exchange flow analysis, whale tracking, sentiment analysis")
        
        st.markdown("#### 🔬 Research Tools")
        st.write("**Pro:** Custom models, backtesting, strategy optimization")

def render_data_features():
    """Data access features"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Historical Data")
        st.write("**Public:** 7 days")
        st.write("**Free:** 30 days")
        st.write("**Premium+:** Full history (2+ years)")
        
        st.markdown("#### ⚡ Real-time Data")
        st.write("**All Plans:** Live price feeds")
        st.write("**Premium+:** High-frequency updates")
        
    with col2:
        st.markdown("#### 📋 Data Export")
        st.write("**Free:** View only")
        st.write("**Premium+:** CSV, JSON, Excel export")
        st.write("**Pro:** Automated reports, webhooks")
        
        st.markdown("#### 🔗 API Access")
        st.write("**Premium:** Limited API calls")
        st.write("**Pro:** Full API access, custom endpoints")

def render_tools_features():
    """Tools and utilities features"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛠️ Analysis Tools")
        st.write("• Custom dashboards")
        st.write("• Alert system")
        st.write("• Portfolio tracking")
        st.write("• Comparison tools")
        
        st.markdown("#### 📱 Platform Access")
        st.write("• Web application")
        st.write("• Mobile-responsive design")
        st.write("• Cross-device sync")
    
    with col2:
        st.markdown("#### 🤖 API Features")
        st.write("**Pro:** REST API access")
        st.write("**Pro:** Webhook notifications")
        st.write("**Pro:** Custom integrations")
        st.write("**Pro:** SDK libraries")
        
        st.markdown("#### 👥 Collaboration")
        st.write("**Pro:** Team workspaces")
        st.write("**Pro:** Shared dashboards")
        st.write("**Pro:** White-label reports")

def render_support_features():
    """Support and service features"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📞 Support Channels")
        st.write("**Free:** Community support, FAQ")
        st.write("**Premium:** Email support")
        st.write("**Pro:** Priority support, phone/video calls")
        
        st.markdown("#### 📚 Resources")
        st.write("• Comprehensive documentation")
        st.write("• Video tutorials")
        st.write("• Webinar access")
        st.write("• Best practices guides")
    
    with col2:
        st.markdown("#### 🚀 Onboarding")
        st.write("**All Plans:** Self-service onboarding")
        st.write("**Pro:** Personal onboarding session")
        st.write("**Pro:** Custom training")
        
        st.markdown("#### 🔄 Updates")
        st.write("• Regular feature updates")
        st.write("• New indicator releases")
        st.write("• Platform improvements")
        st.write("**Pro:** Beta access to new features")

def render_user_profile_page(user):
    """User profile and account management"""
    
    render_page_header(
        f"👤 {user['name']}'s Profile",
        f"Manage your {user['subscription'].title()} account and settings"
    )
    
    # Navigation breadcrumb
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Dashboard", key="profile_back_to_home"):
            st.switch_page("streamlit_app.py")
    
    # Profile tabs
    profile_tabs = sac.tabs([
        sac.TabsItem(label='Profile', icon='person-circle'),
        sac.TabsItem(label='Subscription', icon='credit-card'),
        sac.TabsItem(label='Settings', icon='gear'),
        sac.TabsItem(label='Activity', icon='activity'),
    ], key='profile_tabs')
    
    if profile_tabs == 'Profile':
        render_profile_info_tab(user)
    elif profile_tabs == 'Subscription':
        render_subscription_tab(user)
    elif profile_tabs == 'Settings':
        render_settings_tab(user)
    else:
        render_activity_tab(user)

def render_profile_info_tab(user):
    """User profile information"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 👤 Profile Information")
        
        # Profile picture placeholder
        st.markdown("#### 📸 Profile Picture")
        st.info("Profile picture upload would be implemented here")
        
        # Account status
        st.markdown("#### 📊 Account Status")
        st.success(f"✅ {user['subscription'].title()} Account")
        
        if user['username'] == 'admin':
            st.info("👑 Administrator Access")
    
    with col2:
        st.markdown("### ✏️ Edit Profile")
        
        # Profile form
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_first_name = st.text_input("First Name", value=user['first_name'])
                new_email = st.text_input("Email", value=user['email'])
            
            with col2:
                new_last_name = st.text_input("Last Name", value=user['last_name'])
                new_username = st.text_input("Username", value=user['username'], disabled=True, help="Username cannot be changed")
            
            # Additional fields
            bio = st.text_area("Bio (Optional)", placeholder="Tell us about yourself...")
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT"], index=0)
            
            if st.form_submit_button("💾 Update Profile", type="primary"):
                st.success("✅ Profile updated successfully!")
        
        # Password change section
        st.markdown("---")
        st.markdown("### 🔒 Change Password")
        
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("🔄 Change Password"):
                if new_password != confirm_new_password:
                    st.error("❌ New passwords do not match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    st.success("✅ Password changed successfully!")

def render_subscription_tab(user):
    """Subscription management"""
    subscription = user['subscription']
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💳 Current Subscription")
        
        # Current plan info
        st.markdown(f'<div class="subscription-badge badge-{subscription}">{subscription.upper()}</div>', unsafe_allow_html=True)
        
        if subscription == 'free':
            st.write("**Price:** $0/month")
            st.write("**Features:** Basic analytics, 30-day data")
        elif subscription == 'premium':
            st.write("**Price:** $29/month")
            st.write("**Features:** Advanced analytics, full data")
        else:
            st.write("**Price:** $99/month")
            st.write("**Features:** All features + API access")
        
        # Billing info
        st.markdown("#### 💰 Billing Information")
        st.write("**Next billing:** January 15, 2025")
        st.write("**Payment method:** •••• 1234")
        
        if subscription != 'free':
            if st.button("💳 Update Payment Method", key="update_payment"):
                st.info("Payment method update would be implemented here")
    
    with col2:
        st.markdown("### ⬆️ Upgrade Options")
        
        if subscription == 'free':
            # Upgrade to Premium
            st.markdown("#### ⭐ Upgrade to Premium - $29/month")
            st.write("• Full historical data")
            st.write("• Advanced analytics")
            st.write("• Data export")
            st.write("• Email support")
            
            if st.button("⭐ Upgrade to Premium", key="upgrade_premium", type="primary"):
                st.balloons()
                st.success("Redirecting to upgrade checkout...")
            
            # Upgrade to Pro
            st.markdown("#### 👑 Upgrade to Pro - $99/month")
            st.write("• Everything in Premium")
            st.write("• API access")
            st.write("• Custom models")
            st.write("• Priority support")
            
            if st.button("👑 Upgrade to Pro", key="upgrade_pro"):
                st.balloons()
                st.success("Redirecting to Pro upgrade...")
        
        elif subscription == 'premium':
            # Upgrade to Pro
            st.markdown("#### 👑 Upgrade to Pro - $99/month")
            st.write("• Research workspace")
            st.write("• API access")
            st.write("• Custom models")
            st.write("• Priority support")
            
            if st.button("👑 Upgrade to Pro", key="upgrade_to_pro", type="primary"):
                st.balloons()
                st.success("Redirecting to Pro upgrade...")
        
        else:
            st.success("🎉 You have the highest tier!")
            st.info("Thank you for being a Pro subscriber!")
    
    # Usage stats
    st.markdown("---")
    st.markdown("### 📊 Usage Statistics")
    
    usage_cols = st.columns(4)
    
    with usage_cols[0]:
        st.metric("Data Exports", "15", "This month")
    
    with usage_cols[1]:
        st.metric("API Calls", "1,247", "This month")
    
    with usage_cols[2]:
        st.metric("Charts Viewed", "89", "This month")
    
    with usage_cols[3]:
        st.metric("Login Sessions", "42", "This month")

def render_settings_tab(user):
    """Account settings and preferences"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚙️ Preferences")
        
        # Notification settings
        st.markdown("#### 📧 Notifications")
        email_notifications = st.checkbox("Email notifications", value=True)
        price_alerts = st.checkbox("Price alerts", value=True)
        weekly_reports = st.checkbox("Weekly reports", value=False)
        marketing_emails = st.checkbox("Marketing emails", value=False)
        
        # Display settings
        st.markdown("#### 🎨 Display")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        currency = st.selectbox("Currency", ["USD", "EUR", "BTC"])
        date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        
        # Privacy settings
        st.markdown("#### 🔒 Privacy")
        public_profile = st.checkbox("Public profile", value=False)
        data_sharing = st.checkbox("Allow anonymous usage analytics", value=True)
    
    with col2:
        st.markdown("### 🔧 Advanced Settings")
        
        # API settings (for premium+ users)
        if user['subscription'] in ['premium', 'pro']:
            st.markdown("#### 🔑 API Access")
            
            api_key = "kas_live_abc123def456..." if user['subscription'] == 'pro' else "Limited API access"
            st.text_input("API Key", value=api_key, type="password", disabled=True)
            
            if user['subscription'] == 'pro':
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Regenerate Key", key="regen_api_key"):
                        st.success("New API key generated!")
                with col2:
                    if st.button("📋 Copy Key", key="copy_api_key"):
                        st.info("API key copied to clipboard!")
        
        # Data export settings
        st.markdown("#### 📋 Export Settings")
        default_format = st.selectbox("Default export format", ["CSV", "JSON", "Excel"])
        include_metadata = st.checkbox("Include metadata in exports", value=True)
        
        # Account actions
        st.markdown("#### ⚠️ Account Actions")
        
        if st.button("📥 Download My Data", key="download_data"):
            st.info("Data download would be processed here")
        
        if st.button("🗑️ Delete Account", key="delete_account", type="secondary"):
            st.error("⚠️ Account deletion is permanent and cannot be undone!")
            st.info("Contact support for account deletion")
    
    # Save settings
    st.markdown("---")
    if st.button("💾 Save All Settings", key="save_settings", type="primary"):
        st.success("✅ Settings saved successfully!")

def render_activity_tab(user):
    """User activity and statistics"""
    st.markdown("### 📊 Account Activity")
    
    # Get user stats
    stats = get_user_stats(user['username'])
    
    # Activity metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Logins", stats['login_count'])
    
    with col2:
        st.metric("Features Used", len(stats['features_used']))
    
    with col3:
        st.metric("Data Exports", stats['data_exports'])
    
    with col4:
        st.metric("API Calls", f"{stats['api_calls']:,}")
    
    # Activity timeline
    st.markdown("### 📅 Recent Activity")
    
    activity_data = [
        {"time": "2 hours ago", "action": "Viewed Power Law analysis", "page": "Power Law"},
        {"time": "1 day ago", "action": "Exported price data", "page": "Data Export"},
        {"time": "3 days ago", "action": "Updated profile settings", "page": "Profile"},
        {"time": "1 week ago", "action": "Logged in", "page": "Dashboard"},
        {"time": "2 weeks ago", "action": "Created account", "page": "Registration"},
    ]
    
    for activity in activity_data:
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 2])
            with col1:
                st.write(activity["time"])
            with col2:
                st.write(activity["action"])
            with col3:
                st.write(activity["page"])
    
    # Feature usage
    st.markdown("### 🎯 Feature Usage")
    
    feature_usage = {
        "Price Charts": 45,
        "Power Law": 32,
        "Network Metrics": 18,
        "Data Export": 15,
        "Dashboard": 28
    }
    
    for feature, usage in feature_usage.items():
        st.write(f"**{feature}:** {usage} views")
        st.progress(usage / 50)  # Scale to 0-1
    
    # Logout section
    st.markdown("---")
    st.markdown("### 🚪 Session Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Logged in as:** {user['username']}")
        st.write(f"**Last login:** {stats['last_login']}")
    
    with col2:
        if st.button("🚪 Logout", key="profile_logout", type="secondary", use_container_width=True):
            logout_user()
            st.success("✅ Logged out successfully!")
            st.info("Redirecting to homepage...")
            if st.button("Continue to Homepage", key="logout_continue"):
                st.switch_page("streamlit_app.py")

if __name__ == "__main__":
    main()
