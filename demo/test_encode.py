from fileqrcoder import FileQrcoder
import sys
import argparse

if __name__ == '__main__':
    print('python3 test_encoder.py [path of your file] [secret key (a integer)]')
    # convert a file into a list of QR code images
    parser = argparse.ArgumentParser(description='FileQrcoder')
    parser.add_argument('--file', type=str, default=sys.argv[0],
                       help='file to be encoded')
    parser.add_argument('--sk', type=int, default=None,
                       help='secret key (a integer)')
    parser.add_argument('--qrcode_version', type=int, default=40,
                       help='qrcode version (1-40)')
    args = parser.parse_args()

    print(f'input file = {args.file}, sk = {args.sk}\n')
    fq_encode = FileQrcoder(qrcode_version=args.qrcode_version)
    qrcode_img_paths = fq_encode.gen_qrcodes_from_file(args.file, sk=args.sk) 
    print(qrcode_img_paths)
