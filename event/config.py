from dataclasses import dataclass

@dataclass
class Config:
    logging_handler = [
        {
            "key" : "stdout",
            "level" : "DEBUG"
        },
        {
            "key" : "file",
            "level" : "DEBUG",
            "file" : "app.log"
        }
    ]

    max_retries = 3
    delay = 5
    max_worker = 2
    max_queue_size = 100
    timeout = 5