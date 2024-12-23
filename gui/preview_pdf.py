import streamlit as st
import os
import base64

# Tạo thư mục lưu file upload
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Hàm hiển thị danh sách file đã tải lên
def list_uploaded_files():
    files = os.listdir(UPLOAD_FOLDER)
    return files

# Hàm hiển thị preview PDF trong iframe
def display_pdf(file_path):
    with open(file_path, "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400px" type="application/pdf"></iframe>'
    return pdf_display

# Hàm preview file bằng @st.dialog
@st.dialog("Xem trước PDF")
def preview_file(file_name, file_path):
    st.markdown(f"### File: {file_name}")
    st.markdown(display_pdf(file_path), unsafe_allow_html=True)

# Chèn CSS để cấu hình kích thước hộp thoại
def inject_css():
    st.markdown(
        """
        <style>
        .st-dialog-container {
            max-width: 180vw !important;  /* Chiều rộng tối đa của dialog */
            max-height: 90vh !important; /* Chiều cao tối đa của dialog */
            margin: 0 auto;             /* Canh giữa */
        }
        .st-dialog {
            width: 150%;                /* Chiều rộng nội dung dialog */
            height: auto;              /* Tự động chiều cao theo nội dung */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("Quản lý file PDF")

# Inject CSS
inject_css()

# Khu vực tải file lên
st.header("Tải lên file PDF")
uploaded_file = st.file_uploader("Chọn file PDF", type="pdf")

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Đã tải lên {uploaded_file.name}")

# Hiển thị danh sách file đã tải lên
st.header("Danh sách file PDF")
files = list_uploaded_files()

if files:
    for file_name in files:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Hiển thị tên file và nút chức năng
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(file_name)
        with col2:
            # Nút Preview mở hộp thoại với `@st.dialog`
            if st.button(f"Preview {file_name}", key=f"preview_{file_name}"):
                preview_file(file_name, file_path)
        with col3:
            # Nút Delete xóa file
            if st.button(f"Delete {file_name}", key=f"delete_{file_name}"):
                os.remove(file_path)
                st.rerun()
else:
    st.info("Không có file nào được tải lên.")
