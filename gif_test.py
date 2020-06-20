# Reading an animated GIF file using Python Image Processing Library - Pillow

from PIL import Image

from PIL import GifImagePlugin

 

imageObject = Image.open("ball-1.gif")

print(imageObject.is_animated)

print(imageObject.n_frames)

cont = True
frame = 0
images = []

# Display individual frames from the loaded animated GIF file

for frame in range(0,imageObject.n_frames):
    
    imageObject.seek(frame)
    imageObject.show()
    print(imageObject.tell())
    dummy = input("press enter for next frame")



