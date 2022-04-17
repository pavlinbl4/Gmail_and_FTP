import time
import psutil
from PIL import Image


file_path = "/Volumes/big4photo-2/My photo 2022/5935_PAVL_6738.JPG"
# open and show image
im = Image.open(file_path)
im.show()

# display image for 10 seconds
time.sleep(3)

# hide image
for proc in psutil.process_iter():
    if proc.name() == "Preview":
        proc.kill()