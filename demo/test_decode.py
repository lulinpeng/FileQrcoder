from ..fileqrcoder import FileQrcoder # export LD_LIBRARY_PATH=/opt/homebrew/Cellar/zbar/0.23.93_2/lib/:$LD_LIBRARY_PATH
import sys
import os
# export DYLD_LIBRARY_PATH=/opt/homebrew/lib/
# virtualenv --system-site-packages .dev0:ml-citation{ref="1,5" data="citationList"}  
if __name__ == '__main__':
    print('python3 test_decoder.py [directory path of QR Code images]')
    # convert a file into a list of QR code images
    infile = sys.argv[0] if len(sys.argv) == 1 else sys.argv[1]
    # recover a file from the given list of QR code images

    in_dir = './split/'
    out_dir = './results/'
    if len(sys.argv) == 2:
        in_dir = sys.argv[1]
    if len(sys.argv) == 3:
        out_dir = sys.argv[2]
    qrcodes = os.listdir(in_dir) # get all qrcode images
    qrcodes.sort()
    qrcodes = [in_dir + qrcode for qrcode in qrcodes]
    fq_decode = FileQrcoder()
    outfile = fq_decode.recover_file_from_qrcodes(qrcodes)
    print(f'output file ={outfile}')
