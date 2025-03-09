import mss.tools

def screenshot(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output="output/img.png")
        return(sct_img)