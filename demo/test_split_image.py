import os
import utils
import sys

if __name__ == '__main__':
    indir = './test/'
    outdir = './split/'
    if len(sys.argv) == 2:
        indir = sys.argv[1]
    if len(sys.argv) == 3:
        outdir = sys.argv[2]
    qrcodes = os.listdir(indir) # get all qrcode images
    qrcodes.sort()
    qrcodes = [indir+qrcode for qrcode in qrcodes]
    utils.split_image(qrcodes, 2, 4, outdir)

