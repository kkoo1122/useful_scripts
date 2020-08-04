import os
import glob
import json
from IPython import embed

imagesdir = "./cheese5-good"
labelsdir = "./defect_labels"

classes = {"None":0, "Double Sealed":0, "Two Trays":0, "Sideways Tray":0, "No Seal":0, "Other Defect":0}
labels_list = glob.glob(os.path.join(labelsdir, "*.json"))

cnt = 0
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
            cnt += 1
            filedir = os.path.join(imagesdir, fn)
            if data[fn]:            
                for c in data[fn]:
                    labeldir = os.path.join(imagesdir, c, fn)     
                    try:
                        os.link(filedir, labeldir)    
                        classes[c] += 1            
                    except:
                        pass
            else:
                labeldir = os.path.join(imagesdir, "None", fn)
                try:
                    os.link(filedir, labeldir)    
                    classes["None"] += 1            
                except:
                    pass

print("Total images:", cnt)
for c in classes:
    print(c,":",classes[c])




