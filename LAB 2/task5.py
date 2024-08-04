import os
import cv2

def create_video_from_frames(frame_dir, output_video, fps):
    # Get a list of image files in the directory
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
    
    if not frame_files:
        print("No frames found in the directory.")
        return
    
    # Read the first frame to get the video dimensions
    first_frame = cv2.imread(os.path.join(frame_dir, frame_files[0]))
    height, width, layers = first_frame.shape

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Use 'mp4v' codec
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for frame_file in frame_files:
        frame_path = os.path.join(frame_dir, frame_file)
        frame = cv2.imread(frame_path)
        video.write(frame)
    
    video.release()
    print(f"Video saved as {output_video}")

# Directory containing the extracted I-frames
i_frame_dir = 'I_frames'
output_video = 'I-frame_video.mp4'
fps = 1  # Reduced frame rate

# Create video from I-frames
create_video_from_frames(i_frame_dir, output_video, fps)
