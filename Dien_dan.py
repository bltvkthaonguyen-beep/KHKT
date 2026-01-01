import streamlit as st
import sqlite3
from datetime import datetime
import hashlib
import re

# ============= CẤU HÌNH =============
st.set_page_config(page_title="Diễn Đàn Học Đường", page_icon="💬", layout="wide")

# CSS tùy chỉnh cho giao diện
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: white !important;
        color: #333 !important;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #42A5F5;
        color: white;
        border: none;
        padding: 8px 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1E88E5;
        transform: translateY(-2px);
    }
    .post-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.3s;
    }
    .post-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        transform: translateY(-3px);
    }
    .comment-box {
        background: #F5F5F5;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #42A5F5;
        color: #333;
    }
    .stat-badge {
        display: inline-block;
        background: #E3F2FD;
        padding: 5px 12px;
        border-radius: 15px;
        margin: 5px;
        font-size: 14px;
    }
    .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============= DATABASE =============
def init_db():
    """Khởi tạo database SQLite"""
    conn = sqlite3.connect('forum.db', check_same_thread=False)
    c = conn.cursor()
    
    # Bảng bài viết
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  username TEXT NOT NULL,
                  views INTEGER DEFAULT 0,
                  likes INTEGER DEFAULT 0,
                  created_at TEXT NOT NULL)''')
    
    # Bảng bình luận
    c.execute('''CREATE TABLE IF NOT EXISTS comments
                 (comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  post_id INTEGER NOT NULL,
                  username TEXT NOT NULL,
                  content TEXT NOT NULL,
                  created_at TEXT NOT NULL,
                  FOREIGN KEY (post_id) REFERENCES posts(post_id))''')
    
    # Bảng lưu likes (chống spam like)
    c.execute('''CREATE TABLE IF NOT EXISTS likes
                 (post_id INTEGER NOT NULL,
                  session_id TEXT NOT NULL,
                  PRIMARY KEY (post_id, session_id))''')
    
    # Bảng theo dõi hoạt động hàng ngày (chống spam post/comment)
    c.execute('''CREATE TABLE IF NOT EXISTS daily_activity
                 (session_id TEXT NOT NULL,
                  activity_type TEXT NOT NULL,
                  activity_date TEXT NOT NULL,
                  count INTEGER DEFAULT 0,
                  PRIMARY KEY (session_id, activity_type, activity_date))''')
    
    conn.commit()
    return conn

# ============= CONTENT FILTER =============
def check_content_safety(text):
    """Kiểm tra nội dung có an toàn không"""
    # Danh sách từ khóa cấm (mở rộng theo nhu cầu)
    banned_words = [
        'đồ ngu', 'ngu si', 'óc chó', 'đm', 'dcm', 'vl', 'đcm', 
        'chết đi', 'tự tử', 'giết', 'đánh nhau', 'bạo lực',
        'địt', 'lồn', 'cặc', 'buồi', 'fuck', 'shit'
    ]
    
    text_lower = text.lower()
    
    # Kiểm tra từ ngữ tục tĩu
    for word in banned_words:
        if word in text_lower:
            return False, "Nội dung chứa từ ngữ không phù hợp. Hãy sử dụng ngôn từ lịch sự hơn nhé! 😊"
    
    # Kiểm tra spam ký tự vô nghĩa
    if re.match(r'^[.\s?!]+$', text):
        return False, "Vui lòng nhập nội dung có ý nghĩa! 📝"
    
    # Kiểm tra độ dài tối thiểu (loại bỏ khoảng trắng)
    clean_text = text.strip().replace(' ', '')
    if len(clean_text) < 5:
        return False, "Nội dung quá ngắn. Vui lòng viết ít nhất 5 ký tự! ✍️"
    
    return True, "OK"

# ============= SESSION & TRACKING =============
def get_session_id():
    """Tạo session_id duy nhất cho người dùng ẩn danh"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = hashlib.md5(
            str(datetime.now().timestamp()).encode()
        ).hexdigest()
    return st.session_state.session_id

def get_daily_activity_count(conn, session_id, activity_type):
    """Lấy số lượng hoạt động trong ngày"""
    today = datetime.now().strftime('%Y-%m-%d')
    c = conn.cursor()
    c.execute('''SELECT count FROM daily_activity 
                 WHERE session_id=? AND activity_type=? AND activity_date=?''',
              (session_id, activity_type, today))
    result = c.fetchone()
    return result[0] if result else 0

def increment_daily_activity(conn, session_id, activity_type):
    """Tăng số lượng hoạt động trong ngày"""
    today = datetime.now().strftime('%Y-%m-%d')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO daily_activity 
                 (session_id, activity_type, activity_date, count)
                 VALUES (?, ?, ?, COALESCE(
                     (SELECT count + 1 FROM daily_activity 
                      WHERE session_id=? AND activity_type=? AND activity_date=?), 1))''',
              (session_id, activity_type, today, session_id, activity_type, today))
    conn.commit()

