
import cv2
import numpy as np
import subprocess
import os
import argparse

def extract_frames(mov_file:str, outdir:str):
    os.makedirs(outdir, exist_ok=True)
    tmp_mp4 = os.path.join(outdir, 'tmp.mp4')
    ffmpeg_cmd = ['ffmpeg', '-i', mov_file, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', tmp_mp4]
    subprocess.run(ffmpeg_cmd, check=True)

    # read frames
    cap = cv2.VideoCapture(tmp_mp4)    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(f"{outdir}/frame_{frame_count:05d}.png", frame)
        frame_count += 1
        print(f'{frame_count}-th frame')
    
    cap.release()
    os.remove(tmp_mp4)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extrac all frames of a MOV video')
    parser.add_argument('--infile', type=str, default='in.MOV',
                       help='video file')
    parser.add_argument('--outdir', type=str, default='video_result/',
                       help='direct of output frames')
    args = parser.parse_args()
    extract_frames(args.infile, args.outdir)
