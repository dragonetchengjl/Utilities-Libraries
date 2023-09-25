from mutagen.mp4 import MP4, MP4Cover

#
def addCover(filename, cover):
    audio = MP4(filename)
    data = open(cover, 'rb').read()
    covr = []
    if cover.endswith('png'):
        covr.append(MP4Cover(data, MP4Cover.FORMAT_PNG))
    else:
        covr.append(MP4Cover(data, MP4Cover.FORMAT_JPEG))
    audio['covr'] = covr
    audio.save()
    print(filename + " Cover Art：" + cover + "。")


# File_url = r'C:\Media\2023\Scream VI (2023).mp4'
# img_url = r'C:\Users\imac\Pictures\Saved Pictures\Scream VI - March 10.jpg'
# addCover(File_url, img_url)
