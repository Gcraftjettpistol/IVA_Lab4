import ffmpeg

def extract_frame_info(video_path):
    try:
        # Probe the video file to get information about the frames
        probe = ffmpeg.probe(video_path)
        video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        
        # Extract frame information
        frame_count = int(video_stream['nb_frames'])
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        duration = float(video_stream['duration'])
        avg_frame_rate = eval(video_stream['avg_frame_rate'])
        
        print(f"Frame Count: {frame_count}")
        print(f"Resolution: {width}x{height}")
        print(f"Duration: {duration} seconds")
        print(f"Average Frame Rate: {avg_frame_rate} frames/second")
        
    except ffmpeg.Error as e:
        print(e.stderr.decode('utf-8'))

# Sample video path
video_path = "/content/Y2meta.app-Male Lion Charge. Dangerous Game Hunting.-(480p).mp4"
extract_frame_info(video_path)
