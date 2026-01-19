# Technical Specifications: Authentication Module
# Educational Web Game Demo - Streamlit Platform

## 1. PROJECT OVERVIEW

### 1.1 Module Information
- **Module Name**: Authentication Module (Login & Register)
- **Platform**: Streamlit Cloud
- **Architecture Pattern**: Standalone modular component (designed for later integration into main router)
- **Primary Language**: Python 3.8+
- **Framework**: Streamlit

### 1.2 Purpose
Provide user registration and login functionality for the educational web game platform with in-memory session-based authentication.

---

## 2. SYSTEM ARCHITECTURE

### 2.1 Architecture Pattern
- **Type**: Modular Monolith
- **Deployment**: Single standalone Streamlit module
- **Integration Strategy**: Function-based navigation hooks for main router integration
- **State Management**: Streamlit session_state only (no external database)

### 2.2 Component Structure
```
auth_module.py
├── User Data Storage (in-memory dictionary)
├── Authentication Functions
│   ├── register_user()
│   ├── login_user()
│   └── hash_password()
├── UI Rendering Functions
│   ├── render_login_ui()
│   ├── render_register_ui()
│   └── render_auth_layout()
└── Navigation Placeholder
    └── navigate_to_home()
```

---

## 3. USER INTERFACE SPECIFICATIONS

