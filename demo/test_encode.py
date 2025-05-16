from fileqrcoder import FileQrcoder
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FileQrcoder: convert a file into a list of QR code images')
    parser.add_argument('--file', type=str, default=sys.argv[0],
                       help='file to be encoded')
    parser.add_argument('--sk', type=int, default=None,
                       help='secret key (a integer)')
    parser.add_argument('--qrcode_version', type=int, default=40,
                       help='qrcode version (1-40)')
    parser.add_argument('--qrcode_box_size', type=int, default=4,
                       help='number of pixels of “box” of QR code')
    args = parser.parse_args()

    print(f'input file = {args.file}, sk = {args.sk}\n')
    fq_encode = FileQrcoder(qrcode_version=args.qrcode_version, qrcode_box_size=args.qrcode_box_size)
    qrcode_img_paths = fq_encode.gen_qrcodes_from_file(args.file, sk=args.sk) 
    print(qrcode_img_paths)
