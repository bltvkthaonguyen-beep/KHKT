import streamlit as st
from typing import List, Dict

# ======================================================
# 1. KHỞI TẠO STATE (CHỈ LÀM 1 LẦN)
# ======================================================

def init_shop_state():
    """Khởi tạo state cho Shop – chỉ chạy khi chưa tồn tại"""
    if "user_points" not in st.session_state:
        st.session_state.user_points = 5000  # điểm test

    if "owned_items" not in st.session_state:
        st.session_state.owned_items = []

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Mèo"


# ======================================================
# 2. API NỘI BỘ CHO SHOP (SAU NÀY MODULE KHÁC CÓ THỂ GỌI)
# ======================================================

def get_user_points() -> int:
    return st.session_state.user_points


def update_user_points(new_value: int):
    st.session_state.user_points = new_value


def purchase_item(item: Dict):
    """Xử lý mua vật phẩm – KHÔNG liên quan nhiệm vụ"""
    if item["item_id"] in st.session_state.owned_items:
        st.info("Bạn đã sở hữu vật phẩm này")
        return

    if get_user_points() >= item["price"]:
        update_user_points(get_user_points() - item["price"])
        st.session_state.owned_items.append(item["item_id"])
        st.success(f"Đã mua {item['name']}")
    else:
        st.warning("Không đủ điểm để mua vật phẩm")


# ======================================================
# 3. DỮ LIỆU GIẢ LẬP (SAU NÀY TÁCH SANG MODULE RIÊNG)
# ======================================================

CATEGORIES = [
    "Mèo",
    "Điểm mèo",
    "Cây mèo",
    "Thức ăn & Cát",
    "Vật dụng cho mèo"
]

ITEMS: List[Dict] = [
    # -------- MÈO --------
    {
        "item_id": "cat_01",
        "name": "Mèo xám",
        "category": "Mèo",
        "price": 100000,
        "image_path": "assets/cat_01.png"
    },
    {
        "item_id": "cat_02",
        "name": "Mèo trắng",
        "category": "Mèo",
        "price": 500000,
        "image_path": "assets/cat_02.png"
    },

    # -------- THỨC ĂN & CÁT --------
    {
        "item_id": "food_01",
        "name": "Thanh dinh dưỡng",
        "category": "Thức ăn & Cát",
        "price": 100,
        "image_path": "assets/food_01.png"
    },
    {
        "item_id": "food_02",
        "name": "Thức ăn hộp",
        "category": "Thức ăn & Cát",
        "price": 250,
        "image_path": "assets/food_02.png"
    },

    # -------- CÂY MÈO --------
    {
        "item_id": "tree_01",
        "name": "Cây mèo nhỏ",
        "category": "Cây mèo",
        "price": 1000,
        "image_path": "assets/tree_01.png"
    },

    # -------- VẬT DỤNG --------
    {
        "item_id": "bed_01",
        "name": "Đệm tròn",
        "category": "Vật dụng cho mèo",
        "price": 3500,
        "image_path": "assets/bed_01.png"
    },
]

# ===== NHIỆM VỤ GIẢ LẬP – READ ONLY =====
TASKS = [
    {
        "id": "chat_1",
        "description": "Trả lời câu hỏi của chatbot",
        "reward": 50,
        "status": "pending"
    }
]


# ======================================================
# 4. GIAO DIỆN SHOP
# ======================================================

def render_category_sidebar():
    st.markdown("### 🛒 SHOP")
    for cat in CATEGORIES:
        if st.button(cat, use_container_width=True):
            st.session_state.selected_category = cat


def render_items_grid():
    selected = st.session_state.selected_category
    filtered_items = [i for i in ITEMS if i["category"] == selected]

    cols = st.columns(4)

    for idx, item in enumerate(filtered_items):
        with cols[idx % 4]:
            # ----- ẢNH -----
            if item["image_path"]:
                st.image(item["image_path"], use_container_width=True)
            else:
                st.empty()

            # ----- GIÁ -----
            if st.button(
                f"{item['price']} điểm",
                key=f"buy_{item['item_id']}"
            ):
                purchase_item(item)


def render_task_panel():
    st.markdown("## 🎯 Nhiệm vụ")
    for task in TASKS:
        with st.container(border=True):
            st.write(task["description"])
            st.write(f"🎁 Thưởng: {task['reward']} điểm")
            st.write(f"📌 Trạng thái: {task['status']}")


def render_points_header():
    st.markdown(
        f"""
        <div style="
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
            ">
            ⭐ Điểm hiện tại: {get_user_points()}
        </div>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# 5. HÀM CHẠY MODULE SHOP
# ======================================================

def run_shop():
    init_shop_state()

    col_left, col_center, col_right = st.columns([1, 3, 1])

    with col_left:
        render_category_sidebar()

    with col_center:
        render_items_grid()

    with col_right:
        render_points_header()
        render_task_panel()


# ======================================================
# 6. ĐIỂM TÍCH HỢP MODULE KHÁC (SAU NÀY)
# ======================================================
# - Chatbox module: sẽ cập nhật user_points từ bên ngoài
# - Task module: xử lý hoàn thành nhiệm vụ
# - Shop KHÔNG xử lý các logic này


# ======================================================
# 7. CHẠY TRỰC TIẾP (TEST)
# ======================================================

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    run_shop()

