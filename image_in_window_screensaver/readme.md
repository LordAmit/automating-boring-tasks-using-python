# No Nonsense Image Viewer/ScreenSaver

No nonsense Image viewer/Screensaver is something I created that

- Can show images in full screen / window mode
- Will scroll through images after a regular, customizable interval
- Will follow some conventions I defined (more coming about that a bit later)
- Help me learn a bit about PySide2
- Allow keyboard based control
- Allows finding the image in file browser
- Delete images

etc.

## Setup

To get started,  start the program with the directory path that contains images. The scenario is like this:

- `<root directory>`
  - landscape
  - portrait

For example:

```sh
/Users/amitseal/git/automating-boring-tasks-using-python/image_in_window_screensaver/venv/bin/python /Users/amitseal/git/automating-boring-tasks-using-python/image_in_window_screensaver/main_window.py --path /Users/amitseal/Pictures/somerandomfolder/
```

So, it is assumed that `somerandomfolder` will contain two directories, landscape and portrait. These directories will include images which are landscape and portrait aligned, respectively. I use [this](https://github.com/LordAmit/automating-boring-tasks-using-python/tree/master/image_sort_landscape_portrait/src) for automatic sorting of images.

So, that's the only step of setup. The acceptable image formats are bmp, png and jpg/jpeg. It is assumed that the image files are with proper extensions. This program will crawl through the folders, will create a list in memory that contains images. You can perform other actions by using keyboard. For example, pressing `p` will toggle slideshow (in current window mode).

## Shortcuts

- `s` = Shuffle images in list
- `Left` or `Backspace` = Previous iamge
- `Right` or `Space` or `n` = Next image
- `Delete` = Send Current Image to Trash
- `f` = Toggle Full screen mode
- `v` = View image in File browser
- `b` = bookmark current image
- `1` = landscape images only
- `2` = portrait images only
- `3` = reset all
- `4` = Go to the 1st Image, in whatever applied sort
- `r` = reverse sort
- `e` = sort by date (new to old)
- `d` = sort by date (old to new)
- `p` = toggle play/pause
- `t` = pomodoro time mode, delay increased to 25 minutes
- `y` = fast mode, delay decreased to 1 second  
- `=` = increase delay by 1 second
- `-` = decrease delay by 1 second
- `+` = increase delay by 10 seconds
- `_` = decrease delay by 10 seconds

That's all folks!
