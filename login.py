"""
Authentication Module for Educational Web Game Demo
Streamlit-based Login & Registration System
"""

import streamlit as st
import hashlib
import re


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash password using SHA-256 algorithm
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password in hexadecimal format
    """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email: str) -> bool:
    """
    Validate email format using regex
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_registration(full_name, username, email, gender, password, confirm_password):
    """
    Validate all registration form fields
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check empty fields
    if not all([full_name, username, email, gender, password, confirm_password]):
        return False, "Vui lòng điền đầy đủ thông tin"
    
    # Validate full name
    if len(full_name.strip()) < 2:
        return False, "Họ và tên phải có ít nhất 2 ký tự"
    
    # Validate username
    if len(username.strip()) < 3:
        return False, "Tên đăng nhập phải có ít nhất 3 ký tự"
    
    if not username.isalnum():
        return False, "Tên đăng nhập chỉ được chứa chữ cái và số"
    
    # Check username uniqueness
    if 'users' in st.session_state and username in st.session_state['users']:
        return False, "Tên đăng nhập đã tồn tại"
    
    # Validate email
    if not validate_email(email):
        return False, "Email không hợp lệ"
    
    # Check email uniqueness
    if 'users' in st.session_state:
        for user_data in st.session_state['users'].values():
            if user_data['email'] == email:
                return False, "Email đã được sử dụng"
    
    # Validate password
    if len(password) < 6:
        return False, "Mật khẩu phải có ít nhất 6 ký tự"
    
    # Validate password confirmation
    if password != confirm_password:
        return False, "Mật khẩu xác nhận không khớp"
    
    return True, ""


# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def register_user(full_name, username, email, gender, password):
    """
    Register new user and store in session_state
    
    Args:
        full_name (str): User's full name
        username (str): Unique username
        email (str): User's email address
        gender (str): User's gender
        password (str): User's password (will be hashed)
        
    Returns:
        bool: True if registration successful, False otherwise
    """
    # Initialize users dictionary if not exists
    if 'users' not in st.session_state:
        st.session_state['users'] = {}
    
    # Create user data
    user_data = {
        'username': username,
        'email': email,
        'password_hash': hash_password(password),
        'full_name': full_name,
        'gender': gender
    }
    
    # Store user
    st.session_state['users'][username] = user_data
    
    return True


def login_user(identifier, password):
    """
    Authenticate user with username/email and password
    
    Args:
        identifier (str): Username or email
        password (str): User's password
        
    Returns:
        tuple: (success, username or error_message)
    """
    if 'users' not in st.session_state or not st.session_state['users']:
        return False, "Sai tên đăng nhập hoặc mật khẩu"
    
    # Hash the input password
    password_hash = hash_password(password)
    
    # Search for user by username or email
    for username, user_data in st.session_state['users'].items():
        if (user_data['username'] == identifier or user_data['email'] == identifier):
            if user_data['password_hash'] == password_hash:
                return True, username
    
    return False, "Sai tên đăng nhập hoặc mật khẩu"


# ============================================================================
# NAVIGATION
# ============================================================================

def navigate_to_home():
    """
    Placeholder function for navigation to Home module
    This will be replaced when integrating with main router
    """
    st.success(f"Đăng nhập thành công! Chào mừng {st.session_state['current_user']}")
    st.info("🏠 Module Home sẽ được hiển thị tại đây khi tích hợp vào router chính")


# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_register_ui():
    """Render registration form UI"""
    st.markdown("<h2 style='text-align: center; color: #FF69B4;'>Đăng ký</h2>", unsafe_allow_html=True)
    
    # Form fields
    full_name = st.text_input("Họ và tên", placeholder="Nhập họ và tên", key="reg_fullname")
    username = st.text_input("Tên đăng nhập", placeholder="Tên đăng nhập", key="reg_username")
    email = st.text_input("Email", placeholder="example@email.com", key="reg_email")
    gender = st.selectbox("Giới tính", ["-- Chọn --", "Nam", "Nữ", "Khác"], key="reg_gender")
    password = st.text_input("Mật khẩu", type="password", placeholder="Ít nhất 6 ký tự", key="reg_password")
    confirm_password = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu", key="reg_confirm")
    
    # Error message placeholder
    error_placeholder = st.empty()
    
    # Register button
    if st.button("Đăng ký tài khoản", use_container_width=True, type="primary"):
        # Validate inputs
        gender_value = None if gender == "-- Chọn --" else gender
        is_valid, error_msg = validate_registration(
            full_name, username, email, gender_value, password, confirm_password
        )
        
        if is_valid:
            # Register user
            register_user(full_name, username, email, gender_value, password)
            st.success("✅ Đăng ký thành công! Vui lòng đăng nhập.")
            st.session_state['view'] = 'login'
            st.rerun()
        else:
            error_placeholder.error(error_msg)
    
    # Terms notice
    st.caption("Khi đăng ký, bạn đồng ý với các điều khoản sử dụng.")
    
    # Switch to login
    st.markdown("---")
    if st.button("Đã có tài khoản? Đăng nhập ngay"):
        st.session_state['view'] = 'login'
        st.rerun()


def render_login_ui():
    """Render login form UI"""
    st.markdown("<h2 style='text-align: center; color: #FF69B4;'>Đăng nhập</h2>", unsafe_allow_html=True)
    
    # Form fields
    identifier = st.text_input("Tên đăng nhập hoặc Email", placeholder="Nhập thông tin đăng nhập", key="login_identifier")
    password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu", key="login_password")
    
    # Error message placeholder
    error_placeholder = st.empty()
    
    # Login button
    if st.button("Đăng nhập", use_container_width=True, type="primary"):
        if not identifier or not password:
            error_placeholder.error("Vui lòng điền đầy đủ thông tin")
        else:
            success, result = login_user(identifier, password)
            if success:
                # Set session state
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = result
                st.rerun()
            else:
                error_placeholder.error(result)
    
    # Forgot password notice
    st.caption("Quên mật khẩu? Vui lòng liên hệ quản trị viên.")
    
    # Switch to register
    st.markdown("---")
    if st.button("Chưa có tài khoản? Đăng ký ngay"):
        st.session_state['view'] = 'register'
        st.rerun()


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="Đăng nhập / Đăng ký",
        page_icon="🔐",
        layout="centered"
    )
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%);
        }
        .stButton>button {
            background-color: #FF69B4;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #FF1493;
        }
        div[data-testid="stForm"] {
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'view' not in st.session_state:
        st.session_state['view'] = 'login'
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if 'current_user' not in st.session_state:
        st.session_state['current_user'] = None
    
    # Check if user is already logged in
    if st.session_state['logged_in']:
        navigate_to_home()
        
        # Logout button
        if st.button("Đăng xuất"):
            st.session_state['logged_in'] = False
            st.session_state['current_user'] = None
            st.rerun()
    else:
        # Show authentication forms
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.session_state['view'] == 'login':
                render_login_ui()
            else:
                render_register_ui()


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
