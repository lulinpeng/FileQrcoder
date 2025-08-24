import qrcode
import base64
import logging
import math
import random
import os
import json
import time
import utils
import multiprocessing
import PIL
import sys
import argparse

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)

QRCODE_VERSIONS = {
    1: {'L': 17, 'M': 14, 'Q': 11, 'H': 8},
    2: {'L': 32, 'M': 26, 'Q': 20, 'H': 15},
    3: {'L': 53, 'M': 42, 'Q': 32, 'H': 24},
    4: {'L': 78, 'M': 62, 'Q': 46, 'H': 34},
    5: {'L': 106, 'M': 84, 'Q': 60, 'H': 44},
    6: {'L': 134, 'M': 106, 'Q': 74, 'H': 58},
    7: {'L': 154, 'M': 122, 'Q': 86, 'H': 64},
    8: {'L': 192, 'M': 152, 'Q': 108, 'H': 84},
    9: {'L': 230, 'M': 180, 'Q': 130, 'H': 98},
    10: {'L': 271, 'M': 215, 'Q': 151, 'H': 119},
    11: {'L': 321, 'M': 254, 'Q': 177, 'H': 137},
    12: {'L': 367, 'M': 290, 'Q': 203, 'H': 155},
    13: {'L': 425, 'M': 334, 'Q': 241, 'H': 177},
    14: {'L': 458, 'M': 365, 'Q': 258, 'H': 194},
    15: {'L': 520, 'M': 408, 'Q': 292, 'H': 220},
    16: {'L': 586, 'M': 459, 'Q': 322, 'H': 250},
    17: {'L': 644, 'M': 504, 'Q': 364, 'H': 280},
    18: {'L': 718, 'M': 564, 'Q': 394, 'H': 310},
    19: {'L': 792, 'M': 611, 'Q': 442, 'H': 338},
    20: {'L': 858, 'M': 661, 'Q': 482, 'H': 382},
    21: {'L': 929, 'M': 715, 'Q': 509, 'H': 403},
    22: {'L': 1003, 'M': 779, 'Q': 565, 'H': 439},
    23: {'L': 1091, 'M': 864, 'Q': 611, 'H': 461},
    24: {'L': 1171, 'M': 910, 'Q': 661, 'H': 511},
    25: {'L': 1273, 'M': 958, 'Q': 715, 'H': 535},
    26: {'L': 1367, 'M': 1046, 'Q': 751, 'H': 593},
    27: {'L': 1465, 'M': 1153, 'Q': 805, 'H': 625},
    28: {'L': 1528, 'M': 1219, 'Q': 868, 'H': 658},
    29: {'L': 1628, 'M': 1273, 'Q': 908, 'H': 698},
    30: {'L': 1732, 'M': 1370, 'Q': 982, 'H': 742},
    31: {'L': 1840, 'M': 1452, 'Q': 1030, 'H': 790},
    32: {'L': 1952, 'M': 1538, 'Q': 1112, 'H': 842},
    33: {'L': 2068, 'M': 1628, 'Q': 1168, 'H': 898},
    34: {'L': 2188, 'M': 1722, 'Q': 1228, 'H': 958},
    35: {'L': 2303, 'M': 1809, 'Q': 1283, 'H': 983},
    36: {'L': 2431, 'M': 1911, 'Q': 1351, 'H': 1051},
    37: {'L': 2563, 'M': 1989, 'Q': 1423, 'H': 1093},
    38: {'L': 2699, 'M': 2099, 'Q': 1499, 'H': 1139},
    39: {'L': 2809, 'M': 2213, 'Q': 1579, 'H': 1219},
    40: {'L': 2953, 'M': 2331, 'Q': 1663, 'H': 1273}
}

ERROR_CORRECT_MAP = {
    'L':qrcode.constants.ERROR_CORRECT_L,
    'M':qrcode.constants.ERROR_CORRECT_M,
    'Q':qrcode.constants.ERROR_CORRECT_Q,
    'H':qrcode.constants.ERROR_CORRECT_H
}

