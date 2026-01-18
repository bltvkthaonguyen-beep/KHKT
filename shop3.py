import streamlit as st

# ==========================================
# 1. KHỞI TẠO DỮ LIỆU (MOCK DATA)
# ==========================================

def init_session_state():
    """Khởi tạo trạng thái game nếu chưa có"""
    if 'user_points' not in st.session_state:
        st.session_state.user_points = 5000  # Điểm khởi tạo để test
    
    if 'owned_items' not in st.session_state:
        st.session_state.owned_items = []
        
    if 'current_category' not in st.session_state:
        st.session_state.current_category = "Mèo"

    # Giả lập dữ liệu nhiệm vụ (Sau này sẽ gọi từ Task Module)
    if 'tasks' not in st.session_state:
        st.session_state.tasks = [
            {"id": "task_1", "desc": "Trả lời câu hỏi của chatbox", "reward": 50},
            {"id": "task_2", "desc": "Hoàn thành bài học về mèo", "reward": 100},
            {"id": "task_3", "desc": "Chăm sóc mèo 3 lần", "reward": 30}
        ]

# Danh sách vật phẩm dựa trên ảnh cung cấp
SHOP_DATA = {
    "Mèo": [
        {"id": "cat_01", "name": "Mèo Ragdoll", "price": 100000, "img": "assets/mèo premium.png"},
        {"id": "cat_02", "name": "Mèo Anh lông dài", "price": 500000, "img": "assets/mèo.png"},
    ],
    "Điệm mèo": [
        {"id": "bed_01", "name": "Đệm xanh tròn", "price": 3500, "img": "assets/đệm 1.png"},
        {"id": "bed_02", "name": "Đệm hổ", "price": 3800, "img": "assets/đệm 2.png"},
        {"id": "bed_03", "name": "Đệm bàn chân", "price": 4100, "img": "assets/đệm 3.png"},
        {"id": "bed_04", "name": "Nhà xanh", "price": 4400, "img": "assets/đệm 4.png"},
        {"id": "bed_05", "name": "Nhà tai thỏ", "price": 4600, "img": "assets/đệm 5.png"},
        {"id": "bed_06", "name": "Nhà mèo trắng", "price": 4800, "img": "assets/đệm 6.png"},
        {"id": "bed_07", "name": "Đệm cá mập", "price": 5000, "img": "assets/đệm 7.png"},
    ],
    "Cây mèo": [
        {"id": "tree_01", "name": "Cây gỗ cơ bản", "price": 1000, "img": "assets/cây 1.png"},
        {"id": "tree_02", "name": "Cây hoa sắc màu", "price": 1100, "img": "assets/cây 2.png"},
        {"id": "tree_03", "name": "Cây tháp xám", "price": 1200, "img": "assets/cây 3.png"},
        {"id": "tree_04", "name": "Cây chung cư", "price": 1300, "img": "assets/cây 4.png"},
        {"id": "tree_05", "name": "Cây ngôi sao", "price": 1400, "img": "assets/cây 5.png"},
        {"id": "tree_06", "name": "Cây bậc thang", "price": 1500, "img": "assets/cây 6.png"},
    ],
    "Thức ăn & Cát": [
        {"id": "food_01", "name": "Thanh dinh dưỡng", "price": 100, "img": "assets/thanh dinh dưỡng.png"},
        {"id": "food_02", "name": "Pate cá hồi", "price": 250, "img": "assets/hộp thức ăn.png"},
        {"id": "food_03", "name": "Hạt cao cấp 2kg", "price": 20000, "img": "assets/túi thức ăn.png"},
        {"id": "litter_01", "name": "Cát vệ sinh 10kg", "price": 15000, "img": "assets/cát mèo.png"},
    ],
    "Vật dụng cho mèo": [
        {"id": "tool_01", "name": "Nhà vệ sinh kín", "price": 1200, "img": "assets/nhà vệ sinh.png"},
        {"id": "tool_02", "name": "Balo phi hành gia", "price": 400, "img": "assets/túi đựng.png"},
        {"id": "tool_03", "name": "Máy lọc nước", "price": 900, "img": "assets/khay thức ăn.png"},
        {"id": "tool_04", "name": "Cuộn len", "price": 50, "img": "assets/len.png"},
    ]
}

