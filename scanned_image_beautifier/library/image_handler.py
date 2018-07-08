from PIL import Image

def check_is_image_good_for_thumbnail(img: Image.Image):
    if img.width < 256:
        return True
    return False

def save_thumbnail(img: Image.Image, file_save_address: str) -> Image:

        size = 400, 400
        img.thumbnail(size)
        img.save(file_save_address)

# img = Image.open("/home/amit/git/automating-boring-tasks-using-python/scanned_image_beautifier/test.jpg")
# save_thumbnail(img, "/home/amit/git/automating-boring-tasks-using-python/scanned_image_beautifier/test_thumbnail.jpg")

