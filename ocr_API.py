import os
import requests
import json
from datetime import datetime

# URLs của API
URL_UPLOAD = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"
URL_OCR = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"

# Đường dẫn thư mục chứa hình ảnh cần OCR
IMAGE_DIR = "./temp_images"
# Đường dẫn lưu kết quả OCR
OUTPUT_DIR = "./ocr_results"

# Đảm bảo thư mục lưu kết quả tồn tại
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Batch OCR Script"
}

def log_message(message):
    """In và ghi log thông tin."""
    print(f"{datetime.now()} - {message}")

def upload_image(file_path):
    """Upload một hình ảnh lên server và trả về file_name."""
    mime_type = "image/png" if file_path.lower().endswith(".png") else "image/jpeg"
    with open(file_path, 'rb') as image_file:
        files = {'image_file': (os.path.basename(file_path), image_file, mime_type)}
        response = requests.post(URL_UPLOAD, files=files, headers=HEADERS)
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("is_success"):
            log_message(f"Upload thành công: {file_path}")
            return response_json.get("data", {}).get("file_name")
        else:
            log_message(f"Lỗi khi upload {file_path}: {response_json.get('message')}")
    else:
        log_message(f"HTTP lỗi khi upload {file_path}: {response.status_code}")
    return None

def ocr_image(file_name):
    """Thực hiện OCR trên hình ảnh đã tải lên."""
    ocr_payload = {"ocr_id": 1, "file_name": file_name}
    response = requests.post(
        URL_OCR,
        json=ocr_payload,
        headers={**HEADERS, "Content-Type": "application/json"}
    )
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("is_success"):
            log_message(f"OCR thành công: {file_name}")
            return response_json["data"]["result_ocr_text"], response_json["data"]["result_bbox"]
        else:
            log_message(f"Lỗi khi OCR {file_name}: {response_json.get('message')}")
    else:
        log_message(f"HTTP lỗi khi OCR {file_name}: {response.status_code}")
    return None, None

def save_results(file_name, ocr_text, ocr_bbox):
    """Lưu kết quả OCR dạng JSON."""
    result_data = {
        "file_name": file_name,
        "ocr_text": ocr_text,
        "ocr_bbox": ocr_bbox
    }
    output_file_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_name)[0]}.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(result_data, output_file, ensure_ascii=False, indent=4)
    log_message(f"Kết quả OCR đã lưu vào: {output_file_path}")

def process_images():
    """Xử lý tất cả hình ảnh trong thư mục."""
    for file_name in os.listdir(IMAGE_DIR):
        file_path = os.path.join(IMAGE_DIR, file_name)
        # Kiểm tra xem có phải file hình ảnh không
        if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            log_message(f"Đang xử lý: {file_name}")
            # Upload hình ảnh
            uploaded_file_name = upload_image(file_path)
            if uploaded_file_name:
                # OCR hình ảnh
                ocr_text, ocr_bbox = ocr_image(uploaded_file_name)
                if ocr_text:
                    # Lưu kết quả OCR
                    save_results(file_name, ocr_text, ocr_bbox)
                else:
                    log_message(f"Thất bại khi OCR: {file_name}")
            else:
                log_message(f"Thất bại khi upload: {file_name}")

if __name__ == "__main__":
    process_images()