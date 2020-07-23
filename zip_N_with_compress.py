import os
import glob
import numpy as np
import zipfile
import random
import tqdm
from zipfile import ZipFile
from PIL import Image
from IPython import embed




imagesdir = ""

imgs_savedir = ""

filenamehead = ""

img_num_folder = 


#make directory the same as filename head
if not os.path.exists(os.path.join(imgs_savedir, filenamehead)):
    os.system("mkdir " + os.path.join(imgs_savedir, filenamehead))


def resize_compress_save(fn, imgs_savedir, filenamehead):
    """Resize, Compress, Save images """
    image = Image.open(fn)
    image = image.resize((int(image.size[0]/2), int(image.size[1]/2)), Image.ANTIALIAS)
    image.save(os.path.join(imgs_savedir, filenamehead, os.path.basename(fn)), optimize=True, quality=85)

def main():
    filepaths = ["" for _ in range(img_num_folder)]
    folder_cnt, images_cnt = 0, 0
    filename_list = os.listdir(imagesdir)
    random.shuffle(filename_list)

    with tqdm.tqdm(total=len(filename_list)) as progressbar:
        for idx, fn in enumerate(filename_list):        
            filepaths[images_cnt] = os.path.join(imagesdir, fn)
            images_cnt += 1   
            if images_cnt == img_num_folder:
                filepaths.sort()

                zip_name = filenamehead+'_'+str(folder_cnt)+'.zip'
                with ZipFile(os.path.join(imgs_savedir,filenamehead,zip_name), mode='w') as zip:
                    for f in filepaths:
                        resize_compress_save(f, imgs_savedir, filenamehead)                    
                        filename = os.path.basename(f)
                        zip.write(os.path.join(imgs_savedir, filenamehead, filename), filename)
                        progressbar.update(1)
                                            
                print("finish " + zip_name)
                zip.close()
                folder_cnt += 1
                images_cnt = 0
                filepaths = ["" for _ in range(img_num_folder)]  
        
        #final round
        if images_cnt > 0:
            zip_name = filenamehead+'_'+str(folder_cnt)+'.zip'
            with ZipFile(os.path.join(imgs_savedir,filenamehead,zip_name), mode='w') as zip:
                for f in filepaths:
                    if not f:
                        break
                    resize_compress_save(f, imgs_savedir, filenamehead)                    
                    filename = os.path.basename(f)
                    zip.write(os.path.join(imgs_savedir, filenamehead, filename), filename)
                    progressbar.update(1)
                    
            print("finish " + zip_name)
            zip.close()
    #delete all modified .png in the folder
    os.system("rm "+ os.path.join(imgs_savedir, filenamehead, "*.png"))
    
    
main()

