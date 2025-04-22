from PIL import Image
import random
import math
import qrcode

def gen_and_save_qrcode(data:str, outfile:str='qrcode.png'):
    QR_CODE_CAPATITY_BYTES = 7 
    QR_CODE_VERSION = 1
    QR_CODE_ERROR_CORRECT = qrcode.constants.ERROR_CORRECT_H
    if len(data) > QR_CODE_CAPATITY_BYTES:
        error_msg = f'too many bytes: len(data) = {len(data)} > QR_CODE_CAPATITY_BYTES = {QR_CODE_CAPATITY_BYTES}'
        print(error_msg)
        raise error_msg
    qr = qrcode.QRCode(
        version=QR_CODE_VERSION,
        error_correction=QR_CODE_ERROR_CORRECT,
        box_size=3,  # each pixel size which is default by 1
        border=0,  # frame width which is default by 4
    )
    qr.add_data(data) # add data
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white") # create QR code image
    img.save(outfile)
    return

# get maximum and minimum distace among points
def max_min_dist(points:list):
    min_dist_sq = float('inf')
    max_dist_sq = 0.0
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist_sq = dx**2 + dy**2
            min_dist_sq = dist_sq if dist_sq < min_dist_sq else min_dist_sq
            max_dist_sq = dist_sq if dist_sq > max_dist_sq else max_dist_sq
    return math.sqrt(min_dist_sq), math.sqrt(max_dist_sq)

# generate random points
def gen_points(n:int, width:int, height:int, margin:int = 10):
    while True:
        points = [(random.random(), random.random()) for i in range(n)]
        min_dist, max_dist = max_min_dist(points)
        ratio = max_dist / min_dist
        print(f'ratio = {ratio}')
        if ratio < 10:
            diagonal_len = math.sqrt(width**2 + height**2)
            scale = math.ceil(diagonal_len / min_dist) * 1.1
            print(f'scale = {scale}')
            new_points = [(round(pos[0]*scale + margin), round(pos[1]*scale + margin)) for pos in points]
            total_height = max([pos[1] for pos in new_points]) + margin + math.ceil(diagonal_len)
            total_width = max([pos[0] for pos in new_points]) + margin + math.ceil(diagonal_len)
            return total_width, total_height, new_points

if __name__ == '__main__':
    n = 5
    png_files = []
    for i in range(n):
        data = str(i).zfill(7)
        file = f"qrcode_{data}.png"
        png_files.append(file)
        gen_and_save_qrcode(data, file)

    images = [Image.open(f).convert('RGB') for f in png_files]
    width, height = images[0].size
    print(f'width = {width}, height = {height}')

    total_width, total_height, new_points = gen_points(n, width, height)
    print(f'total_width = {total_width}, total_height = {total_height}')
    new_img = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    for i in range(len(images)):
        new_img.paste(images[i].rotate(random.random()*360, expand=True, fillcolor=(255,255,255)), new_points[i])
    outfile = 'random.png'
    new_img.save(outfile)
    print(f'output {outfile}')
