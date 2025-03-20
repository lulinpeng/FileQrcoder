# FileQrcoder
# INTRODUCTION
FileQrcoder is a basic tool used to convert a file in any format into a list of QRCode images. *Additionally, it also supports encrypting files and then converting them into QRCodes.*

![image](https://github.com/lulinpeng/FileQrcoder/blob/main/intro.png)

# REQUIREMENTS

| Num | target | System  |	Requirements |
|:--------:| :---------: | :---------:|:--------|
|1| test_encode.py | MacOS |```pip install qrcode==8.0 pillow==11.1.0```|
|2| test_decode.py | MacOS |```brew install zar, pip install pyzbar, export DYLD_LIBRARY_PATH=/opt/homebrew/lib/```|

# QUICK START
## First Attempt
```shell
cd FileQrcoder/
export PYTHONPATH="${PYTHONPATH}:${pwd}"

python3 demo/test_encode.py fileqrcoder.py # generate QR code images for file 'file_qrcoder.py'
ls -al qrcodes/
# qrcode_00000000.png
# qrcode_00000001.png
# qrcode_00000002.png
# qrcode_00000003.png


python3 demo/display_qrcodes.py # display the above QR code images
```

## Try Your File
```shell
cd FileQrcoder/
export PYTHONPATH="${PYTHONPATH}:${pwd}"

python3 demo/test_encode.py [PATH OF YOUR FILE] # generate QR code images for 'YOUR FILE'

export DYLD_LIBRARY_PATH=/opt/homebrew/lib/ # for 'libzbar.dylib'
python3 demo/test_decode.py
```

# BENCHMARK
Testing conducted on: **Apple MacBook Pro (13-inch, M1, 2020)**. Specs: Apple M1 chip (8-core CPU/GPU), 16GB RAM, macOS [Sequoia, 15.3.1] 
| Num | Size of input file | CPU cores  |	Num of QR code images | Total time | Rate |
|:--------:| :---------: | :---------:|:--------:| :--------: | :--------: |
|1| 497KB | 1 | 231 | 52 secs| 76.5kbps|


# DOCKER
## BUILD DOCKER IMAGE
```shell
cd FileQrcoder/
export image=fileqrcoder
docker build -t ${image} -f Dockerfile .
```
## TEST IMAGE
```shell
# MacOS
#example: test/a.txt
cd test
export target_file=a.txt target_dir=./ image=fileqrcoder
docker run -v ${target_dir}:/data ${image} sh -c 'cd /data/ && python3 /root/FileQrcoder/test_encode.py ${target_file}'
ls -al qrcodes/ # qrcodes/


# Linux
export target_file=a.txt target_dir=/root/test/ image=fileqrcoder
mkdir -p ${target_dir} && echo "Hello, this is FileQrcoder" > ${target_dir}${target_file}
docker run --mount type=bind,source=${target_dir},target=/data ${image} sh -c 'cd /data/ && python3 /root/FileQrcoder/test_encode.py ${target_file}'
```
# FYI
Base64 symbols are: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']
