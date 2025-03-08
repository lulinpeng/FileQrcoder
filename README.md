# FileQrcoder
# INTRODUCTION
FileQrcoder is a basic tool used to convert a file in any format into a list of QRCode images. Additionally, it also supports encrypting files and then converting them into QRCodes.

![image](https://github.com/lulinpeng/FileQrcoder/blob/main/intro.png)

# REQUIREMENTS

| Num | target | System  |	Requirements |
|:--------:| :---------: | :---------:|:--------|
|1| test_encoder.py | MacOS |```pip install qrcode==8.0 pillow==11.1.0```|
|2| test_decoder.py | MacOS |```brew install zar, pip install pyzbar```|

# RUN
## First Attempt
```shell
python3 test_encoder.py fileqrcoder.py # generate QR code images for file 'file_qrcoder.py'
python3 display_qrcodes.py # display the above QR code images
```

## Try Your File
```python
python3 test_encoder.py [PATH OF YOUR FILE] # generate QR code images for 'YOUR FILE'
```

# FYI
Base64 symbols are: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']
