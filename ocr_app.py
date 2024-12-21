import streamlit as st
from pdf2image import convert_from_bytes
import os
import io
import json
# from api.apiclc import upload, classification, ocr_sino_nom  # Import các hàm từ module apiclc
from PIL import Image
from utils.extract_ocr import pdf_to_images  
from api.CLCapi import upload_image,classification ,ocr_image, save_results,log_message  


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
    if selected_option == "Chữ Nôm":
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

                ocr_id = 1
                # Lấy id_ocr trang đầu tiên cho các trang còn lại
                for retry in range(3):
                    first_image_path = image_paths[0]
                    uploaded_file_name = upload_image(first_image_path)
                    if not uploaded_file_name:
                        st.error(f"Không thể upload file: {first_image_path}")
                    else:
                        ocr_id = classification(uploaded_file_name)
                        if not ocr_id:
                            st.error(f"Không thể phân loại file: {first_image_path}")
                        else:
                            break

                for image_path in image_paths:
                    # Tên file
                    file_name = os.path.basename(image_path)

                    # Gọi API upload ảnh
                    uploaded_file_name = upload_image(image_path)
                    if not uploaded_file_name:
                        st.error(f"Không thể upload file: {image_path}")
                        continue

                    # Gọi API phân loại (classification)
                    # ocr_id = classification(uploaded_file_name)
                    # if not ocr_id:
                    #     st.error(f"Không thể phân loại file: {file_name}")
                    #     continue

                    # Gọi API OCR
                    if uploaded_file_name:
                        ocr_text, ocr_bbox = ocr_image(uploaded_file_name, ocr_id)
                        if ocr_text:
                            # Lưu kết quả OCR
                            save_results(file_name, ocr_text, ocr_bbox)
                            st.write(f"Xử lý OCR thành công: {file_name}")
                        else:
                            log_message(f"Thất bại khi OCR: {file_name}")
                            st.error(f"Thất bại khi OCR: {file_name}")
                    else:
                        log_message(f"Thất bại khi upload: {file_name}")
                st.write("Xử lý OCR hoàn tất!")

                # Xuất file kết quả
                st.write("Xuất file kết quả...")
                options = ["Docx", "PDF"]
                selected_option = st.radio("Chọn loại kết quả", options)

                    

        except Exception as e:
            st.error(f"Lỗi xử lý PDF: {str(e)}")
    else:
        st.error("Chức năng OCR chữ Hán chưa được hỗ trợ!")
