import cv2
import numpy as np
cap=cv2.VideoCapture(0)
lower_range_blue=np.array([97,85,76])
upper_range_blue=np.array([119,255,255])
lower_range_green=np.array([50,54,0])
upper_range_green=np.array([89,213,255])
lower_range_red1=np.array([0,190,0])
upper_range_red1=np.array([5,255,153])
lower_range_red2=np.array([174,99,0])
upper_range_red2=np.array([179,255,255])

def blue(image):
    max=0
    x,y,w,h=0,0,0,0
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range_blue,upper_range_blue)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if len(cnts)!=0 :
        max=cv2.contourArea(cnts[0])
        x,y,w,h=cv2.boundingRect(cnts[0])
    for c in cnts:
        if cv2.contourArea(c)>max:
            max=cv2.contourArea(c)
            x,y,w,h=cv2.boundingRect(c)
            
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.putText(image,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    return max
def green(image):
    max=0
    x,y,w,h=0,0,0,0
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range_green,upper_range_green)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if len(cnts)!=0 :
        max=cv2.contourArea(cnts[0])
        x,y,w,h=cv2.boundingRect(cnts[0])
    for c in cnts:
        if cv2.contourArea(c)>max:
            max=cv2.contourArea(c)
            x,y,w,h=cv2.boundingRect(c)       
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.putText(image,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    return max 
def red(image):
    max=0
    x,y,w,h=0,0,0,0
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range_red1,upper_range_red1)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    mask2=cv2.inRange(hsv,lower_range_red2,upper_range_red2)
    _,mask22=cv2.threshold(mask2,254,255,cv2.THRESH_BINARY)
    mask11=np.ma.mask_or(mask1, mask22)
    mask11=np.uint8(mask11)
    cnts,_=cv2.findContours(mask11,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if len(cnts)!=0 :
        max=cv2.contourArea(cnts[0])
        x,y,w,h=cv2.boundingRect(cnts[0])
    for c in cnts:
        if cv2.contourArea(c)>max:
            max=cv2.contourArea(c)
            x,y,w,h=cv2.boundingRect(c)       
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    return max

def color():
    ret,frame=cap.read()
    red_contour=0
    blue_contour=0
    green_contour=0
    r=0
    b=0
    g=0
    for i in range(20):
        red_contour=red(frame)
        green_contour=green(frame)
        blue_contour=blue(frame)
        if max(red_contour,green_contour,blue_contour) == red_contour:
            r+=1
        elif max(red_contour,green_contour,blue_contour) == green_contour:
            g+=1
        elif max(red_contour,green_contour,blue_contour) == blue_contour:
            b+=1
    #print(r)
    #print(g)
    #print(b)
    cap.release()
    if max(r,g,b) == r:
        return "red"
    if max(r,g,b) == g:
        return "green"
    if max(r,g,b) == b:
        return "blue"
if __name__ == "__main__":  
    color=color()
    print(color)