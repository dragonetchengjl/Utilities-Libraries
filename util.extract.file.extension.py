#Get a file's extension using os.path
import os.path
import os
import shutil

def extractFileExtension(file_path):
    root, extension = os.path.splitext(file_path)
    return extension


#Get the list of all files and directories
def getListofFiles(path):
    dir_list = os.listdir(path)
    return dir_list


src_path = r'C:\\Users\\imac\\Downloads\\'
video_path = r'C:\\Media\\'
software_path = r'C:\\Software\\'
media_supported = ['.3g2', '.3gp', '.3gp2', '.3gpp', '.aac', '.ac3', '.adt', '.adts', '.amr', '.asf', '.avi', '.flac', '.m4a', '.m4v', '.mka', '.mkv', '.mov', '.mp3', '.mp4', '.ogg', '.opus', '.wav','.webm','.wma','.wmv']
software_supported = ['.exe','.msi', '.pkg']
# Check whether the specified path exists or not
isExist = os.path.exists(src_path)
listofFiles = getListofFiles(src_path)
#print(isExist)
if isExist == False:
    print('The directory does not exist.')
elif listofFiles == []:
    print('No file is in the specified directory.')
else:
    #extract the extension from each file
    for File in listofFiles:
        source_file = src_path + File
        
        ext = extractFileExtension(File)
        print(ext)
        if ext in media_supported:
            #move file to video_path
            dest_file = video_path  + File
            print(dest_file)
            shutil.move(source_file, dest_file)
            print('Moved to media file:', File)
        elif ext in software_supported:
            #move file to software_path
            dest_file = software_path + File
            print(dest_file)
            shutil.move(source_file, dest_file)
            print('Moved to software file:', File)