from .id import IDGenerator
import os
import json
import shutil  # Thêm import này vào đầu file
from PIL import Image, ImageDraw
from .dtype import Message, ApiResponse


class UIEvent:
    def __init__(self, memories = "./memories"):
        self.id_generator = IDGenerator()
        self.memories = memories
        self.map = os.path.join(self.memories, "map.json")

    def create_chat(self, chat_name):
        # Create a folder
        id = self.id_generator.generate()
        chat_path = os.path.join(self.memories, str(id))
        os.makedirs(chat_path)
        # Create new mapping id : file_name in mapping.json
        with open(self.map, "r", encoding="utf-8") as f:
            session_map = json.load(f)
        session_map[str(id)] = chat_name

        with open(self.map, "w", encoding="utf-8") as f:
            json.dump(session_map, f, ensure_ascii=False, indent=4)

        return str(id)
    
    def delete_chat(self, chat_id):
        chat_path = os.path.join(self.memories, chat_id)
        if os.path.isdir(chat_path):
            shutil.rmtree(chat_path)

        with open(self.map, "r", encoding="utf-8") as f:
            session_map = json.load(f)
        del session_map[str(chat_id)]

        with open(self.map, "w", encoding="utf-8") as f:
            json.dump(session_map, f, ensure_ascii=False, indent=4)

        return chat_id
    
    def get_chat_names(self):
        with open(self.map, "r", encoding="utf-8") as f:
            session_map = json.load(f)
        return session_map
    

    
    
    


