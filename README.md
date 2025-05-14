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
cd FileQrcoder/demo/
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
export image=fileqrcoder:1.0
docker build -t ${image} -f Dockerfile .
```

## Manual Mode
```shell
# enter your directory
cd xxx
# start a container
docker run -it --name qrcoder --mount type=bind,source="$(pwd)",target=/base fileqrcoder:1.0

cd /root/FileQrcoder/demo
export PYTHONPATH="..":$PYTHONPATH
python3 test_encode.py

python3 test_decode.py qrcodes/
```

## Automated Mode
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

# MORE TESTS
```shell
cd /base/FileQrcoder/demo/
export PYTHONPATH="/base/FileQrcoder/":$PYTHONPATH
python3 generate.py
python3 test_locate.py
```


# FYI
## Base64 Symbols
Base64 symbols are: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']


## QR Code Versions 1-40
The following table shows the complete **8-bit byte** capacity by error correction level (L/M/Q/H) for QR code versions 1-40, where L, M, Q, and H represent the QR code's error correction capability levels: Low (7%), Medium (15%), Quartile (25%), and High (30%).

| Version | L (7%)  | M (15%)  | Q (25%)  | H (30%)  |
|---------|----------|----------|----------|----------|
| 1       | 17       | 14       | 11       | 8        |
| 2       | 32       | 26       | 20       | 15       |
| 3       | 53       | 42       | 32       | 24       |
| 4       | 78       | 62       | 46       | 34       |
| 5       | 106      | 84       | 60       | 44       |
| 6       | 134      | 106      | 74       | 58       |
| 7       | 154      | 122      | 86       | 64       |
| 8       | 192      | 152      | 108      | 84       |
| 9       | 230      | 180      | 130      | 98       |
| 10      | 271      | 215      | 151      | 119      |
| 11      | 321      | 254      | 177      | 137      |
| 12      | 367      | 290      | 203      | 155      |
| 13      | 425      | 334      | 241      | 177      |
| 14      | 458      | 365      | 258      | 194      |
| 15      | 520      | 408      | 292      | 220      |
| 16      | 586      | 459      | 322      | 250      |
| 17      | 644      | 504      | 364      | 280      |
| 18      | 718      | 564      | 394      | 310      |
| 19      | 792      | 611      | 442      | 338      |
| 20      | 858      | 661      | 482      | 382      |
| 21      | 929      | 715      | 509      | 403      |
| 22      | 1003     | 779      | 565      | 439      |
| 23      | 1091     | 864      | 611      | 461      |
| 24      | 1171     | 910      | 661      | 511      |
| 25      | 1273     | 958      | 715      | 535      |
| 26      | 1367     | 1046     | 751      | 593      |
| 27      | 1465     | 1153     | 805      | 625      |
| 28      | 1528     | 1219     | 868      | 658      |
| 29      | 1628     | 1273     | 908      | 698      |
| 30      | 1732     | 1370     | 982      | 742      |
| 31      | 1840     | 1452     | 1030     | 790      |
| 32      | 1952     | 1538     | 1112     | 842      |
| 33      | 2068     | 1628     | 1168     | 898      |
| 34      | 2188     | 1722     | 1228     | 958      |
| 35      | 2303     | 1809     | 1283     | 983      |
| 36      | 2431     | 1911     | 1351     | 1051     |
| 37      | 2563     | 1989     | 1423     | 1093     |
| 38      | 2699     | 2099     | 1499     | 1139     |
| 39      | 2809     | 2213     | 1579     | 1219     |
| 40      | 2953     | 2331     | 1663     | 1273     |


