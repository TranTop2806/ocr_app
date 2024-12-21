import streamlit as st
from pdf2image import convert_from_bytes
import os
import io
from PIL import Image
from api.ocr_API import upload_image, classification, ocr_image, save_results, log_message  

TEMP_FOLDER = "./temp_images"
OUTPUT_FOLDER = "./ocr_results"

os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

st.title("OCR App - Chuyển đổi chữ Hán và chữ Nôm")

# Create a side-by-side layout
col1, col2 = st.columns([3, 3])

with col1:
    st.subheader("Chọn loại ngữ liệu để OCR")
    options = ["Chữ Hán", "Chữ Nôm"]
    selected_option = st.radio("Loại ngữ liệu:", options)

    uploaded_file = st.file_uploader("Tải file PDF để xử lý OCR", type=["pdf"])

with col2:
    st.subheader("Preview")
    if uploaded_file:
        pdf_bytes = uploaded_file.read()
        images = convert_from_bytes(pdf_bytes)
        if len(images) > 0:
            st.image(images[0], caption="Trang đầu tiên của PDF", use_column_width=True)

if uploaded_file:
    if selected_option == "Chữ Nôm":
        try:
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes)
            st.write(f"Tổng số trang PDF: {len(images)}")

            # Save temporary images
            st.write("Đang lưu ảnh từ PDF...")
            image_paths = []
            for idx, image in enumerate(images):
                image_path = os.path.join(TEMP_FOLDER, f"page_{idx + 1}.png")
                image.save(image_path, "PNG")
                image_paths.append(image_path)
            st.success(f"Lưu {len(image_paths)} ảnh thành công!")

            # OCR Process
            if st.button("Tiến hành OCR"):
                st.write("Đang xử lý OCR...")
                results = []

                ocr_id = 1
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
                    file_name = os.path.basename(image_path)

                    # Upload image
                    uploaded_file_name = upload_image(image_path)
                    if not uploaded_file_name:
                        st.error(f"Không thể upload file: {image_path}")
                        continue

                    # OCR process
                    if uploaded_file_name:
                        ocr_text, ocr_bbox = ocr_image(uploaded_file_name, ocr_id)
                        if ocr_text:
                            save_results(file_name, ocr_text, ocr_bbox)
                            st.write(f"Xử lý OCR thành công: {file_name}")
                        else:
                            log_message(f"Thất bại khi OCR: {file_name}")
                            st.error(f"Thất bại khi OCR: {file_name}")
                    else:
                        log_message(f"Thất bại khi upload: {file_name}")
                st.write("Xử lý OCR hoàn tất!")

                # Export result options
                st.write("Xuất file kết quả...")
                options = ["Docx", "PDF"]
                selected_option = st.radio("Chọn loại kết quả", options)

        except Exception as e:
            st.error(f"Lỗi xử lý PDF: {str(e)}")
    else:
        st.error("Chức năng OCR chữ Hán chưa được hỗ trợ!")
