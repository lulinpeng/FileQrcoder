pwd
rm -rf vertical
rm -rf horizontal
rm -rf results
python3 test_encode.py intro.png 45321
python3 test_concat.py ./qrcodes/ ./concat/
python3 test_gif.py ./concat/
ls -alh out.gif