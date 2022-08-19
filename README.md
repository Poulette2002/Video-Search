---
editor_options: 
  markdown: 
    wrap: 72
---

# Project presentation

## Current Topics in Multimedia Systems: Video Search with Deep Learning (623.915, 22S) ##By Klaus Schoffmann

**CALLARD Baptiste Diener Moritz Harivel Alexia**

### Introduction

The aim of the project is to apply the notions of processing and
description seen during the course to the 100 videos dataset of the V3C1
dataset. It is a dataset that contains only 10% of the V3C1. We finally
seek to propose a visualization by the means of an application allowing
to allow anyone to easily evaluate our results.

### Final objective and motivation

We are going to propose an application that allows to find all the
scenes that contain keywords selected by the user. Thus, each video will
be divided into scenes and the search will be done on the scenes. This
application could find its place for example in video editing. For
example, let's imagine that a person has several videos of several hours
and that he wants to find the best scene containing a motorbike and a
sunset. In this usage situation the person to enter the keywords cat and
sun. The model will return the scenes containing this information and
the link to the original video.

### Key words 

YOLO, AlexNet, Inception, shot detection, keyframe extraction

### Materials:

We will not be able to give you all the frames, videos at intermediate
steps because it takes a huge amount of memory, and it is really
difficult to share even within the group. We have created a drive where
you can see our process for the first video with each step:

<https://drive.google.com/drive/folders/13dLyIqrqQul0PRI5OHjJ4nDpeSrzBlf9?usp=sharing>

#### Notebook: 

• shot_detection.ipynb (requirement distances.npy)

• object_concept_extraction.ipynb

• Frame_Extraction_and_Cluster_Analysis.ipynb

#### File: 

• distances.npy (used in the notebook shot_detection.ipynb)

• imagenet_classes.txt (used in the notebook
object_concept_extraction.ipynb for AlexNet)  

### Protocol

#### • Shot detection:

First, we will divide each of the videos into scenes. A scene is a part
of a video between two camera changes. This part has been realized with
a single generic algorithm that compares histograms. To have a robust
method we used the Twin-Comparison Method. We have developed our own
algorithm without using an already implemented library and have obtained
good results.

For this method, we had to make choices to have only one algorithm the
most versatile model. It is hard to find something that suits video in
grey scale or blurry transition we found king of trade of that can
handle each instance (more or less). It is complicated or impossible to
have 100% accuracy. Even for a human sometimes it is hard.

-   Number of bins for the histogram: 64
-   Choice of threshold: after studying all the videos, we chose the
    thresholds using the quantile 0.90 and 0.95
-   Minimum cut for a scene: 20 (avoid multiple consecutive frame
    detected as cut)
-   The scenes were then extracted in .avi format and then in mp4 format
    (because this format takes less space). For our part with the
    application, we reduced the quality to 640 x 360. For the part with
    the key frame extraction, we used the initial quality 1280x720 with
    only 4 frames per second.

#### • Keyframe extraction

The keyframe extraction takes all shots per video as an input and first
transforms all shots into images. We went with 4 frames per second. The
images are saved with the timestamp of the shot.

#### • Cluster Analysis

The cluster analysis takes all images of the keyframe extraction as an
input and does a cluster analysis and gives a unique image per cluster
as an output. We used the agglomerative hierarchical clustering with a
range between 1 and 10 clusters per shot.

#### • Concept/object detection 

AlexNet, Inception, YOLO : For each key frame we applied YOLO, AlexNet
and Inception and kept the predictions with over 66% accuracy.

#### • Creation of the data base

We used the document-oriented database MongoDB. The data base is created
and filled with the file created.py. It uses the .json files where the
predictions of the frames are stored. To run this file, you need the
PyMongo distribution, to download the .json files on the Google Drive
and to change the line 7 of the file with the path of the folder where
all the videos, videos_split and keyframes are stored.

#### • Creation of the interface

We decided to use the Tkinter library to create the interface. To see
the interface, you must run the file interface.py. You need the
llibrairies tkinter, tkVideoplayer and tkvideo.

#### • How does the interface work?

When you lunch the interface.py script, a tkinter window opens. You can
add as many keywords you want thanks to the button Add a Keyword (it
creates a new entry box). If too many entry box, are add, it is not a
problem. Once you enter all the keywords you want (one per entry box),
you can use the Search button. It will show you all the shots where all
the keywords you entered were predicted by our models. When you click on
a picture, the video of the shot is played on the right corner of the
interface.

#### How to run ?

-   **Download the files**

    Inside a folder DB (that the path need to be change in line 7 of the
    file created.py), please download the videos and folders with the
    same names :

    -   Inside a folder video : all the 100 whole videos

    -   Inside a folder video_split : all the 100 folder
        video_split_000XX with the split videos

    -   Inside a folder keyframe : all the 100 folder video_split_000XX
        with the keyframes for every split video

-   **Fill the data base**

    -   Run the file created.py

-   **Use the interface**

    -   Run the file interface.py
