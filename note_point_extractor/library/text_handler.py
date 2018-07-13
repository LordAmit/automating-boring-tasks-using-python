from typing import List

corestring = """Extracted Annotations (7/13/2018, 9:14:41 PM)
sample notes extracted from PDF
#g asd asd asd g#
#b  asd asd
asd b#
#p asd asd asd p#
#i asd asd asd i#
#g asd asd asd g#
#b asd asd asd b#
#p asd asd
 asd p#

"""

tag_pairs = {"#b": "b#", "#g": "g#", "#p": "p#", "#c": "c#"}


def __count_tags(text: str, tag_start: str, tag_end: str) -> int:
    return text.count(tag_start) + text.count(tag_end)


def __count_all_tags(text: str) -> int:
    return __count_tags(text, "#g", "g#") + __count_tags(text, "#b", "b#") + \
        __count_tags(text, "#p", "p#") + __count_tags(text, "#c", "c#")


def __find_tag(text: str):
    if list(tag_pairs)[0] in text:
        return list(tag_pairs)[0]
    if list(tag_pairs)[1] in text:
        return list(tag_pairs)[1]
    if list(tag_pairs)[2] in text:
        return list(tag_pairs)[2]
    if list(tag_pairs)[3] in text:
        return list(tag_pairs)[3]


# all_lines: List[str] = corestring.splitlines()

# good_points: List[str] = []
# bad_points: List[str] = []
# comments: List[str] = []
# i_points: List[str] = []
# all_comments = {"b#": bad_points, "g#": good_points,
#                 "c#": comments, "p#": i_points}

# flag = False
# end_tag: str = ""
# for line in all_lines:
#     if list(tag_pairs)[0] in line or list(tag_pairs)[1] in line or \
#             list(tag_pairs)[2] in line or list(tag_pairs)[3] in line:
#         flag = True
#         end_tag = tag_pairs[__find_tag(line)]
#     if flag:
#         all_comments[end_tag].append(line)
#     if end_tag in line:
#         flag = False


def __beautify_output_lines(lines: List[str], tag_type: str, start_tag: str,
                            markdown: bool = False)->str:
    print(len(lines))
    if len(lines) < 1:
        print("no lines found, exiting")
        return ""
    combined_line: str = tag_type.upper()
    if markdown:
        combined_line = "# " + combined_line
    combined_line += "\n"
    for line in lines:
        line = line.replace(start_tag, "")
        line = line.replace(tag_pairs[start_tag], "")
        line = line.strip()
        if markdown:
            combined_line += "- " + line + "\n"
        else:
            combined_line += line + "\n"
    return combined_line


def process_content(value: str, markdown: bool=False)->str:
    global tag_pairs
    tag_count = __count_all_tags(value)
    if tag_count % 2 is not 0:
        return("problem with tags. total tags: "+str(tag_count))

    all_lines: List[str] = value.splitlines()
    good_points: List[str] = []
    bad_points: List[str] = []
    comments: List[str] = []
    i_points: List[str] = []
    all_comments = {"b#": bad_points, "g#": good_points,
                    "c#": comments, "p#": i_points}
    flag = False
    end_tag: str = ""
    for line in all_lines:
        if list(tag_pairs)[0] in line or list(tag_pairs)[1] in line or \
                list(tag_pairs)[2] in line or list(tag_pairs)[3] in line:
            flag = True
            end_tag = tag_pairs[__find_tag(line)]
        if flag:
            all_comments[end_tag].append(line)
        if end_tag in line:
            flag = False
    full_content: str = __beautify_output_lines(
        good_points, "Good Points", "#g", markdown) + "\n"
    full_content += __beautify_output_lines(bad_points,
                                            "Bad Points",
                                            "#b", markdown) + "\n"
    full_content += __beautify_output_lines(comments,
                                            "Comments", "#c", markdown) + "\n"
    full_content += __beautify_output_lines(i_points,
                                            "Intersting Points",
                                            "#p", markdown) + "\n"
    return full_content
