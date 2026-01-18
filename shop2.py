import streamlit as st

# ======================================================
# 1. KHỞI TẠO STATE
# ======================================================

def init_shop_state():
    if "user_points" not in st.session_state:
        st.session_state.user_points = 5000  # điểm test

    if "owned_items" not in st.session_state:
        st.session_state.owned_items = []

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Mèo"


# ======================================================
# 2. API SHOP (KHÔNG ĐỤNG TASK / CHATBOT)
# ======================================================

def get_user_points():
    return st.session_state.user_points


def update_user_points(value):
    st.session_state.user_points = value


def purchase_item(item):
    if item["item_id"] in st.session_state.owned_items:
        st.info("Đã sở hữu")
        return

    if get_user_points() >= item["price"]:
        update_user_points(get_user_points() - item["price"])
        st.session_state.owned_items.append(item["item_id"])
        st.success(f"Đã mua: {item['name']}")
    else:
        st.warning("Không đủ điểm")


# ======================================================
# 3. DANH MỤC
# ======================================================

CATEGORIES = [
    "Mèo",
    "Điểm mèo",
    "Cây mèo",
    "Thức ăn & Cát",
    "Vật dụng cho mèo"
]


# ======================================================
# 4. DỮ LIỆU ITEM (DÙNG ẢNH CUNG CẤP)
# ======================================================

ITEMS = [
    {
        "item_id": "cat_01",
        "name": "Mèo cơ bản",
        "category": "Mèo",
        "price": 100000,
        "image_path": "/mnt/data/Điệm mèo (14) (1).png"
    },
    {
        "item_id": "food_01",
        "name": "Thức ăn & cát",
        "category": "Thức ăn & Cát",
        "price": 250,
        "image_path": "/mnt/data/Điệm mèo (11) (1).png"
    },
    {
        "item_id": "tree_01",
        "name": "Cây mèo",
        "category": "Cây mèo",
        "price": 1200,
        "image_path": "/mnt/data/Điệm mèo (12) (1).png"
    },
    {
        "item_id": "bed_01",
        "name": "Đệm mèo",
        "category": "Vật dụng cho mèo",
        "price": 3500,
        "image_path": "/mnt/data/Điệm mèo (10) (1).png"
    },
    {
        "item_id": "house_01",
        "name": "Nhà mèo",
        "category": "Vật dụng cho mèo",
        "price": 4800,
        "image_path": "/mnt/data/Điệm mèo (13) (1).png"
    }
]


# ======================================================
# 5. NHIỆM VỤ (READ ONLY – MODULE KHÁC XỬ LÝ)
# ======================================================

TASKS = [
    {
        "id": "chat_1",
        "description": "Trả lời câu hỏi của chatbot",
        "reward": 50,
        "status": "pending"
    }
]


# ======================================================
# 6. UI – SIDEBAR DANH MỤC
# ======================================================

def render_category_sidebar():
    st.markdown("## 🛒 SHOP")
    for cat in CATEGORIES:
        if st.button(cat, use_container_width=True):
            st.session_state.selected_category = cat


# ======================================================
# 7. UI – GRID ITEM
# ======================================================

def render_items():
    selected = st.session_state.selected_category
    items = [i for i in ITEMS if i["category"] == selected]

    cols = st.columns(4)
    for idx, item in enumerate(items):
        with cols[idx % 4]:
            st.image(item["image_path"], use_container_width=True)

            if st.button(
                f"{item['price']} điểm",
                key=item["item_id"]
            ):
                purchase_item(item)


# ======================================================
# 8. UI – TASK PANEL
# ======================================================

def render_tasks():
    st.markdown("## 🎯 Nhiệm vụ")
    for task in TASKS:
        with st.container(border=True):
            st.write(task["description"])
            st.write(f"🎁 +{task['reward']} điểm")
            st.write(f"📌 {task['status']}")


# ======================================================
# 9. UI – HEADER ĐIỂM
# ======================================================

def render_points():
    st.markdown(
        f"""
        <div style="background:white;
                    padding:10px;
                    border-radius:8px;
                    text-align:center;
                    font-weight:bold;">
            ⭐ Điểm hiện tại: {get_user_points()}
        </div>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# 10. RUN SHOP MODULE
# ======================================================

def run_shop():
    init_shop_state()

    col_left, col_center, col_right = st.columns([1, 3, 1])

    with col_left:
        render_category_sidebar()

    with col_center:
        render_items()

    with col_right:
        render_points()
        render_tasks()


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    run_shop()
