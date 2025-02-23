import qrcode
import base64
import logging
import math
import random
import sys

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

QR_CODE_CAPATITY_BYTES = 2953 # max capacity in byte of QR CODE 
INDEX_LENGTH = 8 # index length of slice of base64 string is 8 bytes

class FileQrcoder:
    QR_CODE_CAPATITY_BYTES = 2953  # max capacity in byte of QR CODE 
    
    def __init__(self, file:str, sk:int = None, qrcodes_dir:str = './'):
        '''
        'file': the target file path
        'sk': it is used as secret key enhance privacy, and is None by default
        'qrcodes_dir': the directory for storing all resulting QR code images
        '''
        self.file = file
        self.sk = sk
        self.qrcodes_dir = qrcodes_dir
        logging.info(f'file = {self.file}, secret key = {self.sk}, qrcodes directory = {self.qrcodes_dir}')
        
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
        with open(self.file, 'rb') as f: # read file 
            binary_data = f.read()
        base64_str = base64.b64encode(binary_data).decode('utf-8') # base64 encode
        logging.debug(f'base64 string = {base64_str}')
        if sk != None: # encrypt the result base64 string with secret key 'sk'
            logging.debug('encrypting the result base64 string ...')
            replace_table = self.gen_replace_table()
            encrypted_base64_str = self.encrypt_base64_str(base64_str, replace_table)
            logging.debug(f'encrypted base64 string = {encrypted_base64_str}')
            
        return base64_str
    
    # encrypt base64 string with 'replace table'
    def encrypt_base64_str(self, base64_str:str, replace_table:dict):
        return base64_str.translate(replace_table)
    
    # generate one QR code
    def gen_qrcode(self, data:str):
        if len(data) > QR_CODE_CAPATITY_BYTES:
            raise f"len(data) = {len(data)} != QR_CODE_CAPATITY_BYTES = {QR_CODE_CAPATITY_BYTES}"
        qr = qrcode.QRCode(
            version=40,  # QR code version，1-40, more version, more information, and larger QR code
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # fault tolerance, L(7%)，M(15%)，Q(25%)，H(30%)
            box_size=10,  # each pixel size which is default by 1
            border=4,  # frame width which is default by 4
        )
        qr.add_data(data) # add data
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white") # create picture
        return img
    
    # put an index (8 bytes) in the front of each slice of base64 string
    def embed_index(self, base64_str:str):
        slice_len = self.QR_CODE_CAPATITY_BYTES - 8
        slice_num = math.ceil(len(base64_str) / slice_len)
        logging.debug(f'slice_num = {slice_num}')
        r = ''
        for i in range(slice_num):
            start = i*slice_len
            end = min((i+1)*slice_len, len(base64_str))
            r += (str(i).zfill(8)+base64_str[start:end])
        return r
            
    # generate QR codes for the given file
    def gen_qrcodes(self):
        base64_str = self.file_to_base64_str()
        data = self.embed_index(base64_str)
        logging.debug(f'data = {data}')
        num = math.ceil(len(data) / self.QR_CODE_CAPATITY_BYTES)
        imgs = []
        for i in range(num):
            start = i*self.QR_CODE_CAPATITY_BYTES
            end = min((i+1)*self.QR_CODE_CAPATITY_BYTES, len(data))
            logging.info(f'{i} / {num}, {round((end-start) / 1024 / (4/3), 3)} KB')
            slice_str = data[start:end]
            logging.debug(f'slice_str = {slice_str}')
            img = self.gen_qrcode(slice_str)
            img_path = f"{self.qrcodes_dir}qrcode_{str(i).zfill(8)}.png"
            img.save(img_path)
            imgs.append(img_path)
        return imgs


if __name__ == '__main__':
    logging.info(f'python3 file_qrcoder.py [YOUR FILE]')
    if len(sys.argv) == 1:
        file = sys.argv[0]
    else:
        file = sys.argv[1]
    sk = None # secret key, e.g., 1234, which is 'None' by default
    qrcodes_dir = './'
    fq = FileQrcoder(file, sk, qrcodes_dir)
    qrcode_imgs = fq.gen_qrcodes()
    logging.info(qrcode_imgs)
