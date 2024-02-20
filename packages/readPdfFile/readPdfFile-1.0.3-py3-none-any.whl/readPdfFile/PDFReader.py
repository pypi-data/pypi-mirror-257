import fitz


class PDFReader:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.doc = fitz.open(pdf_file)

    def extract_text(self):
        extract_text = ""
        for page_num in range(len(self.doc)):
            page = self.doc.load_page(page_num)
            text = page.get_text()
            extract_text += text
        return extract_text

