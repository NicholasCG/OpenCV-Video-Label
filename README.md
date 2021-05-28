# OpenCV-Video-Label
This Git repository implements a tkinter/opencv video player which will allow users to play videos and enables them to test their own algorithms in a user friendly environment. Besides, it supports two object tracking algorithms (Re3 and CMT) which make it possible to label an object once, track the object over multiple frames and store the resulting cropped images of the object, this reduces the amount of time needed for image tagging which is usually needed when creating datasets.

[Video demo](https://www.youtube.com/watch?v=3BcrK0O1kb4)

# Dependencies:
1. Python 3.7.10
2. OpenCV 2 
2. Tensorflow and its requirements.
3. NumPy
4. SciPy
5. mss
6. Pillow
7. urllib3
8. requests
9. GoogleDriveDownloader ( only for downloading the re3 model: http://bit.ly/2L5deYF )
10. CUDA (Strongly recommended for Re3)
11. cuDNN (recommended for Re3)

# First Time Setup:
``` 
    git clone git@github.com:natdebru/OpenCV-Video-Label.git
    cd OpenCV-Video-Label
    pip install python-virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
```
The first time you run the program it will download and load the re3 model (700mb), therefore startup will take a bit longer.

# Run the program:
```
    python __main__.py
```

# About the implemented Algorithms:
## [Re3](https://gitlab.com/danielgordon10/re3-tensorflow):
Re3 is a real-time recurrent regression tracker. It offers accuracy and robustness similar to other state-of-the-art trackers while operating at 150 FPS. For more details, contact xkcd@cs.washington.edu. 

This repository implements the training and testing procedure from https://arxiv.org/pdf/1705.06368.pdf. 
A sample of the tracker can be found here: https://youtu.be/RByCiOLlxug.

Re3 is released under the GPL V3.
Please cite Re3 in your publications if it helps your research:

    @article{gordon2018re3,
        title={Re3: Real-Time Recurrent Regression Networks for Visual Tracking of Generic Objects},
        author={Gordon, Daniel and Farhadi, Ali and Fox, Dieter},
        journal={IEEE Robotics and Automation Letters},
        volume={3},
        number={2},
        pages={788--795},
        year={2018},
        publisher={IEEE}
     }
 
## [CMT ](https://github.com/gnebehay/CMT):
CMT (Consensus-based Matching and Tracking of Keypoints for Object Tracking) is a novel keypoint-based method for long-term model-free object tracking in a combined matching-and-tracking framework. Details can be found on the project page and in their publication. 

If you use their algorithm in scientific work, please cite their publication:

    @inproceedings{Nebehay2015CVPR,
        author = {Nebehay, Georg and Pflugfelder, Roman},
        booktitle = {Computer Vision and Pattern Recognition},
        month = jun,
        publisher = {IEEE},
        title = {Clustering of {Static-Adaptive} Correspondences for Deformable Object Tracking},
        year = {2015}
    }
# Input types:
The tool currently supports the following video sources:
1. Regular video files like .mp4 and .avi
2. Webcams
3. IPwebcams (which allows users to stream from their phone)
4. Screencapturing


