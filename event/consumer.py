from queue import Queue
from dtype import Message, SuccessMessage, ErrorMessage, ApiRequest, ApiResponse, HanApiRequest
from typing import Literal, Dict
from api_han import HanOcrApi
from api_nom import NomOcrAPI
import time
from logger import Logger
from config import Config
import threading
from ui_event import Chat

## test
import random

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Consumer(StoppableThread):
    def __init__(self, id: int, type: Literal["nom", "han"], queues: Dict[str, Queue], config=None):
        super().__init__()

        self.config = Config()
        self.id = id
        self.type = type
        self.name = f"Consumer_{type}_{id}"
        self.count = 5

        self.retry_queue = Queue()
        self.task_queue = queues["task"]
        self.error_queue = queues["error"]
        self.success_queue = queues["success"]
        self.logger = Logger(
            name=self.name,
            handlers=self.config.logging_handler
        )
        
        
        if self.type == "nom":
            self.api = NomOcrAPI()
        elif self.type == "han":
            self.api = HanOcrApi(
                email="dotu30257@gmail.com", 
                base_url="https://ocr.kandianguji.com", 
                token="790a0ffd-ad16-421b-962b-2b1f9e89ddda"
            )
        else:
            raise Exception("Invalid type")

    def process_message(self, message : Message, is_retry=True):
        """Xử lý chính của Consumer"""
        retries = self.config.max_retries
        while retries > 0 and not self.stopped():
            try:
                print("REQUEST: ", message.request)
                response = self.api.ocr(message.request)
                self.logger.info(f"OCR SUCCESS: {message.request.input_file}")
            except Exception as e:
                self.logger.error(f"Error OCR API: {e}")
                retries -= 1
                continue
            
            print("RESPONSE: ", response)
            if response.status == 200:
                success_message = SuccessMessage(
                    message=f"Success OCR file: {message.request.input_file}",
                    request=message.request
                )
                try:
                    self.success_queue.put(success_message)
                    self.logger.info(f"Process Successful: {message.request.input_file}")
                    retries = self.config.max_retries
                    # write result to memories
                    chat = Chat(message.chat_id)
                    page_id = chat.get_page_id_from_path(message.request.input_file)
                    chat.write_txt(message.pdf_id, page_id, response.han_text, response.nom_text)
                    # write image
                    if message.request.position:
                        chat.draw_bounding_boxes(message, response, page_id)

                    return
                except Exception as e:
                    self.logger.error(f"Error Putting Message: {message.request.input_file} | {e}")
            print(" STATUS CODE: ", response.status)

            retries -= 1
            self.logger.error(f"{self.name} RETRY OCR API {self.config.max_retries - retries} : {message.request.input_file}")
            time.sleep(self.config.delay)
        if is_retry and retries == 0:
            self.logger.error(f"Process Error: {message.request.input_file}")
            self.retry_queue.put(message)
            retries = self.config.max_retries
            self.logger.warning(f"PUT RETRY Message : {message.request.input_file}")
        else:
            self.error_queue.put(f"Error OCR file: {message.request.input_file}")
            self.logger.error(f"PUT ERROR QUEUE OCR file: {message.request.input_file}")
        

    def process_error(self):
        """Xử lý khi có lỗi xảy ra"""
        self.logger.debug(f"{self.name} Process Error ....")
        try:
            message: Message = self.retry_queue.get(timeout=self.config.timeout)
        except Exception:
            return
    
        self.process_message(message=message, is_retry=False)

    def run(self):
        """Chạy luồng Consumer"""
        self.logger.info(f"{self.name} Start Working ....")
        try:
            while not self.stopped():
                if not self.retry_queue.empty() and self.task_queue.empty():
                    self.process_error()
                try:
                    message: Message = self.task_queue.get(timeout=self.config.timeout)
                    self.count = 5
                except Exception:
                    self.count -= 1
                    if self.count == 0:
                        self.stop()
                        self.logger.info(f"{self.name} Stop Working ....")
                        break
                    continue 
                    

                self.process_message(message=message)
                
        except Exception as e:
            self.logger.error(f"{self.name} Error: {e}")


if __name__ == "__main__":
    num_consumers = 3
    queues = {
        "task": Queue(),
        "error": Queue(),
        "success": Queue()
    }

    # Khởi tạo Consumer
    consumers = [Consumer(id=i, type="han", queues=queues) for i in range(num_consumers)]

    for i in range(6):
        queues["task"].put(Message(
        request=HanApiRequest(
            input_file=f"data/TQDN_1/page_{i+1}.png",
            position=True
        ),
        type="han",
        chat_id="7b5a83c0-9261-5e2b-9aa1-182fa09ce326",
        pdf_id="e2a84ad9-08ec-47fb-ad89-4feb6286b447"
    ))

    # Khởi chạy luồng
    for consumer in consumers:
        consumer.start()


    # Dừng tất cả Consumer
    for consumer in consumers:
        consumer.join()
    print("All consumers stopped.")
