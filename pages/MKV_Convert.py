import re
import os
import subprocess
import pdb

def convert(input_file, output_file):
    subprocess.run(f'ffmpeg -i "{input_file}" -c copy "{output_file}"', shell=True)

if __name__ == '__main__':

    #read the path file
    with open('path.txt') as f:
        folder_path = f.readlines()
        file_path = folder_path[0]

    input_extension = '.mkv'
    output_extension = '.mp4'
    mkv_files = list(filter(lambda a : a.endswith(input_extension), os.listdir(file_path)))
    mkv_files.sort()
    for item in mkv_files:
        item = file_path +"/" + item
        output_item = item.replace(input_extension, output_extension)
        print(f'Converting >>> "{item}" >>> "{output_item}"!')
        convert(item, output_item)


        
	