# JianKangMa
健康码行程码收集自动识别命名

./image 存放需要识别的图片  
./images 识别后的图片  
./people 存放因为特殊字体或其他原因OCR识别失败后，用以图找图识别备用方案的图片  

## Usage
```
python ./img.py
```
需要安装pytesseract,tesseract以及其他py图片库自行查看
自动识别image中的文件进行重命名放到images下
