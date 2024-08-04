import os
from PIL import Image
import cv2
import matplotlib.pyplot as plt

# Function to load and display the first 3 frames using PIL
def display_first_three_frames_pil(frame_dir, frame_type):
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])[:3]
    frames = [Image.open(os.path.join(frame_dir, file)) for file in frame_files]

    plt.figure(figsize=(12, 8))
    for i, frame in enumerate(frames):
        plt.subplot(1, 3, i + 1)
        plt.imshow(frame)
        plt.title(f"{frame_type} Frame {i + 1}")
        plt.axis('off')
    plt.show()

# Function to load and display the first 3 frames using OpenCV
def display_first_three_frames_opencv(frame_dir, frame_type):
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])[:3]
    frames = [cv2.imread(os.path.join(frame_dir, file)) for file in frame_files]

    for i, frame in enumerate(frames):
        cv2.imshow(f"{frame_type} Frame {i + 1}", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Directories where frames are stored
i_frame_dir = 'I_frames'
p_frame_dir = 'P_frames'
b_frame_dir = 'B_frames'

# Display the first 3 frames using PIL
print("Displaying the first 3 I-frames using PIL...")
display_first_three_frames_pil(i_frame_dir, 'I')

print("Displaying the first 3 P-frames using PIL...")
display_first_three_frames_pil(p_frame_dir, 'P')

print("Displaying the first 3 B-frames using PIL...")
display_first_three_frames_pil(b_frame_dir, 'B')

# Display the first 3 frames using OpenCV
print("Displaying the first 3 I-frames using OpenCV...")
display_first_three_frames_opencv(i_frame_dir, 'I')

print("Displaying the first 3 P-frames using OpenCV...")
display_first_three_frames_opencv(p_frame_dir, 'P')

print("Displaying the first 3 B-frames using OpenCV...")
display_first_three_frames_opencv(b_frame_dir, 'B')
