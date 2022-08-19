from importlib.resources import path
from tkinter import *
from tkinter.ttk import *
#from rempli_matrice import *
import datetime
import tkinter.filedialog
import tkinter.messagebox
import math

from matplotlib.pyplot import fill
from matplotlib.transforms import Bbox
from tkvideo import tkvideo
import os
from tkVideoPlayer import TkinterVideo
from PIL import ImageTk
from PIL import Image
#from ttkwidgets.autocomplete import AutocompleteEntry

import pymongo
from pymongo import MongoClient 
import os

import torch

import time
import threading


### CONFIGURATION
root = Tk()
root.title("VIDEO SEARCH CONTENT")
root.geometry("750x500")
root.minsize(650,420)
#fenetre.iconphoto(False, PhotoImage( file = r"C:\Mpmp\SCAN\logo.png"))
s = Style()
s.configure('My.TFrame', background='#a6cf65')

# main frame
main_frame = Frame(root, style='My.TFrame')
main_frame.pack(fill=BOTH, expand = 1)

#canvas 
canvas = Canvas(main_frame)
canvas_left = Canvas(main_frame)

#canvas.grid(row=0, column=0, sticky="nsew")

#scrollbar
scrollbar_x = Scrollbar(main_frame, orient=HORIZONTAL, command=canvas.xview)
#scrollbar_x.grid(row=1, column=0, sticky="ew")
scrollbar_x.pack(side=BOTTOM, fill=X)

scrollbar_y = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
#scrollbar_y.grid(row=0, column=1, sticky="ns")
scrollbar_y.pack(side=RIGHT, fill=Y)

#configure the canvas
canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
canvas.bind("<Configure>", lambda e : canvas.configure(scrollregion = canvas.bbox("all")) )
canvas_left.pack(side = LEFT, fill = Y)
canvas.pack(side = RIGHT, fill = BOTH, expand = 1)



#frame inside the canvas
frame_left = Frame(canvas_left)
frame_right = Frame(canvas)

#add the frame to a window in  the canvas
canvas_left.create_window((0,0), width = 350, window=frame_left, anchor = "nw")
canvas.create_window((350,0), window=frame_right, anchor="nw")




#frame.columnconfigure(0,weight = 432)
#frame.rowconfigure(0,weight = 270 )



#label1 = Label(frame, text="SCAN",background='#a6cf65')
#label1.grid(row = 0, column = 1,sticky = W, pady = 8)

#video = Label(frame)
#video.pack()

#player = tkvideo("/Users/alexiaharivel/Documents/Klagenfurt/Video-Search/web/00001.mp4", video, loop = 1, size = (700, 500))
#player.play()
'''
videoplayer = TkinterVideo(master=fenetre, scaled=True)
print(os.path.exists("/Users/alexiaharivel/Documents/Klagenfurt/Video-Search/web/00001.mp4"))
videoplayer.load(pat)
videoplayer.pack(expand=True, fill="both")
print(os.path.exists("/Users/alexiaharivel/Documents/Klagenfurt/Video-Search/web/00001.mp4"))

videoplayer.play() # play the video '''


# cadre video

im = Image.open("Frame.png")
im1 = im.resize( (350, 1) )
img1 = ImageTk.PhotoImage(im1)
panel1 = Label(frame_left, image = img1)
panel1.image = img1 # keep a reference!
panel1.grid(row = 0 , column =  0, pady = 2)

im2 = im.resize( (1, 219) )
img2 = ImageTk.PhotoImage(im2)
panel2 = Label(frame_left, image = img2)
panel2.image = img2 # keep a reference!
panel2.grid(row = 1 , column =  1, pady = 2)

#autocompleted test
countries = [
        'Antigua and Barbuda', 'Bahamas','Barbados','Belize', 'Canada',
        'Costa Rica ', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador ',
        'Grenada', 'Guatemala ', 'Haiti', 'Honduras ', 'Jamaica', 'Mexico',
        'Nicaragua', 'Saint Kitts and Nevis', 'Panama ', 'Saint Lucia', 
        'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America'
        ]


#left frame
label_keyword = Label(frame_left, text="Keyword : ")
label_keyword.grid(row = 2, column = 0,sticky = "ew", pady = 2)

entry_keyword = Entry(frame_left)
#entry_keyword = AutocompleteEntry(    frame_left,  completevalues=countries )
entry_keyword.grid(row = 3, column = 0, sticky = "ew", pady = 2)

list_entry_keyword = [entry_keyword]

