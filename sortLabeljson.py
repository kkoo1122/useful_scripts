import os
import cv2
import sys
import glob
import json
import numpy as np
from IPython import embed

imagesdir = "/media/kevintsai/cef8b40c-14d2-4a8f-a359-9da3eeceb1d4/Projects/Cloud_Factory_Data/Protein/stfr_meatsauce_july_15_2020/images"
labelsdir = "/media/kevintsai/cef8b40c-14d2-4a8f-a359-9da3eeceb1d4/Projects/Cloud_Factory_Data/Protein/stfr_meatsauce_july_15_2020/labels"
showImage = False
sortingFromJson = False



classes = {"None":0, "Double Sealed":0, "Two Trays":0, "Sideways Tray":0, "No Seal":0, "Other Defect":0}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def sortJsonFiles(imagesdir, labelsdir, classes):
    """
    Sorting Images with .json files
    """
    print("Sorting" + "...")
    labels_list = glob.glob(os.path.join(labelsdir, "*.json"))  
    # create classes and each json file's folder  (data feedbach for Cloud Factory)
    for c in classes:    
        try:
            os.mkdir(os.path.join(imagesdir, c))
        except:
            os.system("rm -rf \""+ os.path.join(imagesdir, c)+"\"")
            os.mkdir(os.path.join(imagesdir, c))
            
        for jf in labels_list:
            labelsjson = os.path.basename(jf)
            try:
                os.mkdir(os.path.join(imagesdir, c, labelsjson))
            except:
                os.system("rm -rf \""+ os.path.join(imagesdir, c, labelsjson)+"\"")
                os.mkdir(os.path.join(imagesdir, c, labelsjson))

    # make hard link into each folder
    cnt, labeled = 0, 0     
    for jf in labels_list:               
        with open(jf) as json_file:
            data = json.load(json_file)
        labelsjson = os.path.basename(jf)
        for fn in data:
            if fn[-3:] != "png":
                continue
            else:
                cnt += 1
                filedir = os.path.join(imagesdir, fn)
                if data[fn]:            
                    for c in data[fn]:
                        labeled += 1
                        labeldir = os.path.join(imagesdir, c, labelsjson, fn)     
                        try:
                            os.link(filedir, labeldir)    
                            classes[c] += 1            
                        except:
                            pass
                else:
                    # class None means nothing labeled in defect sorting
                    labeldir = os.path.join(imagesdir, "None", labelsjson, fn)
                    try:
                        os.link(filedir, labeldir)    
                        classes["None"] += 1            
                    except:
                        pass

    # print sorted result
    sys.stdout.write("\033[F") # Cursor up one line
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"{bcolors.HEADER}{bcolors.BOLD}Total images:{bcolors.ENDC}", cnt)
    print(f"{bcolors.HEADER}{bcolors.BOLD}Total labels:{bcolors.ENDC}", labeled)
    for c in classes:
        if c == "None":
            continue
        print(c,":",classes[c])    
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def showLabelWindow(c, filenme, mark=False):
    labeltxt = np.zeros((256,1000,3))
    cv2.namedWindow("label",cv2.WINDOW_NORMAL)
    labeltxt = cv2.putText(labeltxt, "=== "+c+" ===", (40,100), cv2.FONT_HERSHEY_SIMPLEX ,  
                   2, (0,255,255), 3, cv2.LINE_AA)
    if mark:
        labeltxt = cv2.putText(labeltxt, filenme, (150,180), cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (0,0,255), 2, cv2.LINE_AA)           
    else:
        labeltxt = cv2.putText(labeltxt, filenme, (150,180), cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (255,255,255), 2, cv2.LINE_AA)      
    cv2.imshow("label", labeltxt)
    cv2.resizeWindow("label", 512,256)
    cv2.moveWindow("label", 0, 256)


def showResult(imagesdir, labelsdir, classes, showImage=True):
    wrongLabels = []
    if not showImage:
        if os.path.exists(os.path.join(imagesdir,"wronglabel.txt")):
            file1 = open(os.path.join(imagesdir,"wronglabel.txt"),'r')
            for l in file1:
                wrongLabels.append(os.path.basename(l)[:-1])
            file1.close()

    writelist = []
    wrong, total = 0, 0
    
    classes = list(classes.keys())
    key= -1    
    labelfolders = os.listdir(labelsdir)
    for c in classes:
        if c == "None":
            continue
        
        print(f"{bcolors.BOLD}{bcolors.HEADER}===", c, f"==={bcolors.ENDC}")
        #=========================================================================================
        for labelfolder in labelfolders:
            imgsdir = glob.glob(os.path.join(imagesdir, c, labelfolder,"*.png"))
            if not imgsdir:
                continue
            print(f"{bcolors.OKGREEN} >>",labelfolder, f"{bcolors.ENDC}" )            
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>            
            for fn in imgsdir:
                if wrongLabels:
                    if os.path.basename(fn) in wrongLabels:
                        print(f"      {bcolors.FAIL}{bcolors.BOLD}{bcolors.UNDERLINE}",os.path.basename(fn), f"{bcolors.ENDC}")
                    else:
                        print(f"     ",os.path.basename(fn))
                else:
                    print(f"     ",os.path.basename(fn))
                total += 1
                if showImage:
                    showLabelWindow(c, os.path.basename(fn), mark=False)
                    img = cv2.imread(fn)                    
                    cv2.imshow("image",img)
                    cv2.moveWindow("image", 580, 0)
                    key = cv2.waitKey(0)
                    if key == 27:
                        cv2.destroyAllWindows()
                        showImage = False
                        break
                    
                    if key == ord('m'):  #mark as bad sorting
                        key = ord('m')
                        flag = False                       
                        while key == ord('m') or key == ord('r'):
                            if key == ord('m'):
                                if not flag:
                                    writelist.append(fn)
                                    wrong += 1
                                    flag = True
                                sys.stdout.write("\033[F") # Cursor up one line
                                print(f"     {bcolors.FAIL}{bcolors.BOLD}{bcolors.UNDERLINE}",os.path.basename(fn), f"{bcolors.ENDC}")
                                showLabelWindow(c, os.path.basename(fn), mark=True)
                            if key == ord('r'): # reverse back
                                if flag:
                                    writelist.pop()
                                    wrong -= 1
                                    flag = False
                                sys.stdout.write("\033[F") # Cursor up one line
                                print(f"     ",os.path.basename(fn),"  ")
                                showLabelWindow(c, os.path.basename(fn), mark=False)
                            key = cv2.waitKey(0)
                if key == 27:
                    break
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>                
            if key == 27:
                break
        #=========================================================================================            
        if key == 27:
            break
    
    print(f"{bcolors.BOLD} {bcolors.HEADER}",end="")
    if showImage:        
        print()
        print(">>>>>>>>>>>>> Total Wrong Labeled :", wrong, "<<<<<<<<<<<<<")    
        file1 = open(os.path.join(imagesdir,"wronglabel.txt"),"w") 
        for f in writelist:
            file1.write(f+"\n")

                    


if __name__ == "__main__":    
    if sortingFromJson:      
        sortJsonFiles(imagesdir, labelsdir, classes)
    showResult(imagesdir, labelsdir, classes, showImage=showImage)


