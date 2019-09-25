import numpy as np
import cv2
import urllib
# Open a sample video available in sample-videos
url = 'http://10.100.102.7:8080/shot.jpg'
#if not vcap.isOpened():
#    print "File Cannot be Opened"

while True:
    imgResp=urllib.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    cv2.imshow('test',img)
    if ord('q')==cv2.waitKey(10):
        exit(0)