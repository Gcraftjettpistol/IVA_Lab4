import os

def calculate_frame_sizes(frame_dir):
    frame_files = [f for f in os.listdir(frame_dir) if f.endswith('.png')]
    frame_sizes = [os.path.getsize(os.path.join(frame_dir, file)) for file in frame_files]
    return frame_sizes

def print_frame_size_statistics(frame_type, frame_sizes):
    total_size = sum(frame_sizes)
    num_frames = len(frame_sizes)
    average_size = total_size / num_frames if num_frames > 0 else 0
    print(f"{frame_type} Frames: Total Size = {total_size} bytes, Number of Frames = {num_frames}, Average Size = {average_size:.2f} bytes")

# Directories where frames are stored
i_frame_dir = 'I_frames'
p_frame_dir = 'P_frames'
b_frame_dir = 'B_frames'

# Calculate frame sizes
i_frame_sizes = calculate_frame_sizes(i_frame_dir)
p_frame_sizes = calculate_frame_sizes(p_frame_dir)
b_frame_sizes = calculate_frame_sizes(b_frame_dir)

# Print statistics
print_frame_size_statistics('I', i_frame_sizes)
print_frame_size_statistics('P', p_frame_sizes)
print_frame_size_statistics('B', b_frame_sizes)
