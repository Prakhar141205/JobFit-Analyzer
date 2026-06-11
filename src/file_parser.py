import pymupdf

def pdf_file_parser(pdf_file_path):
    try:
        content = ""
        doc = pymupdf.open(stream=pdf_file_path.read(), filetype="pdf")
        for page in doc:
            content += page.get_text()
            content += "\n"
        return content
    except Exception as e:
        raise FileNotFoundError("File not found")
