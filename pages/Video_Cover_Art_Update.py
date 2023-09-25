import streamlit as st
from PyMovieDb import IMDB
import json
import os
import pandas as pd
import urllib.request
import pathlib
from mutagen.mp4 import MP4, MP4Cover

#read the path file
with open('path.txt') as f:
    folder_path = f.readlines()
    file_path = folder_path[0]

#############################################################################################
#Scan video files with in the folder;
#############################################################################################

def scanVideo(path, format):
    input_extension = format
    video_files = list(filter(lambda a : a.endswith(input_extension), os.listdir(path)))
    video_files.sort()
    return video_files


############################################################################################
#Update the movie metadata of the file;
############################################################################################

def updatecoverart(file_path, filename, filename2, img_file):

    media_file = MP4(filename)

    new_filename = file_path +"/" + filename2 + ".mp4"

    #1. write the cover art

    with open(img_file, "rb") as f:
        media_file["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]

    media_file.save()

    #2. rename the filename
    os.rename(filename, new_filename)

############################################################################################
#Update session status with checkbox;
############################################################################################

# callback to update 'test' based on 'check'
def TVCheck():
    if st.session_state["check"]:
        st.session_state.check = True
    else:
        st.session_state.check = False

############################################################################################
#get the image path from uploader;
############################################################################################

def get_image_path(img):
    # Create a directory and save the uploaded image.
    file_path = f"data/uploadedImages/{img.name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as img_file:
        img_file.write(img.getbuffer())
    return file_path


def main():
    st.title("Easy App for Video Cover Art")

    #side bar
    subtitle = st.sidebar.text("Destination Folder: ")
    folder = st.sidebar.text(file_path)
    #submit_button = st.sidebar.button(label='Submit')

    #step 1: Scan the destination folder and extract the list of the mp4 files
    mp4_files = scanVideo(file_path, '.mp4')

    #step 2: for each mp4 file create form and load the filename:
    for i in range(len(mp4_files)):
        path_str = mp4_files[i]
        display_name = os.path.splitext(os.path.basename(path_str))[0]

        with st.form(key=f"form_{i}"):
            
            filename1 = st.text(display_name)
            filename2 = st.text_input("Movie Name", display_name)
            uploaded_file = st.file_uploader("Upload an image:")
            col1, col2, col3, col4 = st.columns([1,1,2,2])
            with col1:
                update_button = st.form_submit_button('Update')
            
            if update_button:
                img_file = get_image_path(uploaded_file)
                st.image(img_file)
                st.text(img_file)
                old_filename = file_path +"/" + path_str

                #Update the metadata of the mp4 file
                updatecoverart(file_path, old_filename, filename2, img_file)
                #reload the page
                

if __name__ == '__main__':
    main()