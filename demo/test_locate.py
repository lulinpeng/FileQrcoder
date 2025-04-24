from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode

def check_valid(img:Image):
    barcodes = decode(image)
    if len(barcodes) != 4:
        error_msg = f'check_valid: len(barcodes) = {len(barcodes)} != 4'
        print(error_msg)
        return False
    
    orientations = [barcode.orientation for barcode in barcodes]
    if len(set(orientations)) != 1:
        error_msg = f'check_valid: set(orientations) = {set(orientations)} != 1, orientations = {orientations}'
        print(error_msg)
        return False
    orientation = orientations[0]

    codes = [int(barcode.data.decode('utf-8')) for barcode in barcodes]
    print(codes)
    max_code = max(codes)
    min_code = min(codes)
    if len(set(codes)) != (max_code - min_code + 1):
        error_msg = f'check_valid: codes are not continuous, codes = {codes}'
        print(error_msg)
        return False
    return True

if __name__ == '__main__':
    infile = 'random.png'
    print(f'locate and label all QR codes in the image {infile}')
    image = Image.open(infile).convert('RGB')
    draw = ImageDraw.Draw(image)
    barcodes = decode(image)
    print(f'len(barcodes) = {len(barcodes)}')
    for barcode in decode(image):
        print(f'barcode = {barcode}')
        rect = barcode.rect
        print(rect)
        x0, y0 = rect.left, rect.top
        x1, y1 = rect.left + rect.width, rect.top + rect.height
        draw.rectangle(((x0, y0), (x1, y1)), outline='#0080ff')
        draw.polygon(barcode.polygon, outline='#e945ff')
    image.save('out.png')
