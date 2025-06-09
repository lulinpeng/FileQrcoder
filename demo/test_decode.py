from fileqrcoder import FileQrcoder
import os
import argparse
import utils
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recover a file from the given list of images containing QR codes')
    parser.add_argument('--indir', type=str, default='qrcodes/',
                       help='directory of your images')
    parser.add_argument('--outfile', type=str, default='decode.out',
                       help='outoput file')
    parser.add_argument('--sk', type=int, default=None,
                       help='secret key (a integer)')
    args = parser.parse_args()

    print(f'indir = {args.indir}, outfile = {args.outfile}, sk = {args.sk}\n')
    qrcodes = os.listdir(args.indir) # get all qrcode images
    qrcodes.sort()
    qrcodes = [os.path.join(args.indir, qrcode) for qrcode in qrcodes]

    for i in range(len(qrcodes)):
        if qrcodes[i][-5:] == '.HEIC':
            png_qrcode = f'{qrcodes[i][:-5]}.png'
            utils.heic_to_png(qrcodes[i], png_qrcode)
            qrcodes[i] = png_qrcode
    print(qrcodes)
    fq_decode = FileQrcoder(sk=args.sk)
    slices = fq_decode.recover_slices_from_qrcodes(qrcodes, report='report.json')

    reports = ['report.json', 'report.bak.json']
    slices = fq_decode.merge_slice_report(reports)
    print(slices['missed_slice_ids'])
    if len(slices['missed_slice_ids']) == 0:
        fq_decode.recover_file_from_slices(slices, args.outfile)
        print(f'output file ={args.outfile}')
