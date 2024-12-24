from dataclasses import dataclass, field
from typing import Optional, Literal
from abc import abstractmethod


###########################################
# Request
###########################################
@dataclass
class ApiRequest:
    input_file: str       
    output_txt: str = None  
    output_image: str = None 

@dataclass
class HanApiRequest(ApiRequest):
    position: bool = False  

@dataclass
class NomApiRequest(ApiRequest):
    pass  


###########################################
# Response
###########################################
@dataclass
class ApiResponse:
    message: str
    status: int
    lines: Optional[list[tuple[str, list]]] = None

@dataclass
class NomApiResponse(ApiResponse):
    nom_text = list[str]
    viet_text = list[str]

@dataclass
class HanApiResponse(ApiResponse):
    han_text: list[str] = field(default_factory=list)
    nom_text: list[str] = field(default_factory=list)
    width: Optional[int] = None  
    height: Optional[int] = None 
     

###########################################
# OcrApi
###########################################
class OcrApi:
    @abstractmethod
    def ocr():
        pass

###########################################
# Message
###########################################
@dataclass
class Message:
    request: ApiRequest
    type: Literal["nom", "han"]
    chat_id: str
    pdf_id: str

@dataclass
class ErrorMessage:
    message : str
    
@dataclass
class SuccessMessage:
    message: str
    request: ApiRequest


###########################################
# ExtractRequest
###########################################
@dataclass
class ExtractRequest:
    file_path: str      
    output_path: str   
    type: Literal["han", "nom"]

###########################################
# App Request
###########################################
@dataclass
class AppRequest:
    chat_id: str
    type: Literal["han", "nom"]
    pdfs: list[str]  = field(default_factory=list)
    pdf_id: str = None


    
