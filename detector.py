import cv2
import numpy as np
import pytesseract
from PIL import Image
import pymongo

# Connect to the MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Get the "vehicle_details" database
db = client["vehicle_details"]

# Get the "vehicles" collection
vehicles_collection = db["vehicles"]

def fetch_details(license_number):
    # Search for the vehicle with the given license number
    vehicle = vehicles_collection.find_one({"license_number": license_number})
    if vehicle:
        return vehicle
    else:
        return None

def process_image(image):
    # convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # apply thresholding to pre-process the image
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # apply median blur to reduce noise
    gray = cv2.medianBlur(gray, 3)
    
    # apply morphological transformations to extract the license plate
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # extract the license plate
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # apply connected component analysis to isolate the license plate
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [255, 0, 0]
    
    # get the license plate
    plate = None
    for i in range(1, np.max(markers) + 1):
        if np.sum(markers == i) > 1000:
            plate = np.zeros(gray.shape, np.uint8)
            plate[markers == i] = 255
            break
    
    # use pytesseract to extract the license number
    plate_im = Image.fromarray(plate)
    license_number = pytesseract.image_to_string(plate_im, lang = 'eng', 
                                                 config='--psm 11')
    return license_number

# read the video
cap = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = cap.read()
    if ret:
        # process the frame and extract the license number
        license_number = process_image(frame)

        # record the license number and cut the proper amount from the owner's bank account
        print("License Number: ", license_number)
        
        details = fetch_details(license_number)
        
        if details:
            print("Details: ", details)
        else:
            print("No details found for the given license number.")
            
    else:
        break

cap.release()
