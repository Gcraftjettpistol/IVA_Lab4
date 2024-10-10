# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 23:32:03 2024

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

# Create Background Subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Initialize a list to hold consistent regions
consistent_regions = []

# Process the video frame by frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    fg_mask = fgbg.apply(frame)

    # Apply morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours in the cleaned mask
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Track consistent regions
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area threshold
            (x, y, w, h) = cv2.boundingRect(contour)
            consistent_regions.append((x, y, w, h))  # Save the bounding box coordinates

            # Draw bounding box on the original frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display results
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title("Original Frame with Consistent Regions")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cleaned_mask, cmap='gray')
    plt.title("Cleaned Foreground Mask")
    plt.axis('off')

    plt.show()

cap.release()
