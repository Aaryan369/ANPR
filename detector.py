import cv2 as cv
import numpy as np

#variables
nPlateCascade = cv.CascadeClassifier("resources/haarcascades/indian_license_plate.xml")
image_extensions = ["png", "jpg", "jpeg"]

#functions
def find_roi(path):
	extension = path.split(".")[-1]
	if extension in image_extensions:
		scanning_image(path)
	else:
		scanning_video(path)

def find_plate(img):
	plate_rect = nPlateCascade.detectMultiScale(img, scaleFactor = 1.3, minNeighbors = 7)

	if len(plate_rect) == 0:
		return None, None

	for (x,y,w,h) in plate_rect:
		cv.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 3)
		plate_img = img[y:y+h,x:x+w]
		
		roi_coords = [x,y,w,h]

		#print("returning",roi_coords)
		return plate_img, roi_coords

def scanning_image(path):
	img = cv.imread(path)
	#imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	plate_img, roi_coords = find_plate(img)

	#cv.imshow("car gray",imgGray)
	cv.imshow("Plate",plate_img)
	cv.imshow("car",img)

	if cv.waitKey(0) & 0xFF == ord('q'):
		cv.destroyAllWindows()  

def scanning_video(path):
	cap = cv.VideoCapture(path)
	cap.set(3, 640)
	cap.set(4, 480)
	cap.set(10,150)

	success, img = cap.read()
	while success:
		#imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

		plate_img, roi_coords = find_plate(img)

		#cv.imshow("car gray",imgGray)
		if plate_img is not None:
			cv.imshow("Plate",plate_img)
			cv.waitKey(0)
			cv.destroyWindow('Plate')
		cv.imshow("car",img)

		success, img = cap.read()

		if cv.waitKey(1) & 0xFF == ord('q'):
   			cv.destroyAllWindows()  	