def add_keyword():
    print("oui")
    i = len(list_entry_keyword)
    for label in frame_left.grid_slaves():
        if label.grid_info()['row'] > i + 6 :
            label.grid_forget()
    entry =  Entry(frame_left)
    entry.grid(row = 3 + i, column = 0, sticky = "ew", pady = 2)
    button1.grid(row = 4 + i, column = 0,sticky = "ew", pady = 2)
    button2.grid(row = 5 + i, column = 0, sticky = "ew", pady = 2)
    list_entry_keyword.append(entry)
    print(i)


button1 = Button(frame_left,text = 'Add a Keyword',command = add_keyword)
button1.grid(row = 4, column = 0, sticky = "ew", pady = 2)








def play_video(event, pat, num, beg, end, sc):
        i = len(list_entry_keyword)
        for label in frame_left.grid_slaves():
           if label.grid_info()['row'] > i + 7 :
                label.grid_forget()
        
        if not 'videoplayer' in globals() :
            # create the global variable
            global videoplayer
            frame_right.rowconfigure(1,weight = 219 )

        else : 
            # destroy the old video (if it already exist)
            videoplayer.destroy()
            
        videoplayer = TkinterVideo(frame_left, scaled=True)
        videoplayer.grid(row = 1, column = 0, sticky = 'nsew', pady = 2)
        print(event)
        print(pat)
        videoplayer.load(pat)
        videoplayer.seek(beg)
        videoplayer.play() # play the video
        t = threading.Timer(end - beg, videoplayer.pause)
        t.start()
        print(f"path: {pat}")
        print(f"time begin: {beg}")
        print(f"time end: {end}")
        print(f"scene number: {end}")

        label_num = Label(frame_left, text=f"video number: {num}")
        label_num.grid(row = 7 + i, column = 0,sticky = "ew", pady = 2)

        label_scene = Label(frame_left, text=f"scene number: {sc}")
        label_scene.grid(row = 8 + i, column = 0,sticky = "ew", pady = 2)
        
        label_beg = Label(frame_left, text=f"time begin: {beg}")
        label_beg.grid(row = 9 + i, column = 0,sticky = "ew", pady = 2)

        label_end = Label(frame_left, text=f"time end: {end}")
        label_end.grid(row = 10 + i, column = 0,sticky = "ew", pady = 2)

        print(f"https://vbs.videobrowsing.org/api/v1/submit?item={num}&timecode={math.floor(beg/3600)}%3A{math.floor( (beg % 3600) / 60)}%3A{math.floor(beg%3600)}%3A{math.floor((beg * 25)%25)}&session=node0152kr2xcwzim812hlmtlj0fsy033")


       



#### Mongo DB ####
path = "/Users/alexiaharivel/Desktop/DB"

client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.5.0')

db = client.bdd
video = db.video
scene = db.scene




def search() :
    #place image

    # clean the interface
    for label in frame_right.grid_slaves():
           label.grid_forget()

    # get the keywords 
    list_keyword = []
    for entry in list_entry_keyword : 
        key = entry.get().strip()
        if len(key) > 0 : 
            list_keyword.append(key)
    print(list_keyword)

    # get path keyframes and path scene
    list_path_keyframe = []
    list_path_vid = []
    list_num_scene = []
    list_scene_beg = []
    list_scene_end = []
    list_num =[]
    for post in scene.find({ "keyword" : { "$all" : list_keyword }}) :
        list_path_keyframe.append(path + post["path_keyframe"])
        list_num_scene.append(post["id_scene"])
        list_path_vid.append(post["path_video"])
        list_scene_beg.append(post["beg"])
        list_scene_end.append(post["end"])
        list_num.append(post["id_video"])
    
    for i in range (0,(len(list_path_keyframe))) :
        print(i)
        im = Image.open(list_path_keyframe[i])  #list_path_keyframe
        im = im.resize( (192, 120) )
        img = ImageTk.PhotoImage(im)
        panel = Label(frame_right, image = img)
        panel.image = img # keep a reference!
        panel.grid(row = 1 + i//5 , column =  i%5)
        pat = list_path_vid[i]
        num = list_num[i]
        beg = list_scene_beg[i]
        end = list_scene_end[i]
        sc = list_num_scene[i]
        #print(pat)
        panel.bind("<Button 1>",lambda event, p = pat, n = num, b = beg, e = end, s = sc: play_video(event, p, n, b, e, s))



button2 = Button(frame_left,text = 'Search',command = search)
button2.grid(row = 5, column = 0, sticky = "ew", pady = 2)

import sys
print(sys.executable)

#frame.pack(fill = BOTH, expand=1)
root.mainloop()

