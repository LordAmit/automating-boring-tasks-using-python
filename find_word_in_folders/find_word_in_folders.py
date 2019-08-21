#!python3
import custom_log as l
if __name__ == '__main__':
    import folder_walk as walk
    import argument_handler as argh
    from typing import List
    l.disable()

    keyword = argh.get_keyword()
    l.log("started parsing directories")
    file_paths = walk.walk()
    is_print_line: bool = argh.get_print_line()
    l.log("will start scanning files now.")
    for file_path in file_paths:
        l.log("at file: "+file_path)
        lines: List[str] = open(file_path).readlines()
        for line in lines:
            if line.find(keyword) != -1:
                print(line.strip())

