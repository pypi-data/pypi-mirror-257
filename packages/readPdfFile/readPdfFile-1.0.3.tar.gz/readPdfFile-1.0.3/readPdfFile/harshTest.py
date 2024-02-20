import PDFReader as pd

# Specify the path to your pdf file
pdf_file_path = r"D:/python-work/document-reader/document-reader/document/pdf/sample.pdf"

# Instantiate the PDFReader class
pdf_reader = pd.PDFReader(pdf_file_path)

# Extract text from the PDF
extracted_text = pdf_reader.extract_text()
print(extracted_text)
