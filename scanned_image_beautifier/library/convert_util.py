import shlex
import subprocess
import library.file_handler as file_handler


def convert_sample(input_image_address: str, output_image_address, threshold: int):

    command = "convert -density 600 {} -threshold {}% -type bilevel {}".format(
        input_image_address, threshold, output_image_address)
    command_split = shlex.split(command)
    # print(command_split)
    subprocess.check_output(command_split)
    print("completed sample conversion")


def convert_full_image(input_image_address: str,
                       output_image_address, threshold: int):
    command = "convert -density 600 {} -threshold {}% -type bilevel -compress fax {}".format(
        input_image_address, threshold, output_image_address)
    subprocess.check_output(shlex.split(command))
    print("completed conversion")


def convert_image_to_pdf(input_image_address: str, output_pdf_address: str):
    command = "convert {} {}".format(input_image_address,
                                     output_pdf_address)
    subprocess.check_output(shlex.split(command))
    print("completed saving as pdf")


def convert_pdf_to_image(input_pdf_address: str, output_image_addresss):
    command = "convert -density 600 {} -quality 100 {}".format(
        input_pdf_address, output_image_addresss)
    subprocess.check_output(shlex.split(command))
    print("converted pdf to image")
