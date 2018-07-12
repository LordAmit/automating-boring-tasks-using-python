# Scanned Image Beautifier

It is a simple GUI program that acts as a front-end to the legendary tool `convert` from `imagemagick` toolkit. The front-end is built using Python and PyQT4.
You can click on Browse, and then select an image. Next, you need to drag and move the slider to see an preview of the image output. Be aware that even though the preview may seem unclear, because often it is a mere low resolution preview, the end result can still be quite good as output. Also, the grayscale button do not work. And I didn't bother about handling any errors, or help messages. In short, do not bother about using it if you do not know what you are doing. Chances are, you do not, and I do.

Anyway, it is adviced that you scan the images using 600DPI 8 bit grayscale format. The underlying scripts will maintain the DPI, but will convert it to biliear format (i.e. 0 and 1 image); which will decrease it's size. Furthermore, it will compress it using `convert`'s `fax` level compression - thus drastically reducing the size of the image, while maintaing the crisp resolution and clarity. The original of the sample image used below had a resolution of 5054x4030; and size of 14.3MB. The original output image had the same resolution; but only 180KB. So yeah, all hail ImageMagick!



