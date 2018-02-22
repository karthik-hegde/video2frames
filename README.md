# video2frames
This is an efficient subprocess pipe based module to extract all the frames of a video to a numpy array.

Requirements: ffmpeg callable from terminal.

Usage:

    import video2frames
    video_stack = video2frames.read_video(VID_PATH)
