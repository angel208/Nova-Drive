from datetime import datetime
from PIL import Image
import hashlib
import io

#checks if request file is image
def check_if_image( file_type ):

    allowed_image_extensions = {'image/png', 'image/jpg', 'image/jpeg', 'image/gif'}
    return file_type in allowed_image_extensions


def create_custom_internal_filename( file_name ):
    datestamp = datetime.today().strftime('%Y%m%d%H%M%S')
    internal_file_name = datestamp + "_" + file_name
    return internal_file_name

# 200x200
def generate_tumbnail( file ):

    pillow_image = Image.open(file)
    pillow_image.thumbnail([100, 100])

    return pillow_image



def get_file_size(fobj):
    if fobj.content_length:
        return fobj.content_length

    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  #seek to end
        size = fobj.tell()
        fobj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

    # in-memory file object that doesn't support seeking or tell
    return 0  #assume small enough


def calculate_md5(file):

    pos = file.tell()

    hash_md5 = hashlib.md5()

    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)

    file.seek(pos)  # back to original position

    return hash_md5.hexdigest()