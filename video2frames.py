## Author: Kartik Hegde
## hegdekartik7@gmail.com

import subprocess as sp
import numpy as np
from PIL import Image
import sys

def get_num_frames(vid_path):
    command = [ "ffprobe",
                '-v', 'error',
                '-count_frames', 
                '-select_streams', 'v:0',
                '-show_entries',
                'stream=nb_read_frames',
                '-of','default=nokey=1:noprint_wrappers=1',
                vid_path]
    return int(float(sp.check_output(command)))

def get_resolution(vid_path):
    command_w = [ "ffprobe",
                '-v', 'error',
                '-of', 'flat=s=_',
                '-select_streams', 'v:0',
                '-show_entries',
                'stream=width',
                '-of','default=nokey=1:noprint_wrappers=1',
                vid_path]

    command_h = [ "ffprobe",
                '-v', 'error',
                '-of', 'flat=s=_',
                '-select_streams', 'v:0',
                '-show_entries',
                'stream=height',
                '-of','default=nokey=1:noprint_wrappers=1',
                vid_path]

    width  = int(sp.check_output(command_w))
    height = int(sp.check_output(command_h))

    video_res = [height, width]

    return video_res

def video_pipe(vid_path, MAX_VID_SIZE):
    """
    Create a pipe to read video frames using ffmpeg
    Inputs:
    vid_path : Path to the video to be read
    MAX_VID_SIZE
    Ouput:
    Subprocess Pipe
    """
    command = [ "ffmpeg",
            '-hide_banner',
            '-nostats',
            '-i', vid_path,
            '-loglevel', 'error',
            '-threads', '1',
            #'-vf' , "select='eq(pict_type\,I)'",
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']

    return sp.Popen(command, stdout = sp.PIPE, bufsize=MAX_VID_SIZE)


def read_frame(pipe,video_resolution, NUM_FRAMES):
    """
    Returns a generator than can be iterated over to read each frame.
    Inputs:
    pipe: Subprocess pipe that has the entire video
    """

    #Get the video Features
    HEIGHT, WIDTH = video_resolution
    frame_count = 0
    while True:
        # read a frame
        raw_image = pipe.stdout.read(HEIGHT*WIDTH*3)
        # transform the byte read into a numpy array
        image =  np.fromstring(raw_image, dtype='uint8')
        image = image.reshape((HEIGHT, WIDTH,3))

        #Skip the last frame
        if(frame_count == NUM_FRAMES-1):
            # throw away the data in the pipe's buffer.
            pipe.stdout.flush()
            pipe.kill()
            break
        frame_count = frame_count + 1
        yield image

def read_video(VID_PATH):
    """
    Main function of the module to read the video.
    It returns a Numpy array of the size (NUM_FRAMES,HEIGHT, WIDTH, 3)
    """
    #Get the video Features
    NUM_FRAMES = get_num_frames(VID_PATH)
    video_resolution  = get_resolution(VID_PATH)
    HEIGHT, WIDTH = video_resolution
    MAX_VID_SIZE = HEIGHT * WIDTH * 3 * (NUM_FRAMES + 1)

    #Create video pipe
    pipe = video_pipe(VID_PATH, MAX_VID_SIZE)
    #Frame Generator
    read_generate = read_frame(pipe,video_resolution, NUM_FRAMES)

    #Placeholder for storing the video frames
    image_stack = np.zeros((NUM_FRAMES,HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame_count = 0

    #Iterate through generator
    for i in read_generate:
        image_stack[frame_count] = i
        frame_count = frame_count + 1


    return image_stack

def show_image(im_array):
    """
    Receive a numpy array of the format (HEIGHT, WIDTH, 3)
    and show the image
    """
    img = Image.fromarray(im_array, 'RGB')
    img.show()

if __name__ == "__main__":
    #Use any test video
    VID_PATH = sys.argv[1]
    image_stack = read_video(VID_PATH)
    show_image(image_stack[56])
