import os
import glob
import json
from IPython import embed

imagesdir = "./cheese5-bad"
labelsdir = "./defect_labels"

classes = {"Double Sealed", "Two Trays", "Sideways Tray", "No Seal", "Other Defect"}
labels_list = glob.glob(os.path.join(labelsdir, "*.json"))

for labelsjson in labels_list:
    with open(labelsjson) as json_file:
        data = json.load(json_file)


    for c in classes:    
        try:
            os.mkdir(os.path.join(imagesdir,c))
        except:
            os.system("rm -rf \""+ os.path.join(imagesdir,c)+"\"")
            os.mkdir(os.path.join(imagesdir,c))

    for fn in data:
        if fn[-3:] != "png":
            continue
        else:
            if data[fn]:
                filedir = os.path.join(imagesdir, fn)
                for c in data[fn]:
                    labeldir = os.path.join(imagesdir, c, fn)     
                    try:
                        os.link(filedir, labeldir)
                    except:
                        pass







