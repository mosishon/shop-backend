from PIL import Image
from typing import BinaryIO


def is_image(file: BinaryIO):
    try:
        # Open the file as an image
        with Image.open(file) as img:
            # Check if it's a valid image
            img.verify()
            return True
    except Exception as e:
        # If an error occurs or the file is not a valid image
        return False

def is_slug(string:str)->bool:
    return string == string.lower().replace(" ","")