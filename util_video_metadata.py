import os
import sys
import mimetypes
import exifread
import mutagen.mp3
from PyMovieDb import IMDB
import json

#Scan video files with in the folder;
def scanVideo(path, format):
    input_extension = format
    video_files = list(filter(lambda a : a.endswith(input_extension), os.listdir(path)))
    video_files.sort()
    return video_files

# files = scanVideo('C:/Downloads', '.mp4')
# print(files)

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
    director = data['director']
    actors = data['actor']
    actor_list = [a.get('name') for a in actors]
    actor = ', '.join(actor_list)
    return title, cover, descr, year, director, actor

#Download the cover art from URL;

#Edit the Video File Metadata with IMDB inputs;