class FileQrcoder:
    qrcode_capacity:int = None  # max capacity in byte of QR CODE 
    qrcode_version:int = None  # QR code version，1-40, more version, more information, and larger QR code
    qrcode_box_size:int = None # each pixel size which is default by 1
    qrcode_error_correct:int = None  # fault tolerance, L(7%)，M(15%)，Q(25%)，H(30%)
    index_len = 5 # index length of slice of base64 string is 8 bytes
    max_index_len = 5 # index length of max slice number
    
    def __init__(self, qrcode_version:int=40, qrcode_error_correct:str='L', qrcode_box_size:int=4, sk:int=None, logger_file:str=None):
        self.logger_file = 'fileqrcoder.log' if logger_file is None else logger_file
        f_handler = logging.FileHandler(self.logger_file)
        f_handler.setLevel(logging.DEBUG)
        f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
        self.logger = logging.getLogger()
        self.logger.addHandler(f_handler)
        self.logger.info(f'Initialize a FileQrcoder instance. qrcode_version = {qrcode_version}, qrcode_error_correct = {qrcode_error_correct}, sk={sk}')
        self.qrcode_version = qrcode_version
        self.qrcode_error_correct = ERROR_CORRECT_MAP[qrcode_error_correct]
        self.qrcode_capacity = QRCODE_VERSIONS[qrcode_version][qrcode_error_correct]
        self.qrcode_box_size = qrcode_box_size
        self.sk = sk
        return

    # generate base64 symbol table
    def gen_base64_symbols(self):
        return [chr(ord('A')+i) for i in range(26)] + [chr(ord('a')+i) for i in range(26)] + [chr(ord('0')+i) for i in range(10)] + ['+', '/']
    
    # generate replace table for encryption 
    def gen_replace_table(self):
        random.seed(self.sk)
        base64_symbols = self.gen_base64_symbols()
        shuffled_base64_symbols = self.gen_base64_symbols()
        random.shuffle(shuffled_base64_symbols)
        replace_table = {}
        for i in range(len(base64_symbols)):
            replace_table[ord(base64_symbols[i])] = ord(shuffled_base64_symbols[i])
        return replace_table
    
    # base64 encode the file
    def file_to_base64_str(self):
        with open(self.infile, 'rb') as f: # read file 
            binary_data = f.read()
        base64_str = base64.b64encode(binary_data).decode('utf-8') # base64 encode
        self.logger.debug(f'base64 string = {base64_str}')
        if self.sk != None: # encrypt the result base64 string with secret key 'sk'
            self.logger.debug('encrypting the result base64 string ...')
            replace_table = self.gen_replace_table()
            encrypted_base64_str = self.encrypt_base64_str(base64_str, replace_table)
            self.logger.debug(f'encrypted base64 string = {encrypted_base64_str}')
        
        return base64_str
    
    # encrypt base64 string with 'replace table'
    def encrypt_base64_str(self, base64_str:str, replace_table:dict):
        return base64_str.translate(replace_table)
    
    # generate one QR code for a given string
    def gen_qrcode(self, data:str):
        if len(data) > self.qrcode_capacity:
            raise BaseException(f"len(data) = {len(data)} != qrcode_capacity = {self.qrcode_capacity}")
        qr = qrcode.QRCode(
            version=self.qrcode_version,
            error_correction=self.qrcode_error_correct,
            box_size=self.qrcode_box_size,  # each pixel size which is default by 1
            border=4,  # frame width which is default by 4
        )
        qr.add_data(data) # add data
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white") # create QR code image
        return img
    
    # put an index (index_len bytes) in the front of each slice of base64 string
    def embed_index(self, base64_str:str):
        slice_len = self.qrcode_capacity - self.index_len - self.max_index_len
        slice_num = math.ceil(len(base64_str) / slice_len)
        self.logger.debug(f'slice_num = {slice_num}')
        max_slice_id = int('9'*self.max_index_len)
        if slice_num >= max_slice_id:
            raise BaseException(f'slice num = {slice_num} should be less than max_slice_id = {max_slice_id}')
        r = ''
        for i in range(slice_num):
            start = i * slice_len
            end = min((i + 1) * slice_len, len(base64_str))
            r += f'{str(i).zfill(self.index_len)}{str(slice_num).zfill(self.max_index_len)}{base64_str[start:end]}'
        return r

    def gen_qrcodes_from_file(self, start_id:int, end_id:int, id:str):
        for i in range(start_id, end_id):
            start = i * self.qrcode_capacity
            end = min((i + 1) * self.qrcode_capacity, len(self.data))
            self.logger.info(f'generate {i - start_id}-th / {end_id - start_id} where range is [ {start_id, end_id}) and image id is {i}, {round((end-start) / 1024 / (4/3), 3)} KB')
            slice_str = self.data[start:end]
            self.logger.debug(f'slice_str = {slice_str}')
            img_path = os.path.join(self.qrcodes_dir, f"{self.identity}qrcode_{str(i).zfill(self.index_len)}.png")
            self.logger.debug(f'img_path = {img_path}')
            img = self.gen_qrcode(slice_str)
            img.save(img_path)
        return
    
    # generate QR codes for the given file, and put the resulting QR code images in 'qrcodes_dir'
    def gen_qrcodes_from_file_in_parallel(self, infile:str, qrcodes_dir:str=None, identity:str=None, processes:int = None):
        '''
        Generate QR codes for the given file, and put the resulting QR code images in 'qrcodes_dir'
          'infile': the input file path
          'sk': it is used as secret key enhance privacy, and is None by default
          'qrcodes_dir': the directory for storing all resulting QR code images
        '''
        processes = os.cpu_count() if processes == None else processes
        self.infile = infile
        self.qrcodes_dir = './qrcodes/' if qrcodes_dir is None else qrcodes_dir
        os.makedirs(self.qrcodes_dir, exist_ok=True)
        self.identity = '' if identity is None else identity

        base64_str = self.file_to_base64_str()
        self.data = self.embed_index(base64_str)
        self.logger.debug(f'data = {self.data}')
        self.total_num_of_qrcodes = math.ceil(len(self.data) / self.qrcode_capacity)
        self.logger.info(f'total number of qrcodes = {self.total_num_of_qrcodes}')
        intervals = utils.split_range_equally(0, self.total_num_of_qrcodes, processes)
        self.logger.info(f'intervals = {intervals}')

        tasks = []
        for interval in intervals:
            self.logger.info(f'{interval}')
            task = multiprocessing.Process(target=self.gen_qrcodes_from_file, args=(interval[0], interval[1], id, ))
            tasks.append(task)
            task.start()
            
        for task in tasks:
            task.join()

        # all paths of the resulting QR code images
        img_paths = [os.path.join(self.qrcodes_dir, f"{self.identity}qrcode_{str(i).zfill(self.index_len)}.png") for i in range(self.total_num_of_qrcodes)]

        return img_paths
    
    # return a list of ids of all missed slices
    def find_missed_slices(self, all_slices:dict):
        max_slice_id = all_slices['max_slice_id']
        self.logger.debug(f'max_slice_id = {max_slice_id}')
        missed_slice_ids = []
        for i in range(max_slice_id):
            if str(i) not in all_slices:
                missed_slice_ids.append(i)
        return missed_slice_ids
    
    # concatenate all slice information
    def concat_all_slices(self, all_slices:dict):
        max_slice_id =  all_slices['max_slice_id']
        content = ''
        header_len = self.index_len+self.max_index_len
        for i in range(max_slice_id):
            self.logger.debug(f'concating {i} / {max_slice_id} slice')
            content += all_slices[str(i)][header_len:]
        return content
    
    # decode the given base64 string into bytes which is then written to file
    def base64_str_to_file(self, base64_str:str, outfile:str):
        decoded_bytes = base64.b64decode(base64_str)
        with open(outfile, 'wb') as f:
            f.write(decoded_bytes)
        return
    
    def recover_from_qrcode(self, qrcode_img:str):
        image = PIL.Image.open(qrcode_img)
        from pyzbar import pyzbar
        decoded_objects = pyzbar.decode(image)
        contents = [obj.data for obj in decoded_objects]
        return contents

    def parse_content(self, content_bytes:bytes):
        content = content_bytes.decode("utf-8")
        if len(content) <= self.index_len + self.max_index_len:
            self.logger.info(f'length of content ({len(content)}) is less than header length ({self.index_len + self.max_index_len})')
            return None, None, None
        try:
            slice_id = int(content[:self.index_len])
            max_slice_id = int(content[self.index_len:(self.index_len + self.max_index_len)])
        except Exception as e:
            self.logger.error(f'parse error:{str(e)}')
            return None, None, None
        return slice_id, max_slice_id, content
    
    def recover_slices_from_qrcodes_in_parallel(self, qrcodes:list, processes:int = None, report_dir:str=None):
        processes = os.cpu_count() if processes == None else processes
        intervals = utils.split_range_equally(0, len(qrcodes), processes)
        self.logger.info(f'intervals = {intervals}')
        tasks, reports = [], []
        report_dir = f'report_{utils.timestamp_str()}' if report_dir is None else report_dir
        os.makedirs(report_dir, exist_ok=True)
        pid = 0
        for interval in intervals:
            qrcodes_sub = qrcodes[interval[0]:interval[1]]
            report = os.path.join(report_dir, f'report_{str(interval[0]).zfill(6)}_{str(interval[1]).zfill(6)}.json')
            reports.append(report)
            self.logger.info(f'{interval}: prepare report_file = {report}')
            task = multiprocessing.Process(target=self.recover_slices_from_qrcodes, args=(pid, qrcodes_sub, report,))
            tasks.append(task)
            task.start()
            pid += 1
        
        for task in tasks:
            task.join()
        final_reports = []
        for report in reports:
            if os.path.isfile(report):
                final_reports.append(report)
        if len(final_reports) == 0:
            self.logger.info(f'remove empty report dir {report_dir}')
            os.rmdir(report_dir)
        self.logger.info(f'intervals = {intervals}')
        return final_reports
    
    # recover a file from the given list of QR Code images
    # def recover_slices_from_qrcodes(self, qrcode_imgs:list, outfile:str = './recovered_file'):
    def recover_slices_from_qrcodes(self, process_id:int, qrcode_imgs:list, report:str = './report.json'):
        print(f'recover_slices_from_qrcodes: len(qrcode_imgs) = {len(qrcode_imgs)}')
        from pyzbar import pyzbar
        from PIL import Image
        all_slices = {}
        max_slice_id = None
        for i in range(len(qrcode_imgs)):
            self.logger.info(f'{process_id}-th process: recover {i} / {len(qrcode_imgs)}, {qrcode_imgs[i]}')
            image = Image.open(qrcode_imgs[i])
            decoded_objects = pyzbar.decode(image)
            if len(decoded_objects) == 0:
                self.logger.info(f'no qr code inside {i}-th image')
                continue
            for obj in decoded_objects:
                slice_id, max_slice_id, content = self.parse_content(obj.data)
                if slice_id is None:
                    time_str = time.strftime('%m%d%H%M%S')
                    tmp_report = f'{report}.{time_str}.tmp.json'
                    with open(report + '.tmp.json', 'w') as f:
                        json.dump(all_slices, f)
                    self.logger.error(f'temp report is saved in file {tmp_report}, skip {i}-th images {qrcode_imgs[i]}')
                    continue
                self.logger.info(f'{process_id}-th process: recover {i} / {len(qrcode_imgs)}, {round((len(content)) / 1024 / (4/3), 3)} KB, slice_id = {slice_id}, img path = {qrcode_imgs[i]}')
                all_slices[slice_id] = content
       
        if max_slice_id is None: # save resolved slices
            self.logger.info('not found any qrcode')
            return None
        all_slices['max_slice_id'] = max_slice_id
        missed_slice_ids = self.find_missed_slices(all_slices)
        all_slices['missed_slice_ids'] = missed_slice_ids
        with open(report, 'w') as f:
            json.dump(all_slices, f)
        return all_slices
    
    def save_slices(self, slices:dict, path:str=None):
        self.logger.info('save slices')
        path = 'slices.json' if path is None else path
        if len(slices) % 10 == 0 or slices['max_slice_id'] == len(slices) - 1:
            with open(path, 'w') as f:
                json.dump(slices, f)
        return
    
    def load_slices(self, path:str=None):
        self.logger.info('loading slices')
        path = 'slices.json' if path is None else path
        with open(path) as f:
            slices = json.load(f)
        return slices
    
    def recover_from_camera(self, fps:float=None, exist_slices_path:str=None):
        import cv2
        fps = 20 if fps is None else fps
        self.width = 720
        self.height = 720
        stream_url = "http://192.168.1.5:8080/video"
        self.cap = cv2.VideoCapture(stream_url)
        self.logger.info(f'CAP_PROP_FRAME_WIDTH = {self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}')
        self.logger.info(f'CAP_PROP_FRAME_HEIGHT = {self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}')
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.logger.info(f'CAP_PROP_FRAME_WIDTH = {self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}')
        self.logger.info(f'CAP_PROP_FRAME_HEIGHT = {self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}')
        outdir = 'camera'
        os.makedirs(outdir, exist_ok=True)
        MAX_IMG_ID = 100000
        img_id = 0
        exist_slices_path = 'slices.json'
        all_slices = {} if exist_slices_path is None else self.load_slices(exist_slices_path)
        while True:
            success, img = self.cap.read() # read a frame
            if success:
                cv2.imshow("FileQrcoder", img)
                interval = round(1000 / fps)
                img_id = (img_id + 1) % MAX_IMG_ID
                img_path = os.path.join(outdir, f'{str(img_id).zfill(math.ceil(math.log10(MAX_IMG_ID)))}.jpg')
                cv2.imwrite(img_path, img)
                contents = self.recover_from_qrcode(img_path)
                self.logger.info(f"detected {len(contents)} object inside {img_path}")
                for i in range(len(contents)):
                    slice_id, max_slice_id, content = self.parse_content(contents[i])
                    if slice_id is not None:
                        progress = (len(all_slices) - 1) / max_slice_id
                        self.logger.info(f"{i}-th: progress = {progress}, slice_id = {slice_id}, max_slice_id = {max_slice_id}, length of content is {len(content)}")
                        all_slices[slice_id] = content
                        all_slices['max_slice_id'] = max_slice_id
                        self.save_slices(all_slices)
                cv2.waitKey(interval)
            else:
                self.logger.info(f'failed to read frame: {success}')
                break
        return
    # recover file from slices
    def recover_file_from_slices(self, slices:dict, outfile='./outfile'):
        content = self.concat_all_slices(slices)
        base64_str = content
        if self.sk is not None:
            base64_str = content
        self.base64_str_to_file(base64_str, outfile)
        return
    
    def recover_file_from_report(self, report:str='report.json', outfile='./outfile'):
        self.logger.info(f'report = {report}, outfile = {outfile}')
        with open(report) as f:
            r = json.load(f)
        missed_slice_ids = r['missed_slice_ids']
        max_slice_id = r['max_slice_id']
        if len(missed_slice_ids) > 0:
            self.logger.error(f'{len(missed_slice_ids)} slices are missed (max slice id = {max_slice_id}), miss rate is {round(len(missed_slice_ids)/max_slice_id * 100, 2)}%')
            return
        self.recover_file_from_slices(r, outfile)
        return

    # merge all reports, i.e., merge all dictionaries
    def merge_reports(self, reports:list, merged_report:str=None):
        merged_report = f'report_{utils.timestamp_str()}.json' if merged_report is None else merged_report
        self.logger.info(f'merge reports: {reports} => {merged_report}')
        slices = {}
        for report in reports:
            with open(report) as f:
                slices.update(json.load(f))
        max_slice_id = slices['max_slice_id']
        missed_slice_ids = []
        for i in range(max_slice_id):
            if str(i) not in slices:
                missed_slice_ids.append(i)
        slices['missed_slice_ids'] = missed_slice_ids
        with open(merged_report, 'w') as f:
            json.dump(slices, f)
        return merged_report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FileQrcoder: convert a file into a list of QR code images')
    subparsers = parser.add_subparsers( dest="command", title="available commands", metavar="command")
    parser_encode = subparsers.add_parser("encode", help="encode file into QR Code images", description="encode file into QR Code images")
    parser_encode.add_argument('--infile', type=str, help='file to be encoded', required=True)
    parser_encode.add_argument('--sk', type=int, default=None, help='secret key (a integer)')
    parser_encode.add_argument('--qrcode_version', type=int, default=27, help='qrcode version (1-40)')
    parser_encode.add_argument('--qrcode_box_size', type=int, default=4, help='number of pixels of “box” of QR code')
    parser_encode.add_argument('--id', type=str, default=None, help='batch id of this time')
    parser_encode.add_argument('--outdir', type=str, default=None, help='directory used to store all qrcode images')

    parser_decode = subparsers.add_parser("decode", help="recover a file from the given list of images containing QR codes", description="recover a file from the given list of images containing QR codes")
    parser_decode.add_argument('--indir', type=str, default=None, help='directory of your images')
    parser_decode.add_argument('--infile', type=str, default=None, help='a qrcode image')
    parser_decode.add_argument('--outdir', type=str, default=None, help='output directory of generated JSON reports')
    parser_decode.add_argument('--outfile', type=str, default=None, help='output file of JSON report')
    
    parser_decodelist = subparsers.add_parser("decodelist", help="recover a file from the given list of images containing QR codes", description="recover a file from the given list of images containing QR codes")
    parser_decodelist.add_argument('--listfile', type=str, help='images id list file', required=True)
    parser_decodelist.add_argument('--cmdfile', type=str, help='command file', required=True)
    
    parser_decodecamera = subparsers.add_parser("decodecamera", help="recover a file from camera", description="recover a file from camera")
    # parser_decode.add_argument('--listfile', type=str, help='images id list file', required=True)
    # parser_decode.add_argument('--cmdfile', type=str, help='command file', required=True)

    parser_merge = subparsers.add_parser("merge", help="merge all JSON reports", description="merge all JSON reports")
    parser_merge.add_argument('--indir', type=str, help='directory of your JSON reports', required=True)
    parser_merge.add_argument('--outfile', type=str, default=None, help='path or name of the merged report')
    
    parser_recover = subparsers.add_parser("recover", help="recover a file from your report", description="recover a file from you report")
    parser_recover.add_argument('--report', type=str, help='your JSON report file', required=True)
    parser_recover.add_argument('--outfile', type=str, default='recover.out', help='outoput file')
    parser_recover.add_argument('--sk', type=int, default=None, help='secret key (a integer)')
    
    parser_image2video = subparsers.add_parser("image2video", help="recover a file from your report", description="recover a file from you report")
    parser_image2video.add_argument('--indir', type=str, help='directory of qrcode images', required=True)
    parser_image2video.add_argument('--outfile', type=str, default=None, help='name of output video')
    parser_image2video.add_argument('--fps', type=float, default=15.0, help='frames per second')
    
    parser_video2image = subparsers.add_parser("video2image", help="extrac all frames of a video", description="extrac all frames of a video")
    parser_video2image.add_argument('--infile', type=str, help='a video file', required=True)
    parser_video2image.add_argument('--outdir', type=str, default=None, help='directory used to store all frames of the video')
    
    parser_video2audio = subparsers.add_parser("video2audio", help="extract the audio of a video", description="extract the audio of a video")
    parser_video2audio.add_argument('--infile', type=str, help='a video file', required=True)
    parser_video2audio.add_argument('--outfile', type=str, default=None, help='path of the extracted audio file')
    
    parser_addaudio = subparsers.add_parser("addaudio", help="add audio to a slient video", description="add audio to a slient video")
    parser_addaudio.add_argument('--video', type=str, help='your video file', required=True)
    parser_addaudio.add_argument('--audio', type=str, default=None, help='your audio file')
    parser_addaudio.add_argument('--outfile', type=str, default=None, help='path of the extracted audio file')
    
    parser_descvideo = subparsers.add_parser("descvideo", help="describe the video", description="describe the video")
    parser_descvideo.add_argument('--video', type=str, help='your video file', required=True)
    
    parser_compressvideo = subparsers.add_parser("compressvideo", help="compress the video", description="compress the video")
    parser_compressvideo.add_argument('--infile', type=str, help='original video file', required=True)
    parser_compressvideo.add_argument('--outfile', type=str, default=None, help='compressed video file')
    parser_compressvideo.add_argument('--width', type=int, help='width', required=True)
    parser_compressvideo.add_argument('--height', type=int, help='height', required=True)
    parser_compressvideo.add_argument('--bitrate', type=int, help='bit rate', required=True)
    parser_compressvideo.add_argument('--fps', type=float, help='frame per second (float type)', required=True)
    
    parser_concatimage = subparsers.add_parser("concatimage", help="concat images vertically or horizontally", description="concat images vertically or horizontally")
    parser_concatimage.add_argument('--indir', type=str, help='directory of all input images', required=True)
    parser_concatimage.add_argument('--rows', type=int, help='row number', required=True)
    parser_concatimage.add_argument('--cols', type=int, help='column number', required=True)
    parser_concatimage.add_argument('--outdir', type=str, default=None, help='directory of all concatented images')
    parser_concatimage.add_argument('--interval', type=int, default=None, help='image interval')
    
    parser_splitimage = subparsers.add_parser("splitimage", help="split images", description="split images")
    parser_splitimage.add_argument('--indir', type=str, help='directory of all input images', required=True)
    parser_splitimage.add_argument('--rows', type=int, help='row number', required=True)
    parser_splitimage.add_argument('--cols', type=int, help='column number', required=True)
    parser_splitimage.add_argument('--outdir', type=str, default=None, help='directory of all splited images')
    
    parser_flipimage = subparsers.add_parser("flipimage", help="flip images horizontally or vertically", description="flip images horizontally or vertically")
    parser_flipimage.add_argument('--infile', type=str, help='directory of all input images', required=True)
    parser_flipimage.add_argument('--direction', type=str, help='vertical or horizontal', required=True)
    parser_flipimage.add_argument('--outfile', type=str, default=None, help='path of the flipped image')
    
    parser_image2gif = subparsers.add_parser("image2gif", help="convert a list of images into a GIF picture", description="convert a list of images into a GIF picture")
    parser_image2gif.add_argument('--indir', type=str, help='directory of all input images', required=True)
    parser_image2gif.add_argument('--outfile', type=str, default=None, help='path of the GIF')
    parser_image2gif = subparsers.add_parser("compress", help="compress a file", description="compress a file")
    parser_image2gif.add_argument('--infile', type=str, help='input file', required=True)
    parser_image2gif.add_argument('--outfile', type=str, default=None, help='output file')
    parser_image2gif.add_argument('--level', type=int, default=None, help='ZSTD compress level')
    
    parser_image2gif = subparsers.add_parser("decompress", help="decompress a file", description="decompress a file")
    parser_image2gif.add_argument('--infile', type=str, help='input file', required=True)
    parser_image2gif.add_argument('--outfile', type=str, default=None, help='output file')
    
  
    args = parser.parse_args()
    
    if not hasattr(args, "command") or args.command is None:
        parser.print_help()
    if args.command == 'encode':
        print(f'+++++ encode +++++')
        print(f'input file = {args.infile}, sk = {args.sk}\n')
        fq_encode = FileQrcoder(qrcode_version=args.qrcode_version, qrcode_box_size=args.qrcode_box_size, sk=args.sk)
        qrcode_img_paths = fq_encode.gen_qrcodes_from_file_in_parallel(args.infile, qrcodes_dir=args.outdir, identity=args.id) 
        print(qrcode_img_paths)
    elif args.command == 'decode':
        print(f'+++++ decode +++++')
        if args.indir is not None: # many qrcode images
            print(f'indir = {args.indir}, outfile = {args.outdir}\n')
            qrcodes = os.listdir(args.indir)
            qrcodes.sort()
            qrcodes = [os.path.join(args.indir, qrcode) for qrcode in qrcodes]
            for i in range(len(qrcodes)):
                if qrcodes[i][-5:] == '.HEIC':
                    png_qrcode = f'{qrcodes[i][:-5]}.png'
                    utils.heic_to_png(qrcodes[i], png_qrcode)
                    qrcodes[i] = png_qrcode
            print(qrcodes)
            fq_decode = FileQrcoder()
            reports = fq_decode.recover_slices_from_qrcodes_in_parallel(qrcodes, report_dir=args.outdir)
            print(f'\nreports = {reports}')
        elif args.infile is not None: # single one qrcode image
            fq = FileQrcoder(sk=args.sk)
            contents = fq.recover_from_qrcode(args.infile)
            for c in contents:
                print(f'{c}\n')
        else:
            print('one of --indir and --infile must not be empty')
    elif args.command == 'decodelist':
        print(f'+++++ decode from image list +++++')
        print(f'listfile = {args.listfile}, cmdfile = {args.cmdfile}\n')
        old_batch_id = ''
        while True:
            print('decode by image list ... ')
            with open(args.cmdfile, 'w') as f:
                f.write('batch')
            time.sleep(1)
            if os.path.isfile(args.listfile):
                with open(args.listfile) as f:
                    lines = [line.strip() for line in f.readlines()]
                batch_id = lines[0]
                if batch_id == old_batch_id:
                    print(f'batch_id {batch_id} == old_batch_id {old_batch_id}')
                    continue
                qrcodes = lines[1:]
                print(qrcodes)
                fq_decode = FileQrcoder()
                reports = fq_decode.recover_slices_from_qrcodes_in_parallel(qrcodes, report_dir=f'batch/batch_{batch_id}')
                print(f'\nreports = {reports}')
                if len(reports) == 0:
                    print(f'no qrcode is found, sleep for a while')
                    time.sleep(5)
                else:
                    print(f'generate {len(reports)} reports')
                    time.sleep(2)
    elif args.command == 'decodecamera':
        print(f'+++++ decode from camera +++++')
        fq = FileQrcoder()
        fq.recover_from_camera()
        print(f'----- decode from camera -----')
    elif args.command == 'merge':
        print(f'+++++ merge +++++')
        print(f'indir = {args.indir}')
        fq = FileQrcoder()
        reports = os.listdir(args.indir)
        reports = [os.path.join(args.indir, report) for report in reports]
        merged_report = fq.merge_reports(reports, args.outfile)
        print(f'merged report: {merged_report}')
    elif args.command == 'recover':
        print(f'+++++ recover +++++')
        print(f'report = {args.report}, outfile = {args.outfile}')
        fq = FileQrcoder(sk=args.sk)
        fq.recover_file_from_report(args.report, args.outfile)
        print(f'report = {args.report}, outfile = {args.outfile}')
    elif args.command == 'image2video':
        print(f'+++++ image2video +++++')
        video_trt = utils.evaluate_video_total_running_time(args.indir, args.fps)
        if video_trt > 120:
            user_input = input('The video longer than 2 minutes, do you still want to proceed? ').strip()
            if user_input == 'N' or user_input == "n":
                sys.exit()
        images = os.listdir(args.indir)
        images = [os.path.join(args.indir, image) for image in images]
        outfile = utils.imgs_to_video(images, outfile=args.outfile, fps=args.fps)
        print(f'output video: {outfile}')
    elif args.command == 'video2image':
        print(f'+++++ video2image +++++')
        utils.extract_frames(args.infile, args.outdir)
    elif args.command == 'video2audio':
        print(f'+++++ video2audio +++++')
        print(args.infile, args.outfile)
        utils.extract_audio(args.infile, args.outfile)
    elif args.command == 'addaudio':
        print(f'+++++ addaudio +++++')
        print(args.video, args.audio, args.outfile)
        utils.add_audio(args.video, args.audio, args.outfile)
    elif args.command == 'descvideo':
        print(f'+++++ descvideo +++++')
        utils.describe_video(args.video)
    elif args.command == 'compressvideo':
        print(f'+++++ compressvideo +++++')
        utils.compress_video(args.infile, args.width, args.height, args.bitrate, args.fps, args.outfile)
    elif args.command == 'concatimage':
        print(f'+++++ concatimage +++++')
        images = os.listdir(args.indir)
        images.sort()
        images = [os.path.join(args.indir, image) for image in images]
        utils.concat_img(images, args.rows, args.cols, interval=0)
    elif args.command == 'splitimage':
        print(f'+++++ splitimage +++++')
        images = os.listdir(args.indir)
        images.sort()
        images = [os.path.join(args.indir, image) for image in images]
        utils.split_image(images, args.rows, args.cols, args.outdir)
    elif args.command == 'flipimage':
        print(f'+++++ flipimage +++++')
        utils.flip_image(args.infile, args.outfile, args.direction)
    elif args.command == 'image2gif':
        print(f'+++++ image2gif +++++')
        images = os.listdir(args.indir)
        images.sort()
        images = [os.path.join(args.indir, image) for image in images]
        utils.images2gif(images, args.outfile)
    elif args.command == 'compress':
        print(f'+++++ compress +++++')
        utils.compress_file(args.infile, args.outfile, level=args.level)    
    elif args.command == 'decompress':
        print(f'+++++ decompress +++++')
        utils.decompress_file(args.infile, args.outfile)
