# import module
import cv2
import datetime
import os
import json

import threading
"""
def hello():
    print("hello, world")

t = threading.Timer(5.0, hello)
t.start()
"""


"""
path_split = '/Users/alexiaharivel/Desktop/DB/video_split/'
path_keyframe = '/Users/alexiaharivel/Desktop/DB/keyframe/'

for dir in os.listdir(path_split) : 
    n_split = len(os.listdir(path_split  + dir))
    n_keyframe = len(os.listdir(path_keyframe + dir))
    if abs(n_split - n_keyframe) > 1 : 
        print(dir)
        print(f"nb split: {n_split}")
        print(f"n keyframe: {n_keyframe}")
        print("----") """


#### FRAME VIDEOO 39 ET 44
"""
for file in os.listdir(path) :
    name, extension = os.path.splitext(file)
    print(name)
    os.makedirs(path + name, exist_ok=True)

    cap = cv2.VideoCapture(path + file)


    cap = cv2.VideoCapture('/Users/alexiaharivel/Desktop/DB/video_split/video_split_00039/' + file)
    count = 0
    num = cap.get(cv2.CAP_PROP_FRAME_COUNT) // 2
    print( cap.get(cv2.CAP_PROP_FRAME_COUNT) // 2)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        #cv2.imwrite("frame%d.jpg" % ret, frame)     # save frame as JPEG file
        count +=1

        if count == num : 
            os.chdir(path + name)
            cv2.imwrite('frame%d.jpg'%count, frame) 
            print('save')
            os.chdir(path)
        
            break

    print(count)


"""

def name_scene_to_num_scene(l) : 
    n = len(l)
    if n == 11 :
        num_scene = "00" + l[6]
    elif n == 12 : 
        num_scene = "0" + l[6:8]
    else : 
        num_scene = l[8:11]
    return num_scene

#### AJOUTER LES TIMING DANS BDD

path = '/Users/alexiaharivel/Desktop/DB/video_split/'


l = []
dix = []

for i in range(1, 101) : 
    if i < 10 : 
        l.append("0000"+str(i))
    elif i < 100 : 
        l.append("000"+str(i))
    else :
        l.append("00"+str(i))
print(l)
"""
    dct_yolo = {}
    for path_video in tqdm(os.listdir()):
        dct_yolo[path_video]={}
        for path_scene in os.listdir(path_video):
            dct_yolo[path_video][path_scene]={}
            for path_key_frame in os.listdir(path_video+"\\"+path_scene):
                im = cv.imread(path_video+"\\"+path_scene+"\\"+path_key_frame)
                results = model(im)
                plen = len(results.pandas().xyxy[0])
                if plen > 0:
                    idx = 0
                    while idx < plen:
                        conf = results.pandas().xyxy[0]['confidence'][idx]
                        classnum = results.pandas().xyxy[0]['class'][idx]
                        name = results.pandas().xyxy[0]['name'][idx]
                        #print(f'{name},{classnum},{conf}')
                        if conf>0.66:
                            if name not in dct_yolo[path_video][path_scene].keys():
                                dct_yolo[path_video][path_scene][name]=1
                            else:
                                dct_yolo[path_video][path_scene][name]+=1
                        idx = idx + 1
    save_dct_as_json(dct_yolo,"yolo", path_json)
"""
dct = {}


for num in l :
    dct["video_split_"+ str(num)]={}
    print(num)
    nb_split = 0
    duree_somme = 0

    x = 0
    for file in sorted(os.listdir(path + "video_split_" + num + "/")) :
        dct["video_split_"+ str(num)]["video_" + str(x)]={}
        nb_split = nb_split + 1
        data = cv2.VideoCapture(path + "video_split_" + num + "/" + file)
        
        # count the number of frames
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = data.get(cv2.CAP_PROP_FPS)

        # calculate duration of the video
        seconds = frames / fps
        duree_somme = duree_somme + seconds
        #dct_yolo[path_video][path_scene]["beg"]=1
        #dct_yolo[path_video][path_scene]["end"]=1
        x = x +1

    print(f"duration sum in seconds: {duree_somme}")

    data2 = cv2.VideoCapture('/Users/alexiaharivel/Desktop/DB/video/' + num + '.mp4')
    
    # count the number of frames
    frame2 = data2.get(cv2.CAP_PROP_FRAME_COUNT)
    fps2 = data2.get(cv2.CAP_PROP_FPS)
    
    # calculate duration of the video
    duree_init = frame2 / fps2

    print(f"duration in seconds: {duree_init}")
    print(f"nb split: {nb_split}")
    print(f"ratio : {abs(duree_somme - duree_init) / nb_split}")
    print("----")

    #if abs(duree - seconds2) > 5  : 
    #    dix.append(num)

    ratio = abs(duree_somme - duree_init) / (nb_split - 1)

    beg = [0]
    dct["video_split_"+ str(num)]["video_" + str(0)]["beg"]=0
    end = []
    t = 0
    sec = []

    f = sorted(os.listdir(path + "video_split_" + num + "/"))
    n = len(f)
    f =  list(range(0,n))
    f2 = [path + "video_split_" + num + "/video_" + str(x) + ".mp4" for x in f]
    print(len(f2))
    x = 0
    for file in f2 :
        print(file)

        #dct[path_video][path_scene]={}

        data = cv2.VideoCapture(file)
        
        # count the number of frames
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = data.get(cv2.CAP_PROP_FPS)

        # calculate duration of the video
        seconds = frames / fps
        print(seconds)
        t = t + seconds
        sec.append(seconds)
        if t + ratio/2 > duree_init : 
            e = duree_init
            if t - ratio/2 > duree_init : 
                b = (duree_init - seconds)
            else : 
                b = (t - ratio/2)
        else :
            e = (t + ratio/2)
            if t - ratio/2 > duree_init : 
                b = (duree_init - seconds)
            else : 
                b = (t - ratio/2)
        
        if x + 1 < n :
            dct["video_split_"+ str(num)]["video_" + str(x + 1)]["beg"]=round(b)
        
        dct["video_split_"+ str(num)]["video_" + str(x)]["end"]=round(e)
        x = x + 1

    #dct["video_split_"+ str(num)]["video_" + str(x)]["end"]=e
    end.append(duree_init)

    beg = [round(x) for x in beg]
    end = [round(x) for x in end]
    sec = [round(x) for x in sec]
    diff = []


    print(beg)
    print(end)
    print(sec)


    print(dct)


os.chdir("/Users/alexiaharivel/Desktop")
with open("time.json", 'w') as fp:
        json.dump(dct, fp)
#print(dix)
#print(len(dix))
