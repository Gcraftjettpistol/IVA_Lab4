# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 23:00:38 2024

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
# Spatio-Temporal Segmentation
# a. Color Thresholding for White
def color_thresholding(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Adjusted bounds for white
    lower_bound = np.array([0, 0, 200])  # White lower bound (low saturation, high value)
    upper_bound = np.array([180, 50, 255])  # White upper bound (still low saturation, high value)
    
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    segmented_frame = cv2.bitwise_and(frame, frame, mask=mask)
    return segmented_frame

# b. Edge Detection
def edge_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

# c. Foreground vs. Background Segmentation using MOG2
fgbg = cv2.createBackgroundSubtractorMOG2()

def background_segmentation(frame):
    fg_mask = fgbg.apply(frame)
    return fg_mask

# Scene Cut Detection
# a. Hard Cuts Using Pixel-based Comparison
def detect_hard_cuts(frames, threshold=30):
    cuts = []
    for i in range(1, len(frames)):
        diff = cv2.absdiff(frames[i], frames[i - 1])
        non_zero_count = np.count_nonzero(diff)
        
        if non_zero_count > threshold * diff.size:
            cuts.append(i)
    return cuts

# b. Soft Cuts Using Histogram Differences
def detect_soft_cuts(frames, threshold=0.5):
    cuts = []
    for i in range(1, len(frames)):
        hist_prev = cv2.calcHist([cv2.cvtColor(frames[i-1], cv2.COLOR_BGR2HSV)], [0], None, [256], [0, 256])
        hist_curr = cv2.calcHist([cv2.cvtColor(frames[i], cv2.COLOR_BGR2HSV)], [0], None, [256], [0, 256])
        
        hist_diff = cv2.compareHist(hist_prev, hist_curr, cv2.HISTCMP_CORREL)
        if hist_diff < threshold:
            cuts.append(i)
    return cuts

# Mark Scene Cuts
hard_cuts = detect_hard_cuts(frames)
soft_cuts = detect_soft_cuts(frames)

# Result Visualization
def display_frame_with_results(frame, cut_detected=False):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    
    ax[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    ax[0].set_title("Original Frame")

    ax[1].imshow(color_thresholding(frame))
    ax[1].set_title("White Color Thresholding")

    ax[2].imshow(edge_detection(frame), cmap='gray')
    ax[2].set_title("Edge Detection")

    if cut_detected:
        plt.suptitle("Scene Cut Detected", color='red')

    plt.show()

# Example: Display scene cut frames with results
all_cuts = hard_cuts + soft_cuts
all_cuts = sorted(set(all_cuts))  # Combine and sort unique cut indices

# Output the number of scene cuts and frame numbers
print(f"Number of Hard Cuts Detected: {len(hard_cuts)} at frames: {hard_cuts}")
print(f"Number of Soft Cuts Detected: {len(soft_cuts)} at frames: {soft_cuts}")
print(f"Total Number of Scene Cuts Detected: {len(all_cuts)}")

# Visualize cuts
for cut in all_cuts:
    print(f"Displaying scene cut at frame {cut}")
    display_frame_with_results(frames[cut], cut_detected=True)
