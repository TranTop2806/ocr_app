from google.cloud import translate_v2 as translate
import requests
import base64
import os
from .dtype import HanApiRequest, HanApiResponse, OcrApi
from .extract import ExtractRequest, Extractor

from dotenv import load_dotenv

load_dotenv()


class HanOcrApi(OcrApi):
    def __init__(self, base_url="https://ocr.kandianguji.com", email=None, token=None):
        self.base_url = base_url
        self.email = email
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        self.session = requests.session()
        self.proxies = None
        self.translate_client = translate.Client()

    def translate(self, han_text: str):
        """Dịch văn bản từ chữ Hán sang tiếng Việt sử dụng Google Cloud Translation API."""
        try:
            if not han_text:
                return ""
            
            han_text = han_text.split("\n")

            
            result_viet = []
            for han_line in han_text:
                result = self.translate_client.translate(
                    han_line,
                    source_language='zh',
                    target_language='vi'
                )
                result_viet.append(result['translatedText'].lower())

            return result_viet
        except Exception as e:
            print(f"Lỗi khi dịch văn bản bằng Google Cloud Translation: {e}")
            return ""
        
    def ocr(self, request: HanApiRequest):
        """OCR và dịch văn bản"""
        try:
            with open(request.input_file, "rb") as f:
                image = base64.b64encode(f.read()).decode("utf-8")
        except FileNotFoundError:
            print(f"File not found: {request.input_file}")
            return

        data = {
            "image": image,
            "email": self.email,
            "token": self.token,
            "return_position": request.position
        }

        try:
            response = self.session.post(f"{self.base_url}/ocr_api", json=data, headers=self.headers)
            status = response.status_code
            response.raise_for_status()
            res_json = response.json()

            result_message = res_json.get("message", "")
            if result_message == "error":
                return HanApiResponse(
                    message=res_json.get("error", ""),
                    status=404,
                    han_text=[],
                    nom_text=[],
                    lines=[],
                    width=None,
                    height=None
                )

            result_text = res_json.get("data", {}).get("texts", [])
            viet_text = self.translate("\n".join(result_text)) if result_text else ""

            if request.position:
                result_width = res_json.get("data", {}).get("width", None)
                result_height = res_json.get("data", {}).get("height", None)
                text_lines = res_json.get("data", {}).get("text_lines", [])
                lines = [(line.get("text", ""), line.get("position", [])) for line in text_lines]
            else:
                result_width = result_height = lines = None

            return HanApiResponse(
                message=result_message,
                status=status,
                han_text=result_text,
                nom_text=viet_text,
                lines=lines,
                width=result_width,
                height=result_height
            )

        except requests.exceptions.RequestException as e:
            print(f"Error OCR API HAN: {e}")
            return None

        if request.output_image:
            try:
                self.draw_bounding_boxes(request, result)
            except Exception as e:
                print(f"Error drawing bounding boxes: {e}")


if __name__ == "__main__":
    pdf = "memories/419568ca-cb1b-496e-bf44-0218a54de0d4/162d41d3-9509-4e1b-9af1-f822de3e497a/pdf/file.pdf"
    output_path = os.path.join("/".join(pdf.split("/")[:-2]))
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    request = ExtractRequest(
        file_path=pdf,
        type="han"
    )

    extractor = Extractor()
    api_requests = extractor.extract_images(request)

    chat_id = os.path.basename(os.path.dirname(os.path.dirname(pdf)))
    pdf_id = os.path.basename(os.path.dirname(pdf))

    api = HanOcrApi(
        email=os.getenv("EMAIL"),
        base_url="https://ocr.kandianguji.com",
        token=os.getenv("TOKEN")
    )

    for input_file in os.listdir(os.path.join(output_path, "images")):
        if not input_file.endswith(".png"):
            continue
        request = HanApiRequest(
            input_file=os.path.join(output_path, "images", input_file),
            output_txt=None,
            output_image=f"memories/{chat_id}/{pdf_id}/ocr/{input_file}",
            position=True
        )

        response = api.ocr(request)
        if response:
            print("Dịch thành công:", response.nom_text)
