from fileqrcoder import FileQrcoder # export LD_LIBRARY_PATH=/opt/homebrew/Cellar/zbar/0.23.93_2/lib/:$LD_LIBRARY_PATH
import sys
import os
import argparse
# export DYLD_LIBRARY_PATH=/opt/homebrew/lib/
# virtualenv --system-site-packages .dev0:ml-citation{ref="1,5" data="citationList"}  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recover a file from the given list of QR code images')
    parser.add_argument('--in_dir', type=str, default='qrcodes/',
                       help='directory of your images')
    parser.add_argument('--outfile', type=str, default='decode.out',
                       help='outoput file')
    parser.add_argument('--sk', type=int, default=None,
                       help='secret key (a integer)')
    args = parser.parse_args()

    print(f'in_dir = {args.in_dir}, outfile = {args.outfile}, sk = {args.sk}\n')
    qrcodes = os.listdir(args.in_dir) # get all qrcode images
    qrcodes = [args.in_dir + qrcode for qrcode in qrcodes]
    fq_decode = FileQrcoder(sk=args.sk)
    fq_decode.recover_file_from_qrcodes(qrcodes, outfile=args.outfile)
    print(f'output file ={args.outfile}')
