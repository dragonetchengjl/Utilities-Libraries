import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages
import os

#############################################################################################
#Scan video files with in the folder;
#############################################################################################

def scanVideo(path, format):
    input_extension = format
    video_files = list(filter(lambda a : a.endswith(input_extension), os.listdir(path)))
    video_files.sort()
    return video_files

#read the path file
with open('path.txt') as f:
    folder_path = f.readlines()
    file_path = folder_path[0]

st.set_page_config(
    page_title = "",
    page_icon = "",
)

folder = st.sidebar.text_input('Choose your destination folder', file_path)
submit_button = st.sidebar.button(label='Submit')

if submit_button:
    if folder == "":
        st.text("Please fill in the destination folder!")
    else:
        f = open("path.txt", "w")
        new_folder = folder.replace('\\', "/")
        f.write(new_folder)
        f.close()

        #step 1: Scan the destination folder and extract the list of the mp4 files
        mp4_files = scanVideo(new_folder, '.mp4')
        #step 2: for each mp4 file create form and load the filename:
        for i in range(len(mp4_files)):
            print(mp4_files)

st.title("Video Manager")


