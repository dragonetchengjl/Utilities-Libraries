import re
import os
import subprocess
import pdb

def convert(input_file, output_file):
    subprocess.run(f'ffmpeg -i "{input_file}" "{output_file}"', shell=True)

if __name__ == '__main__':
    input_extension = '.rmvb'
    output_extension = '.mp4'
    rmvb_files = list(filter(lambda a : a.endswith(input_extension), os.listdir()))
    rmvb_files.sort()
    for item in rmvb_files:
        output_item = item.replace(input_extension, output_extension)
        print(f'Converting >>> "{item}" >>> "{output_item}"!')
        convert(item, output_item)