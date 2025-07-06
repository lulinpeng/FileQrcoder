import utils
import argparse
import sys
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Images to video')
    parser.add_argument('--indir', type=str, default='qrcodes', help='directory of your qrcode images', required=True)
    parser.add_argument('--outfile', type=str, default='out', help='name of output video')
    parser.add_argument('--fps', type=int, default=15, help='frames per second')
    args = parser.parse_args()
    video_trt = utils.evaluate_video_total_running_time(args.indir, args.fps)
    if video_trt > 120:
        # print('The video longer than 2 minutes, do you still want to proceed?')
        user_input = input('The video longer than 2 minutes, do you still want to proceed? ').strip()
        if user_input == 'N' or user_input == "n":
            sys.exit()
    images = os.listdir(args.indir)
    images = [os.path.join(args.indir, image) for image in images]
    # image_ids = [116, 179, 195, 259]
    # images = [f'qrcodes/qrcode_{str(image_id).zfill(5)}.png' for image_id in image_ids]
    outfile = utils.imgs_to_video(images, outfile=args.outfile, fps=args.fps)
    print(f'output video {outfile}')
