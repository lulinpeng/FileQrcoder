import os
import utils
import sys

if __name__ == '__main__':
    in_dir = './qrcodes/'
    out_dir = './results/'
    if len(sys.argv) == 2:
        in_dir = sys.argv[1]
    if len(sys.argv) == 3:
        out_dir = sys.argv[2]
    qrcodes = os.listdir(in_dir) # get all qrcode images
    qrcodes.sort()
    qrcodes = [in_dir + qrcode for qrcode in qrcodes]
    print(qrcodes)
    utils.concat_img(qrcodes, 2, 4, interval=0)
    #vertical_qrcodes = utils.vertical_concat_img(qrcodes, 2) # concatenate images vertically
    #horizontal_qrcodes = utils.horizontal_concat_img(vertical_qrcodes, 4, out_dir=out_dir) # concatenate images horizontally