class Chat:
    def __init__(self, chat_id, memories = "./memories"):
        self.chat_id = chat_id
        self.memories = memories
        self.chat_path = os.path.join(self.memories, chat_id)
        self.map = os.path.join(self.chat_path, "map.json")
        self.id_generator = IDGenerator()

    def get_pdfs_name(self):
        pdfs = [d for d in os.listdir(self.chat_path) if os.path.isdir(os.path.join(self.chat_path, d))]
        return pdfs
    
    def create_new_map(self, pdf_name, id):
        # check map
        if not os.path.exists(self.map):
            with open(self.map, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        with open(self.map, "r", encoding="utf-8") as f:
            session_map = json.load(f)
        session_map[str(id)] = pdf_name

        with open(self.map, "w", encoding="utf-8") as f:
            json.dump(session_map, f, ensure_ascii=False, indent=4)

        return str(id)
    
    def delete_map(self, id):
        with open(self.map, "r", encoding="utf-8") as f:
            session_map = json.load(f)
        del session_map[str(id)]

        with open(self.map, "w", encoding="utf-8") as f:
            json.dump(session_map, f, ensure_ascii=False, indent=4) 
    
    def add_pdf(self, pdf_name):
        id = self.id_generator.generate()
        pdf_path = os.path.join(self.chat_path, str(id))
        os.makedirs(pdf_path)

        # make dir contain ocr results
        ocr_path = os.path.join(pdf_path, "ocr")
        os.makedirs(ocr_path)

        # make dir contain txt files
        txt_path = os.path.join(pdf_path, "txt")
        os.makedirs(txt_path)

        return self.create_new_map(pdf_name, id)
    
    def remove_pdf(self, pdf_id):
        pdf_path = os.path.join(self.chat_path, pdf_id)
        if os.path.isdir(pdf_path):  # Nếu pdf_path là thư mục
            shutil.rmtree(pdf_path)  # Xóa toàn bộ thư mục
        elif os.path.isfile(pdf_path):  # Nếu pdf_path là file
            os.remove(pdf_path)  # Xóa file
        else:
            raise FileNotFoundError(f"The path {pdf_path} does not exist or is not accessible.")
        return self.delete_map(pdf_id)

    def write_txt(self, pdf_id, page_id, han_text, viet_text):
        txt_path = os.path.join(self.chat_path, pdf_id , "txt" , page_id + ".txt")
        # write han_text in the first part
        with open(txt_path, "w", encoding="utf-8") as f:
            for line in han_text:
                f.write(line)
                f.write("\n")
            f.write("\n\n")
            for line in viet_text:
                f.write(line)
                f.write("\n")

        return txt_path
    
    def write_ocr(self, pdf_id, page_id, ocr_text):
        ocr_path = os.path.join(self.chat_path, pdf_id , "ocr" , page_id + ".txt")
        with open(ocr_path, "w", encoding="utf-8") as f:
            f.write(ocr_text)
        return ocr_path
    
    def get_text(self, pdf_id, page_id):
        txt_path = os.path.join(self.chat_path, pdf_id , "txt" , page_id + ".txt")
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        text = text.split("\n\n")  
        han_text = text[0].split("\n")
        for han in han_text:
            if han == "":
                han_text.remove(han)

        nom_text = text[1].split("\n")
        for nom in nom_text:
            if nom == "":
                nom_text.remove(nom)

        return han_text, nom_text
    
    def get_pdf_names(self):
        with open(self.map, "r", encoding="utf-8") as f:
            session_map = json.load(f)
        
        return session_map
        
    def get_page_id_from_path(self, path):
        return path.split("/")[-1].split(".")[0]
    
    def draw_bounding_boxes(self,message : Message, response : ApiResponse, page_id):
        """
        Vẽ bounding boxes trên hình ảnh dựa trên tọa độ bbox.
        """
        if not response.lines or not response.width or not response.height:
            raise Exception("Invalid response")
        image_path = message.request.input_file
        output_path = f"memories/{message.chat_id}/{message.pdf_id}/ocr/{page_id}.png"
        lines = response.lines
        width = response.width
        height = response.height

        image = Image.open(image_path)
        image = image.resize((width, height))
        draw = ImageDraw.Draw(image)

        for line, bbox in lines:
            points = [(x, y) for x, y in bbox]
            points.append(points[0]) 
            draw.line(points, fill="blue", width=2)  

        image.save(output_path)


        

if __name__ == "__main__":
    ui_event = UIEvent()
    # chat_id = ui_event.create_chat("chat1")
    # print(chat_id)

    chat_event = Chat("7b5a83c0-9261-5e2b-9aa1-182fa09ce326")
    # id = chat_event.add_pdf("pdf1")
    # chat_event.remove_pdf("9fa09562-ba2f-5ba5-9d86-0631e38eeded")
    
   
    # han_text = [
    #     "謝休走張養覧率急遂投河而死帝翼隊留王未知盛賞又敢高銘伏於河過亂草之内軍馬四敬去蓬不知帝之",
    #     "所在帝興王伏至四更露冰又下腹中飢餘相抱而哭又泊人知覺吞歸草非之中陳盥王曰此間千百成懿光芒黜耀兄",
    #     "澤沃路於崖二一人以衣相結恕上岸邊藻地荆蘇濕暗之中不見行路正無紊何忽見流聲千百成懿光芒黜耀兄",
    #     "在帝前弼游陳留王日此天助我兄弟也遂圖蠻火而行海漸見路行至五更足痛不能行山處過見一草推帝與"  
    # ]

    # nom_text = [
    #     "tạ hưu tẩu trương dưỡng lẳm suất cấp toại đầu hà nhi tử đế dực đội lưu vương vị tri thịnh thưởng lại dám cao minh phục ở hà qua loạn thảo chi nội quân mã tứ kính khứ bồng bất tri đí chi",
    #     "sở tại đế hưng vương phục chí tứ canh lộ băng hựu hạ phúc trung cơ dư tương bão nhi khóc hựu bạc nhân tri giác thôn quy thảo phi chi trung trần an vương viết thử gian bất khả phụ trừng tua biết", 
    #     "trạch óc lộ ở nhai nhị nhất nhân dĩ y tương kết thứ thượng ngạn biên tảo địa kinh tô thấp ám chi trung bất kiến hành lộ chính vô vặn hà hốt kiến lưu thanh thiên bách thành ý quang mang truất diệu huynh",
    #     "tại đế tiền bật du trần lưu vương nhật thử thiên trợ ngã huynh đệ dã toại đồ man hoả nhi hành hải tiệm kiến lộ hành chí ngũ canh túc thống bất năng hành sơn xứ quá kiến nhứt thảo suy đấy giữa"
    # ]

    # chat_event.write_txt("2845dd8c-7930-4aa6-89cc-7df03b4a2cb1", "page_1", han_text, nom_text)

    # han_text , nom_text = chat_event.get_text("2845dd8c-7930-4aa6-89cc-7df03b4a2cb1", "page_1")
    # print(han_text)
    # print(nom_text)

    pdfs = chat_event.get_pdf_names()
    print(pdfs)

    # chat_names = ui_event.get_chat_names()
    # print(chat_names)