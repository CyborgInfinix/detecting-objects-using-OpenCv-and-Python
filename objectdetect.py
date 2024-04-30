import numpy as np
import matplotlib.pyplot as plt
import cv2


vc = cv2.VideoCapture(0)
cv2.namedWindow("preview")


#img_counter = 0
while True:
    #to read video capture
    ret, frame = vc.read()
    if not ret:
        print(" closing...")
        break
    #to display captured frame
    cv2.imshow("preview", frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        vc.release()
        cv2.destroyWindow("preview")
        break
    elif k%256 == 32:
        #SPACE pressed
        img_name = "E:\Github\CapturedImg.png"
        cv2.imwrite(img_name, frame)
        print("Process begins..")
        image = cv2.imread("E:\Github\CapturedImg.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(src=gray, ksize=(3, 5), sigmaX=0.5)
        cv2.imshow("Gray", gray)
        cv2.waitKey(0)
        #edge detection
        canny = cv2.Canny(gray, 0, 200)
        canny = cv2.dilate(canny, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        thresh = cv2.adaptiveThreshold(canny,255,1,1,11,2)
        cv2.imshow("Edged", thresh)
        cv2.waitKey(0)
        # find contours in the image 
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        #identifying the book
        def detectbook(page):
            biggest = None
            max_area = 0
            indexReturn = -1
            for index in range(len(contours)):
                    i = contours[index]
                    area = cv2.contourArea(i)
                    if area > 100:
                            peri = cv2.arcLength(i,True)
                            approx = cv2.approxPolyDP(i,0.1*peri,True)
                            if area > max_area: #and len(approx)==4:
                                    biggest = approx
                                    max_area = area
                                    indexReturn = index
            return indexReturn

        indexReturn = detectbook(contours)
        Book = cv2.drawContours(image, contours, indexReturn, (0,255,0))
        #display the outline of object identified
        cv2.imshow("Output", Book)
        cv2.waitKey(0)
        vc.release()
        cv2.destroyAllWindows()
        
vc.release()
cv2.destroyAllWindows()
        





	






