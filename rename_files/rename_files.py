from json.tool import main
import os
import custom_log as l
import argument_handler as argh
import file_walker


def rename_files(prefix: str, force_run: bool = False):
    # print(prefix)
    files = file_walker.get_files()
    for i in range(0, len(files)):
        current_filepath = files[i]
        # current_filename = os.path.basename(current_filepath)
        current_path, current_filename = os.path.split(current_filepath)
        old_prefix, extension = os.path.splitext(current_filename)
        # l.log([current_path, current_filename, old_prefix, extension])
        new_filepath = current_path + '/'+prefix + str(i) + extension
        # print("{0} --> {1}".format('a', 'b'))
        print("{0} --> {1}".format(current_filepath, new_filepath))
        if force_run:
            os.rename(current_filepath, new_filepath)
        # new_filename = prefix
        # break


if __name__ == '__main__':
    argh._get_arguments()
    # print(file_walker.walk())
    # print(os.getcwd())
    rename_files(argh.prefix(), argh.force_run())
