import pymongo
from pymongo import MongoClient 
import os
import pprint
import json

## change the path here
path = "/Users/alexiaharivel/Desktop/DB"

client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.5.0')

db = client.bdd
scene = db.scene


new_path = path + "/video/"


def name_scene_to_num_scene(l) : 
    n = len(l)
    if n == 7 :
        num_scene = "00" + l[6]
    elif n == 8 : 
        num_scene = "0" + l[6:8]
    else : 
        num_scene = l[6:9]
    return num_scene

## change the path here
with open('/Users/alexiaharivel/Desktop/time.json') as json_data:
        data_dict = json.load(json_data)

        for num_video, value in data_dict.items() : 
            print(num_video)
            if isinstance(value, dict):

                for sub_key, sub_value in value.items():
                    num_scene = name_scene_to_num_scene(sub_key)
                    #print(num_video[12:17],num_scene)
                    beg_end = []
                    for t, nb in sub_value.items() :
                        beg_end.append(nb)
                        
                    #print(keyword_list)
                    #scene.find_one_and_update({"id_scene" : num_scene, "id_video" : num_video[12:17]}, {"$set": {"keyword" : keyword_list}})
                    scene.insert_one({"id_scene" : num_scene, "id_video" : num_video[12:17], "path_video" : path + "/video/"+ num_video[12:17] + ".mp4" ,  "beg" : beg_end[0], "end" : beg_end[1] }  )


            else:
                #print(num_video,value)
                print("")



### Insert every path to the keyfframes to the scenes in the DB
i = 0
new_path = path + "/keyframe/"
for dir in os.listdir(new_path) : 
    num = dir[12:17]
    for subdir in os.listdir(new_path + "/" + dir) :
        i = i +1
        num_scene = name_scene_to_num_scene(subdir)
        nb_keyframe = len(os.listdir(new_path + "/" + dir + "/" + subdir))
        path_photo = "/keyframe/" + dir + "/" + subdir + "/" + sorted(os.listdir(new_path + "/" + dir + "/" + subdir))[nb_keyframe//2]
        scene.find_one_and_update({"id_scene" : num_scene, "id_video" : num}, {"$set": {"path_keyframe" : path_photo}})

print(i)


## Add the prediction to the data base
json_list = ['yolo_B.json', 'inception.json', 'alexNet_B.json', 'yolo_M.json', 'alexNet_M.json']


for json_file in json_list :

    print(json_file)
    ### change the path here
    with open('/Users/alexiaharivel/Desktop/json/' + json_file) as json_data:
        data_dict = json.load(json_data)

        for num_video, value in data_dict.items() : 
            if isinstance(value, dict):

                for sub_key, sub_value in value.items():
                    num_scene = name_scene_to_num_scene(sub_key)
                    keyword_list = []
                    for keyword, nb_keword in sub_value.items() :
                        keyword_list.append(keyword)
                        
                    #print(keyword_list)
                    scene.update_one({"id_scene" : num_scene, "id_video" : num_video[12:17]}, { '$addToSet' : { "keyword" :{ '$each' : keyword_list} } }  )


            else:
                print("")



