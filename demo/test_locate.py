from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode

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
