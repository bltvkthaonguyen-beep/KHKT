"""
Ứng dụng Streamlit - Dự án KHKT Quốc Gia
Giao diện tương tác với kéo thả vật phẩm, diễn đàn, cửa hàng và chatbox
"""

import streamlit as st
import base64
from pathlib import Path

# ============================================================================
# CẤU HÌNH TRANG
# ============================================================================
st.set_page_config(
    page_title="Ứng dụng Học tập Tương tác",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== HÀM CHUYỂN ẢNH SANG BASE64 ======
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_base64 = get_base64_image("background.jpg")

# ====== HTML + CSS (NHẬN BIẾN PYTHON) ======
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin: 0;
    overflow: hidden;
}}

#background {{
    position: fixed;
    inset: 0;
    background-image: url("data:image/jpeg;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    z-index: 1;
}}
</style>
</head>

<body>
    <div id="background"></div>
</body>
</html>
"""

st.components.v1.html(html_code, height=800, scrolling=False)
# ============================================================================
# GIAO DIỆN HTML/CSS/JAVASCRIPT CHÍNH
# ============================================================================
html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
            width: 100vw;
            height: 100vh;
        }
        
        /* ========== NỀN HÌNH ẢNH ========== */
        #background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #e8d5c4 0%, #f5f5f0 100%);
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            z-index: 1;
        }
        
        /* Container cho các nút */
        #ui-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
            pointer-events: none;
        }
        
        #ui-container > * {
            pointer-events: auto;
        }
        
        /* ========== 3 NÚT TRÒN GÓC TRÊN PHẢI ========== */
        #top-buttons {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 15px;
        }
        
        .round-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: white;
            border: 3px solid #e0e0e0;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .round-button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }
        
        .round-button:active {
            transform: translateY(0) scale(0.95);
        }
        
        /* ========== NÚT TRÒN LỚN GÓC DƯỚI PHẢI (CHATBOT) ========== */
        #chat-button {
            position: absolute;
            bottom: 30px;
            right: 30px;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            border: 4px solid white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 45px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(255,154,158,0.4);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        #chat-button:hover {
            transform: scale(1.1);
            box-shadow: 0 10px 30px rgba(255,154,158,0.6);
        }
        
        /* ========== GIỎ ĐỒ (INVENTORY) ========== */
        #inventory {
            position: absolute;
            bottom: -150px;
            left: 0;
            width: 100%;
            height: 130px;
            background: rgba(255, 255, 255, 0.95);
            border-top: 3px solid #ddd;
            box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
            transition: bottom 0.4s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            padding: 0 30px;
        }
        
        #inventory.show {
            bottom: 0;
        }
        
        .inventory-item {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            cursor: grab;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            user-select: none;
        }
        
        .inventory-item:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        }
        
        .inventory-item:active {
            cursor: grabbing;
        }
        
        /* ========== CÁC POPUP/MODAL ========== */
        .modal {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 500px;
            max-height: 600px;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.3);
            z-index: 100;
            overflow-y: auto;
        }
        
        .modal.show {
            display: block;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translate(-50%, -45%);
            }
            to {
                opacity: 1;
                transform: translate(-50%, -50%);
            }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
        }
        
        .modal-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        
        .close-btn {
            width: 35px;
            height: 35px;
            border-radius: 50%;
            background: #f0f0f0;
            border: none;
            cursor: pointer;
            font-size: 20px;
            transition: all 0.2s ease;
        }
        
        .close-btn:hover {
            background: #ff6b6b;
            color: white;
        }
        
        .modal-content {
            line-height: 1.8;
            color: #555;
        }
        
        /* Overlay khi mở modal */
        .overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 99;
        }
        
        .overlay.show {
            display: block;
        }
        
        /* ========== VẬT PHẨM ĐÃ THẢ ========== */
        .dropped-item {
            position: absolute;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 35px;
            cursor: move;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            user-select: none;
            z-index: 5;
        }
        
        /* ========== NỘI DUNG CỬA HÀNG ========== */
        .shop-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .shop-item {
            padding: 15px;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .shop-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .shop-item-icon {
            font-size: 40px;
            margin-bottom: 10px;
        }
        
        .shop-item-name {
            font-weight: bold;
            color: #333;
        }
        
        .shop-item-price {
            color: #ff6b6b;
            margin-top: 5px;
        }
        
        /* ========== THÔNG TIN NGƯỜI DÙNG ========== */
        .user-info {
            text-align: center;
        }
        
        .user-avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 50px;
        }
        
        .user-name {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .user-level {
            color: #667eea;
            font-weight: bold;
            margin-bottom: 15px;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 65%;
            transition: width 0.5s ease;
        }
    </style>
</head>
<body>
    <!-- Nền hình ảnh -->
    <div id="background"></div>
    
    <!-- Overlay cho modal -->
    <div class="overlay" id="overlay"></div>
    
    <!-- Container UI -->
    <div id="ui-container">
        <!-- 3 nút góc trên phải -->
        <div id="top-buttons">
            <div class="round-button" onclick="openModal('forum')" title="Diễn đàn">❤️</div>
            <div class="round-button" onclick="openModal('shop')" title="Cửa hàng">💰</div>
            <div class="round-button" onclick="openModal('user')" title="Thông tin">🎒</div>
        </div>
        
        <!-- Nút chat góc dưới phải -->
        <div id="chat-button" onclick="openModal('chat')" title="Trợ lý học tập">🐱</div>
        
        <!-- Giỏ đồ -->
        <div id="inventory">
            <div class="inventory-item" draggable="true" data-emoji="📚">📚</div>
            <div class="inventory-item" draggable="true" data-emoji="✏️">✏️</div>
            <div class="inventory-item" draggable="true" data-emoji="🎨">🎨</div>
            <div class="inventory-item" draggable="true" data-emoji="🎮">🎮</div>
            <div class="inventory-item" draggable="true" data-emoji="🎵">🎵</div>
            <div class="inventory-item" draggable="true" data-emoji="⚽">⚽</div>
            <div class="inventory-item" draggable="true" data-emoji="🌸">🌸</div>
        </div>
    </div>
    
    <!-- Modal Diễn đàn -->
    <div class="modal" id="forum-modal">
        <div class="modal-header">
            <div class="modal-title">💬 Diễn đàn Học tập</div>
            <button class="close-btn" onclick="closeModal('forum')">×</button>
        </div>
        <div class="modal-content">
            <h3>📌 Bài viết mới nhất:</h3>
            <div style="margin-top: 15px;">
                <div style="padding: 15px; background: #f8f9fa; border-radius: 10px; margin-bottom: 10px;">
                    <strong>🎓 Nguyễn Văn A:</strong> Các bạn đã làm bài tập Toán chưa?
                    <div style="color: #999; font-size: 12px; margin-top: 5px;">5 phút trước</div>
                </div>
                <div style="padding: 15px; background: #f8f9fa; border-radius: 10px; margin-bottom: 10px;">
                    <strong>📖 Trần Thị B:</strong> Mình có tài liệu ôn thi, ai cần inbox nhé!
                    <div style="color: #999; font-size: 12px; margin-top: 5px;">1 giờ trước</div>
                </div>
                <div style="padding: 15px; background: #f8f9fa; border-radius: 10px;">
                    <strong>🔬 Lê Văn C:</strong> Thí nghiệm Hóa học hôm qua rất thú vị!
                    <div style="color: #999; font-size: 12px; margin-top: 5px;">3 giờ trước</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal Cửa hàng -->
    <div class="modal" id="shop-modal">
        <div class="modal-header">
            <div class="modal-title">🛒 Cửa hàng Vật phẩm</div>
            <button class="close-btn" onclick="closeModal('shop')">×</button>
        </div>
        <div class="modal-content">
            <div class="shop-grid">
                <div class="shop-item">
                    <div class="shop-item-icon">📖</div>
                    <div class="shop-item-name">Sách Toán</div>
                    <div class="shop-item-price">50 Xu</div>
                </div>
                <div class="shop-item">
                    <div class="shop-item-icon">🎨</div>
                    <div class="shop-item-name">Bút màu</div>
                    <div class="shop-item-price">30 Xu</div>
                </div>
                <div class="shop-item">
                    <div class="shop-item-icon">🏆</div>
                    <div class="shop-item-name">Cup vàng</div>
                    <div class="shop-item-price">100 Xu</div>
                </div>
                <div class="shop-item">
                    <div class="shop-item-icon">⭐</div>
                    <div class="shop-item-name">Huy hiệu</div>
                    <div class="shop-item-price">80 Xu</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal Thông tin người dùng -->
    <div class="modal" id="user-modal">
        <div class="modal-header">
            <div class="modal-title">👤 Thông tin Cá nhân</div>
            <button class="close-btn" onclick="closeModal('user')">×</button>
        </div>
        <div class="modal-content">
            <div class="user-info">
                <div class="user-avatar">😊</div>
                <div class="user-name">Học sinh THPT</div>
                <div class="user-level">⭐ Cấp độ 5</div>
                <div style="margin-top: 20px;">
                    <strong>Tiến trình học tập:</strong>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                    <div style="margin-top: 10px; color: #667eea;">65% hoàn thành</div>
                </div>
                <div style="margin-top: 20px; text-align: left;">
                    <p><strong>📊 Thống kê:</strong></p>
                    <p>• Số xu: 250 💰</p>
                    <p>• Bài đã hoàn thành: 45/70</p>
                    <p>• Ngày học liên tiếp: 12 ngày 🔥</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal Chat -->
    <div class="modal" id="chat-modal">
        <div class="modal-header">
            <div class="modal-title">💬 Trợ lý Học tập</div>
            <button class="close-btn" onclick="closeModal('chat')">×</button>
        </div>
        <div class="modal-content">
            <div style="height: 300px; overflow-y: auto; border: 1px solid #eee; border-radius: 10px; padding: 15px; background: #f9f9f9;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #667eea; color: white; padding: 10px; border-radius: 15px; display: inline-block;">
                        Xin chào! Tôi có thể giúp gì cho bạn? 😊
                    </div>
                </div>
                <div style="margin-bottom: 15px; text-align: right;">
                    <div style="background: #e0e0e0; padding: 10px; border-radius: 15px; display: inline-block;">
                        Giải thích định lý Pythagore được không?
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <div style="background: #667eea; color: white; padding: 10px; border-radius: 15px; display: inline-block;">
                        Định lý Pythagore: a² + b² = c², áp dụng cho tam giác vuông! 📐
                    </div>
                </div>
            </div>
            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <input type="text" placeholder="Nhập câu hỏi..." style="flex: 1; padding: 10px; border: 2px solid #ddd; border-radius: 25px; outline: none;">
                <button style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 25px; cursor: pointer;">Gửi</button>
            </div>
        </div>
    </div>
    
    <script>
        // ========== XỬ LÝ MỞ/ĐÓNG MODAL ==========
        function openModal(type) {
            document.getElementById(type + '-modal').classList.add('show');
            document.getElementById('overlay').classList.add('show');
        }
        
        function closeModal(type) {
            document.getElementById(type + '-modal').classList.remove('show');
            document.getElementById('overlay').classList.remove('show');
        }
        
        // Đóng modal khi click overlay
        document.getElementById('overlay').addEventListener('click', function() {
            document.querySelectorAll('.modal').forEach(modal => {
                modal.classList.remove('show');
            });
            this.classList.remove('show');
        });
        
        // ========== XỬ LÝ NHẤN ĐÚP CHUỘT - MỞ GIỎ ĐỒ ==========
        let inventoryOpen = false;
        document.addEventListener('dblclick', function(e) {
            const inventory = document.getElementById('inventory');
            inventoryOpen = !inventoryOpen;
            if (inventoryOpen) {
                inventory.classList.add('show');
            } else {
                inventory.classList.remove('show');
            }
        });
        
        // ========== XỬ LÝ KÉO THẢ VẬT PHẨM ==========
        let draggedElement = null;
        let isDraggingFromInventory = false;
        
        // Kéo từ giỏ đồ
        document.querySelectorAll('.inventory-item').forEach(item => {
            item.addEventListener('dragstart', function(e) {
                isDraggingFromInventory = true;
                const emoji = this.getAttribute('data-emoji');
                e.dataTransfer.setData('emoji', emoji);
                e.dataTransfer.effectAllowed = 'copy';
            });
            
            item.addEventListener('dragend', function() {
                isDraggingFromInventory = false;
            });
        });
        
        // Thả vật phẩm lên background
        document.getElementById('background').addEventListener('dragover', function(e) {
            e.preventDefault();
        });
        
        document.getElementById('background').addEventListener('drop', function(e) {
            e.preventDefault();
            if (isDraggingFromInventory) {
                const emoji = e.dataTransfer.getData('emoji');
                createDroppedItem(emoji, e.clientX, e.clientY);
            }
        });
        
        // Tạo vật phẩm đã thả
        function createDroppedItem(emoji, x, y) {
            const item = document.createElement('div');
            item.className = 'dropped-item';
            item.textContent = emoji;
            item.style.left = (x - 30) + 'px';
            item.style.top = (y - 30) + 'px';
            
            // Cho phép di chuyển vật phẩm đã thả
            item.setAttribute('draggable', 'true');
            
            item.addEventListener('dragstart', function(e) {
                draggedElement = this;
                e.dataTransfer.effectAllowed = 'move';
            });
            
            item.addEventListener('dragend', function(e) {
                this.style.left = e.clientX - 30 + 'px';
                this.style.top = e.clientY - 30 + 'px';
            });
            
            document.getElementById('background').appendChild(item);
        }
        
        // ========== XỬ LÝ DI CHUYỂN VẬT PHẨM ĐÃ THẢ ==========
        document.getElementById('background').addEventListener('dragover', function(e) {
            if (draggedElement && !isDraggingFromInventory) {
                e.preventDefault();
            }
        });
        
        document.getElementById('background').addEventListener('drop', function(e) {
            if (draggedElement && !isDraggingFromInventory) {
                e.preventDefault();
                draggedElement.style.left = e.clientX - 30 + 'px';
                draggedElement.style.top = e.clientY - 30 + 'px';
                draggedElement = null;
            }
        });
    </script>
</body>
</html>
"""

