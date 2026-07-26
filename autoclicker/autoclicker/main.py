import sys
import time

import pyautogui
from pyautogui import Point

times_per_second = 20
delay_between_clicks = 1 / times_per_second

x_offset = 30


def __initial_delay(delay: int):
    time.sleep(delay)
    print("finished delay")


def clicks(click_times: int = 10, delay_before_start: int = 3):
    global delay_between_clicks
    if delay_before_start != 0:
        __initial_delay(delay_before_start)

    start_position: pyautogui.Point = pyautogui.position()
    for i in range(0, click_times):
        pyautogui.click()
        time.sleep(delay_between_clicks)
        current_position: pyautogui.Point = pyautogui.position()
        # print("current position = " + str(current_position))
        # print("start position: " + str(start_position))
        if current_position != start_position:
            print("not equal position")
            break


def click_image_mode(delay_before_start: int = 3):
    __initial_delay(delay_before_start)
    global x_offset
    image_abs_path = '/Users/amitseal/git/' \
                     'automating-boring-tasks-using-python/' \
                     'autoclicker/autoclicker/images/eye.png'

    try:
        print("entering while")
        for i in range(0, 5):
            print("in while")

            print("trying to find image")
            start_x = 79
            end_x = 1346
            start_y = 152
            end_y = 871
            width = end_x - start_x
            height = end_y - start_y
            image_location: Point = pyautogui.locateOnScreen(
                image_abs_path,
                region=(start_x, width, start_y, height),
                confidence=0.6)
            pyautogui.screenshot('img{}.png'.format(str(i)),
                                 region=(
                                     start_x, start_y, width * 2, height * 2))

            print("found image!")
            print(image_location)
            break
            continue
            start_position = Point(image_location.x - x_offset,
                                   image_location.y)
            pyautogui.moveTo(start_position, image_location.y)
            current_position: pyautogui.Point = pyautogui.position()
            time.sleep(delay_between_clicks)
            pyautogui.click()
            if current_position != start_position:
                print("not equal position")
                break
            break
    except pyautogui.ImageNotFoundException:
        print("image not found, break")


def find_current_position():
    __initial_delay(2)
    while True:
        current = pyautogui.position()
        print(current)
        time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(sys.argv)
        # exit()
        clicks(1000, int(sys.argv[1]))
    else:
        clicks(1000, 2)
    # click_image_mode()
    # find_current_position()
