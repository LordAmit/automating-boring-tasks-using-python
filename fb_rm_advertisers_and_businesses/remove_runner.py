import pyautogui
import pyperclip
import logging

logging.basicConfig(
    level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

pyautogui.PAUSE = 0.5
# pyautogui.FAILSAFE = True
numbers = ''
"""
Caution: Experimental Code. Most probably won't work in your machine due to a myriad of unobservable factors. 

basic form of algo - written before implementation; so I kind of wrote based on this - but also deviated from here. But you will get a good idea about how I approached it from here. : 
- run program with delay of 5 seconds,
- visit https://www.facebook.com/ads/preferences/?entry_product=ad_settings_screen
- hover mouse on first advertiser name, but not on close button
- take screenshot of present screen at region selection
- find position of first close button, store this as firstCloseButtonPosition
- Click on it
- Move horizontally to next potential close button using relative close button distance, store increment countRight with index 0
- move mouse horizontally from -2 to 2 to make the close button visible
- take another screenshot at this button position, this time using overapproximation region to make things faster
- if close button is visible, click on it, repeat horizontally
- If countRight is equal to 5, move vertically down from firstCloseButtonPosition
- go for see more procedure
"""

import time
time.sleep(5)

logging.debug('starting')
scroll_value = -4.7


def click_two_rows(firstCloseButtonPosition: tuple) -> tuple:

    for j in range(2):
        logging.debug("clicking at " + str(firstCloseButtonPosition))
        pyautogui.moveTo(firstCloseButtonPosition)
        pyautogui.click(firstCloseButtonPosition)

        for i in range(5):
            logging.debug("i = " + str(i))
            pyautogui.move(120, 0)
            # pyautogui.move(0, -60)
            x, y = pyautogui.position()
            current_position_location = pyautogui.locateOnScreen(
                'close.png',
                region=(x - 100, y - 100, 200, 200),
                grayscale=True)
            current_position = pyautogui.center(current_position_location)
            pyautogui.moveTo(current_position)
            pyautogui.click(current_position)
            logging.debug("clicking at " + str(current_position))

        logging.debug("horiontal done, returning at position: " +
                      str(firstCloseButtonPosition))

        firstCloseButtonPosition = firstCloseButtonPosition[
            0], firstCloseButtonPosition[1] + 204
        logging.debug("vertical adjustment done, returning at position: " +
                      str(firstCloseButtonPosition))
        pyautogui.moveTo(firstCloseButtonPosition)
    return firstCloseButtonPosition


try:
    for i in range(10):
        firstCloseButton = pyautogui.locateOnScreen(
            'close.png', region=(459, 124, 986, 913), grayscale=True)
        firstCloseButtonPosition = pyautogui.center(firstCloseButton)
        firstCloseButtonPosition = click_two_rows(firstCloseButtonPosition)
        logging.debug("looking for seemore button")
        seemore_loc = pyautogui.locateOnScreen(
            'seemore.png', region=(800, 200, 200, 800), grayscale=True)
        seemore_position = pyautogui.center(seemore_loc)
        pyautogui.moveTo(seemore_position)
        pyautogui.click(seemore_position)
        logging.debug("seemore position clicked at : " + str(seemore_position))
        logging.debug(
            "moving back to first position: " + str(firstCloseButtonPosition))
        # input()
        pyautogui.moveTo(firstCloseButtonPosition[0],
                         firstCloseButtonPosition[1] - 204)
        # input()
        pyautogui.move(-70, 0)
        # input()
        pyautogui.scroll(scroll_value)
        logging.debug("scrolled by " + str(scroll_value))

except Exception as e:

    print(e)
