import os
import utils
import sys

if __name__ == '__main__':
    indir = './qrcodes/'
    outdir = './results/'
    if len(sys.argv) == 2:
        indir = sys.argv[1]
    if len(sys.argv) == 3:
        outdir = sys.argv[2]
    qrcodes = os.listdir(indir) # get all qrcode images
    qrcodes.sort()
    qrcodes = [indir + qrcode for qrcode in qrcodes]
    print(qrcodes)
    utils.concat_img(qrcodes, 2, 4, interval=0)
    #vertical_qrcodes = utils.vertical_concat_img(qrcodes, 2) # concatenate images vertically
    #horizontal_qrcodes = utils.horizontal_concat_img(vertical_qrcodes, 4, outdir=outdir) # concatenate images horizontally
