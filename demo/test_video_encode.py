import utils
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Images to video')
    parser.add_argument('--in_dir', type=str, default='qrcodes',
                       help='directory of your images')
    parser.add_argument('--pattern', type=str, default='qrcode_%08d.png',
                       help='image name pattern for FFMPEG')
    parser.add_argument('--outfile', type=str, default='out.mp4',
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
    utils.imgs_to_video(in_dir=args.in_dir, pattern=args.pattern, outfile=args.outfile, fps=args.fps)
