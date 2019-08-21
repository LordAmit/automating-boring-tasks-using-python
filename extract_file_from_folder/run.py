#!/usr/bin/python3.6


def find_name(line: str):

    line = line.split("ken/")[1].split("/src/")[0]
    if(line.find("/")):
        line = line.split(
            '/')[0].replace("(", "_").replace(")", "_").replace(" ", "")
    return line

def process_line(line: str):
    line = line.replace("file://", "").replace("\n", "")
    name = find_name(line)
    return line, name


search_result_filepath = "/home/amit/.softwares/Moss/basicrobot/BasicRobotKen2"

file = open(search_result_filepath, 'r')

lines = file.readlines()
for line in lines:
    # print(process_line(line))
    print(line)
    cp_address, dir_name = process_line(line)
    new_adress = "/home/amit/.softwares/Moss/basicrobot/{}".format(dir_name)
    print("mkdir " + new_adress)
    print("cp \"{}\" \"{}\"".format(
        cp_address, new_adress+"/BasicRobot.java"))
    # print("cp \"{}\" \"/home/amit/.softwares/Moss/basicrobot/{}_BasicRobot.java\"".format(
    #     process_line(line)[0], process_line(line)[1]))
