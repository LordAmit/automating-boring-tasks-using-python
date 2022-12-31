from sys import argv
from PyPDF2 import PdfMerger, PdfFileReader
import sys
import shutil, os

def add_pages(input_pdf_path: str, template_pdf_path: str):
    input_pdf = open(input_pdf_path, "rb")
    page_count: int = PdfFileReader(input_pdf_path).getNumPages()
    template = open(template_pdf_path, "rb")
    merger = PdfMerger()

    print("original page count: " + str(page_count))
    for i in range(0, page_count):
        print("adding templatr page at "+ str(2 * i + 1))
        merger.append(fileobj=input_pdf, pages=(i, i+1))
        append_index = (2 * i) + 1
        merger.merge(position=append_index, fileobj=template, pages=(0, 1))

    template.close()
    input_pdf.close()
    output_filepath = write_file(input_pdf_path, merger)
    rename_file(input_pdf_path, output_filepath)

def write_file(input_pdf_path: str, merger: PdfMerger)->str:
    output_file_path = input_pdf_path+"merged.pdf"
    with open(output_file_path, "wb") as out:
        merger.write(out)
    merger.close()
    return output_file_path

def rename_file(input_filepath, output_filepath):
    input_filename, ext = os.path.splitext(input_filepath)
    backup_filepath = input_filename+"_backup"+ext
    os.rename(input_filepath, backup_filepath)
    os.rename(output_filepath, input_filepath)

def main():

    print(sys.argv)
    if len(sys.argv) != 3:
        print("Please specify the absolute paths to the input file and template file")
        print("Format: add_comment_page input_pdf_path template_pdf_path ")
        exit()
    input_pdf_path = sys.argv[1]
    template_pdf_path = sys.argv[2]
    add_pages(input_pdf_path, template_pdf_path)

if __name__ == "__main__":
    main()