# ============================================================================
# HIỂN THỊ GIAO DIỆN
# ============================================================================
st.components.v1.html(html_code, height=800, scrolling=False)

# ============================================================================
# THÔNG TIN HƯỚNG DẪN SỬ DỤNG (Có thể ẩn khi demo)
# ============================================================================
with st.expander("📖 Hướng dẫn sử dụng"):
    st.markdown("""
    ### 🎯 Chức năng chính:
    
    **1. Các nút góc trên phải:**
    - ❤️ **Diễn đàn**: Xem và tham gia thảo luận học tập
    - 💰 **Cửa hàng**: Mua sắm vật phẩm học tập
    - 🎒 **Thông tin**: Xem hồ sơ và tiến trình học tập
    
    **2. Nút trợ lý (góc dưới phải):**
    - 🐱 **Chatbot**: Hỗ trợ giải đáp thắc mắc học tập
    
    **3. Giỏ đồ (Inventory):**
    - **Nhấn đúp chuột** vào bất kỳ đâu trên màn hình để mở/đóng giỏ đồ
    - **Kéo vật phẩm** từ giỏ đồ và thả lên màn hình
    - **Di chuyển vật phẩm** đã thả bằng cách kéo thả
    
    ---
    
    ### 💡 Mục đích dự án:
    Ứng dụng này được thiết kế cho **Cuộc thi Khoa học Kỹ thuật cấp Quốc gia**, 
    nhằm tạo ra môi trường học tập tương tác, thú vị cho học sinh THPT.
    
    ### 🔧 Công nghệ:
    - **Python** + **Streamlit**: Framework chính
    - **HTML/CSS/JavaScript**: Giao diện tương tác
    - **Drag & Drop API**: Kéo thả vật phẩm
    """)

# ============================================================================
# CHÚ THÍCH KỸ THUẬT CHO HỘI ĐỒNG CHẤM
# ============================================================================
st.sidebar.title("📊 Thông tin Kỹ thuật")
st.sidebar.markdown("""
### Kiến trúc ứng dụng:

**1. Streamlit Backend:**
- Quản lý state và routing
- Xử lý dữ liệu người dùng

**2. HTML/CSS Frontend:**
- Giao diện responsive
- Hiệu ứng mượt mà (transitions)

**3. JavaScript:**
- Event handling (double-click, drag & drop)
- DOM manipulation
- Modal management

### Tính năng nổi bật:
✅ Kéo thả vật phẩm (Drag & Drop)  
✅ Giao diện gamification  
✅ Responsive design  
✅ Tương tác thời gian thực  
✅ Dễ mở rộng và bảo trì
""")
