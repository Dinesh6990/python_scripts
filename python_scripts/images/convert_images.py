from PIL import Image
import os
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import fnmatch

src= 'Source Directory'
dst = 'Destination Directory'

for subdirs, dirs, files in os.walk(src):
    for extension in ('*.jpg', '*.jpeg'):
        for file in (fnmatch.filter(files, extension)):
            f=file.split('.')[0]
            print(f)        
            i = Image.open(os.path.join(subdirs,file))
            rgb_img = i.convert('RGB')
            rgb_img.save(os.path.join(dst,f+'.JPEG'))
            os.chdir(src)
            continue