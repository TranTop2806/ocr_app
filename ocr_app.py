import streamlit as st
from pdf2image import convert_from_bytes
import os
import io
import json
from api.apiclc import upload, classification, ocr_sino_nom  # Import các hàm từ module apiclc
from PIL import Image
from extract_ocr import pdf_to_images  # Import hàm từ module extract_ocr

TEMP_FOLDER = "./temp_images"
OUTPUT_FOLDER = "./ocr_results"

os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

st.title("OCR App - Chuyển đổi chữ Hán và chữ Nôm")

st.subheader("Chọn loại ngữ liệu để OCR")
options = ["Chữ Hán", "Chữ Nôm"]
selected_option = st.radio("Loại ngữ liệu:", options)

uploaded_file = st.file_uploader("Tải file PDF để xử lý OCR", type=["pdf"])

if uploaded_file:
    try:
        # Chuyển đổi PDF sang ảnh
        pdf_bytes = uploaded_file.read()
        images = convert_from_bytes(pdf_bytes)
        st.write(f"Tổng số trang PDF: {len(images)}")

        # Hiển thị trang đầu tiên
        st.image(images[0], caption="Trang đầu tiên của PDF", use_column_width=True)

        # Lưu ảnh tạm thời để xử lý OCR
        st.write("Đang lưu ảnh từ PDF...")
        image_paths = []
        for idx, image in enumerate(images):
            image_path = os.path.join(TEMP_FOLDER, f"page_{idx + 1}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)
        st.success(f"Lưu {len(image_paths)} ảnh thành công!")

        # Tiến hành OCR khi nhấn nút
        if st.button("Tiến hành OCR"):
            st.write("Đang xử lý OCR...")
            results = []

            for image_path in image_paths:
                # Tên file
                file_name = os.path.basename(image_path)

                # Gọi API upload ảnh
                server_file_name = upload(image_path, file_name)
                if not server_file_name:
                    st.error(f"Không thể upload file: {file_name}")
                    continue

                # Gọi API phân loại (classification)
                ocr_id = classification(server_file_name)
                if not ocr_id:
                    st.error(f"Không thể phân loại file: {file_name}")
                    continue

                # Gọi API OCR
                ocr_result = ocr_sino_nom(file_name, server_file_name, ocr_id)
                if ocr_result:
                    # Lưu kết quả
                    output_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file_name)[0]}.json")
                    with open(output_path, "w", encoding="utf-8") as output_file:
                        json.dump(ocr_result, output_file, ensure_ascii=False, indent=4)
                    st.success(f"OCR thành công: {file_name}")
                    results.append(ocr_result)
                else:
                    st.error(f"OCR thất bại: {file_name}")

            # Hiển thị kết quả
            if results:
                st.write("Kết quả OCR:")
                for result in results:
                    st.json(result)

    except Exception as e:
        st.error(f"Lỗi xử lý PDF: {str(e)}")
