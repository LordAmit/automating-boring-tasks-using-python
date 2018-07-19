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
