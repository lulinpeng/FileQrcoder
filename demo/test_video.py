import utils
import argparse

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
    utils.imgs_to_video(in_dir=args.in_dir, pattern=args.pattern, outfile=args.outfile, fps=args.fps)
