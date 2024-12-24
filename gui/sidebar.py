import os
import streamlit as st

class Sidebar:
    def __init__(self, memory_dir):
        """
        Initialize the Sidebar class.

        Args:
            memory_dir (str): Path to the directory containing folders to display.
        """
        self.memory_dir = memory_dir

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
                height: 50px; /* Equal height for all items */
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
            </style>
            """,
            unsafe_allow_html=True,
        )

    def render(self):
        """
        Render the Sidebar component to display a list of folders as styled list items with button functionality.
        """
        self.inject_css()  # Ensure CSS is injected

        # Loop through folders in reverse order
        for id, folder_name in reversed(list(st.session_state["folders"].items())):
            folder_path = os.path.join(self.memory_dir, id)

            if os.path.isdir(folder_path):
                if st.sidebar.button(folder_name, key=f"folder_{id}"):
                    st.session_state["selected_folder"] = id
                    st.rerun()

# Example usage:
# sidebar = Sidebar("path/to/memory_dir")
# sidebar.render()
