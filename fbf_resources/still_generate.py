# This is meant to be run in the main directory

# If looking to just make a couple of folders, alter the characters and moves text files

import os.path 
from os import path

from PIL import Image

from PIL import GifImagePlugin


with open('fbf_resources/characterstxt') as file:
    name_array = file.read().splitlines()

with open('fbf_resources/moves.txt') as f:
    move_array = f.read().splitlines()


base_input_path = "/home/mitchhit234/git/meleeWebProject/static/gifs/"
base_output_path = "/home/mitchhit234/git/meleeWebProject/static/gif_stills/"

for name in name_array:

    for move in move_array:

        full_input_path = base_input_path + name + "/" + move + ".gif"

        #remove mario and dr mario neutral b gifs since they technically are pngs
        if os.path.isfile(full_input_path):
            
            imageObject = Image.open(full_input_path)  

            total_frames = imageObject.n_frames

            output_dir = name + "/" + move + "/"

            for frame in range(0, total_frames):
        
                imageObject.seek(frame)

                img_name = str(frame) + ".png"

                full_output_path = base_output_path + output_dir + img_name

                imageObject.save(full_output_path, 'PNG')

            print(name + " " + move + " saved ")




