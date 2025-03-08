# FILE ==> List of QR Code Images
from fileqrcoder import FileQrcoder
import sys

if __name__ == '__main__':
    print('python3 test_encoder.py [path of your file]')
    # convert a file into a list of QR code images
    infile = sys.argv[0] if len(sys.argv) == 1 else sys.argv[1]
    print(f'input file = {infile}')

    fq_encode = FileQrcoder()
    qrcode_img_paths = fq_encode.gen_qrcodes_from_file(infile) 
    
    print(qrcode_img_paths)
