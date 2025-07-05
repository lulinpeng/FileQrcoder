from fileqrcoder import FileQrcoder
import os
import argparse
import utils
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recover a file from a report')
    parser.add_argument('--report', type=str,
                       help='directory of your images')
    parser.add_argument('--outfile', type=str, default='recover.out',
                       help='outoput file')
    parser.add_argument('--sk', type=int, default=None,
                       help='secret key (a integer)')
    args = parser.parse_args()
    print(f'report = {args.report}, outfile = {args.outfile}')
    fq = FileQrcoder(sk=args.sk)
    fq.recover_file_from_report(args.report, args.outfile)
    print(f'report = {args.report}, outfile = {args.outfile}')