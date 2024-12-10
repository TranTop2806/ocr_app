import streamlit as st
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import requests
import io
from docx import Document

st.title("OCR App")

# Tạo button chọn loại ngữ liệu
st.subheader("Chọn loại ngữ liệu để OCR")

options = ["Chữ Hán", "Chữ Nôm"]
selected_option = st.radio("Loại ngữ liệu:", options)

# Hiển thị lựa chọn người dùng
st.write(f"Bạn đã chọn: {selected_option}")

# Tải ngữ liệu PDF
uploaded_file = st.file_uploader("Tải ngữ liệu PDF", type=["pdf"])

if selected_option == "Chữ Hán":
    if uploaded_file is not None:
        # Đọc ngữ liệu PDF
        # st.write("Đang đọc ngữ liệu PDF...")

        # Logic đọc ngữ liệu

        # Thông báo hoàn thành
        st.write("Đã đọc xong ngữ liệu PDF")

        # Chọn API OCR
        ocr_options = ["KanDianKuJi", "PaddleOCR"]
        selected_ocr_option = st.radio("Chọn API OCR:", ocr_options)
        st.write(f"Bạn đã chọn: {selected_ocr_option}")

        # Button tiến hành OCR
        st.button("Tiến hành OCR")
    
        # Logic API OCR
elif selected_option == "Chữ Nôm":
    if uploaded_file is not None:
        # Đọc ngữ liệu PDF
        st.write("Đang đọc ngữ liệu PDF...")

        # Logic đọc ngữ liệu

        # Thông báo hoàn thành
        st.write("Đã đọc xong ngữ liệu PDF")

        # Chọn API OCR
        st.write(f"Mặc định chọn API CLC!")

        # Logic API OCR
        st.button("Tiến hành OCR")

        



