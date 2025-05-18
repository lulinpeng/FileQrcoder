
from fileqrcoder import FileQrcoder 
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Images to video')
    parser.add_argument('--in_dir', type=str, default='video_result/',
                       help='directory of your images')
    parser.add_argument('--outfile', type=str, default='decode.video.out',
                       help='name of output video')
    parser.add_argument('--sk', type=int, default=None,
                       help='secret key (a integer)')
    args = parser.parse_args()
    print(f'in_dir = {args.in_dir}, outfile = {args.outfile}, sk = {args.sk}\n')
    qrcodes = os.listdir(args.in_dir) # get all qrcode images
    qrcodes = [os.path.join(args.in_dir, qrcode) for qrcode in qrcodes]
    fq_decode = FileQrcoder(sk=args.sk)
    fq_decode.recover_file_from_qrcodes(qrcodes, outfile=args.outfile)
    print(f'output file ={args.outfile}')