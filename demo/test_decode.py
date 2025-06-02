from fileqrcoder import FileQrcoder
import os
import argparse

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
    qrcodes = [os.path.join(args.indir, qrcode) for qrcode in qrcodes]
    fq_decode = FileQrcoder(sk=args.sk)
    slices = fq_decode.recover_slices_from_qrcodes(qrcodes, report='report.json')
    if len(slices['missed_slice_ids']) == 0:
        fq_decode.recover_file_from_slices(slices, args.outfile)
        print(f'output file ={args.outfile}')
