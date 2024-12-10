import os
import requests
import time
import json

delay = 12 # 60/5
max_retries = 3
HEADERS = {
    "User-Agent": "Batch OCR Script"
}

def upload(file_path, file_name):
    api_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"

    for retries in range(1, max_retries + 1):
        with open(file_path, "rb") as file:
            files = {
                "image_file": (file_name, file, (f"image/{file_name.split(".")[-1].lower()}"))  # Specify the file name and MIME type
            }
            response = requests.post(api_url, files=files, headers=HEADERS)

        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data.get("is_success"):
                    print(f"Successfully upload {file_name}")
                    return json_data.get("data", {}).get("file_name")
                else:
                    print(f"Failed to upload {file_name}")
                    time.sleep(delay)
                    if retries == max_retries:
                        print(f"Error {response.status_code}. Failed to upload {file_name}")

            except (ValueError, IndexError):
                time.sleep(delay)
                if retries == max_retries:
                    print(f"Failed to upload {file_name}")
        else:
            time.sleep(delay)
            if retries == max_retries:
                print(f"Error {response.status_code}. Failed to upload {file_name}")

def classification(file_name):
    api_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-classification"
    for retries in range(1, max_retries + 1):
        with open(file_name, "rb") as file:
            payload = {
                "file_name": file_name
            }
            response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data.get("is_success"):
                    print(f"Successfully classify {file_name}")
                    return json_data.get("data", {}).get("ocr_id")
                else:
                    print(f"Failed to classify {file_name}")
                    time.sleep(delay)
                    if retries == max_retries:
                        print(f"Error {response.status_code}. Failed to classify {file_name}")

            except (ValueError, IndexError):
                time.sleep(delay)
                if retries == max_retries:
                    print(f"Failed to classify {file_name}")
        else:
            time.sleep(delay)
            if retries == max_retries:
                print(f"Error {response.status_code}. Failed to classify {file_name}")

def ocr_sinoNom(file_name, name, ocr_id):
    api_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"
    for retries in range(1, max_retries + 1):
        payload = {
            "ocr_id": ocr_id,
            "file_name": name
        }
        response = requests.post(api_url, json=payload, headers={**HEADERS, "Content-Type": "application/json"})

        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data.get("is_success"):
                    print(f"Successfully OCR {file_name}")
                    return json_data.get("data", {})
                elif response.status_code == 200:
                    print(f"Error: data: {json_data.get("data", {})}")
                    return
                else:
                    print(f"Failed to OCR {file_name}")
                    time.sleep(delay)
                    if retries == max_retries:
                        print(f"Error {response.status_code}. Failed to OCR {file_name}")

            except (ValueError, IndexError):
                time.sleep(delay)
                if retries == max_retries:
                    print(f"Failed to OCR {file_name}")
        else:
            time.sleep(delay)
            if retries == max_retries:
                print(f"Error {response.status_code}. Failed to OCR {file_name}")


if __name__ == '__main__':
    folder_path = "./TestSino/"
    text_path = "./TestSino/TextFiles"
    file_names = os.listdir(folder_path)
    file_names.sort()

    # text = ""
    cnt = 0
    ocr_id = 1
    for i in range(0, len(file_names)):
        file_name = file_names[i]
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            name = upload(file_path, file_name)
            text = ocr_sinoNom(file_name, name, ocr_id)
            if text is not None:
                json.dump(text.get("result_bbox", {}), open(os.path.join(text_path, f"{os.path.splitext(os.path.basename(file_name))[0]}.json"), "w"))