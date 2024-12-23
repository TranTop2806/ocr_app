import uuid

class IDGenerator:
    def generate_from_string(self, string):
        return uuid.uuid5(uuid.NAMESPACE_URL, string)
    
    def generate(self):
        return uuid.uuid4()
    
    def parse(self, string):
        return uuid.UUID(string)
    
if __name__ == "__main__":
    id_gen = IDGenerator()
    id_from_string = id_gen.generate_from_string("https://www.example.com")
    print(id_from_string)

    string_from_id = id_gen.parse(str(id_from_string))
    