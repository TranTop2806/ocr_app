from dataclasses import dataclass
import requests
import base64
from .dtype import HanApiRequest, HanApiResponse, OcrApi

class HanOcrApi(OcrApi):
    def __init__(self, base_url="https://ocr.kandianguji.com" , email=None, token=None):
        self.base_url = base_url
        self.email = email
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        self.session = requests.session()
        self.proxies = None

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
        
    def ocr(self, request: HanApiRequest):
        # Formdata for uploading image
        # - image : file base 64
        # - email : email
        # - token : token

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
            response = requests.post(f"{self.base_url}/ocr_api", json=data, headers=self.headers)
            status = response.status_code
            response.raise_for_status()
            res_json = response.json()

            result_message = res_json.get("message", ""),
            if result_message[0] == "error":
                result_message = res_json.get("error", "")
                return  HanApiResponse(
                    message=result_message,
                    status=404,
                    han_text=[],
                    nom_text=[],
                    lines=[],
                    width=None,
                    height=None

                )
            result_text = res_json.get("data", []).get("texts", []),
            
            if request.position:
                result_width = res_json.get("data", []).get("width", None)
                result_height = res_json.get("data", []).get("height", None)
                text_lines = res_json.get("data",[]).get("text_lines", [])
                lines = []
                for line in text_lines:
                    postion = line.get("position", [])
                    text = line.get("text", [])
                    lines.append((text, postion))
                result_lines = lines

            try:
                viet_text = self.translate(result_text) # Dịch văn bản
            except Exception as e:
                viet_text = ""
                print(f"Error: {e}")
            
            result = HanApiResponse(
                message=result_message,
                status=status,
                han_text=result_text[0],
                nom_text=viet_text,
                lines=result_lines,
                width=result_width,
                height=result_height
            )
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return

        if request.output_image:
            try:
                self.draw_bounding_boxes(request, result)
            except Exception as e:
                print(f"Error drawing bounding boxes: {e}")

        return result
         
                
if __name__ == "__main__":
    api = HanOcrApi(
        email="dotu30257@gmail.com", 
        base_url="https://ocr.kandianguji.com", 
        token="790a0ffd-ad16-421b-962b-2b1f9e89ddda"
    )

    request = HanApiRequest(
        input_file="data/TQDN_1/page_1.png",
        output_txt=None,
        output_image="memories/e2a84ad9-08ec-47fb-ad89-4feb6286b447/ocr/page_1.png",
        position=True
    )

    response = api.ocr(request)
    print("Message:", response.message)
    print("Status:", response.status)
    print("Text:", response.han_text)
    print("Nom text:", response.nom_text)
    print("Lines:", response.lines)
    print("Width:", response.width)
    print("Height:", response.height)

