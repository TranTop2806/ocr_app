import fitz
import os

def pdf_to_images(pdf_path, output_folder, dpi=200):
    """
    Chuyển đổi các trang PDF thành ảnh PNG và lưu vào thư mục.

    Args:
        pdf_path (str): Đường dẫn đến file PDF.
        output_folder (str): Thư mục lưu ảnh.
        dpi (int): Độ phân giải DPI của ảnh xuất ra.
    """
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    os.makedirs(output_folder, exist_ok=True)

    image_paths = []
    for page_index in range(total_pages):
        page = pdf_document.load_page(page_index)
        pix = page.get_pixmap(dpi=dpi)
        output_file = os.path.join(output_folder, f"page_{page_index + 1}.png")
        pix.save(output_file)
        image_paths.append(output_file)
    pdf_document.close()

    return image_paths  # Trả về danh sách các đường dẫn ảnh
