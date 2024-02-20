import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_file_path):
    """
    Extract text from a PDF file and print it.

    Args:
    pdf_file_path (str): The path to the PDF file.
    """
    # Open the PDF file
    doc = fitz.open(pdf_file_path)

    # Extract text from each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        print(text)
