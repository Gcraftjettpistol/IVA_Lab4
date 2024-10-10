# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 23:57:18 2024

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

# Soft Cuts Detection Using Histogram Differences
def detect_soft_cuts(frames, threshold=0.5):
    soft_cuts = []
    
    for i in range(1, len(frames)):
        # Calculate histograms for both frames in HSV color space
        hist_prev = cv2.calcHist([cv2.cvtColor(frames[i - 1], cv2.COLOR_BGR2HSV)], [0], None, [256], [0, 256])
        hist_curr = cv2.calcHist([cv2.cvtColor(frames[i], cv2.COLOR_BGR2HSV)], [0], None, [256], [0, 256])
        
        # Normalize histograms
        cv2.normalize(hist_prev, hist_prev)
        cv2.normalize(hist_curr, hist_curr)
        
        # Calculate histogram correlation
        hist_diff = cv2.compareHist(hist_prev, hist_curr, cv2.HISTCMP_CORREL)
        
        # If the correlation is low, it indicates a soft cut
        if hist_diff < threshold:
            soft_cuts.append(i)  # Store the index of the frame where a soft cut occurred
            
    return soft_cuts

# Detect Soft Cuts
soft_cuts = detect_soft_cuts(frames)

# Display results
print(f"Detected Soft Cuts at frames: {soft_cuts}")

# Visualization of Histograms for Soft Cuts
def display_histograms(frames, soft_cuts):
    for i in soft_cuts:
        # Calculate histogram for the detected soft cut frame
        hist = cv2.calcHist([cv2.cvtColor(frames[i], cv2.COLOR_BGR2HSV)], [0], None, [256], [0, 256])
        hist_next = cv2.calcHist([cv2.cvtColor(frames[i + 1], cv2.COLOR_BGR2HSV)], [0], None, [256], [0, 256]) if i + 1 < len(frames) else None
        
        # Normalize the histograms
        cv2.normalize(hist, hist)
        if hist_next is not None:
            cv2.normalize(hist_next, hist_next)
        
        # Plot the histograms
        plt.figure(figsize=(12, 6))
        plt.plot(hist, color='b', label='Current Frame Histogram')
        if hist_next is not None:
            plt.plot(hist_next, color='r', label='Next Frame Histogram')
        plt.title(f'Histogram for Frame {i} and Frame {i + 1}')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.legend()
        plt.xlim([0, 256])
        plt.show()

# Example: Display histograms for detected soft cuts
display_histograms(frames, soft_cuts)