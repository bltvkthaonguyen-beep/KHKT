"""
MODULE SHOP - GAME GIÁO DỤC CHĂM SÓC MÈO
Dự án Khoa học Kỹ thuật cấp Quốc gia

Chức năng:
- Hiển thị cửa hàng vật phẩm cho mèo
- Xử lý mua bán vật phẩm
- Quản lý điểm người chơi
- Hiển thị nhiệm vụ (read-only)
"""

import streamlit as st
from typing import Dict, List
import os

# ============================================================
# PHẦN 1: CẤU HÌNH & DỮ LIỆU
# ============================================================

# Cấu hình trang
st.set_page_config(
    page_title="Shop - Game Chăm Sóc Mèo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS tùy chỉnh để tạo giao diện giống thiết kế
st.markdown("""
<style>
    /* Ẩn header và footer mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Style cho toàn bộ app */
    .stApp {
        background-color: #f5e6d3;
    }
    
    /* Container chính của shop */
    .shop-container {
        background-color: #d4a574;
        border: 8px solid #8b5a3c;
        border-radius: 15px;
        padding: 20px;
        margin: 20px;
    }
    
    /* Style cho nút danh mục */
    .category-button {
        background-color: #d4a574;
        border: 3px solid #8b5a3c;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        text-align: center;
        font-family: 'Brush Script MT', cursive;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .category-button:hover {
        background-color: #c49563;
        transform: translateX(5px);
    }
    
    .category-button.active {
        background-color: #b8844f;
        border: 3px solid #6b4423;
    }
    
    /* Style cho vật phẩm */
    .item-card {
        background-color: white;
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        margin: 10px;
        transition: all 0.3s;
    }
    
    .item-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-5px);
    }
    
    .item-price {
        font-size: 24px;
        font-weight: bold;
        margin-top: 10px;
        cursor: pointer;
        padding: 8px;
        border-radius: 5px;
        transition: all 0.3s;
    }
    
    .item-price:hover {
        background-color: #f0f0f0;
    }
    
    .item-price.affordable {
        color: #4CAF50;
    }
    
    .item-price.expensive {
        color: #ff6b6b;
    }
    
    /* Style cho khung nhiệm vụ */
    .task-card {
        background-color: #fef5d4;
        border: 3px solid #ff69b4;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        font-size: 16px;
    }
    
    /* Style cho điểm số */
    .points-display {
        background-color: white;
        border: 2px solid #333;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    /* Header shop */
    .shop-header {
        background-color: #fef5d4;
        border: 3px solid #8b5a3c;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
        position: relative;
    }
    
    .shop-title {
        color: #8b4513;
        font-size: 36px;
        font-weight: bold;
        font-family: 'Comic Sans MS', cursive;
        text-decoration: underline;
        text-decoration-color: #8b4513;
    }
    
    /* Nút đóng */
    .close-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #d4a574;
        border: 3px solid #8b5a3c;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 30px;
        color: #8b5a3c;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Thanh điểm ở trên cùng */
    .top-points-bar {
        background-color: #e8b87e;
        border: 3px solid #8b5a3c;
        border-radius: 10px;
        padding: 10px 20px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PHẦN 2: DỮ LIỆU VẬT PHẨM (STATIC DATA)
# ============================================================

# Dữ liệu vật phẩm - dựa trên các ảnh thiết kế
SHOP_ITEMS = [
    # DANH MỤC: MÈO
    {"id": "cat_01", "name": "Mèo tam thể", "category": "Mèo", "price": 100000, "image": "assets/mèo.png"},
    {"id": "cat_02", "name": "Mèo Ba Tư", "category": "Mèo", "price": 500000, "image": "assets/mèo premium.png"},
    
    # DANH MỤC: VẬT DỤNG KHÁCKHÁC (Vật dụng nhỏ)
    {"id": "accessory_01", "name": "Nhà vệ sinh mèo", "category": "Điểm mèo", "price": 1200, "image": "assets/nhà vệ sinh.png"},
    {"id": "accessory_02", "name": "Ba lô vận chuyển", "category": "Điểm mèo", "price": 400, "image": "assets/túi đựng.png"},
    {"id": "accessory_03", "name": "Bát ăn đôi", "category": "Điểm mèo", "price": 900, "image": "assets/khay thức ăn.png"},
    {"id": "accessory_04", "name": "Bóng len chơi", "category": "Điểm mèo", "price": 50, "image": "assets/len.png"},
    
    # DANH MỤC: CÂY MÈO
    {"id": "tree_01", "name": "Cây mèo cỡ nhỏ", "category": "Cây mèo", "price": 1000, "image": "assets/cây 1.png"},
    {"id": "tree_02", "name": "Cây mèo cỡ trung", "category": "Cây mèo", "price": 1100, "image": "assets/cây 2.png"},
    {"id": "tree_03", "name": "Cây mèo cỡ lớn", "category": "Cây mèo", "price": 1200, "image": "assets/cây 3.png"},
    {"id": "tree_04", "name": "Cây mèo cao cấp", "category": "Cây mèo", "price": 1300, "image": "assets/cây 4.png"},
    {"id": "tree_05", "name": "Cây mèo mini", "category": "Cây mèo", "price": 1400, "image": "assets/cây 5.png"},
    {"id": "tree_06", "name": "Cây mèo deluxe", "category": "Cây mèo", "price": 1500, "image": "assets/cây 6.png"},
    
    # DANH MỤC: THỨC ĂN & CÁT
    {"id": "food_01", "name": "Thức ăn que", "category": "Thức ăn & Cát", "price": 100, "image": "assets/thanh dinh dưỡng.png"},
    {"id": "food_02", "name": "Pate cao cấp", "category": "Thức ăn & Cát", "price": 250, "image": "assets/hộp thức ăn.png"},
    {"id": "food_03", "name": "Hạt khô dinh dưỡng", "category": "Thức ăn & Cát", "price": 20000, "image": "assets/túi thức ăn.png"},
    {"id": "food_04", "name": "Cát vệ sinh", "category": "Thức ăn & Cát", "price": 15000, "image": "assets/cát mèo.png"},
    
    # DANH MỤC: ĐỆM MÈO
    {"id": "bed_01", "name": "Đệm tròn xanh", "category": "Vật dụng cho mèo", "price": 3500, "image": "assets/đệm 1.png"},
    {"id": "bed_02", "name": "Đệm mèo vằn", "category": "Vật dụng cho mèo", "price": 3800, "image": "assets/đệm 2.png"},
    {"id": "bed_03", "name": "Đệm chân mèo", "category": "Vật dụng cho mèo", "price": 4100, "image": "assets/đệm 3.png"},
    {"id": "bed_04", "name": "Túi ngủ xanh", "category": "Vật dụng cho mèo", "price": 4400, "image": "assets/đệm 4.png"},
    {"id": "bed_05", "name": "Giường mèo hồng", "category": "Vật dụng cho mèo", "price": 4600, "image": "assets/đệm 5.png"},
    {"id": "bed_06", "name": "Giường động vật", "category": "Vật dụng cho mèo", "price": 4800, "image": "assets/đệm 6.png"},
    {"id": "bed_07", "name": "Đệm cá ngủ", "category": "Vật dụng cho mèo", "price": 5000, "image": "assets/đệm 7.png"},
]

# Danh sách danh mục
CATEGORIES = [
    "Mèo",
    "Điểm mèo", 
    "Cây mèo",
    "Thức ăn & Cát",
    "Vật dụng cho mèo"
]

# ============================================================
# PHẦN 3: DỮ LIỆU NHIỆM VỤ GIẢ LẬP (CHỈ ĐỂ HIỂN THỊ)
# ============================================================

# Dữ liệu nhiệm vụ mẫu - sẽ được thay thế bởi module Task sau này
MOCK_TASKS = [
    {
        "id": "chat_1",
        "description": "Trả lời câu hỏi của chatbox",
        "reward": 50,
        "status": "pending"
    },
    {
        "id": "quiz_1", 
        "description": "Hoàn thành bài kiểm tra",
        "reward": 200,
        "status": "pending"
    },
    {
        "id": "daily_1",
        "description": "Đăng nhập hàng ngày",
        "reward": 100,
        "status": "completed"
    }
]

# ============================================================
# PHẦN 4: QUẢN LÝ TRẠNG THÁI (SESSION STATE)
# ============================================================

def initialize_session_state():
    """
    Khởi tạo các biến session state cần thiết
    Chạy một lần duy nhất khi app khởi động
    """
    # Điểm người chơi - khởi tạo 5000 điểm để test
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 5000
    
    # Danh sách vật phẩm đã mua
    if 'owned_items' not in st.session_state:
        st.session_state.owned_items = []
    
    # Danh mục đang được chọn
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = "Mèo"
    
    # Danh sách nhiệm vụ (sau này sẽ được module Task cung cấp)
    if 'tasks' not in st.session_state:
        st.session_state.tasks = MOCK_TASKS

# ============================================================
# PHẦN 5: HÀM HỖ TRỢ - QUẢN LÝ ĐIỂM VÀ VẬT PHẨM
# ============================================================

def get_user_points() -> int:
    """Lấy số điểm hiện tại của người chơi"""
    return st.session_state.user_points

def update_user_points(new_value: int):
    """
    Cập nhật điểm người chơi
    Args:
        new_value: Giá trị điểm mới
    """
    st.session_state.user_points = new_value

def purchase_item(item: Dict) -> bool:
    """
    Xử lý mua vật phẩm
    Args:
        item: Dictionary chứa thông tin vật phẩm
    Returns:
        True nếu mua thành công, False nếu không đủ điểm
    """
    current_points = get_user_points()
    
    # Kiểm tra đủ điểm
    if current_points >= item['price']:
        # Trừ điểm
        new_points = current_points - item['price']
        update_user_points(new_points)
        
        # Thêm vào danh sách đã mua
        st.session_state.owned_items.append(item['id'])
        
        return True
    else:
        return False

def is_item_owned(item_id: str) -> bool:
    """Kiểm tra vật phẩm đã được mua chưa"""
    return item_id in st.session_state.owned_items

def get_items_by_category(category: str) -> List[Dict]:
    """
    Lấy danh sách vật phẩm theo danh mục
    Args:
        category: Tên danh mục
    Returns:
        Danh sách vật phẩm trong danh mục đó
    """
    return [item for item in SHOP_ITEMS if item['category'] == category]

# ============================================================
# PHẦN 6: GIAO DIỆN - CÁC COMPONENT
# ============================================================

def render_category_sidebar():
    """
    Hiển thị thanh danh mục bên trái
    Xử lý sự kiện khi người dùng chọn danh mục
    """
    st.markdown("<div style='background-color: #a67c52; padding: 20px; border-radius: 10px; border: 5px solid #6b4423;'>", unsafe_allow_html=True)
    
    # Header "SHOP"
    st.markdown("<div class='shop-header'><div class='shop-title'>SHOP</div></div>", unsafe_allow_html=True)
    
    # Các nút danh mục
    for category in CATEGORIES:
        # Xác định class active nếu đang được chọn
        active_class = "active" if st.session_state.selected_category == category else ""
        
        # Tạo nút với callback
        if st.button(
            category,
            key=f"cat_{category}",
            use_container_width=True,
            type="secondary" if active_class == "" else "primary"
        ):
            st.session_state.selected_category = category
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_item_grid():
    """
    Hiển thị lưới vật phẩm ở khu vực trung tâm
    Dựa trên danh mục đang được chọn
    """
    # Lấy danh sách vật phẩm theo danh mục
    items = get_items_by_category(st.session_state.selected_category)
    current_points = get_user_points()
    
    # Hiển thị thanh điểm phía trên
    st.markdown(f"""
    <div class='top-points-bar'>
        <span style='font-size: 18px; color: #6b4423;'>💰 Điểm hiện tại: </span>
        <span style='font-size: 24px; font-weight: bold; color: #2c5f2d;'>{current_points}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị vật phẩm dạng lưới (4 cột)
    cols_per_row = 4
    
    for i in range(0, len(items), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, item in enumerate(items[i:i+cols_per_row]):
            with cols[j]:
                render_item_card(item, current_points)

def render_item_card(item: Dict, current_points: int):
    """
    Hiển thị một thẻ vật phẩm
    Args:
        item: Dictionary chứa thông tin vật phẩm
        current_points: Số điểm hiện tại của người chơi
    """
    # Container cho thẻ vật phẩm
    st.markdown("<div class='item-card'>", unsafe_allow_html=True)
    
    # Hiển thị hình ảnh hoặc placeholder
    if os.path.exists(item['image']):
        st.image(item['image'], use_container_width=True)
    else:
        # Placeholder nếu không có ảnh
        st.markdown("""
        <div style='
            width: 100%;
            height: 150px;
            background-color: #f0f0f0;
            border: 2px dashed #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
        '>
            <span style='color: #999;'>Chưa có ảnh</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Kiểm tra đủ điểm hay không
    can_afford = current_points >= item['price']
    price_class = "affordable" if can_afford else "expensive"
    
    # Kiểm tra đã mua chưa
    owned = is_item_owned(item['id'])
    
    if owned:
        # Nếu đã mua - hiển thị dấu check
        st.markdown(f"""
        <div style='
            font-size: 20px;
            font-weight: bold;
            color: #4CAF50;
            margin-top: 10px;
        '>✓ Đã sở hữu</div>
        """, unsafe_allow_html=True)
    else:
        # Nếu chưa mua - hiển thị giá và cho phép click để mua
        if st.button(
            f"💎 {item['price']}", 
            key=f"buy_{item['id']}",
            disabled=not can_afford,
            use_container_width=True
        ):
            # Xử lý mua hàng
            success = purchase_item(item)
            if success:
                st.success(f"✅ Đã mua {item['name']}!")
                st.rerun()
            else:
                st.error("❌ Không đủ điểm!")
        
        # Hiển thị cảnh báo nếu không đủ điểm
        if not can_afford:
            st.markdown("<div style='color: #ff6b6b; font-size: 12px;'>Không đủ điểm</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_task_sidebar():
    """
    Hiển thị thanh nhiệm vụ bên phải
    CHỈ HIỂN THỊ - không xử lý logic hoàn thành nhiệm vụ
    """
    st.markdown("<div style='background-color: #d4a574; padding: 15px; border-radius: 10px; border: 4px solid #8b5a3c;'>", unsafe_allow_html=True)
    
    # Hiển thị điểm ở đầu
    current_points = get_user_points()
    st.markdown(f"""
    <div class='points-display'>
        💰 Điểm: {current_points}
    </div>
    """, unsafe_allow_html=True)
    
    # Header nhiệm vụ
    st.markdown("""
    <div style='
        background-color: #f4a460;
        border: 3px solid #8b5a3c;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    '>Nhiệm vụ</div>
    """, unsafe_allow_html=True)
    
    # Hiển thị danh sách nhiệm vụ
    tasks = st.session_state.tasks
    
    if not tasks:
        st.info("Chưa có nhiệm vụ nào")
    else:
        for task in tasks:
            status_icon = "✓" if task['status'] == 'completed' else "⭐"
            status_color = "#4CAF50" if task['status'] == 'completed' else "#333"
            
            st.markdown(f"""
            <div class='task-card' style='border-color: {"#4CAF50" if task["status"] == "completed" else "#ff69b4"};'>
                <div style='color: {status_color}; font-weight: bold;'>
                    {status_icon} {task['description']}
                </div>
                <div style='color: #ff6b4a; font-weight: bold; margin-top: 5px;'>
                    +{task['reward']} điểm
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Ghi chú cho developer
    st.markdown("""
    <div style='
        margin-top: 15px;
        padding: 10px;
        background-color: #fff3cd;
        border: 2px dashed #856404;
        border-radius: 5px;
        font-size: 12px;
    '>
        <b>📝 Ghi chú tích hợp:</b><br/>
        Module Shop CHỈ hiển thị nhiệm vụ.<br/>
        Logic hoàn thành nhiệm vụ và cộng điểm<br/>
        sẽ do module Task xử lý.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PHẦN 7: MAIN - ĐIỂM VÀO CỦA ỨNG DỤNG
# ============================================================

def main():
    """
    Hàm main - điểm khởi đầu của ứng dụng
    Tổ chức layout và gọi các component
    """
    # Khởi tạo session state
    initialize_session_state()
    
    # Tiêu đề ứng dụng
    st.title("🐱 Cửa Hàng Chăm Sóc Mèo")
    
    # Layout chính: 3 cột
    # Cột trái (20%): Danh mục
    # Cột giữa (55%): Hiển thị vật phẩm  
    # Cột phải (25%): Nhiệm vụ
    
    col_left, col_center, col_right = st.columns([2, 5.5, 2.5])
    
    with col_left:
        render_category_sidebar()
    
    with col_center:
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; min-height: 600px;'>", unsafe_allow_html=True)
        render_item_grid()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_right:
        render_task_sidebar()
    
    # ============================================================
    # VỊ TRÍ TÍCH HỢP MODULE KHÁC (CHÚ THÍCH QUAN TRỌNG)
    # ============================================================
    
    st.markdown("---")
    st.markdown("""
    ### 📌 Hướng dẫn tích hợp với các module khác:
    
    **1. Module Task (Nhiệm vụ):**
    - Thay thế biến `MOCK_TASKS` bằng dữ liệu thực từ module Task
    - Module Task sẽ cung cấp hàm: `get_active_tasks()` → trả về list nhiệm vụ
    - Module Task sẽ xử lý hoàn thành nhiệm vụ và cộng điểm vào `st.session_state.user_points`
    
    **2. Module Chatbox (Trò chuyện AI):**
    - Khi người chơi trả lời đúng câu hỏi của chatbot
    - Module Chatbox gọi hàm: `update_user_points(current_points + reward)`
    - Shop sẽ tự động cập nhật hiển thị điểm mới
    
    **3. Luồng tích hợp:**
    ```
    Chatbox/Task → Cộng điểm → st.session_state.user_points
                                          ↓
                                    Shop đọc và hiển thị
    ```
    
    **4. API cần thiết cho các module khác:**
    - `get_user_points()` - Lấy điểm hiện tại
    - `update_user_points(new_value)` - Cập nhật điểm mới
    - `st.session_state.owned_items` - Danh sách vật phẩm đã mua
    """)

# ============================================================
# PHẦN 8: KHỞI CHẠY ỨNG DỤNG
# ============================================================

if __name__ == "__main__":
    main()
