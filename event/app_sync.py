from .config import Config
from .dtype import Message, ExtractRequest, AppRequest, OcrApi, ApiRequest, ApiResponse, SuccessMessage, ErrorMessage
from .extract import Extractor
from .logger import Logger
import os
from .api_han import HanApiRequest, HanApiResponse, HanOcrApi
from .api_nom import NomApiRequest, NomApiResponse, NomOcrAPI
from .ui_event import Chat
from typing import Dict, Union
import time
import streamlit as st

class Processor:
    def __init__(self):
        self.api : Dict[str, OcrApi] = {
            "han" :  HanOcrApi(
                email="dotu30257@gmail.com", 
                base_url="https://ocr.kandianguji.com", 
                token="790a0ffd-ad16-421b-962b-2b1f9e89ddda"
            ),
            "nom" : NomOcrAPI()
        }

    
    def run(self, request : Message):
        request_type = request.type
        response = self.api[request_type].ocr(request.request)

        if request_type == "han":
            return self.post_process_han(request, response)
        

    def post_process_han(self, request : Message, response : ApiResponse):
        # write result to memories
        try:
            chat = Chat(request.chat_id)
            page_id = chat.get_page_id_from_path(request.request.input_file)
            chat.write_txt(request.pdf_id, page_id, response.han_text, response.nom_text)
            # write image
            if request.request.position:
                chat.draw_bounding_boxes(request, response, page_id)
            
            return SuccessMessage(
                message=f"OCR Success- : {request.request.input_file}",
                request=request.request
            )
        except Exception as e:
            return ErrorMessage(
                message=f"Error OCR : {e}"
            )
            

class AppSync:
    def __init__(self):
        self.config = Config()
        self.logger = Logger(name="App", handlers=self.config.logging_handler)
        self.extractor = Extractor()
        self.processor = Processor()

    def start(self, pdf_path, type="han", progress_bar = None, status_text = None, test=False):
            
        try:
            # Extract PDF to image
            extract_request = ExtractRequest(
                file_path=pdf_path,
                type="han"
            )

            api_requests = self.extractor.extract_images(extract_request)
            
            num_page = len(api_requests)
            print(api_requests)

            progress_bar = st.progress(0)
            status_text = st.empty()

            response_message = []
            current = 0
            for api_request in api_requests:
                components = pdf_path.split(os.sep)

                chat_id = components[1]  
                pdf_id = components[2]
                request_ocr = Message(
                    request=api_request,
                    chat_id=chat_id,
                    pdf_id=pdf_id,
                    type=type
                )
                if test:
                    time.sleep(1)
                    response = (SuccessMessage(
                        message="OCR Oke",
                        request=None
                    ))

                    response_message.append(response)
                else:
                    response = self.processor.run(request_ocr)
                if isinstance(response, SuccessMessage):
                    response_message.append(response_message)
                    if progress_bar and status_text:
                        current += 1
                        progress_bar.progress(current / num_page)
                        status_text.write(f"Processing {current}/{num_page}")
            
            return response_message
        except Exception as e:
            print("Error OCR :", e) 
            return []           
        

if __name__ == "__main__" :
    pdf_path = "memories/7b5a83c0-9261-5e2b-9aa1-182fa09ce326/e2a84ad9-08ec-47fb-ad89-4feb6286b447/pdf/file.pdf"

    app = AppSync()

    response = app.start(pdf_path=pdf_path, type="han")

    print(response)

        

    