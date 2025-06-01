import os
import utils
import sys

if __name__ == '__main__':
    in_dir = './test/'
    out_dir = './split/'
    if len(sys.argv) == 2:
        in_dir = sys.argv[1]
    if len(sys.argv) == 3:
        out_dir = sys.argv[2]
    qrcodes = os.listdir(in_dir) # get all qrcode images
    qrcodes.sort()
    qrcodes = [in_dir+qrcode for qrcode in qrcodes]
    utils.split_image(qrcodes, 2, 4, out_dir)

