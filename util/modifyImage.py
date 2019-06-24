"""modify image
@author: cjing9017
@date: 2019/05/13
"""

from PIL import Image


class ModifyImage:

    @staticmethod
    def modifySize(infile, width, height):
        image = Image.open(infile)
        new_image = image.resize((width, height), Image.ANTIALIAS)
        new_image.save(infile)
