from PyPDF2 import PdfFileReader, PdfFileWriter, PdfWriter
from pip import main

def get_pages(input_pdf: PdfFileReader):
    return input_pdf.getNumPages()


def add_pages(input_pdf_path: str, template_pdf_path: str) -> PdfFileWriter:
    writer = PdfFileWriter()
    input_reader = PdfFileReader(input_pdf_path)
    template_reader = PdfFileReader(template_pdf_path)

    for i in range(0, get_pages(input_reader)):
        writer.addPage(input_reader.getPage(i))
        writer.addPage(template_reader.getPage(0))

    return writer

def write_file(input_pdf_path: str, writer: PdfFileWriter):
    with open(input_pdf_path+"merged.pdf", "wb") as out:
        writer.write(out)

def main():
    input_pdf_path = "test.pdf"
    template_pdf_path = "template/cornelllined.pdf"
    write_file(input_pdf_path, add_pages(input_pdf_path, template_pdf_path))

if __name__ == "__main__":
    main()