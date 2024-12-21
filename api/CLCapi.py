import os
import requests
import json
from datetime import datetime
import time

# URLs của API
URL_UPLOAD = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"
URL_OCR = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"
URL_TRANS = ""
# Đường dẫn thư mục chứa hình ảnh cần OCR
IMAGE_DIR = "./temp_images"
# Đường dẫn lưu kết quả OCR
OUTPUT_DIR = "./ocr_results"
DELAY = 1
MAX_RETRIES = 3
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
    for retries in range(1, MAX_RETRIES + 1):
        with open(file_path, 'rb') as image_file:
            files = {'image_file': (os.path.basename(file_path), image_file, mime_type)}
            response = requests.post(URL_UPLOAD, files=files, headers=HEADERS)
        if response.status_code == 200:
            try:
                response_json = response.json()
                if response_json.get("is_success"):
                    log_message(f"Upload thành công: {file_path}")
                    return response_json.get("data", {}).get("file_name")
                else:
                    log_message(f"Lỗi khi upload {file_path}: {response_json.get('message')}")
            except (ValueError, KeyError) as e:
                log_message(f"JSON parsing lỗi: {str(e)}")
        else:
            log_message(f"HTTP lỗi khi upload {file_path}: {response.status_code}")
        time.sleep(DELAY)
    log_message(f"Max retries reached. Thất bại khi upload {file_path}")
    return None

def classification(server_file_name):
 
    api_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-classification"
    payload = {"file_name": server_file_name}

    for retries in range(1, MAX_RETRIES + 1):
        response = requests.post(api_url, json=payload, headers=HEADERS)
        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data.get("is_success"):
                    log_message(f"Phân loại thành công: {server_file_name}")
                    return json_data.get("data", {}).get("ocr_id")
                else:
                    log_message(f"Thất bại khi phân loại {server_file_name}, đang thử lại...")
            except (ValueError, KeyError) as e:
                log_message(f"JSON parsing lỗi: {str(e)}")
        else:
            log_message(f"Lỗi {response.status_code}: {response.text}")
        time.sleep(DELAY)

        log_message(f"Max retries reached. Thất bại khi phân loại {server_file_name}")
        return None

def ocr_image(file_name, ocr_id=1):
    """Thực hiện OCR trên hình ảnh đã tải lên."""
    ocr_payload = {"ocr_id": ocr_id, "file_name": file_name}

    for retries in range(1, MAX_RETRIES + 1):
        response = requests.post(
            URL_OCR,
            json=ocr_payload,
            headers={**HEADERS, "Content-Type": "application/json"}
        )
        if response.status_code == 200:
            try:
                response_json = response.json()
                if response_json.get("is_success"):
                    log_message(f"OCR thành công: {file_name}")
                    return response_json["data"]["result_ocr_text"], response_json["data"]["result_bbox"]
                else:
                    log_message(f"Lỗi khi OCR {file_name}: {response_json.get('message')}")
            except (ValueError, KeyError) as e:
                log_message(f"JSON parsing lỗi: {str(e)}")
        else:
            log_message(f"HTTP lỗi khi OCR {file_name}: {response.status_code}")
        
        time.sleep(DELAY)    
    log_message(f"Max retries reached. Thất bại khi OCR {file_name}")
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
