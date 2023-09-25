import streamlit as st
from PyMovieDb import IMDB
import json
import os
import pandas as pd
import mutagen
from mutagen.mp4 import MP4, MP4Cover

#define the path of file
file_path = 'C:/Downloads'

#Scan video files with in the folder;
def scanVideo(path, format):
    input_extension = format
    video_files = list(filter(lambda a : a.endswith(input_extension), os.listdir(path)))
    video_files.sort()
    return video_files

#Output the movie metadata from IMDB;
def imdbmetadata(name):
    imdb = IMDB()
    res = imdb.get_by_name(name)
    #convert string to json:
    data = json.loads(res)
    #extract the specfic value from json with key:
    title = data['name']
    cover = data['poster']
    descr = data['description']
    year = data['datePublished'][0:4]
    directors = data['director']
    actors = data['actor']
    actor_list = [a.get('name') for a in actors]
    director_list = [a.get('name') for a in directors]
    actor = ', '.join(actor_list)
    director = ', '.join(director_list)
    return title, cover, descr, year, director, actor

#Edit the movie metadata of the file;
def editmetadata(filename, title, director, year, descr, actors, cover):
    with open(filename, 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        print('before:', media_file.pprint(), end='\n\n')
        media_file['title'] = title
        media_file['year'] = year
        media_file['description'] = descr
        media_file['composer'] = director
        media_file['artist'] = actors
        media_file.save(file)

    #change cover art of the mp4
    audio = MP4(filename)
    data = open(cover, 'rb').read()
    covr = []
    covr.append(MP4Cover(data, MP4Cover.FORMAT_JPEG))
    audio['covr'] = covr
    audio.save()

def main():
    st.title("Easy App for Video CoverArt")

    #subtitle
    st.subheader("Display Video Scan")

    #step 1: Scan the destination folder and extract the list of the mp4 files
    mp4_files = scanVideo(file_path, '.mp4')

    #step 2: for each mp4 file create form and load the filename:
    for i in range(len(mp4_files)):
        #Context Manager
        path_str = mp4_files[i]
        filename = os.path.splitext(os.path.basename(path_str))[0]
        with st.form(key=f"form_{i}"):
            col1, col2, col3, col4 = st.columns([2,2,1,1])
            with col1:
                filename1 = st.text_input("File Name", filename)
            with col2:
                filename2 = st.text_input("Movie Name")
            with col3:
                st.text("")
                st.text("")
                submit_button = st.form_submit_button(label='Submit')
            with col4:
                st.text("")
                st.text("")
                Edit_button = st.form_submit_button(label='Edit')

            if submit_button:
                with st.expander("Movie Information"):
                    title, cover, descr, year, director, actor = imdbmetadata(filename2)
                    df = pd.DataFrame(
                        [
                            {"Title": title, "Year": year, "Description": descr, "Director": director, "Actor": actor}
                        ])
                    df = df.T
                    st.dataframe(df, use_container_width=True)
                    st.image(cover, width=400, caption=title)


if __name__ == '__main__':
    main()