### 3.1 Layout Design
- **Container**: Two-column card layout with centered alignment
- **Background**: Light pink gradient (#FFF0F5 to #FFE4E1)
- **Card Styling**: White rounded containers with subtle shadow
- **Responsive Behavior**: Stack columns on mobile devices

### 3.2 Left Column - Registration Form (Đăng ký)

#### 3.2.1 Visual Elements
- **Title**: "Đăng ký" (Pink, centered, bold)
- **Form Fields** (top to bottom):
  1. Full Name input ("Ho và tên")
     - Placeholder: "Nhập ho và tên"
  2. Username input ("Tên đăng nhập")
     - Placeholder: "Tên đăng nhập"
  3. Email input ("Email")
     - Placeholder: "example@email.com"
  4. Gender dropdown ("Giới tính")
     - Placeholder: "-- Chọn --"
     - Options: Male, Female, Other
  5. Password input ("Mật khẩu")
     - Placeholder: "Ít nhất 6 ký tự"
     - Type: password
  6. Confirm Password input ("Xác nhận mật khẩu")
     - Placeholder: "Nhập lại mật khẩu"
     - Type: password

#### 3.2.2 Action Elements
- **Primary Button**: "Đăng ký tài khoản"
  - Color: Pink (#FF69B4)
  - Full width
  - Rounded corners
- **Footer Text**: "Khi đăng ký, bạn đồng ý với các điều khoản sử dụng."
  - Font size: Small
  - Color: Gray

### 3.3 Right Column - Login Form (Đăng nhập)

#### 3.3.1 Visual Elements
- **Title**: "Đăng nhập" (Pink, centered, bold)
- **Form Fields** (top to bottom):
  1. Username/Email input ("Tên đăng nhập hoặc Email")
     - Placeholder: "Nhập thông tin đăng nhập"
  2. Password input ("Mật khẩu")
     - Placeholder: "Nhập mật khẩu"
     - Type: password

#### 3.3.2 Action Elements
- **Primary Button**: "Đăng nhập"
  - Color: Pink (#FF69B4)
  - Full width
  - Rounded corners
- **Footer Text**: "Quên mật khẩu? Vui lòng liên hệ quản trị viên."
  - Font size: Small
  - Color: Gray

### 3.4 Default View Behavior
- **Initial State**: Login form (right column) displayed
- **View Toggle**: Clicking "Register" button switches to registration form
- **No Popups**: All error/success messages displayed inline

---

## 4. FUNCTIONAL REQUIREMENTS

### 4.1 User Registration

#### 4.1.1 Input Validation
| Field | Validation Rules |
|-------|-----------------|
| Full Name | Required, min 2 characters |
| Username | Required, min 3 characters, alphanumeric only, must be unique |
| Email | Required, valid email format, must be unique |
| Gender | Required, must select from dropdown |
| Password | Required, minimum 6 characters |
| Confirm Password | Required, must match Password field |

#### 4.1.2 Registration Logic
1. Validate all input fields
2. Check username and email uniqueness
3. Hash password using secure algorithm
4. Store user data in session_state dictionary
5. Display success message inline
6. Auto-switch to login view

#### 4.1.3 Error Handling
- Display specific validation errors inline below respective fields
- Errors in Vietnamese language
- No popup dialogs

### 4.2 User Login

#### 4.2.1 Authentication Flow
1. Accept username OR email as identifier
2. Validate credentials against stored user data
3. Compare hashed password
4. On success: Call `navigate_to_home()` function
5. On failure: Display inline error message

#### 4.2.2 Error Messages
- "Sai tên đăng nhập hoặc mật khẩu" (Incorrect username/email or password)
- Displayed in red below login button
- No popup alerts

---

## 5. DATA SPECIFICATIONS

### 5.1 User Data Structure

```python
user_data = {
    "username": str,      # Unique identifier
    "email": str,         # Unique email address
    "password_hash": str, # Hashed password (never store plaintext)
    "full_name": str,     # Display name
    "gender": str         # "Male", "Female", or "Other"
}
```

### 5.2 Storage Implementation
- **Primary Storage**: `st.session_state['users']` (dictionary)
- **Key**: Username (string)
- **Value**: User data dictionary
- **Persistence**: Session-only (cleared on page refresh)

### 5.3 Session State Variables

```python
st.session_state = {
    'users': {},              # All registered users
    'logged_in': False,       # Authentication status
    'current_user': None,     # Currently logged-in username
    'view': 'login'           # Current view: 'login' or 'register'
}
```

---

## 6. SECURITY REQUIREMENTS

### 6.1 Password Security
- **Hashing Algorithm**: hashlib.sha256 (minimum requirement)
- **Salt**: Optional per implementation
- **Storage**: Only hashed passwords stored, never plaintext
- **Transmission**: N/A (no network transmission in this module)

### 6.2 Input Sanitization
- Strip whitespace from all inputs
- Validate email format using regex
- Prevent SQL injection (N/A - no database)
- Prevent XSS (handled by Streamlit framework)

---

## 7. TECHNICAL CONSTRAINTS

### 7.1 Dependencies
```python
streamlit>=1.28.0
hashlib (standard library)
re (standard library)
```

### 7.2 Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### 7.3 Performance Requirements
- Page load time: < 2 seconds
- Form submission: < 500ms response time
- No database queries (in-memory only)

---

## 8. CODE STRUCTURE REQUIREMENTS

### 8.1 File Organization
```python
# auth_module.py

# 1. Imports
import streamlit as st
import hashlib
import re

# 2. Helper Functions
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    pass

def validate_email(email: str) -> bool:
    """Validate email format using regex"""
    pass

def validate_registration(full_name, username, email, gender, password, confirm_password) -> tuple:
    """Validate all registration fields"""
    pass

# 3. Authentication Functions
def register_user(full_name, username, email, gender, password) -> bool:
    """Register new user and store in session_state"""
    pass

def login_user(identifier, password) -> bool:
    """Authenticate user with username/email and password"""
    pass

# 4. Navigation
def navigate_to_home():
    """Placeholder function for navigation to Home module"""
    pass

# 5. UI Rendering Functions
def render_login_ui():
    """Render login form UI"""
    pass

def render_register_ui():
    """Render registration form UI"""
    pass

def main():
    """Main application entry point"""
    pass

# 6. Application Entry
if __name__ == "__main__":
    main()
```

### 8.2 Naming Conventions
- **Functions**: snake_case
- **Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Session State Keys**: snake_case

### 8.3 Documentation Requirements
- Docstrings for all functions
- Inline comments for complex logic
- Vietnamese text for user-facing strings
- English for code comments

---

## 9. INTEGRATION SPECIFICATIONS

### 9.1 Module Interface
```python
# Expected integration pattern in main router:

if st.session_state.get('logged_in', False):
    home_module.main()  # Navigate to home
else:
    auth_module.main()  # Show authentication
```

### 9.2 State Handoff
- `st.session_state['logged_in']` = True on successful login
- `st.session_state['current_user']` = username of logged-in user
- Other modules can check authentication status via session_state

---

## 10. ERROR HANDLING

### 10.1 User Input Errors
| Error Type | Message (Vietnamese) | Display Location |
|------------|---------------------|------------------|
| Empty field | "Vui lòng điền đầy đủ thông tin" | Inline below field |
| Invalid email | "Email không hợp lệ" | Below email field |
| Password too short | "Mật khẩu phải có ít nhất 6 ký tự" | Below password field |
| Password mismatch | "Mật khẩu xác nhận không khớp" | Below confirm password |
| Username exists | "Tên đăng nhập đã tồn tại" | Below username field |
| Email exists | "Email đã được sử dụng" | Below email field |
| Login failed | "Sai tên đăng nhập hoặc mật khẩu" | Below login button |

### 10.2 System Errors
- Graceful degradation on session_state issues
- No crash on invalid state transitions
- Fallback to login view on any unexpected error

---

## 11. TESTING REQUIREMENTS

### 11.1 Unit Tests
- Password hashing function
- Email validation regex
- Registration validation logic
- Login authentication logic

### 11.2 Integration Tests
- Complete registration flow
- Complete login flow
- View switching (login ↔ register)
- Session state persistence

### 11.3 UI/UX Tests
- All form fields render correctly
- Buttons trigger correct actions
- Error messages display inline
- Vietnamese text displays properly

---

## 12. DEPLOYMENT SPECIFICATIONS

### 12.1 Streamlit Cloud Configuration
```toml
# .streamlit/config.toml
[theme]
primaryColor = "#FF69B4"
backgroundColor = "#FFF0F5"
secondaryBackgroundColor = "#FFE4E1"
textColor = "#333333"
font = "sans serif"
```

### 12.2 Requirements File
```txt
# requirements.txt
streamlit>=1.28.0
```

### 12.3 Environment Variables
- None required for this module

---

## 13. MAINTENANCE & EXTENSIBILITY

### 13.1 Future Enhancement Hooks
- Database integration placeholder (replace session_state storage)
- Password reset functionality (currently shows admin contact message)
- Email verification (placeholder in registration flow)
- OAuth integration points

### 13.2 Code Comments for Future Integration
```python
# TODO: Replace with database query when integrating with backend
# TODO: Add email verification before account activation
# TODO: Implement password reset via email
# TODO: Add rate limiting for login attempts
```

---

## 14. ACCEPTANCE CRITERIA

### 14.1 UI Match
✅ Visual design matches provided screenshot exactly
✅ No additional UI elements beyond specification
✅ Correct Vietnamese text labels
✅ Proper spacing and alignment

### 14.2 Functionality
✅ Registration creates new user account
✅ Login authenticates existing users
✅ Password hashing implemented
✅ Input validation works correctly
✅ Error messages display inline
✅ View switching works smoothly

### 14.3 Code Quality
✅ Self-contained module (single file)
✅ No syntax errors
✅ Clear function documentation
✅ Modular, reusable functions
✅ Easy to integrate into main router

---

## 15. GLOSSARY

| Term | Definition |
|------|------------|
| Session State | Streamlit's built-in state management system |
| In-memory Storage | Data stored in RAM, cleared on page refresh |
| Hash | One-way encryption of passwords |
| Inline Error | Error message displayed within the form, not in popup |
| Module | Standalone Python file with specific functionality |
| Router | Main application file that switches between modules |

---

## DOCUMENT CONTROL

**Version**: 1.0
**Last Updated**: 2026-01-19
**Author**: Senior Python Engineer
**Status**: Ready for Implementation
