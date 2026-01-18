import streamlit as st
from typing import List, Dict

# ======================================================
# 1. KHỞI TẠO STATE (CHỈ DÙNG ĐỂ TEST SHOP)
# ======================================================

def init_shop_state():
    """Khởi tạo state nếu chưa tồn tại"""
    if "user_points" not in st.session_state:
        st.session_state.user_points = 5000  # điểm test ban đầu

    if "owned_items" not in st.session_state:
        st.session_state.owned_items = []

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Mèo"


# ======================================================
# 2. CÁC HÀM QUẢN LÝ ĐIỂM (READ / UPDATE)
# ======================================================

def get_user_points() -> int:
    return st.session_state.user_points


def update_user_points(new_value: int):
    st.session_state.user_points = new_value


# ======================================================
# 3. DỮ LIỆU SHOP (STATIC – DỄ MỞ RỘNG)
# ======================================================

CATEGORIES = [
    "Mèo",
    "Điểm mèo",
    "Cây mèo",
    "Thức ăn & Cát",
    "Vật dụng cho mèo",
]

ITEMS: List[Dict] = {
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

# ======================================================
# 4. GIẢ LẬP DỮ LIỆU NHIỆM VỤ (READ-ONLY)
# ======================================================

TASKS = [
    {
        "id": "chat_1",
        "description": "Trả lời câu hỏi của chatbot",
        "reward": 50,
        "status": "pending",
    },
    {
        "id": "chat_2",
        "description": "Hoàn thành 3 câu hỏi",
        "reward": 100,
        "status": "pending",
    },
]


# ======================================================
# 5. LOGIC MUA VẬT PHẨM
# ======================================================

def purchase_item(item: Dict):
    """Xử lý mua vật phẩm"""
    if item["item_id"] in st.session_state.owned_items:
        st.info("Bạn đã sở hữu vật phẩm này")
        return

    if get_user_points() >= item["price"]:
        update_user_points(get_user_points() - item["price"])
        st.session_state.owned_items.append(item["item_id"])
        st.success(f"Đã mua {item['name']}")
    else:
        st.warning("Không đủ điểm để mua vật phẩm này")


# ======================================================
# 6. GIAO DIỆN SHOP
# ======================================================

def render_category_sidebar():
    """Thanh danh mục bên trái"""
    st.markdown("## SHOP")
    for cat in CATEGORIES:
        if st.button(cat, use_container_width=True):
            st.session_state.selected_category = cat


def render_items_grid():
    """Khu vực trung tâm hiển thị vật phẩm"""
    selected = st.session_state.selected_category
    filtered_items = [i for i in ITEMS if i["category"] == selected]

    cols = st.columns(4)

    for idx, item in enumerate(filtered_items):
        with cols[idx % 4]:
            if item.get("image_path"):
                st.image(item["image_path"], use_container_width=True)
            else:
                st.empty()  # placeholder nếu chưa có ảnh

            st.caption(item["name"])

            # Click vào GIÁ để mua
            if st.button(f"{item['price']} điểm", key=item["item_id"]):
                purchase_item(item)


def render_task_panel():
    """Thanh nhiệm vụ bên phải (READ-ONLY)"""
    st.markdown("### 🎯 Nhiệm vụ")

    # Hiển thị điểm hiện tại
    st.markdown(f"**Điểm hiện tại:** {get_user_points()}")

    st.divider()

    for task in TASKS:
        st.markdown(
            f"""
            **{task['description']}**  
            🎁 Thưởng: {task['reward']}  
            ⏳ Trạng thái: {task['status']}
            """
        )
        st.divider()


# ======================================================
# 7. HÀM CHÍNH – SHOP MODULE
# ======================================================

def shop_app():
    """
    SHOP MODULE
    - Chỉ chịu trách nhiệm hiển thị & mua
    - Không xử lý nhiệm vụ / chatbot
    """
    init_shop_state()

    left, center, right = st.columns([2, 6, 3])

    with left:
        render_category_sidebar()

    with center:
        render_items_grid()

    with right:
        render_task_panel()


# ======================================================
# 8. ENTRY POINT
# ======================================================

if __name__ == "__main__":
    st.set_page_config(
        page_title="Cat Shop",
        layout="wide",
    )
    shop_app()
