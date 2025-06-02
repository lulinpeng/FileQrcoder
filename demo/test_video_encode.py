import utils
import argparse
import sys
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Images to video')
    parser.add_argument('--in_dir', type=str, default='qrcodes',
                       help='directory of your images')
    parser.add_argument('--pattern', type=str, default='qrcode_%05d.png',
                       help='image name pattern for FFMPEG')
    parser.add_argument('--outfile', type=str, default='out',
                       help='name of output video')
    parser.add_argument('--fps', type=int, default=15,
                       help='frames per second')
    args = parser.parse_args()
    video_trt = utils.evaluate_video_total_running_time(args.in_dir, args.fps)
    if video_trt > 120:
        # print('The video longer than 2 minutes, do you still want to proceed?')
        user_input = input('The video longer than 2 minutes, do you still want to proceed? ').strip()
        if user_input == 'N' or user_input == "n":
            sys.exit()
    images = os.listdir(args.in_dir)
    images = [os.path.join(args.in_dir, image) for image in images]
    utils.imgs_to_video(images, outfile=args.outfile, fps=args.fps)
