import streamlit as st
import os
import json
import PyPDF2
import time
import base64
from gui.sidebar import Sidebar
from event.ui_event import UIEvent

# struct session 
# - folder_id


class OCRApp:
    def __init__(self):
        self.memory_dir = "memories"
        self.map_file = os.path.join(self.memory_dir, "map.json")
        self.session_map = {}

        self.sidebar = Sidebar(self.memory_dir)
        self.ui_event = UIEvent(self.memory_dir)
        

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
                pdf_path = os.path.join(folder_path, uploaded_pdf.name)
                with open(pdf_path, "wb") as f:
                    f.write(uploaded_pdf.read())
                st.success(f"{uploaded_pdf.name} added successfully!")


            files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
            for file in files:
                col1_1, col1_2, col1_3 = st.columns([3, 1, 1])
                
                with col1_1:
                    file_path = os.path.join(folder_path, file)
                    st.write(f"**{file}**")
                
                with col1_2:
                    if st.button("Delete", key=f"delete_{file}"):
                        os.remove(file_path)
                        st.rerun()

                with col1_3:
                    if st.button("OCR", key=f"ocr_{file}"):
                        with st.container():
                            st.subheader(f"OCR Options for {file}")
                            ocr_option = st.radio("Select OCR Type", ["Hán", "Nôm"], key=f"ocr_option_{file}")
                            if st.button("Start OCR", key=f"start_ocr_{file}"):
                                with st.spinner("Running OCR..."):
                                    time.sleep(2)  # Simulate OCR process
                                    st.success(f"OCR completed for {file} with option {ocr_option}.")

        with tabs[1]:
            files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
            selected_file = st.selectbox("Select a file to preview", files, key="preview_select")
            if selected_file:
                file_path = os.path.join(folder_path, selected_file)
                st.markdown(self.display_pdf(file_path), unsafe_allow_html=True)

        
        
        # Tab 3: OCR Results
        with tabs[2]:
            st.subheader("OCR Results")
            st.write("OCR results functionality to be implemented.")

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
    app = OCRApp()
    app.run()
