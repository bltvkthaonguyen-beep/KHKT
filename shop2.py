import streamlit as st

# ======================================================
# 1. KHỞI TẠO STATE
# ======================================================

def init_state():
    if "user_points" not in st.session_state:
        st.session_state.user_points = 5000  # điểm test

    if "owned_items" not in st.session_state:
        st.session_state.owned_items = []

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Mèo"


# ======================================================
# 2. API SHOP (KHÔNG ĐỤNG MODULE KHÁC)
# ======================================================

def get_user_points():
    return st.session_state.user_points


def update_user_points(value):
    st.session_state.user_points = value


def purchase_item(item):
    if item["item_id"] in st.session_state.owned_items:
        st.info("Bạn đã sở hữu vật phẩm này")
        return

    if get_user_points() >= item["price"]:
        update_user_points(get_user_points() - item["price"])
        st.session_state.owned_items.append(item["item_id"])
        st.success(f"Đã mua: {item['name']}")
    else:
        st.warning("Không đủ điểm để mua")


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
# 4. DANH SÁCH VẬT PHẨM (ĐẦY ĐỦ – ĐÚNG ẢNH)
# ======================================================

ITEMS = {

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
# 5. NHIỆM VỤ (CHỈ HIỂN THỊ)
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

def render_categories():
    st.markdown("## 🛒 SHOP")
    for cat in CATEGORIES:
        if st.button(cat, use_container_width=True):
            st.session_state.selected_category = cat


# ======================================================
# 7. UI – HIỂN THỊ VẬT PHẨM
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
# 8. UI – NHIỆM VỤ
# ======================================================

def render_tasks():
    st.markdown("## 🎯 Nhiệm vụ")
    for task in TASKS:
        with st.container(border=True):
            st.write(task["description"])
            st.write(f"🎁 +{task['reward']} điểm")
            st.write(f"📌 {task['status']}")


# ======================================================
# 9. UI – HIỂN THỊ ĐIỂM
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
# 10. CHẠY MODULE SHOP
# ======================================================

def run_shop():
    init_state()

    col_left, col_center, col_right = st.columns([1, 3, 1])

    with col_left:
        render_categories()

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
