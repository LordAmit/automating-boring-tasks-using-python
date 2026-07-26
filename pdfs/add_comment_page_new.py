from sys import argv
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfWriter, PdfMerger
from pip import main
import sys


def get_pages(input_pdf: PdfFileReader):
    return input_pdf.getNumPages()


def add_template_page(writer: PdfFileWriter, template_pdf_path):
    pass
    # template_reader: PdfFileReader = PdfFileReader(template_pdf_path)
    # template_page = template_reader.getPage(0)
    # writer.add_page(template_page)


def add_pages(input_pdf_path: str, template_pdf_path: str) -> PdfFileWriter:
    input_pdf = open(input_pdf_path, "rb")
    page_count: int = PdfFileReader(input_pdf_path).getNumPages()
    template = open(template_pdf_path, "rb")
    merger = PdfMerger()

    print("original page count: " + str(page_count))
    for i in range(0, page_count):
        print("adding page at "+ str(2 * i + 1))
        merger.append(fileobj=input_pdf, pages=(i, i+1))
        append_index = (2 * i) + 1
        merger.merge(position=append_index, fileobj=template, pages=(0, 1))

    template.close()
    input_pdf.close()
    write_file(input_pdf_path, merger)

    # writer: PdfFileWriter = PdfFileWriter()
    # input_reader = PdfFileReader(input_pdf_path)

    # for i in range(0, get_pages(input_reader)):
    #     writer.addPage(input_reader.getPage(i))
    #     writer.addPage(template_reader.getPage(0))

    # return writer

# def write_file(input_pdf_path: str, writer: PdfFileWriter):
#     with open(input_pdf_path+"merged.pdf", "wb") as out:
#         writer.write(out)


def write_file(input_pdf_path: str, merger: PdfMerger):
    with open(input_pdf_path+"merged.pdf", "wb") as out:
        merger.write(out)
    merger.close()


def main(input_pdf, template):
    add_pages(input_pdf, template)
    # print(sys.argv)
    # if len(sys.argv) != 3:
    #     print("Please specify the absolute paths to the input file and template file")
    #     print("Format: add_comment_page input_pdf_path template_pdf_path ")
    #     exit()
    # input_pdf_path = sys.argv[1]
    # template_pdf_path = sys.argv[2]
    # write_file(input_pdf_path, add_pages(input_pdf_path, template_pdf_path))


if __name__ == "__main__":
    main("/Users/amitseal/git/automating-boring-tasks-using-python/pdfs/test.pdf", "/Users/amitseal/git/automating-boring-tasks-using-python/pdfs/template/cornelllined.pdf")
