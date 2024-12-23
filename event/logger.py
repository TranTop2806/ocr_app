import logging
import sys

class Logger(logging.Logger):
    def __init__(self, name: str, handlers: list = []):
        super().__init__(name)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        for handler in handlers:
            key = handler["key"]
            level = handler["level"]
            if key == "stdout":
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(logging._nameToLevel.get(level))
                handler.setFormatter(formatter)
                self.addHandler(handler)
            elif key == "file":
                filename = handler["file"]
                handler = logging.FileHandler(filename)
                handler.setLevel(logging._nameToLevel.get(level))
                handler.setFormatter(formatter)
                self.addHandler(handler)  

if __name__ == "__main__":
    handlers = [
        {
            "key" : "stdout",
            "level" : "DEBUG",
        },
        {
            "key" : "file",
            "level" : "DEBUG",
            "file" : "errors.log"
        }
    ]
    logger = Logger(
        name="test",
        handlers=handlers
    )
    logger.debug("test messgae")

