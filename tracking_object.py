# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 23:19:48 2024

@author: Goutham
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load Video
video_path = "D:\\Assignments\\image and vdo\\LAB\\LAB 4\\sample_video_Lab4.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video file")
else:
    print("Video loaded successfully")

# Frame Extraction
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()
print(f"Total Frames Extracted: {len(frames)}")

# Function to apply color thresholding for segmentation (white objects)
def color_thresholding(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 0, 200])  # Lower bound for white
    upper_bound = np.array([180, 30, 255])  # Upper bound for white
    
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    segmented_frame = cv2.bitwise_and(frame, frame, mask=mask)
    return segmented_frame, mask

# Function to find contours and track objects
def track_objects(mask, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tracked_objects = []
    
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area threshold
            (x, y, w, h) = cv2.boundingRect(contour)
            tracked_objects.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw bounding box
            
    return tracked_objects

# Track and visualize objects across frames
for i, frame in enumerate(frames):
    segmented_frame, mask = color_thresholding(frame)
    tracked_objects = track_objects(mask, frame)

    # Display results
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(segmented_frame, cv2.COLOR_BGR2RGB))
    plt.title("Segmented Frame")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title("Tracked Objects")
    plt.axis('off')
    
    plt.show()

