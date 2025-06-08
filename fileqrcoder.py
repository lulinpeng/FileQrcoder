import qrcode
import base64
import logging
import math
import random
import os
import json
import time

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

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
    
    def __init__(self, qrcode_version:int=40, qrcode_error_correct:str='L', qrcode_box_size:int=4, sk:int=None):
        logging.info(f'Initialize a FileQrcoder instance. qrcode_version = {qrcode_version}, qrcode_error_correct = {qrcode_error_correct}, sk={sk}')
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
        logging.debug(f'base64 string = {base64_str}')
        if self.sk != None: # encrypt the result base64 string with secret key 'sk'
            logging.debug('encrypting the result base64 string ...')
            replace_table = self.gen_replace_table()
            encrypted_base64_str = self.encrypt_base64_str(base64_str, replace_table)
            logging.debug(f'encrypted base64 string = {encrypted_base64_str}')
        
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
        logging.debug(f'slice_num = {slice_num}')
        max_slice_id = int('9'*self.max_index_len)
        if slice_num >= max_slice_id:
            raise BaseException(f'slice num = {slice_num} should be less than max_slice_id = {max_slice_id}')
        r = ''
        for i in range(slice_num):
            start = i * slice_len
            end = min((i + 1) * slice_len, len(base64_str))
            r += f'{str(i).zfill(self.index_len)}{str(slice_num).zfill(self.max_index_len)}{base64_str[start:end]}'
        return r

    # generate QR codes for the given file, and put the resulting QR code images in 'qrcodes_dir'
    def gen_qrcodes_from_file(self, infile:str, qrcodes_dir:str = './qrcodes/', id:str=''):
        '''
        Generate QR codes for the given file, and put the resulting QR code images in 'qrcodes_dir'
          'infile': the input file path
          'sk': it is used as secret key enhance privacy, and is None by default
          'qrcodes_dir': the directory for storing all resulting QR code images
        '''
        self.infile = infile
        self.qrcodes_dir = qrcodes_dir
        os.makedirs(qrcodes_dir, exist_ok=True)

        base64_str = self.file_to_base64_str()
        data = self.embed_index(base64_str)
        logging.debug(f'data = {data}')
        num = math.ceil(len(data) / self.qrcode_capacity)
        img_paths = [] # all paths of the resulting QR code images
        for i in range(num):
            start = i*self.qrcode_capacity
            end = min((i+1)*self.qrcode_capacity, len(data))
            logging.info(f'generate {i} / {num}, {round((end-start) / 1024 / (4/3), 3)} KB')
            slice_str = data[start:end]
            logging.debug(f'slice_str = {slice_str}')
            img_path = f"{self.qrcodes_dir}{id}qrcode_{str(i).zfill(self.index_len)}.png"
            logging.debug(f'img_path = {img_path}')
            img = self.gen_qrcode(slice_str)
            img.save(img_path)
            img_paths.append(img_path)

        return img_paths
    
    # return a list of ids of all missed slices
    def find_missed_slices(self, all_slices:dict):
        max_slice_id = all_slices['max_slice_id']
        missed_slice_ids = []
        for i in range(max_slice_id):
            if i not in all_slices:
                missed_slice_ids.append(i)
        return missed_slice_ids
    
    # concatenate all slice information
    def concat_all_slices(self, all_slices:dict):
        max_slice_id =  all_slices['max_slice_id']
        content = ''
        header_len = self.index_len+self.max_index_len
        for i in range(max_slice_id):
            print(f'concating {i} / {max_slice_id} slice')
            content += all_slices[str(i)][header_len:]
        return content
    
    # decode the given base64 string into bytes which is then written to file
    def base64_str_to_file(self, base64_str:str, outfile:str):
        decoded_bytes = base64.b64decode(base64_str)
        with open(outfile, 'wb') as f:
            f.write(decoded_bytes)
        return
            
    # recover a file from the given list of QR Code images
    # def recover_slices_from_qrcodes(self, qrcode_imgs:list, outfile:str = './recovered_file'):
    def recover_slices_from_qrcodes(self, qrcode_imgs:list, report:str = './report.json'):
        from pyzbar import pyzbar
        from PIL import Image
        all_slices = {}
        for i in range(len(qrcode_imgs)):
            print(f'recover {i} / {len(qrcode_imgs)}, {qrcode_imgs[i]}')
            image = Image.open(qrcode_imgs[i])
            
            decoded_objects = pyzbar.decode(image)
            if len(decoded_objects) == 0:
                print(f'no qr code inside {i}-th image')
                continue
            for obj in decoded_objects:
                content = obj.data.decode("utf-8")
                idx = content[:self.index_len]
                max_idx = int(content[self.index_len:(self.index_len + self.max_index_len)])
                print(f'recover {i} / {len(qrcode_imgs)}, {round((len(content)) / 1024 / (4/3), 3)} KB, idx = {idx}, img path = {qrcode_imgs[i]}')
                try:
                    slice_id = int(content[:self.index_len])
                except:
                    raise BaseException(f'The content of {qrcode_imgs[i]} is invalid')
                all_slices[slice_id] = content
        # save resolved slices
        all_slices['max_slice_id'] = max_idx
        missed_slice_ids = self.find_missed_slices(all_slices)
        all_slices['missed_slice_ids'] = missed_slice_ids
        with open(report, 'w') as f:
            json.dump(all_slices, f)
        return all_slices
    
    # recover file from slices
    def recover_file_from_slices(self, slices:dict, outfile='./outfile'):
        content = self.concat_all_slices(slices)
        base64_str = content
        if self.sk is not None:
            base64_str = content
        self.base64_str_to_file(base64_str, outfile)
        return

    # merge all slices reports, i.e., merge dictionaries
    def merge_slice_report(self, reports:list):
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
        return slices
