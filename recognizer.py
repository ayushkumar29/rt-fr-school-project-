############################################
## Modified By Ayush And Abhinandan       ##
##                                        ##
############################################


import cv2
import numpy as np
import os
import time

                                # taking names from pictures

imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
names=["."]
for imagePath in imagePaths:
    PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
    img_numpy = np.array(PIL_img,'uint8')

    name = str(os.path.split(imagePath)[-1].split(".")[2])
    if name in names:                                   #checking the names if it exist or not !!!
      conitnue
    
    else:
        names.append(name)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')   #load trained model
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX


#iniciate id counter, the number of persons you want to include
id = len(names)

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

xaxis=[]
yaxis=[]

while True:

    ret, img =cam.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        print(confidence)
        

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if ((100-confidence) < 100) and ((100-confidence) > 35) :
            id = names[id]
            confidence = "  {0}%".format(round(confidence))
        else:
            id = "unknown person !!( bhag yaha se)"
            confidence = "  {0}%".format(round(confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
