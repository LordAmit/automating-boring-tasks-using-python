import pyperclip

def main():
    clip = pyperclip.paste()
    lines = clip.splitlines()
    new_lines = ""
    for line in lines:
        line = line.replace("[00 --> 00]","")
        if "->" in line:
            if "[" in line and "]" in line:
                line = line[25:]
            else:
                continue
        new_lines += line.replace("\n", " ").replace("  ", " ").replace("’", "'") + " "
    print(new_lines)
    pyperclip.copy(new_lines.replace("  ", " "))

if __name__ == "__main__":
    main()