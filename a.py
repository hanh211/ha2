import sys
import cv2
import numpy as np
import os
import telepot
net = cv2.dnn.readNet('public/yolov3.weights','public/yolov3.cfg')
classes=[]
with open('public/coco.names',"r") as f:
    classes = f.read().splitlines()
cap=cv2.VideoCapture("rtsp://admin:admin1234@192.168.1.15:554/cam/realmonitor?channel=1&subtype=0")
while True:
    ret,img=cap.read()
    height,width,_ = img.shape
    colors= np.random.uniform(0,255,size=(len(classes),3))
    layer_names = net.getLayerNames()
    outputlayers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)
    net.setInput(blob)
    outs = net.forward(outputlayers)
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)


                x=int(center_x - w/2)
                y=int(center_y - h/2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    # print(len(boxes))
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)
    # print(indexes.flatten())
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            x1=(x+w)/2
            y1=(y+h)/2
            cv2.rectangle(img,(0,0),(800,500),color,3)
            b=(0,0)[0]<x1<(800,500)[0] and (0,0)[1]<y1<(800,500)[1]
            if b:
                token = "6275415240:AAF3yDdT45-VIn8GdBrQUHH0XmtMXo0MC28"
                receiver_id=5877612764
                bot = telepot.Bot(token)
                a=cv2.imwrite("a.jpg",img)
                bot.sendPhoto(receiver_id,photo=open("a.jpg", "rb"),caption="Có xâm nhập, nguy hiêm!")
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            # cv2.rectangle(img,(0,0),(800,500),color,3)
            cv2.putText(img,label,(x,y+30),cv2.FONT_HERSHEY_SIMPLEX, 1,color,1,cv2.LINE_AA)
    cv2.imshow("img",img)
    if cv2.waitKey(1)==ord('q'):
        break
