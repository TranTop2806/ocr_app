import streamlit as st
import os
import json
import PyPDF2
import time
import base64
from gui.sidebar import Sidebar
from event.ui_event import UIEvent, Chat
from event.app import App, AppRequest, Listener
import threading

# struct session 
# - folder_id

class OCRApp:
    def __init__(self, worker):
        self.memory_dir = "memories"
        self.map_file = os.path.join(self.memory_dir, "map.json")
        self.session_map = {}
        self.worker = worker

        self.sidebar = Sidebar(self.memory_dir)
        self.ui_event = UIEvent(self.memory_dir)
        print("RESTART APP")
        print("Current session state: ", st.session_state)
        if "selected_folder" in st.session_state:
            self.chat = Chat(st.session_state["selected_folder"], self.memory_dir)
            self.folder_path = os.path.join(self.memory_dir, st.session_state["selected_folder"])
        

    def init_app(self):
        # get data from memory
        if "folders" not in st.session_state:
            st.session_state["folders"] = self.ui_event.get_chat_names()
        st.set_page_config(page_title="PDF OCR App", layout="wide")

    def reload_folder(self):
        st.session_state["folders"] = self.ui_event.get_chat_names()
        return st.session_state["folders"]

    def ensure_memory_dir(self):
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)

    def load_session_map(self):
        if os.path.exists(self.map_file):
            with open(self.map_file, "r", encoding="utf-8") as f:
                self.session_map = json.load(f)

    def save_session_map(self):
        with open(self.map_file, "w", encoding="utf-8") as f:
            json.dump(self.session_map, f, ensure_ascii=False, indent=4)

    def display_sidebar(self):
        with st.sidebar:
            st.header("📂 Folder Structure")

            for id, folder_name in st.session_state["folders"].items():
                print(id, folder_name)
                folder_path = os.path.join(self.memory_dir, folder_name)
                if os.path.isdir(folder_path):
                    if st.button(folder_name, key=f"folder_{folder_name}"):
                        st.session_state["selected_folder"] = folder_name

            st.sidebar.markdown("---")

            if st.button("➕ New Folder", key="new_folder_button"):
                st.session_state["new_folder"] = True

            if st.button("⚙️ Settings", key="settings_button"):
                st.session_state["settings_open"] = True
    
    def preview_file(self, file_name, file_path):
            st.markdown(f"### File: {file_name}")
            st.markdown(self.display_pdf(file_path), unsafe_allow_html=True)

    def display_pdf(self, file_path):
        with open(file_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
        return pdf_display

    def new_folder_interface(self):
        st.header("New Folder")
        folder_name = st.text_input("Folder Name", key="folder_name")

        if st.button("Create Folder", key="create_folder_button"):
            if folder_name:
                folder_path = os.path.join(self.memory_dir, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                self.session_map[folder_name] = folder_name
                self.save_session_map()

                st.session_state["selected_folder"] = folder_name
                st.session_state["new_folder"] = False
                st.success("Folder created successfully!")
                st.rerun()
            else:
                st.error("Please provide a folder name.")

    def folder_work_interface(self, folder_path):
        st.header("Working in Directory")
        tabs = st.tabs(["File Management", "Preview", "OCR Results"])

        # Tab 1: File Management
        with tabs[0]:
            st.subheader("File Management")                
            uploaded_pdf = st.file_uploader("Choose a PDF file to upload", type="pdf", key="pdf_uploader")
            if uploaded_pdf:
                try:
                    self.chat.add_pdf(uploaded_pdf)
                    st.success(f"{uploaded_pdf.name} added successfully!")
                    # Clear the uploaded file
                    uploaded_pdf = None
                except Exception as e:
                    st.error(f"Error Upload file: {e}")


            map_file = self.chat.get_pdf_names()
            if map_file == {}: 
                st.info("No PDF files found in the selected directory.")
            else: 
                for id, file in map_file.items():
                    col1_1, col1_2, col1_3 = st.columns([3, 1, 1])
                    
                    with col1_1:
                        file_path = os.path.join(folder_path, id)
                        st.write(f"**{file}**")
                        is_ocred = len(os.listdir(os.path.join(file_path, "ocr"))) > 0
                    
                    with col1_2:
                        if st.button("Delete", key=f"delete_{id}"):
                            try:
                                self.chat.remove_pdf(id)
                                st.success(f"File {file} removed successfully.")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        
                            st.rerun()

                    with col1_3:
                        if is_ocred:
                            # button green and block click
                            st.button("OCR Completed", key=f"ocr_completed_{id}", disabled=True, help="OCR has been completed for this file.")
                        
                        elif "is_ocr" not in st.session_state:
                            if st.button("OCR", key=f"ocr_{id}"):
                                st.session_state["is_ocr"] = True
                                st.rerun()
                                # with st.container():
                                #     st.subheader(f"OCR Options for {file}")
                                #     ocr_option = st.radio("Select OCR Type", ["Hán", "Nôm"], key=f"ocr_option_{id}")
                                #     if st.button("Start OCR", key=f"start_ocr_{id}"):
                                #         with st.spinner("Running OCR..."):
                                #             time.sleep(2)  # Simulate OCR process
                                #             st.success(f"OCR completed for {file} with option {ocr_option}.")

                        
                        else:
                            
                            pdf_path = os.path.join(folder_path, id , "pdf", "file.pdf")
                            
                        
        # Tab 2: Preview
        with tabs[1]:
            files = []
            print("Current folder: ", st.session_state["selected_folder"])
            for file_id , file_name in reversed(self.chat.get_pdf_names().items()):
                files.append(file_name)
            selected_file = st.selectbox("Select a file to preview", files, key=f"preview_select {time.time()}")
            if selected_file:
                file_path = self.chat.get_pdf_path(self.chat.id_by_name(selected_file))
                st.markdown(self.display_pdf(file_path), unsafe_allow_html=True)

        # Tab 3: OCR Results
        with tabs[2]:
            st.subheader("OCR Results")
            
            # Lấy danh sách file từ chat
            files = []
            print("Current folder: ", st.session_state["selected_folder"])
            files_ids = self.chat.get_files_ids()
            for file_id, file_name in reversed(self.chat.get_pdf_names().items()):
                files.append(file_name)
            
            # Chọn file từ danh sách
            selected_file = st.selectbox("Select a file to preview", files, key="preview_select")
            
            if selected_file:
                file_id = self.chat.id_by_name(selected_file)
                file_folder_path = os.path.join(self.memory_dir, st.session_state["selected_folder"], file_id)
                text_dir = os.path.join(file_folder_path, "txt")
                ocr_dir = os.path.join(file_folder_path, "ocr")
                
                # Lấy danh sách hình ảnh OCR và file văn bản
                ocr_images = sorted([os.path.join(ocr_dir, f) for f in os.listdir(ocr_dir) if f.endswith(".png")])
                text_files = sorted([os.path.join(text_dir, f) for f in os.listdir(text_dir) if f.endswith(".txt")])
                
                if ocr_images and text_files:
                    st.header(f"Results for {selected_file}")
                    for idx, (img_path, txt_path) in enumerate(zip(ocr_images, text_files)):
                        with open(txt_path, "r", encoding="utf-8") as f:
                            text_content = f.read()

                        # Tách phần chữ Hán và Việt
                        try:
                            nom_text, vi_text = text_content.split("\n\n")
                        except ValueError:
                            st.error(f"File {txt_path} không đúng định dạng Hán-Việt. Kiểm tra lại nội dung.")
                            continue

                        han_lines = nom_text.splitlines()
                        viet_lines = vi_text.splitlines()

                        # Nếu số dòng không khớp, chỉ lấy phần chung
                        min_length = min(len(han_lines), len(viet_lines))
                        combined_text = "\n".join(
                            f"{han_lines[i]}\n{viet_lines[i]}" for i in range(min_length)
                        )

                        st.subheader(f"Page: {os.path.basename(img_path).replace('.png', '')}")
                        cols = st.columns([1, 2])

                        with cols[0]:
                            st.image(img_path, caption="OCR Image", use_container_width=True)

                        with cols[1]:
                            st.text_area("Hán-Việt Combined Text", combined_text, height=410, max_chars=None, key=f"combined_text_{idx}")
                else:
                    st.warning("No OCR images or text files found in the selected directory.")
            else:
                st.info("Please select a file to preview OCR results.")


    def preview_pdf(self, file_path):
        st.subheader(f"Preview: {os.path.basename(file_path)}")
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            for i in range(min(3, num_pages)):
                page = reader.pages[i]
                st.write(f"Page {i+1}: {page.extract_text()}")


    def render_home(self):
        st.title("📄 PDF OCR Application")
        st.write("""
        Chào mừng bạn đến với **PDF OCR App** – ứng dụng giúp bạn quản lý và xử lý tài liệu PDF bằng OCR.
        
        - **📂 Quản lý thư mục và tệp PDF**  
        - **🔍 OCR (Trích xuất văn bản từ PDF)**  
        - **🛠️ Cấu hình OCR linh hoạt**  
        """)

        st.info("Hãy tạo hoặc chọn một thư mục để bắt đầu làm việc.")
        
        # Nút tạo thư mục mới
        st.header("➕ Tạo Thư Mục Mới")
        folder_name = st.text_input("Nhập tên thư mục:", key="new_folder_name")
        if st.button("Tạo Thư Mục"):
            if folder_name:
                folder_id = self.ui_event.create_chat(folder_name)
                st.session_state["selected_folder"] = folder_id
                self.reload_folder()
                st.rerun()
            else:
                st.error("Vui lòng nhập tên thư mục trước khi tạo.")



    def run(self):
        self.init_app()
        self.ensure_memory_dir()
        self.load_session_map() 

        self.sidebar.render()

        if st.session_state.get("new_folder", False):
            self.new_folder_interface()
        else:
            selected_folder = st.session_state.get("selected_folder", None)
            if selected_folder:
                folder_path = os.path.join(self.memory_dir, selected_folder)
                self.folder_work_interface(folder_path)
            else:
                self.render_home()

        st.write("\n---")   
        st.write("**PDF OCR App** - Developed with Streamlit")

if __name__ == "__main__":
    if "worker" not in st.session_state:
        worker = App()

    app = OCRApp(worker=worker)
    app.run()

    
