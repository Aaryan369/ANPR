import cv2 as cv
import numpy as np

def find_plate(img):
	plate_rect = nPlateCascade.detectMultiScale(img, scaleFactor = 1.3, minNeighbors = 7)

	for (x,y,w,h) in plate_rect:
		a,b = 0,0
		a,b = (int(0.02*img.shape[0]), int(0.025*img.shape[1])) 
		plate = img[y+a:y+h-a, x+b:x+w-b, :]
		cv.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 3)
		plate_img = img[y:y+h,x:x+w]
		#print(x,y,w,h)
		cv.imshow("plate",plate_img)
	

nPlateCascade = cv.CascadeClassifier("resources/haarcascades/indian_license_plate.xml")

img = cv.imread("resources/Plate1.jpeg")
'''
cap = cv.VideoCapture("resources/Plate1.jpeg")
cap.set(3, 640)
cap.set(4, 480)
cap.set(10,150)

success, img = cap.read()
'''
#imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
find_plate(img)
#cv.imshow("car gray",imgGray)
cv.imshow("car",img)

if cv.waitKey(0) & 0xFF == ord('q'):
    cv.destroyAllWindows()       