# ============= DATABASE OPERATIONS =============
def create_post(conn, title, content, username):
    """Tạo bài viết mới và cộng điểm"""
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''INSERT INTO posts (title, content, username, created_at)
                 VALUES (?, ?, ?, ?)''', (title, content, username, now))
    conn.commit()
    
    # Cộng điểm cho người đăng bài
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 0
    st.session_state.user_points += 15
    
    return c.lastrowid

def get_all_posts(conn):
    """Lấy tất cả bài viết"""
    c = conn.cursor()
    c.execute('''SELECT post_id, title, username, views, likes, created_at,
                 (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.post_id) as comment_count
                 FROM posts ORDER BY created_at DESC''')
    return c.fetchall()

def get_post_detail(conn, post_id):
    """Lấy chi tiết bài viết"""
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE post_id=?', (post_id,))
    return c.fetchone()

def increment_view(conn, post_id):
    """Tăng lượt xem"""
    c = conn.cursor()
    c.execute('UPDATE posts SET views = views + 1 WHERE post_id=?', (post_id,))
    conn.commit()

def toggle_like(conn, post_id, session_id):
    """Thích/bỏ thích bài viết"""
    c = conn.cursor()
    
    # Kiểm tra đã like chưa
    c.execute('SELECT * FROM likes WHERE post_id=? AND session_id=?', (post_id, session_id))
    already_liked = c.fetchone()
    
    if already_liked:
        # Bỏ like
        c.execute('DELETE FROM likes WHERE post_id=? AND session_id=?', (post_id, session_id))
        c.execute('UPDATE posts SET likes = likes - 1 WHERE post_id=?', (post_id,))
        conn.commit()
        return False
    else:
        # Thêm like
        c.execute('INSERT INTO likes (post_id, session_id) VALUES (?, ?)', (post_id, session_id))
        c.execute('UPDATE posts SET likes = likes + 1 WHERE post_id=?', (post_id,))
        conn.commit()
        return True

def check_liked(conn, post_id, session_id):
    """Kiểm tra đã like chưa"""
    c = conn.cursor()
    c.execute('SELECT * FROM likes WHERE post_id=? AND session_id=?', (post_id, session_id))
    return c.fetchone() is not None

def add_comment(conn, post_id, username, content):
    """Thêm bình luận và cộng điểm"""
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''INSERT INTO comments (post_id, username, content, created_at)
                 VALUES (?, ?, ?, ?)''', (post_id, username, content, now))
    conn.commit()
    
    # Cộng điểm cho người bình luận
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 0
    st.session_state.user_points += 5

def get_comments(conn, post_id):
    """Lấy tất cả bình luận của bài viết"""
    c = conn.cursor()
    c.execute('SELECT * FROM comments WHERE post_id=? ORDER BY created_at DESC', (post_id,))
    return c.fetchall()

