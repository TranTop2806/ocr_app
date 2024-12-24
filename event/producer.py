from .logger import Logger
from .config import Config
from .dtype import Message, ApiRequest
from queue import Queue

class Producer:
    def __init__(self, id: int, queues : dict):
        self.id = id
        self.name = f"Producer_{id}"
        self.app_config = Config()
        
        self.nom_queue = queues["nom"]
        self.han_queue = queues["han"]
        
        self.logger = Logger(
            name=self.name,
            handlers=self.app_config.logging_handler
        )

    def produce(self, message : Message):
        try:
            if message.type == "nom":
                self.nom_queue.put(message)
                self.logger.info(f"Produce NOM message: {message.request.input_file}")
                return True
            elif message.type == "han":
                self.han_queue.put(message)
                self.logger.info(f"Produce HAN message: {message.request.input_file}")
                return True
            else:
                self.logger.error(f"Invalid message type: {message.type}")
                raise Exception(f"Invalid message type: {message.type}")
        except Exception as e:
            self.logger.error(f"Error Putting Message: {message.request.input_file} | {e}")
            raise Exception(f"Error Putting Message: {message.request.input_file} | {e}")
        
if __name__ == "__main__":
    queues = {
        "nom": Queue(),
        "han": Queue(),
    }
    producer = Producer(1, queues=queues)
    
    for i in range(10):
        message = Message(
            request=ApiRequest(
                input_file=f"test_{i}.txt"
            ),
            type="nom" if i % 2 == 0 else "han"
        )
        try:
            producer.produce(message)
        except Exception as e:
            print(e)

    while not queues["nom"].empty():
        print(queues["nom"].get())

    while not queues["han"].empty():
        print(queues["han"].get())
        


    
        

        