import os
import requests
import time
import json

# Cấu hình chung
DELAY = 12  # Thời gian chờ giữa các lần retry
MAX_RETRIES = 3
HEADERS = {
    "User-Agent": "Batch OCR Script",
    "Content-Type": "application/json"
}

def upload(file_path, file_name):
    """
    Upload hình ảnh lên API.

    Args:
        file_path (str): Đường dẫn tới file.
        file_name (str): Tên file.

    Returns:
        str: Tên file trên server nếu upload thành công, None nếu thất bại.
    """
    api_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"

    for retries in range(1, MAX_RETRIES + 1):
        with open(file_path, "rb") as file:
            files = {
                "image_file": (file_name, file, f"image/{file_name.split('.')[-1].lower()}")
            }
            response = requests.post(api_url, files=files, headers=HEADERS)

        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data.get("is_success"):
                    print(f"[Upload] Successfully uploaded {file_name}")
                    return json_data.get("data", {}).get("file_name")
                else:
                    print(f"[Upload] Failed to upload {file_name}, retrying...")
            except (ValueError, KeyError) as e:
                print(f"[Upload] JSON parsing error: {str(e)}")
        else:
            print(f"[Upload] Error {response.status_code}: {response.text}")

        time.sleep(DELAY)

    print(f"[Upload] Max retries reached. Failed to upload {file_name}")
    return None


def classification(file_name):
    """
    Phân loại hình ảnh đã upload.

    Args:
        file_name (str): Tên file trên server.

    Returns:
        int: OCR ID nếu thành công, None nếu thất bại.
    """
    api_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-classification"
    payload = {"file_name": file_name}

    for retries in range(1, MAX_RETRIES + 1):
        response = requests.post(api_url, json=payload, headers=HEADERS)

        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data.get("is_success"):
                    print(f"[Classification] Successfully classified {file_name}")
                    return json_data.get("data", {}).get("ocr_id")
                else:
                    print(f"[Classification] Failed to classify {file_name}, retrying...")
            except (ValueError, KeyError) as e:
                print(f"[Classification] JSON parsing error: {str(e)}")
        else:
            print(f"[Classification] Error {response.status_code}: {response.text}")

        time.sleep(DELAY)

    print(f"[Classification] Max retries reached. Failed to classify {file_name}")
    return None


def ocr_sino_nom(file_name, server_file_name, ocr_id):
    """
    OCR chữ Nôm từ hình ảnh.

    Args:
        file_name (str): Tên file gốc.
        server_file_name (str): Tên file trên server.
        ocr_id (int): ID OCR.

    Returns:
        dict: Kết quả OCR nếu thành công, None nếu thất bại.
    """
    api_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"
    payload = {
        "ocr_id": ocr_id,
        "file_name": server_file_name
    }

    for retries in range(1, MAX_RETRIES + 1):
        response = requests.post(api_url, json=payload, headers=HEADERS)

        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data.get("is_success"):
                    print(f"[OCR] Successfully processed {file_name}")
                    return json_data.get("data", {})
                else:
                    print(f"[OCR] Failed to process {file_name}, retrying...")
            except (ValueError, KeyError) as e:
                print(f"[OCR] JSON parsing error: {str(e)}")
        else:
            print(f"[OCR] Error {response.status_code}: {response.text}")

        time.sleep(DELAY)

    print(f"[OCR] Max retries reached. Failed to process {file_name}")
    return None


if __name__ == "__main__":
    # Thư mục chứa ảnh
    folder_path = "./TestSino/"
    text_path = "./TestSino/TextFiles"
    os.makedirs(text_path, exist_ok=True)

    file_names = os.listdir(folder_path)
    file_names.sort()

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            server_file_name = upload(file_path, file_name)
            if server_file_name:
                ocr_id = classification(server_file_name)
                if ocr_id:
                    text = ocr_sino_nom(file_name, server_file_name, ocr_id)
                    if text:
                        output_path = os.path.join(text_path, f"{os.path.splitext(file_name)[0]}.json")
                        with open(output_path, "w", encoding="utf-8") as output_file:
                            json.dump(text.get("result_bbox", {}), output_file, ensure_ascii=False, indent=4)
