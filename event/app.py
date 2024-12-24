from queue import Queue
from .config import Config
from .producer import Producer
from .consumer import Consumer, StoppableThread
from .dtype import Message, ExtractRequest, AppRequest
from .extract import Extractor
from .logger import Logger
import os

class App:
    def __init__(self):
        self.nom_queue = Queue()
        self.han_queue = Queue()
        self.error_queue = Queue()
        self.success_queue = Queue()
    
        self.config = Config()
        self.producer = Producer(id = 1, queues={
            "nom": self.nom_queue,
            "han": self.han_queue
        })

        self.logger = Logger(name="App", handlers=self.config.logging_handler)

        self.extractor = Extractor()

        self.consumers : list[Consumer] = []
    
    def start_consumers(self, type):
        for i in range(self.config.max_worker):
            if type == "han":
                consumer = Consumer(
                    id=i,
                    type="han",
                    queues={
                        "task": self.han_queue,
                        "error": self.error_queue,
                        "success": self.success_queue
                    }
                )
            elif type == "nom":
                consumer = Consumer(
                    id=i,
                    type="nom",
                    queues={
                        "task": self.nom_queue,
                        "error": self.error_queue,
                        "success": self.success_queue
                    }
                )

            self.consumers.append(consumer)

        for consumer in self.consumers:
            consumer.start()

    def stop_consumers(self):
        for consumer in self.consumers:
            consumer.stop()
            consumer.join()
            self.logger.info(f"Consumer {consumer.name} stopped")

    def start(self, app_request: AppRequest):
        num_message = 0
        self.start_consumers(app_request.type)  

        # Validate request
        if len(app_request.pdfs) == 0:
            self.logger.error("No PDFs found")
            self.error_queue.put("No PDFs found")
            return

        for pdf in app_request.pdfs:
            if not os.path.exists(pdf):
                self.logger.error(f"File not found: {pdf}")
                self.error_queue.put(f"File not found: {pdf}")
                continue

            output_path = os.path.join("/".join(pdf.split("/")[:-2]) , "images")
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            request = ExtractRequest(
                file_path=pdf,
                output_path=output_path,
                type=app_request.type
            )
            api_requests = self.extractor.extract_images(request)
            for api_request in api_requests:
                message = Message(
                    request=api_request,
                    type=app_request.type,
                    chat_id=app_request.chat_id,
                    pdf_id=app_request.pdf_id

                )
                self.producer.produce(message)
                num_message += 1
        
        return num_message

class Listener(StoppableThread):
    def __init__(self, app: Queue):
        super().__init__()
        self.app = app
        
    def run(self , progress_bar, status_text, num_message):
        while not self.stopped():
            try:
                message = self.worker.success_queue.get(timeout=self.worker.config.timeout)
                progress_bar.progress(progress_bar.progress + 1)
                status_text.write(f"Processing {progress_bar.progress}/{num_message}")
            except Exception:
                continue

            try:
                error = self.worker.error_queue.get(timeout=self.worker.config.timeout)
                print("UI Error: ", error)
            except Exception:
                continue


if __name__ == "__main__":
    pdfs = [
        "data/TQDN_1.pdf"
    ]

    app_request = AppRequest(
        type="han",
        pdfs=pdfs,
        chat_id=""
    )

    app = App()

    listener = Listener(app)
    listener.start()

    app.start(app_request)
    print("App started")

    # time.sleep(100)
    for consumer in app.consumers:
        consumer.join()
        
    listener.stop()
    listener.join()
    print("Listener stopped")




            





        


        
