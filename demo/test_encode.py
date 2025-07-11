from fileqrcoder import FileQrcoder
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FileQrcoder: convert a file into a list of QR code images')
    parser.add_argument('--file', type=str, default=sys.argv[0], help='file to be encoded', required=True)
    parser.add_argument('--sk', type=int, default=None, help='secret key (a integer)')
    parser.add_argument('--qrcode_version', type=int, default=27, help='qrcode version (1-40)')
    parser.add_argument('--qrcode_box_size', type=int, default=4, help='number of pixels of “box” of QR code')
    parser.add_argument('--id', type=str, default='', help='batch id of this time')
    args = parser.parse_args()

    print(f'input file = {args.file}, sk = {args.sk}\n')
    fq_encode = FileQrcoder(qrcode_version=args.qrcode_version, qrcode_box_size=args.qrcode_box_size, sk=args.sk)
    qrcode_img_paths = fq_encode.gen_qrcodes_from_file_in_parallel(args.file, id=args.id) 
    print(qrcode_img_paths)
