# importing headers
import cv2
import numpy as np

# opening the video
cap = cv2.VideoCapture("data/conveyor.mp4")

if not cap.isOpened():
    print("Error: Could not open video")
    exit()

# initialize the background substractor MOG2
backSub = cv2.createBackgroundSubtractorMOG2()

# output video config
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_mask.avi', fourcc, fps, (frame_width, frame_height), isColor=True)

# initializing the kernel for the morphology (erosion + dilatio)
kernel = np.ones((5,5), np.uint8)

# initializing the constants 
count = 0
line_x = frame_width // 2  # line that will needed to be passed by the object
cx = 0
roi_y_start = int(frame_height * 0.30)
roi_y_end = int(frame_height * 0.80)
previous_cx = frame_width   

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # croping the Region of interset frame only
    roi = frame[roi_y_start:roi_y_end, 0:frame_width]
    # converting the ROI frame to Gray
    gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # applying backsub
    mask = backSub.apply(gray_frame)
    clean_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # finding the contours on the frame
    contours, hierarchy = cv2.findContours(clean_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # putting the line on the frame and not on ROI
    cv2.line(frame, (line_x, roi_y_start), (line_x, roi_y_end), (0,255,0), 4)
    
    if len(contours) > 0:  
        # finding the max contours instead of looping each countour on the frame 
        largest_contour = max(contours, key=lambda c: cv2.contourArea(c))
        area = cv2.contourArea(largest_contour)
        
        if area > 500:
            x, y, w, h = cv2.boundingRect(largest_contour)  
            cx = x + w//2
            cy = y + h//2
            if previous_cx >= line_x and cx < line_x:
                count += 1
            previous_cx = cx
               
    
    cv2.putText(frame, f"Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)   

    out.write(frame)

print(f"Total count: {count}") 

cap.release()
out.release()