# ==========================================
# 2. LOGIC XỬ LÝ
# ==========================================

def buy_item(item):
    """Xử lý logic mua hàng"""
    if st.session_state.user_points >= item['price']:
        st.session_state.user_points -= item['price']
        st.session_state.owned_items.append(item['id'])
        st.toast(f"Đã mua {item['name']} thành công!", icon="✅")
    else:
        st.error(f"Không đủ điểm để mua {item['name']}!")

# ==========================================
# 3. GIAO DIỆN (UI)
# ==========================================

def render_shop():
    init_session_state()

    # Thiết lập Style CSS để mô phỏng giao diện trong ảnh
    st.markdown("""
        <style>
        .shop-container { background-color: #FDF5E6; padding: 20px; border-radius: 15px; border: 3px solid #8B4513; }
        .category-btn { width: 100%; text-align: left; background-color: #D2B48C; border-radius: 5px; margin-bottom: 5px; }
        .item-card { text-align: center; border: 1px solid #ddd; padding: 10px; border-radius: 10px; background: white; }
        .price-tag { font-weight: bold; color: #4B0082; }
        .task-card { background-color: #FFE4B5; border: 2px solid #DEB887; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)

    # Layout chính: 3 cột (Danh mục | Sản phẩm | Nhiệm vụ)
    col_nav, col_main, col_task = st.columns([1.5, 5, 2])

    # --- (A) THANH BÊN TRÁI: DANH MỤC ---
    with col_nav:
        st.markdown("### 🛒 SHOP")
        for cat in SHOP_DATA.keys():
            if st.button(cat, use_container_width=True, key=f"btn_{cat}"):
                st.session_state.current_category = cat

    # --- (B) KHU VỰC TRUNG TÂM: SẢN PHẨM ---
    with col_main:
        # Thanh trắng phía trên hiển thị điểm
        st.markdown(f"""
            <div style="background-color: white; padding: 10px; border-radius: 20px; text-align: center; border: 2px solid #8B4513; margin-bottom: 20px;">
                <h3 style="margin:0; color: #8B4513;">🐾 Điểm hiện có: {st.session_state.user_points:,}</h3>
            </div>
        """, unsafe_allow_html=True)

        current_cat = st.session_state.current_category
        items = SHOP_DATA[current_cat]
        
        # Hiển thị dạng lưới (Grid 3 cột)
        cols = st.columns(3)
        for idx, item in enumerate(items):
            with cols[idx % 3]:
                st.markdown(f"<div class='item-card'>", unsafe_allow_html=True)
                try:
                    st.image(item['img'], use_column_width=True)
                except:
                    # Placeholder nếu không tìm thấy ảnh
                    st.warning("Ảnh lỗi")
                
                # Nút bấm mua hàng (Hiển thị giá)
                if st.button(f"{item['price']:,}", key=item['id'], use_container_width=True):
                    buy_item(item)
                st.markdown("</div>", unsafe_allow_html=True)

    # --- (C) THANH BÊN PHẢI: NHIỆM VỤ ---
    with col_task:
        st.markdown("""
            <div style="background-color: #FF8C00; color: white; padding: 5px 15px; border-radius: 5px; text-align: center; font-weight: bold;">
                Nhiệm vụ
            </div>
        """, unsafe_allow_html=True)
        
        for task in st.session_state.tasks:
            st.markdown(f"""
                <div class="task-card">
                    <small>ID: {task['id']}</small><br>
                    <b>{task['desc']}</b><br>
                    <span style="color: #D2691E;">★ +{task['reward']}</span>
                </div>
            """, unsafe_allow_html=True)

# Chạy module
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    render_shop()
