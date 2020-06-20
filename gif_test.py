# Reading an animated GIF file using Python Image Processing Library - Pillow

from PIL import Image

from PIL import GifImagePlugin

 

imageObject = Image.open("ball-1.gif")

print(imageObject.is_animated)

print(imageObject.n_frames)

cont = True
frame = 0

# Display individual frames from the loaded animated GIF file

#for frame in range(0,imageObject.n_frames):

    #imageObject.seek(frame)

    #imageObject.show() 

while cont == True:

    cont = input("Continue?")

    if cont != "y":
        cont = False
    else:
        cont = True

    imageObject.seek(frame)
    imageObject.show()

    frame += 1

