# FILE ==> List of QR Code Images
from fileqrcoder import FileQrcoder
import sys

if __name__ == '__main__':
    print('python3 test_encoder.py [path of your file] [secret key (a integer)]')
    # convert a file into a list of QR code images
    sk = None
    if len(sys.argv) == 1:
        infile = sys.argv[0]
    elif len(sys.argv) == 2:
        infile = sys.argv[1] 
    elif len(sys.argv) == 3: 
        infile = sys.argv[1]
        sk = int(sys.argv[2])

    print(f'input file = {infile}, sk = {sk}\n')
    fq_encode = FileQrcoder()
    qrcode_img_paths = fq_encode.gen_qrcodes_from_file(infile, sk=None) 
    
    print(qrcode_img_paths)
