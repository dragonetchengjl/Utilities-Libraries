import re
import os
import subprocess
import pdb

input_file = r"C:\Media\2005\Batman Begins (2005).mp4"
output_file = r"C:\Media\2005\Batman Begins (2005).jpg"
subprocess.run(f'ffmpeg -i "{input_file}" -map 0:v -map -0:V -c copy "{output_file}"', shell=True)