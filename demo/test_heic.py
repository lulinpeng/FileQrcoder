import utils

if __name__ == '__main__':
    heic_path = '/Users/lulinpeng/Downloads/test.HEIC'
    png_path = 'test.png'
    utils.heic_to_png(heic_path, png_path)
    print(f'heic_path = {heic_path}')
    print(f'png_path = {png_path}')