from PIL import ImageGrab

def screenshot(x, y, width, height):
    # bbox = (x, y, x + width, y + height)
    # img = ImageGrab.grab(bbox)
    # save_img(img)
    return ImageGrab.grab((x, y, x + width, y + height))

def save_img(img):
    img.save("output/img.png")