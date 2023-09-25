import streamlit as st
from PyMovieDb import IMDB
import json
import os
import pandas as pd
import urllib.request
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

#############################################################################################
#Output the movie metadata from IMDB;
#############################################################################################

#Output the movie metadata from IMDB;
def imdbmetadata(name, id):
    imdb = IMDB()
    if id == None or id == '':
        res = imdb.get_by_name(name)
    else:
        res = imdb.get_by_id(id)
    print(res)
    #convert string to json:
    data = json.loads(res)
    #extract the specfic value from json with key:
    try:
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
        msg = 'Success!'
    except:
        title = ''
        cover = ''
        descr = ''
        year = ''
        director = ''
        actor = ''
        msg = 'No Result Found! please try Movie ID or choose different VPN.'
    return title, cover, descr, year, director, actor, msg

############################################################################################
#Update the movie metadata of the file;
############################################################################################

def updatemetadata(file_path, filename, title, director, year, descr, actors, cover):

    new_title = title.replace(":", "：")
    img_file= file_path +"/" + new_title +'.jpg'
    new_filename = file_path +"/" + new_title + " (" + year + ")" + '.mp4'

    media_file = MP4(filename)
    #1. write the movie title
    if title == None:
        media_file["\xa9nam"] = " "
    else:
        media_file['\xa9nam'] = title
    
    #2. write the year
    if year == None:
        media_file["\xa9day"] = " "
    else:
        media_file['\xa9day'] = year
    
    #3. write the artists
    if actors == None:
        media_file["\xa9ART"] = " "
    else:
        media_file['\xa9ART'] = actors
    
    #4. write the director
    if director == None:
        media_file["\xa9wrt"] = " "
    else:
        media_file["\xa9wrt"] = director
    
    #5. write the description
    if descr == None:
        media_file["desc"] = " "
    else:
        media_file["desc"] = descr

    #6. write the cover art
    #6.1 download the cover art

    urllib.request.urlretrieve(cover, img_file)

    with open(img_file, "rb") as f:
        media_file["covr"] = [
            MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
        ]

    media_file.save()

    #7. rename the filename
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


def main():
    st.title("Easy App for Video Metadata")

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
            filename2 = st.text_input("Movie Name")
            movieid = st.text_input("IMDB ID")
            col1, col2, col3, col4 = st.columns([1,1,2,2])
            with col1:
                info_button = st.form_submit_button('Submit')
            with col2:
                update_button = st.form_submit_button('Update')

            if info_button:
                with st.expander("Movie Information"):
                    title, cover, descr, year, director, actor, msg = imdbmetadata(filename2, movieid)
                    if msg == 'Success!':
                        df = pd.DataFrame(
                            [
                                {"Title": title, "Year": year, "Description": descr, "Director": director, "Actor": actor}
                            ])
                        df = df.T
                        st.dataframe(df, use_container_width=True)
                        st.image(cover, width=400, caption=title)
                    else:
                        st.text(msg)
            
            if update_button:
                title, cover, descr, year, director, actor, msg = imdbmetadata(filename2, movieid)
                old_filename = file_path +"/" + path_str
                #Update the metadata of the mp4 file
                updatemetadata(file_path, old_filename, title, director, year, descr, actor, cover)
                #reload the page
                


if __name__ == '__main__':
    main()