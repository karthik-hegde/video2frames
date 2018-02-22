# video2frames
This is an efficient subprocess pipe based module to extract all the frames of a video to a numpy array.

This has 3 functionalities:

1. Get the resolution of the video
2. Get the number of frames in a video
3. Get all the frames in the video as a numpy array

*Requirements:* ffmpeg callable from terminal.

Usage:

    import video2frames
    video_stack = video2frames.read_video(VID_PATH)
