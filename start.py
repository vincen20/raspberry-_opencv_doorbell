#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os,time,subprocess,shlex
from multiprocessing import Process
mp='mplayer /home/pi/opencv/project/DoorBell/01.mp3'
cmds= 'fswebcam -d /dev/video0 -r 800x600 -S 5 --bottom-banner --title RasPIC@"%s" --no-timestamp image/"%s".jpg'
###=========================
def playm():
    subprocess.call(shlex.split(mp))
##===========================
def cos_up(time_now,date_now):
    from qcloud_cos import CosClient
    from qcloud_cos import UploadFileRequest
    import logging,sys
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger = logging.getLogger(__name__)
    appid=xxxxxxxxxx # 替换为用户的appid
    secret_id = u'xxxxxxxxxxxxxxxxx'  # 替换为用户的secret_id
    secret_key = u'xxxxxxxxxxxxxxxxxxxxx'         # 替换为用户的secret_key
    region = "chengdu" #           # 替换为用户的region，目前可以为 shanghai/guangzhou
    cos_client = CosClient(appid, secret_id, secret_key, region)
    # 设置要操作的bucket
    bucket = u'rasp'
    ############################################################################
    # 文件操作                                                                 #
    ############################################################################
    # 2. 上传文件(覆盖文件)
    request = UploadFileRequest(bucket,u'/%s/%s.jpg' % (date_now,time_now),u'./image/%s.jpg' % (time_now))
    request.set_insert_only(0)  # 设置允许覆盖
    upload_file_ret = cos_client.upload_file(request)    
    logger.info('overwrite file, return message:' + str(upload_file_ret))
########
def face_base(xml,time_now,date_now):
    face_cascade = cv2.CascadeClassifier(xml)
    img = cv2.imread('./image/%s.jpg' % (time_now))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    if len(faces)>0:
	print("Face DEtect")
	print(xml)
        p = Process(target=playm,args=())
        p.start()
        p2=Process(target=cos_up,args=(time_now,date_now))
        p2.start()
        try:
            cv2.destroyWindow(lastx)
        except:
            print("except")
        cv2.namedWindow(time_now)
        cv2.imshow(time_now,img)
        lastx=time_now
    else:
        print("NO Face DEtect")
	return 0
###=======================
def facex(time_now,date_now):
    subprocess.call(shlex.split(cmds % (time_now,time_now)))
    if face_base('./haarcascades/haarcascade_frontalface_default.xml',time_now,date_now)==0:
	if face_base('./haarcascades/haarcascade_frontalface_alt.xml',time_now,date_now)==0:
	    if face_base('./haarcascades/haarcascade_fullbody.xml',time_now,date_now)==0:
		if face_base('./haarcascades/haarcascade_frontalface_alt2.xml',time_now,date_now)==0:
                    if face_base('./haarcascades/haarcascade_frontalface_alt_tree.xml',time_now,date_now)==0:
			if face_base('./haarcascades/haarcascade_lowerbody.xml',time_now,date_now)==0:
                            if face_base('./haarcascades/haarcascade_upperbody.xml',time_now,date_now)==0:
                                if face_base('./haarcascades/haarcascade_profileface.xml',time_now,date_now)==0:
                                   print("No Detecte PeoPLE.")
                                   os.remove('./image/%s.jpg'% (time_now)) 
if __name__ == '__main__':
    lastx='1'
    while True:
    	time_now = time.strftime('%Y-%m-%d-%H-%M-%S')
    	date_now=time.strftime('%Y-%m-%d')
        facex(time_now,date_now)
        if cv2.waitKey(1000)==27:
            break