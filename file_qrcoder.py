import qrcode
import base64
import logging
import math
import random
import sys

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


class FileQrcoder:
    QR_CODE_CAPATITY_BYTES = 2953  # max capacity in byte of QR CODE 
    QR_CODE_VERSION = 40  # QR code version，1-40, more version, more information, and larger QR code
    QR_CODE_ERROR_CORRECT = qrcode.constants.ERROR_CORRECT_L  # fault tolerance, L(7%)，M(15%)，Q(25%)，H(30%)
    INDEX_LENGTH = 8 # index length of slice of base64 string is 8 bytes
    
    def __init__(self, sk:int = None):
        logging.info('Initialize a FileQrcoder instance')
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
        if len(data) > self.QR_CODE_CAPATITY_BYTES:
            raise f"len(data) = {len(data)} != QR_CODE_CAPATITY_BYTES = {self.QR_CODE_CAPATITY_BYTES}"
        qr = qrcode.QRCode(
            version=self.QR_CODE_VERSION,
            error_correction=self.QR_CODE_ERROR_CORRECT,
            box_size=3,  # each pixel size which is default by 1
            border=4,  # frame width which is default by 4
        )
        qr.add_data(data) # add data
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white") # create QR code image
        return img
    
    # put an index (INDEX_LENGTH bytes) in the front of each slice of base64 string
    def embed_index(self, base64_str:str):
        slice_len = self.QR_CODE_CAPATITY_BYTES - self.INDEX_LENGTH
        slice_num = math.ceil(len(base64_str) / slice_len)
        logging.debug(f'slice_num = {slice_num}')
        r = ''
        for i in range(slice_num):
            start = i*slice_len
            end = min((i+1)*slice_len, len(base64_str))
            r += (str(i).zfill(self.INDEX_LENGTH)+base64_str[start:end])
        return r

    # generate QR codes for the given file, and put the resulting QR code images in 'qrcodes_dir'
    def gen_qrcodes_from_file(self, infile:str, qrcodes_dir:str = './', sk:int = None):
        '''
        Generate QR codes for the given file, and put the resulting QR code images in 'qrcodes_dir'
          'infile': the input file path
          'sk': it is used as secret key enhance privacy, and is None by default
          'qrcodes_dir': the directory for storing all resulting QR code images
        '''
        self.sk = sk
        self.infile = infile
        self.qrcodes_dir = qrcodes_dir
        base64_str = self.file_to_base64_str()
        data = self.embed_index(base64_str)
        logging.debug(f'data = {data}')
        num = math.ceil(len(data) / self.QR_CODE_CAPATITY_BYTES)
        img_paths = [] # all paths of the resulting QR code images
        for i in range(num):
            start = i*self.QR_CODE_CAPATITY_BYTES
            end = min((i+1)*self.QR_CODE_CAPATITY_BYTES, len(data))
            logging.info(f'generate {i} / {num}, {round((end-start) / 1024 / (4/3), 3)} KB')
            slice_str = data[start:end]
            logging.debug(f'slice_str = {slice_str}')
            img_path = f"{self.qrcodes_dir}qrcode_{str(i).zfill(self.INDEX_LENGTH)}.png"
            logging.debug(f'img_path = {img_path}')
            img = self.gen_qrcode(slice_str)
            img.save(img_path)
            img_paths.append(img_path)

        return img_paths
        
    def check_slice_ids(self, slice_ids:list):
        min_slice_id = min(slice_ids)
        if min_slice_id != 0:
            logging.error(f'min_slice_id = {min_slice_id} != 0')
            raise 'min_slice_id != 0'
        max_slice_id = max(slice_ids)
        for i in range(max_slice_id+1):
            if i not in slice_ids:
                logging.error(f'the {i}-th slice is missing')
                raise 'some slice is missing'
        return
    
    def concat_all_slices(self, all_slices:dict):
        slice_ids = list(all_slices.keys())
        logging.debug(f'all slice ids are {slice_ids}')
        self.check_slice_ids(slice_ids)
        max_slice_id = max(slice_ids)
        content = ''
        for i in range(max_slice_id+1):
            content += all_slices[i]
        return content
    
    # convert the given base64 string into bytes array, and wirte the array to file
    def base64_str_to_file(self, base64_str:str, outfile:str):
        decoded_bytes = base64.b64decode(base64_str)
        with open(outfile, 'wb') as f:
            f.write(decoded_bytes)
            
    # recover a file from the given list of QR Code images
    def recover_file_from_qrcodes(self, qrcode_imgs:list, sk:int = None, outfile:str = './recovered_file'):
        from pyzbar.pyzbar import decode
        from PIL import Image
        all_slices = {}
        for i in range(len(qrcode_imgs)):
            image = Image.open(qrcode_imgs[i])
            decoded_objects = decode(image)
            for obj in decoded_objects:
                content = obj.data.decode("utf-8")
                logging.info(f'recover {i} / {len(qrcode_imgs)}, {round((len(content)) / 1024 / (4/3), 3)} KB')
                logging.debug(f'{content[:self.INDEX_LENGTH]}')
                try:
                    slice_id = int(content[:self.INDEX_LENGTH])
                except:
                    raise f'The content of {qrcode_imgs[i]} is invalid'
                all_slices[slice_id] = content[self.INDEX_LENGTH:]
            
        content = self.concat_all_slices(all_slices)
        base64_str = content
        if sk is not None:
            base64_str = content
        self.base64_str_to_file(base64_str, outfile)
        return outfile

if __name__ == '__main__':
    logging.info('python3 file_qrcoder.py [YOUR FILE]')
    # convert a file into a list of QR code images
    infile = sys.argv[0] if len(sys.argv) == 1 else sys.argv[1]
    logging.info(f'input file = {infile}')
    fq_encode = FileQrcoder()
    qrcode_img_paths = fq_encode.gen_qrcodes_from_file(infile, qrcodes_dir = './') 
    logging.info(qrcode_img_paths)
    
    # recover a file from the given list of QR code images
    fq_decode = FileQrcoder()
    outfile = fq_decode.recover_file_from_qrcodes(qrcode_img_paths)
    logging.info(f'output file ={outfile}')