# ============= UI COMPONENTS =============
def display_header():
    """Hiển thị header"""
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.markdown("# 💬 Diễn Đàn Học Đường")
        st.markdown("*Không gian chia sẻ an toàn cho học sinh*")
    
    # Hiển thị điểm
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 0
    st.sidebar.markdown(f"### 🏆 Điểm của bạn: **{st.session_state.user_points}**")
    st.sidebar.markdown("---")
    st.sidebar.markdown("📝 **Đăng bài:** +15 điểm")
    st.sidebar.markdown("💬 **Bình luận:** +5 điểm")

def generate_avatar(username):
    """Tạo avatar từ tên người dùng"""
    return username[0].upper()

def display_post_card(post):
    """Hiển thị card bài viết"""
    post_id, title, username, views, likes, created_at, comment_count = post
    
    col1, col2 = st.columns([1, 12])
    
    with col1:
        st.markdown(f"""
        <div class="avatar">{generate_avatar(username)}</div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="post-card">
            <h3 style="margin:0; color:#1976D2;">{title}</h3>
            <p style="margin:5px 0; color:#666;">👤 {username} • 🕒 {created_at}</p>
            <div>
                <span class="stat-badge">👁️ {views} lượt xem</span>
                <span class="stat-badge">❤️ {likes} thích</span>
                <span class="stat-badge">💬 {comment_count} bình luận</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Xem chi tiết", key=f"view_{post_id}"):
            st.session_state.current_page = 'detail'
            st.session_state.selected_post_id = post_id
            st.rerun()

# ============= PAGES =============
def forum_list_page(conn):
    """Trang danh sách bài viết"""
    display_header()
    
    # Nút tạo bài viết mới
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➕ Tạo Bài Viết Mới", use_container_width=True):
            st.session_state.show_create_form = True
    
    # Form tạo bài viết
    if st.session_state.get('show_create_form', False):
        st.markdown("---")
        st.markdown("### ✍️ Tạo Bài Viết Mới")
        
        # Kiểm tra giới hạn hàng ngày
        session_id = get_session_id()
        post_count_today = get_daily_activity_count(conn, session_id, 'post')
        
        if post_count_today >= 3:
            st.error("⚠️ Bạn đã đạt giới hạn 3 bài viết trong ngày. Hãy quay lại vào ngày mai nhé!")
        else:
            with st.form("create_post_form"):
                username = st.text_input("Tên hiển thị (ẩn danh)", placeholder="VD: Học sinh năm 10")
                title = st.text_input("Tiêu đề", placeholder="Nhập tiêu đề bài viết...")
                content = st.text_area("Nội dung", placeholder="Chia sẻ suy nghĩ của bạn...", height=200)
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("📤 Đăng Bài")
                with col2:
                    cancel = st.form_submit_button("❌ Hủy")
                
                if cancel:
                    st.session_state.show_create_form = False
                    st.rerun()
                
                if submit:
                    if not username or not title or not content:
                        st.error("⚠️ Vui lòng điền đầy đủ thông tin!")
                    else:
                        # Kiểm tra nội dung
                        safe, msg = check_content_safety(title + " " + content)
                        if not safe:
                            st.error(f"⚠️ {msg}")
                        else:
                            create_post(conn, title, content, username)
                            increment_daily_activity(conn, session_id, 'post')
                            st.success(f"✅ Đăng bài thành công! +15 điểm 🎉")
                            st.session_state.show_create_form = False
                            st.rerun()
    
    st.markdown("---")
    
    # Danh sách bài viết
    posts = get_all_posts(conn)
    
    if not posts:
        st.info("📭 Chưa có bài viết nào. Hãy là người đầu tiên chia sẻ!")
    else:
        st.markdown(f"### 📚 Tất cả bài viết ({len(posts)})")
        for post in posts:
            display_post_card(post)

def post_detail_page(conn):
    """Trang chi tiết bài viết"""
    post_id = st.session_state.selected_post_id
    session_id = get_session_id()
    
    # Nút quay lại
    if st.button("← Quay lại diễn đàn"):
        st.session_state.current_page = 'list'
        st.rerun()
    
    # Tăng lượt xem (chỉ tăng 1 lần khi vào trang)
    if f'viewed_{post_id}' not in st.session_state:
        increment_view(conn, post_id)
        st.session_state[f'viewed_{post_id}'] = True
    
    # Lấy thông tin bài viết
    post = get_post_detail(conn, post_id)
    if not post:
        st.error("❌ Không tìm thấy bài viết!")
        return
    
    _, title, content, username, views, likes, created_at = post
    
    # Hiển thị bài viết
    st.markdown(f"# {title}")
    st.markdown(f"*👤 {username} • 🕒 {created_at}*")
    st.markdown("---")
    st.markdown(content)
    st.markdown("---")
    
    # Nút thích và thống kê
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        liked = check_liked(conn, post_id, session_id)
        like_emoji = "❤️" if liked else "🤍"
        if st.button(f"{like_emoji} Thích", use_container_width=True):
            toggle_like(conn, post_id, session_id)
            st.rerun()
    
    with col2:
        st.metric("👁️ Lượt xem", views)
    
    with col3:
        st.metric("❤️ Lượt thích", likes)
    
    with col4:
        comments = get_comments(conn, post_id)
        st.metric("💬 Bình luận", len(comments))
    
    st.markdown("---")
    
    # Form bình luận
    st.markdown("### 💬 Bình luận")
    
    # Kiểm tra giới hạn bình luận hàng ngày
    comment_count_today = get_daily_activity_count(conn, session_id, 'comment')
    
    if comment_count_today >= 10:
        st.warning("⚠️ Bạn đã đạt giới hạn 10 bình luận trong ngày. Hãy quay lại vào ngày mai!")
    else:
        with st.form("comment_form"):
            comment_username = st.text_input("Tên của bạn", placeholder="VD: Bạn cùng lớp")
            comment_content = st.text_area("Nội dung bình luận", placeholder="Chia sẻ ý kiến của bạn...", height=100)
            submit = st.form_submit_button("📤 Gửi bình luận")
            
            if submit:
                if not comment_username or not comment_content:
                    st.error("⚠️ Vui lòng điền đầy đủ thông tin!")
                else:
                    # Kiểm tra nội dung
                    safe, msg = check_content_safety(comment_content)
                    if not safe:
                        st.error(f"⚠️ {msg}")
                    else:
                        add_comment(conn, post_id, comment_username, comment_content)
                        increment_daily_activity(conn, session_id, 'comment')
                        st.success("✅ Bình luận thành công! +5 điểm 🎉")
                        st.rerun()
    
    # Hiển thị danh sách bình luận
    comments = get_comments(conn, post_id)
    
    if not comments:
        st.info("💭 Chưa có bình luận nào. Hãy là người đầu tiên bình luận!")
    else:
        st.markdown(f"#### 📝 Tất cả bình luận ({len(comments)})")
        for comment in comments:
            _, _, c_username, c_content, c_created_at = comment
            st.markdown(f"""
            <div class="comment-box">
                <strong style="color: #1976D2;">👤 {c_username}</strong> • <small style="color: #666;">🕒 {c_created_at}</small>
                <p style="margin-top:8px; color: #333;">{c_content}</p>
            </div>
            """, unsafe_allow_html=True)

# ============= MAIN APP =============
def main():
    """Hàm chính"""
    # Khởi tạo database
    conn = init_db()
    
    # Khởi tạo session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'list'
    if 'selected_post_id' not in st.session_state:
        st.session_state.selected_post_id = None
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 0
    
    # Routing
    if st.session_state.current_page == 'list':
        forum_list_page(conn)
    elif st.session_state.current_page == 'detail':
        post_detail_page(conn)

if __name__ == "__main__":
    main()
