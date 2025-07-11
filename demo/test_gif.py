import os
import sys
import utils

if __name__ == '__main__':
    print('python3 test_gif.py [directory path of QR Code images]')
    indir = sys.argv[1] if len(sys.argv) == 2 else "./qrcodes/"
    print(f'Directory of QR code images is {indir}')
    qrcodes = os.listdir(indir) # get all qrcode images
    qrcodes.sort()
    qrcodes = [indir+qrcode for qrcode in qrcodes]
    utils.images2gif(qrcodes, "out.gif") # generate GIF picture