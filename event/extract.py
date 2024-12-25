from dataclasses import dataclass
import os
import fitz
from .logger import Logger
from .config import Config
from .dtype import ExtractRequest, HanApiRequest, NomApiRequest
  

class Extractor:
    def __init__(self):
        self.logger = Logger(name="Extractor", handlers=Config().logging_handler)
    
    def extract_images(self, request: ExtractRequest):
        type = request.type
        api_requests = []
        if not os.path.exists(request.file_path):
            print(f"File not found: {request.file_path}")
            return

        if not request.file_path.lower().endswith(".pdf"):
            print(f"Invalid file format: {request.file_path}")
            return
        
        pdf_folder = os.path.dirname(request.file_path)  
        pdf_folder = os.path.dirname(pdf_folder)
        output_path = os.path.join(pdf_folder, "images")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        pdf_document = fitz.open(request.file_path)
        print(f"Opened PDF: {request.file_path} - Total pages: {pdf_document.page_count}")
        
        try:
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                image = page.get_pixmap()  
                output_file = os.path.join(output_path, f"page_{page_number + 1}.png")
                image.save(output_file)  

                if request.type == "han":
                    api_request = HanApiRequest(
                        input_file=output_file,
                        position=True
                    )
                else:
                    api_request = NomApiRequest(
                        input_file=output_file,
                        # memories\\419568ca-cb1b-496e-bf44-0218a54de0d4\\a1843577-e115-4ee6-84dd-b88f847a8529\\images\\page_1.png => memories\\419568ca-cb1b-496e-bf44-0218a54de0d4\\a1843577-e115-4ee6-84dd-b88f847a8529\\ocr\\page_1.png
                        # images => ocr
                        output_image=output_file.replace("images", "ocr")
                    )
                api_requests.append(api_request)
        except Exception as e:
            self.logger.error(f"Error extracting pdf: {e}")
        finally:
            pdf_document.close()
            
        return api_requests

if __name__ == "__main__":
    request = ExtractRequest(
        file_path="memories/7b5a83c0-9261-5e2b-9aa1-182fa09ce326/e2a84ad9-08ec-47fb-ad89-4feb6286b447/pdf/file.pdf",     
        type = "han"
    )
    
    extractor = Extractor()
    request_api = extractor.extract_images(request)
    for req in request_api:
        print(req)
