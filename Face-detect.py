import cv2 
import numpy as np

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
genderNet = cv2.dnn.readNet(genderModel, genderProto)
ageNet = cv2.dnn.readNet(ageModel,ageProto)
w,h = 360,200
fbRange = [6200,6800]
genderList= ['Male', 'Female']
ageList = ['(0, 2)', '(4, 6)', '(8, 12)', '(13, 19)', '(20, 25)', '(25, 38)', '(39, 50)', '(50,70)','(70,90)','(90,100)']


def findFace (img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2,8)
    myFaceListC = []
    myFaceListArea = []
    blob = cv2.dnn.blobFromImage(img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds = genderNet.forward()
    gender = genderList[genderPreds[0].argmax()]
    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    age = ageList[agePreds[0].argmax()]
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = x+w //2
        cy = y+h //2
        area = w*h
        cv2.circle(img,(cx,cy),5,(0,255,0),cv2.FILLED)
        myFaceListC.append([cx,cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]],gender,age
    else:
        return img, [[0,0],0],"Not Identified", "Unkown age"  
    
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        p,img = cap.read()
        img = cv2.resize(img,(w,h))
        img, info, g,a = findFace(img)
        print("Area",info[1],"Center",info[0],"Gender",g,"Age",a)
        cv2.imshow("Output",img)
        keyCode = cv2.waitKey(1)
        if cv2.getWindowProperty("Output", cv2.WND_PROP_VISIBLE) <1:
            break
    cv2.destroyAllWindows()