import os
import requests
import json
from fake_useragent import UserAgent
import urllib3
from .dtype import NomApiRequest, NomApiResponse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from .proxy import Proxies, Agent
import random

class NomOcrAPI():
    def __init__(self, base_url="https://tools.clc.hcmus.edu.vn/", proxies=None):
        self.session = requests.session()
        self.base_url = base_url
        self.proxies = proxies or {
        }
        self.headers = {
            "Authorization": "Bearer 123", 
            "User-Agent": self._get_user_agent()
        }
        self.agents = [
                Agent(ip='198.23.239.134', port=6540, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='207.244.217.165', port=6712, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='107.172.163.27', port=6543, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='64.137.42.112', port=5157, username='qqxnuqlx', password='h4eapuuligg9'),
                # Agent(ip='173.211.0.148', port=6641, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='161.123.152.115', port=6360, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='167.160.180.203', port=6754, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='154.36.110.199', port=6853, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='173.0.9.70', port=5653, username='qqxnuqlx', password='h4eapuuligg9'),
                Agent(ip='173.0.9.209', port=5792, username='qqxnuqlx', password='h4eapuuligg9')
        ]

        self.proxy_generator = Proxies(self.agents)

    def _get_user_agent(self):
        ua = UserAgent()
        return ua.random

    def upload_image(self, input_file: str):
        """Upload hình ảnh lên server"""
        url = f"{self.base_url}api/web/clc-sinonom/image-upload"

        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")

        headers = {**self.headers, "User-Agent": self._get_user_agent()}

        with open(input_file, "rb") as f:
            # base 64
            files = {"image_file": f}
            print("size", os.path.getsize(input_file))
            try:
                response = self.session.post(url, files=files, headers=headers, proxies=self.proxies, verify=False)
                response.raise_for_status()

                res_json = response.json()
                if not res_json.get("is_success", False):
                    raise Exception(res_json.get("message", "Image upload failed"))

                print(f"Image uploaded successfully: {res_json}")
                return res_json.get("data", {}).get("file_name")
            except requests.exceptions.RequestException as e:
                print(f"Error uploading image: {e}")
                raise e

    def download_image(self, file_name: str, output_path: str):
        """Tải hình ảnh về từ server"""
        url = f"{self.base_url}api/web/clc-sinonom/image-download?file_name={file_name}"
        headers = {**self.headers, "User-Agent": self._get_user_agent()}

        try:
            response = self.session.get(url, headers=headers, proxies=self.proxies, verify=False)
            response.raise_for_status()

            if "image" not in response.headers.get("Content-Type", ""):
                raise Exception("Response is not an image file")

            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded successfully: {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            raise e

    def perform_ocr(self, file_name: str, output_file: str = None):
        """Gửi yêu cầu OCR và lưu kết quả vào file JSON"""
        url = f"{self.base_url}api/web/clc-sinonom/image-ocr"
        headers = {**self.headers, "User-Agent": self._get_user_agent()}
        body = {"ocr_id": 1, "file_name": file_name}

        try:
            response = self.session.post(url, headers=headers, json=body, proxies=self.proxies, verify=False)
            response.raise_for_status()

            res_json = response.json()
            if not res_json.get("is_success", False):
                raise Exception(res_json.get("message", "OCR processing failed"))
            
            text = res_json.get("data", {}).get("result_ocr_text", [])
            result_bbox = res_json.get("data", {}).get("result_bbox", [])
            lines = []
            for line in result_bbox:
                text_line = line[0]
                bbox = line[1][0]
                lines.append((text_line, bbox))

            viet_text = self.translate(text)

            result = NomApiResponse(
                message="Success performing OCR" if response.status_code == 200 else "Failed performing OCR",
                status=response.status_code,
                nom_text=text,
                viet_text=viet_text,
                lines=lines
            )


            # Lưu kết quả vào file JSON
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(res_json, f, ensure_ascii=False, indent=4)
                print(f"OCR result saved to: {output_file}")

            return result
        except requests.exceptions.RequestException as e:
            print(f"Error performing OCR: {e}")
            raise e
        
    def translate(self, nom_text: str):
        """Dịch văn bản từ chữ Hán sang tiếng Việt"""

        def clean_text_list(input_list: list[str]) -> list[str]:
            result = []
            for item in input_list:
                cleaned_item = (
                    item.replace('[', '')
                        .replace(']', '')
                        .replace('"', '')
                        .replace(',', '')
                        .strip()
                )
                if cleaned_item and len(cleaned_item) > 1:
                    result.append(cleaned_item)
            return result
        
        url = f"https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/sinonom-transliteration"
        headers = {**self.headers, "User-Agent": "Mozilla/5.0" }
        body = {"text": nom_text}

        try:
            response = self.session.post(url, headers=headers, json=body, proxies=self.proxies, verify=False)
            response.raise_for_status()

            res_json = response.json()
            if not res_json.get("is_success", False):
                raise Exception(res_json.get("message", "Translation failed"))

            print(f"Translation result: {res_json}")
            viet_text = res_json.get("data", {}).get("result_text_transcription", "")
            return clean_text_list(viet_text)
        except requests.exceptions.RequestException as e:
            print(f"Error translating text: {e}")


    def ocr(self, request: NomApiRequest):
        """Thực hiện toàn bộ quy trình OCR"""
        i = random.randint(0, len(self.agents) - 1) 
        self.proxies = self.proxy_generator.get_proxies(i)
        try:
            print("Starting OCR process...")

            # 1. Upload image
            uploaded_file_name = self.upload_image(request.input_file)

            # 2. Perform OCR
            result = self.perform_ocr(uploaded_file_name)

            # 3. Download processed image
            if request.output_image:
                self.download_image(uploaded_file_name, request.output_image)

            print("OCR process completed successfully!")

            return result
        except Exception as e:
            print(f"OCR process failed: {e}")
            raise e


if __name__ == "__main__":
    request = NomApiRequest(
        input_file="data/TQDN_1/page_1.png",  
        output_image="output_image.png"    
    )

    api = NomOcrAPI()
    result = api.ocr(request)
    print("Message:", result.message)
    print("Status:", result.status)
    print("Text:", result.nom_text)
    print("Lines:", result.lines)
    print("Viet text: ", result.viet_text)

