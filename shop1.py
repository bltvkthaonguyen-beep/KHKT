import streamlit as st
from typing import List, Dict
import os

# ============================================================================
# PHẦN 1: CẤU HÌNH VÀ DỮ LIỆU TĨNH
# ============================================================================

# Cấu hình trang
st.set_page_config(page_title="Shop Mèo", layout="wide")

# CSS tùy chỉnh cho giao diện - Phong cách vẽ tay như trong ảnh gốc
st.markdown("""
<style>
    /* Ẩn header và footer mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background tổng thể */
    .stApp {
        background-color: #F5F5DC;
    }
    
    /* Ẩn padding mặc định */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    
    /* Style cho nút danh mục - Giống ảnh gốc */
    .stButton > button {
        width: 100%;
        padding: 15px;
        margin: 5px 0;
        background-color: #D9C3A0;
        border: 3px solid #8B6F47;
        border-radius: 8px;
        font-family: 'Brush Script MT', cursive, 'Segoe UI', sans-serif;
        font-size: 20px;
        color: #5C4033;
        text-align: center;
        font-weight: normal;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Nút được chọn */
    .stButton > button[kind="primary"] {
        background-color: #C9A87C;
        border: 4px solid #8B6F47;
        font-weight: bold;
    }
    
    /* Style cho header SHOP */
    .shop-header {
        background-color: #D9A76A;
        border: 4px solid #8B6F47;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #8B4513;
        font-family: 'Brush Script MT', cursive, 'Segoe UI', sans-serif;
        margin-bottom: 15px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        text-decoration: underline;
        text-decoration-color: #8B4513;
        text-decoration-thickness: 3px;
    }
    
    /* Panel bên trái - Sidebar */
    .left-panel {
        background-color: #C9A87C;
        border: 4px solid #8B4513;
        border-radius: 10px;
        padding: 20px 10px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        height: 100%;
    }
    
    .left-panel-header {
        background-color: #F5DEB3;
        border: 3px solid #8B6F47;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #8B4513;
        font-family: 'Brush Script MT', cursive;
        margin-bottom: 20px;
        text-decoration: underline;
    }
    
    /* Khu vực trung tâm */
    .center-area {
        background-color: #EDD9B8;
        border: 4px solid #8B6F47;
        border-radius: 10px;
        padding: 20px;
        min-height: 500px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    
    /* Style cho card vật phẩm */
    .item-card {
        background-color: #FFFFFF;
        border: 3px solid #CCCCCC;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        height: 100%;
    }
    
    .item-image {
        width: 100%;
        height: 150px;
        object-fit: contain;
        margin-bottom: 10px;
    }
    
    .item-price {
        font-size: 28px;
        font-weight: bold;
        color: #9370DB;
        margin-top: 10px;
        cursor: pointer;
        padding: 8px;
        background-color: #F0F0F0;
        border-radius: 8px;
        border: 2px solid #CCCCCC;
    }
    
    .item-price:hover {
        background-color: #E6E6FA;
        border-color: #9370DB;
    }
    
    /* Panel bên phải - Nhiệm vụ */
    .right-panel {
        background-color: #EDD9B8;
        border: 4px solid #8B6F47;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }
    
    .task-header {
        background-color: #E8A668;
        border: 3px solid #8B6F47;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #000000;
        font-family: 'Brush Script MT', cursive;
        margin-bottom: 15px;
    }
    
    .points-box {
        background-color: #FFFACD;
        border: 3px solid #8B6F47;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .task-card {
        background-color: #FFFACD;
        border: 3px solid #FF69B4;
        border-radius: 10px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        min-height: 100px;
    }
    
    /* Ẩn các element không cần thiết */
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# PHẦN 2: DỮ LIỆU VẬT PHẨM (DATABASE GIẢ LẬP)
# ============================================================================

# Danh sách vật phẩm trong shop
# Lưu ý: Đường dẫn ảnh sẽ cần được cập nhật theo cấu trúc thư mục thực tế
SHOP_ITEMS = [
    # DANH MỤC: MÈO
    {
        "id": "cat_01",
        "name": "Mèo Đốm",
        "category": "Mèo",
        "price": 100000,
        "image": "assets/cat_spotted.png"  # Ảnh mèo đốm từ Image 1
    },
    {
        "id": "cat_02",
        "name": "Mèo Lông Dài",
        "category": "Mèo",
        "price": 500000,
        "image": "assets/cat_fluffy.png"  # Ảnh mèo lông dài từ Image 1
    },
    
    # DANH MỤC: ĐIỂM MÈO (Giường ngủ)
    {
        "id": "bed_01",
        "name": "Đệm Tròn Xanh",
        "category": "Điểm mèo",
        "price": 3500,
        "image": "assets/bed_blue_round.png"
    },
    {
        "id": "bed_02",
        "name": "Đệm Mèo Vằn",
        "category": "Điểm mèo",
        "price": 3800,
        "image": "assets/bed_striped.png"
    },
    {
        "id": "bed_03",
        "name": "Đệm Gấu",
        "category": "Điểm mèo",
        "price": 4100,
        "image": "assets/bed_bear.png"
    },
    {
        "id": "bed_04",
        "name": "Nhà Mèo Xanh",
        "category": "Điểm mèo",
        "price": 4400,
        "image": "assets/bed_house_blue.png"
    },
    {
        "id": "bed_05",
        "name": "Đệm Tròn Hồng",
        "category": "Điểm mèo",
        "price": 4600,
        "image": "assets/bed_pink.png"
    },
    {
        "id": "bed_06",
        "name": "Đệm Đen Trắng",
        "category": "Điểm mèo",
        "price": 4800,
        "image": "assets/bed_blackwhite.png"
    },
    {
        "id": "bed_07",
        "name": "Giường Kẻ Sọc",
        "category": "Điểm mèo",
        "price": 5000,
        "image": "assets/bed_striped_red.png"
    },
    
    # DANH MỤC: CÂY MÈO
    {
        "id": "tree_01",
        "name": "Cây Mèo Cam",
        "category": "Cây mèo",
        "price": 1000,
        "image": "assets/tree_orange.png"
    },
    {
        "id": "tree_02",
        "name": "Cây Mèo Xanh",
        "category": "Cây mèo",
        "price": 1100,
        "image": "assets/tree_blue.png"
    },
    {
        "id": "tree_03",
        "name": "Cây Mèo Kem",
        "category": "Cây mèo",
        "price": 1200,
        "image": "assets/tree_cream.png"
    },
    {
        "id": "tree_04",
        "name": "Cây Mèo Xám",
        "category": "Cây mèo",
        "price": 1300,
        "image": "assets/tree_gray.png"
    },
    {
        "id": "tree_05",
        "name": "Cây Mèo Mini",
        "category": "Cây mèo",
        "price": 1400,
        "image": "assets/tree_mini.png"
    },
    {
        "id": "tree_06",
        "name": "Cây Mèo Lớn",
        "category": "Cây mèo",
        "price": 1500,
        "image": "assets/tree_large.png"
    },
    
    # DANH MỤC: THỨC ĂN & CÁT
    {
        "id": "food_01",
        "name": "Snack Mèo (3 vị)",
        "category": "Thức ăn & Cát",
        "price": 100,
        "image": "assets/food_snack_3.png"
    },
    {
        "id": "food_02",
        "name": "Pate Cá Ngừ",
        "category": "Thức ăn & Cát",
        "price": 250,
        "image": "assets/food_pate.png"
    },
    {
        "id": "food_03",
        "name": "Thức Ăn Khô",
        "category": "Thức ăn & Cát",
        "price": 20000,
        "image": "assets/food_dry.png"
    },
    {
        "id": "litter_01",
        "name": "Cát Vệ Sinh",
        "category": "Thức ăn & Cát",
        "price": 15000,
        "image": "assets/cat_litter.png"
    },
    
    # DANH MỤC: VẬT DỤNG CHO MÈO
    {
        "id": "util_01",
        "name": "Nhà Vệ Sinh",
        "category": "Vật dụng cho mèo",
        "price": 1200,
        "image": "assets/litter_box.png"
    },
    {
        "id": "util_02",
        "name": "Balo Vận Chuyển",
        "category": "Vật dụng cho mèo",
        "price": 400,
        "image": "assets/carrier.png"
    },
    {
        "id": "util_03",
        "name": "Bát Ăn Đôi",
        "category": "Vật dụng cho mèo",
        "price": 900,
        "image": "assets/bowl_double.png"
    },
    {
        "id": "util_04",
        "name": "Bóng Len",
        "category": "Vật dụng cho mèo",
        "price": 50,
        "image": "assets/toy_yarn.png"
    },
]

# Danh sách danh mục
CATEGORIES = [
    "Mèo",
    "Điểm mèo",
    "Cây mèo",
    "Thức ăn & Cát",
    "Vật dụng cho mèo"
]


# ============================================================================
# PHẦN 3: DỮ LIỆU NHIỆM VỤ (GIẢ LẬP - CHỜ TÍCH HỢP MODULE TASK)
# ============================================================================

# Dữ liệu nhiệm vụ giả lập
# Trong tương lai, dữ liệu này sẽ được lấy từ module Task
MOCK_TASKS = [
    {
        "id": "task_chat_1",
        "description": "Trả lời câu hỏi của chatbox ×50",
        "reward": 50,
        "status": "pending"
    },
    # Có thể thêm nhiệm vụ khác ở đây
]


# ============================================================================
# PHẦN 4: HÀM QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
# ============================================================================

def init_session_state():
    """
    Khởi tạo session state cho ứng dụng.
    Chỉ chạy 1 lần khi app được load lần đầu.
    """
    if 'user_points' not in st.session_state:
        # ĐIỂM KHỞI TẠO ĐỂ TEST: 5000 điểm
        st.session_state.user_points = 5000
        
    if 'owned_items' not in st.session_state:
        # Danh sách ID các vật phẩm đã mua
        st.session_state.owned_items = []
        
    if 'selected_category' not in st.session_state:
        # Danh mục đang được chọn
        st.session_state.selected_category = "Mèo"
        
    if 'tasks' not in st.session_state:
        # Danh sách nhiệm vụ (sẽ được thay thế bằng data từ module Task)
        st.session_state.tasks = MOCK_TASKS


def get_user_points() -> int:
    """
    Lấy số điểm hiện tại của người chơi.
    
    Returns:
        int: Số điểm hiện tại
    """
    return st.session_state.user_points


def update_user_points(new_value: int):
    """
    Cập nhật số điểm của người chơi.
    
    Args:
        new_value (int): Giá trị điểm mới
    """
    st.session_state.user_points = new_value


def add_owned_item(item_id: str):
    """
    Thêm vật phẩm vào danh sách đã sở hữu.
    
    Args:
        item_id (str): ID của vật phẩm
    """
    if item_id not in st.session_state.owned_items:
        st.session_state.owned_items.append(item_id)


def is_item_owned(item_id: str) -> bool:
    """
    Kiểm tra xem vật phẩm đã được mua chưa.
    
    Args:
        item_id (str): ID của vật phẩm
        
    Returns:
        bool: True nếu đã mua, False nếu chưa
    """
    return item_id in st.session_state.owned_items


# ============================================================================
# PHẦN 5: LOGIC MUA VẬT PHẨM
# ============================================================================

def purchase_item(item: Dict) -> tuple[bool, str]:
    """
    Xử lý logic mua vật phẩm.
    
    Args:
        item (Dict): Thông tin vật phẩm cần mua
        
    Returns:
        tuple[bool, str]: (Thành công hay không, Thông báo)
    """
    item_id = item['id']
    price = item['price']
    current_points = get_user_points()
    
    # Kiểm tra đã mua chưa
    if is_item_owned(item_id):
        return False, f"Bạn đã sở hữu {item['name']} rồi!"
    
    # Kiểm tra đủ điểm chưa
    if current_points < price:
        return False, f"Không đủ điểm! Bạn cần thêm {price - current_points} điểm."
    
    # Thực hiện mua
    update_user_points(current_points - price)
    add_owned_item(item_id)
    
    return True, f"Đã mua {item['name']} thành công! Còn lại {get_user_points()} điểm."


# ============================================================================
# PHẦN 6: GIAO DIỆN - HIỂN THỊ CÁC THÀNH PHẦN
# ============================================================================

def display_item_card(item: Dict, col):
    """
    Hiển thị thẻ vật phẩm theo phong cách ảnh gốc.
    
    Args:
        item (Dict): Thông tin vật phẩm
        col: Cột Streamlit để hiển thị
    """
    with col:
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        
        # Hiển thị ảnh vật phẩm
        if os.path.exists(item['image']):
            st.image(item['image'], use_container_width=True)
        else:
            # Placeholder với viền nét đứt như trong ảnh gốc
            st.markdown("""
                <div style='background-color: #E8E8E8; 
                            height: 180px; 
                            border: 3px dashed #999999; 
                            border-radius: 10px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: #666;
                            font-size: 18px;
                            margin: 10px 0;'>
                    [Chưa có ảnh]
                </div>
            """, unsafe_allow_html=True)
        
        # Hiển thị giá theo đúng màu trong ảnh gốc
        owned = is_item_owned(item['id'])
        if owned:
            st.markdown(f"""
                <div style='text-align: center; 
                            font-size: 24px; 
                            color: #228B22; 
                            font-weight: bold;
                            margin-top: 15px;
                            padding: 10px;
                            background-color: #90EE90;
                            border-radius: 8px;
                            border: 2px solid #228B22;'>
                    ✓ Đã sở hữu
                </div>
            """, unsafe_allow_html=True)
        else:
            # Màu giá theo ảnh gốc (tím, cam, hồng, xanh...)
            price_colors = ['#9370DB', '#FF8C00', '#FF69B4', '#4169E1', '#32CD32']
            color = price_colors[hash(item['id']) % len(price_colors)]
            
            # Nút mua (click vào giá)
            if st.button(
                f"{item['price']:,}", 
                key=f"buy_{item['id']}", 
                use_container_width=True
            ):
                success, message = purchase_item(item)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            
            # Style cho giá sau khi render button
            st.markdown(f"""
                <style>
                button[data-testid="baseButton-secondary"][kind="secondary"]:has-text("{item['price']:,}") {{
                    font-size: 28px !important;
                    font-weight: bold !important;
                    color: {color} !important;
                    background-color: #F5F5F5 !important;
                    border: 2px solid #CCCCCC !important;
                    padding: 10px !important;
                    margin-top: 10px !important;
                }}
                </style>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


def display_items_grid(items: List[Dict]):
    """
    Hiển thị lưới vật phẩm.
    
    Args:
        items (List[Dict]): Danh sách vật phẩm cần hiển thị
    """
    if not items:
        st.info("Không có vật phẩm nào trong danh mục này.")
        return
    
    # Hiển thị 4 cột mỗi hàng
    num_cols = 4
    for i in range(0, len(items), num_cols):
        cols = st.columns(num_cols)
        for j, item in enumerate(items[i:i+num_cols]):
            display_item_card(item, cols[j])


def display_tasks_panel():
    """
    Hiển thị panel nhiệm vụ bên phải.
    
    Lưu ý: Phần này CHỈ HIỂN THỊ nhiệm vụ.
    Logic hoàn thành nhiệm vụ sẽ do module Task xử lý.
    """
    st.markdown('<div class="shop-header">Nhiệm vụ</div>', unsafe_allow_html=True)
    
    # Hiển thị điểm hiện tại
    st.markdown(f"""
        <div class="points-display">
            💰 Điểm hiện tại: {get_user_points():,}
        </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị danh sách nhiệm vụ
    tasks = st.session_state.tasks
    
    if not tasks:
        st.info("Chưa có nhiệm vụ nào.")
    else:
        for task in tasks:
            status_icon = "⏳" if task['status'] == 'pending' else "✅"
            st.markdown(f"""
                <div class="task-card">
                    <div style="font-size: 16px; margin-bottom: 5px;">
                        {status_icon} {task['description']}
                    </div>
                    <div style="color: #FF1493; font-weight: bold;">
                        Phần thưởng: +{task['reward']} điểm
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Thông tin tích hợp
    st.markdown("""
        ---
        <div style='text-align: center; color: #888; font-size: 12px;'>
            <i>💡 Hoàn thành nhiệm vụ để nhận điểm<br/>
            (Logic nhiệm vụ sẽ được xử lý bởi module Task)</i>
        </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PHẦN 7: MAIN - LAYOUT CHÍNH CỦA SHOP
# ============================================================================

def main():
    """
    Hàm main - Điểm vào của ứng dụng Shop.
    """
    # Khởi tạo session state
    init_session_state()
    
    # Header
    st.markdown('<div class="shop-header">🏪 SHOP</div>', unsafe_allow_html=True)
    
    # Layout chính: 3 cột
    col_left, col_center, col_right = st.columns([1, 3, 1.5])
    
    # ========================================================================
    # (A) CỘT TRÁI - DANH MỤC
    # ========================================================================
    with col_left:
        st.markdown("### 📋 Danh mục")
        
        for category in CATEGORIES:
            if st.button(
                category, 
                key=f"cat_{category}",
                use_container_width=True,
                type="primary" if st.session_state.selected_category == category else "secondary"
            ):
                st.session_state.selected_category = category
                st.rerun()
    
    # ========================================================================
    # (B) CỘT GIỮA - HIỂN THỊ VẬT PHẨM
    # ========================================================================
    with col_center:
        st.markdown(f"### 🛍️ {st.session_state.selected_category}")
        
        # Lọc vật phẩm theo danh mục đã chọn
        filtered_items = [
            item for item in SHOP_ITEMS 
            if item['category'] == st.session_state.selected_category
        ]
        
        # Hiển thị lưới vật phẩm
        display_items_grid(filtered_items)
    
    # ========================================================================
    # (C) CỘT PHẢI - NHIỆM VỤ
    # ========================================================================
    with col_right:
        display_tasks_panel()


# ============================================================================
# PHẦN 8: ĐIỂM KHỞI ĐỘNG
# ============================================================================

if __name__ == "__main__":
    main()


# ============================================================================
# HƯỚNG DẪN TÍCH HỢP MODULE KHÁC (CHO DEV)
# ============================================================================
"""
TÍCH HỢP VỚI MODULE TASK:
-------------------------
1. Import module Task vào đầu file:
   from task_module import get_tasks, complete_task

2. Thay thế MOCK_TASKS trong init_session_state():
   st.session_state.tasks = get_tasks()

3. Module Task sẽ chịu trách nhiệm:
   - Quản lý danh sách nhiệm vụ
   - Xử lý logic hoàn thành nhiệm vụ
   - Cộng điểm cho người chơi khi hoàn thành


TÍCH HỢP VỚI MODULE CHATBOX:
-----------------------------
1. Import module Chatbox:
   from chatbox_module import get_chatbox_questions

2. Module Chatbox sẽ:
   - Hiển thị câu hỏi cho người chơi
   - Kiểm tra câu trả lời
   - Gọi hàm update_user_points() từ shop_module để cộng điểm


CẤU TRÚC THỨ MỤC ĐỀ XUẤT:
-------------------------
project/
├── shop_module.py           (file này)
├── task_module.py           (module nhiệm vụ - sẽ được phát triển)
├── chatbox_module.py        (module chatbot - sẽ được phát triển)
├── main.py                  (file tích hợp tất cả module)
└── assets/
    ├── cat_spotted.png
    ├── cat_fluffy.png
    ├── bed_blue_round.png
    └── ... (các asset khác)


API CÔNG KHAI CỦA SHOP MODULE:
-------------------------------
- get_user_points() -> int
  Lấy số điểm hiện tại của người chơi

- update_user_points(new_value: int)
  Cập nhật số điểm (module khác gọi khi cộng điểm từ nhiệm vụ)

- purchase_item(item: Dict) -> tuple[bool, str]
  Xử lý mua vật phẩm


LƯU Ý QUAN TRỌNG:
-----------------
- Shop module KHÔNG xử lý logic nhiệm vụ
- Shop module KHÔNG xử lý chatbot
- Shop module CHỈ quản lý mua/bán và hiển thị
- Tất cả logic cộng điểm từ nhiệm vụ do module Task xử lý
"""
