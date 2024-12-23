from dataclasses import dataclass
import os
import fitz
from logger import Logger
from config import Config
from dtype import ExtractRequest, HanApiRequest, NomApiRequest
  

class Extractor:
    def __init__(self):
        self.logger = Logger(name="Extractor", handlers=Config().logging_handler)
    
    def extract_images(self, request: ExtractRequest):
        api_requests = []
        if not os.path.exists(request.file_path):
            print(f"File not found: {request.file_path}")
            return

        if not request.file_path.lower().endswith(".pdf"):
            print(f"Invalid file format: {request.file_path}")
            return
        
        output_folder = os.path.basename(request.file_path).split(".")[0]
        output_path = os.path.join(request.output_path, output_folder)
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
                        input_file=output_file
                    )
                api_requests.append(api_request)
        except Exception as e:
            self.logger.error(f"Error extracting pdf: {e}")
        finally:
            pdf_document.close()
            
        return api_requests

if __name__ == "__main__":
    request = ExtractRequest(
        file_path="data/TQDN_1.pdf",     
        output_path="data/",
        type = "han"
    )
    
    extractor = Extractor()
    extractor.extract_images(request)
