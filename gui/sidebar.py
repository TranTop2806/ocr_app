import os
import streamlit as st
import json

class Sidebar:
    def __init__(self, memory_dir, ui_event):
        """
        Initialize the Sidebar class.

        Args:
            memory_dir (str): Path to the directory containing folders to display.
        """
        self.memory_dir = memory_dir
        self.new_folder_name = None  
        self.ui_event = ui_event

    def inject_css(self):
        """
        Inject custom CSS for styling the sidebar items.
        """
        st.markdown(
            """
            <style>
            .folder-item {
                display: flex;
                align-items: center;
                justify-content: flex-start;
                width: 100%; /* Ensure equal width */
                height: 40px; /* Equal height for all items */
                padding: 0 10px;
                margin-bottom: 5px;
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                overflow: hidden; /* Hide overflow text */
                text-overflow: ellipsis; /* Add ellipsis for overflow */
                white-space: nowrap;
            }
            .folder-item:hover {
                background-color: #e0e0e0; /* Change color on hover */
                cursor: pointer;
            }
            .new-folder-input {
                width: 100%;
                margin-bottom: 10px;
            }
            .stButton>button {
                width: 100%;
                text-align: left; /* Ensure button content is left-aligned */
                justify-content: left; /* Also left align the button content */

            }
            .stButton>button span {
            text-align: left !important; /* Left-align the text within the button */
                display: block; /* Ensure full text width*/
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
    def reload_folder(self):
        st.session_state["folders"] = self.ui_event.get_chat_names()
        return st.session_state["folders"]

    def render(self):
        """
        Render the Sidebar component to display a list of folders as styled list items with button functionality.
        Folders are now ordered by creation time (newest to oldest).
        """
        self.inject_css()  # Ensure CSS is injected

        st.sidebar.title("Manage Directories")
        # st.sidebar.header("ð Folder Structure")

        # New Folder Input & Button
        with st.sidebar.expander("📁 New Folder", expanded=False):
            folder_name = st.text_input("Enter folder name:", key="new_folder_input",
                                                placeholder="My Folder Name",
                                                label_visibility="collapsed",
                                                )

            if st.button("Create", key="create_button_newfolder"):
                if folder_name:
                    folder_id = self.ui_event.create_chat(folder_name)
                    st.session_state["selected_folder"] = folder_id
                    self.reload_folder()
                    st.rerun()
                else:
                    st.error("Vui lòng nhập tên thư mục trước khi tạo.")


        st.sidebar.markdown("---")

        for id, folder_name in reversed(list(st.session_state["folders"].items())):
            folder_path = os.path.join(self.memory_dir, id)

            if os.path.isdir(folder_path):
                if st.sidebar.button(folder_name, key=f"folder_{id}"):
                    st.session_state["selected_folder"] = id
                    st.rerun()
# Example usage:
# sidebar = Sidebar("path/to/memory_dir")
# sidebar.render()
