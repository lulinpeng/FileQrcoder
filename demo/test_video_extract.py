import argparse
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extrac all frames of a MOV video')
    parser.add_argument('--infile', type=str, default='in.MOV',
                       help='video file')
    parser.add_argument('--outdir', type=str, default='video_result/',
                       help='direct of output frames')
    args = parser.parse_args()
    utils.extract_frames(args.infile, args.outdir)
