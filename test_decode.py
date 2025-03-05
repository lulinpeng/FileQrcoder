from fileqrcoder import FileQrcoder
import sys

if __name__ == '__main__':
    print('python3 test_decoder.py [directory path of QR Code images]')
    # convert a file into a list of QR code images
    infile = sys.argv[0] if len(sys.argv) == 1 else sys.argv[1]
    # recover a file from the given list of QR code images
    qrcode_img_dir = ''
    qrcode_img_paths = ['qrcode_00000000.png', 'qrcode_00000001.png', 'qrcode_00000002.png', 'qrcode_00000003.png']
    fq_decode = FileQrcoder()
    outfile = fq_decode.recover_file_from_qrcodes(qrcode_img_paths)
    print(f'output file ={outfile}')
