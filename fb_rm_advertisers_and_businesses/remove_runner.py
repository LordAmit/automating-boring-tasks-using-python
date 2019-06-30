import pyautogui
import pyperclip
import logging

logging.basicConfig(
    level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
"""
There is also an optional region keyword argument, if you do not want a screenshot of the entire screen. You can pass a four-integer tuple of the left, top, width, and height of the region to capture:
>>> im = pyautogui.screenshot(region=(0,0, 300, 400))

These "locate" functions are fairly expensive; they can take a full second to run. The best way to speed them up is to pass a region argument (a 4-integer tuple of (left, top, width, height)) to only search a smaller region of the screen instead of the full screen:
>>> pyautogui.locateOnScreen('someButton.png', region=(0,0, 300, 400))

>>> button7location = pyautogui.locateOnScreen('calc7key.png', grayscale=True)


left = 459, 
top = 124,
width = 986, 
height = 913

left side In [2]: pyautogui.position()                                                     
Out[2]: Point(x=459, y=412) x left

In [3]: pyautogui.position()                                                    
Out[3]: Point(x=1443, y=416) 986 width

In [4]: pyautogui.position()  top panel                                                  
Out[4]: Point(x=466, y=128) height 

In [5]: pyautogui.position()                                                    
Out[5]: Point(x=462, y=125) y top

In [6]: pyautogui.position()   bottom panel                                                  
Out[6]: Point(x=439, y=1037)

Distance between close buttons horizontally 160 

In [7]: pyautogui.position()                                                    
Out[7]: Point(x=605, y=389)

In [8]: pyautogui.position()                                                    
Out[8]: Point(x=765, y=385)

Distance between close buttons vertically 204

In [10]: pyautogui.position()                                                   
Out[10]: Point(x=605, y=448)

In [11]: pyautogui.position()                                                   
Out[11]: Point(x=605, y=652)

close button size region overapproximation: 40, 40
In [20]: pyautogui.position()                                                   
Out[20]: Point(x=591, y=546)

In [21]: pyautogui.position()                                                   
Out[21]: Point(x=620, y=545)


"""

pyautogui.PAUSE = 1
# pyautogui.FAILSAFE = True
numbers = ''
"""

algo: 
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

try:

    firstCloseButton = pyautogui.locateOnScreen(
        'close.png', region=(459, 124, 986, 913), grayscale=True)
    firstCloseButtonPosition = pyautogui.center(firstCloseButton)
    for j in range(2):
        logging.debug("clicking at " + str(firstCloseButtonPosition))
        pyautogui.moveTo(firstCloseButtonPosition)
        # pyautogui.click(firstCloseButtonPosition)
        logging.debug("clicking at: " + str(firstCloseButtonPosition))

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
            # pyautogui.click()
            logging.debug("clicking at " + str(current_position))

        logging.debug("horiontal done, returning at position: " +
                      str(firstCloseButtonPosition))

        firstCloseButtonPosition = firstCloseButtonPosition[
            0], firstCloseButtonPosition[1] + 204
        logging.debug("vertical adjustment done, returning at position: " +
                      str(firstCloseButtonPosition))
        pyautogui.moveTo(firstCloseButtonPosition)
    pyautogui.locateOnScreen('seemore.png')
except Exception as e:

    print(e)
