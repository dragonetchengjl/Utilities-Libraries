import os
import sys
import mimetypes
import exifread
import mutagen.mp3

def extract_metadata(file_path):
    # Get the file type and extension
    file_type, file_ext = mimetypes.guess_type(file_path)
    if file_ext is None:
        file_ext = os.path.splitext(file_path)[1][1:]

    # Handle different file types
    if file_type is not None and file_type.startswith('image'):
        # Extract EXIF metadata from images
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            metadata = {tags.get(key, key): value for key, value in tags.items()}
    elif file_ext.lower() == 'mp3':
        # Extract metadata from MP3 files
        metadata = mutagen.mp3.EasyMP3(file_path).info
    else:
        # Return basic file information for other types of files
        metadata = {
            'filename': os.path.basename(file_path),
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path)
        }

    return metadata

# Example usage
file_path = sys.argv[1] if len(sys.argv) > 1 else 'example.jpg'
metadata = extract_metadata(file_path)
print(metadata)