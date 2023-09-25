from PyMovieDb import IMDB
import json
import os
import pandas as pd
from mutagen.mp4 import MP4, MP4Cover
import urllib.request

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

#Edit the movie metadata of the file;
def updatemetadata(filename, title, director, year, descr, actors, cover):

    new_title = title.replace(":", "：")
    img_file= 'C:/Downloads/'+ new_title +'.jpg'
    new_filename = 'C:/Downloads/' + new_title + " (" + year + ")" + '.mp4'

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

title, cover, descr, year, director, actors, msg = imdbmetadata('Green Book 2018','')

updatemetadata('C:/Downloads/The Green Book： Guide to Freedom (2019).mp4', title, director, year, descr, actors, cover)

print(title)
print(cover)