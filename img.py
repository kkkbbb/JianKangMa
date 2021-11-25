#coding=utf-8
from PIL import Image
from pytesseract import image_to_string
import numpy
import cv2
import aircv as ac
import os

def check(img,x,y):
    try:
        r,g,b = img.getpixel((x,y))
    except Exception as e:
        print(e)
    if r > 248 and g > 248 and b > 248 and x < width*0.1 and y < height*0.5 and y > height*0.1:
        return True
    return False

def check_px(img,x,y):
    if check(img,x-1,y) and check(img,x-1,y-1) and check(img,x-1,y+1) and check(img,x+1,y) and check(img,x+1,y-1) and check(img,x+1,y+1):
        for i in range(250):
            if not check(img,x,y+i):
                return False
        return True
    return False

def find_px(img):
    for y in range(height):
        for x in range(width):
            try:
                r,g,b = img.getpixel((x,y))
            except Exception as e:
                print(e)
                r,g,b = (0,0,0)
            if r > 248 and g > 248 and b > 248 and x < width*0.1 and y < height*0.5 and check_px(img,x,y):
               return x,y 
    return (1,1)
               
def check_name(name):
    global dong,person
    phone = {'7459':'蔡慧','4376':'陈慧子','4248':'雷志会','7658':'陈丽容','9215':'戴劲','7091':'戴祥宇','2681':'段云仙','3603':'付涛','0291':'杲嘉欣','6974':'古涛龙','4530':'胡缅湘','1670':'胡缅湘','5516':'黄数敏','6075':'蒋海刚','0919':'雷志会','8579':'李建林','3818':'李柯瑾','0631':'李舒梦','4742':'廖志强','6603':'刘慧','6376':'刘涛','3710':'罗彩云','1910':'骆超','3843':'马轩','6534':'马轩','9117':'欧润辉','7574':'潘慧','6070':'彭师怡','2550':'彭正昌','7386':'钱之星','9580':'权志广','9132':'申弋杰','5818':'谭慧','9395':'谭慧','5621':'田嘉伟','3060':'汤达','6307':'田嘉伟','2547':'伍文彪','4225':'肖舒晴','0037':'谢高明','0736':'杨慧庭','8745':'尹慧琪','0919':'余柳湘','6065':'张琦','2249':'张悦','5191':'赵彦','6458':'赵玉芳','6251':'周志骏','1940':'朱志圣','0121':'祝薪宇'}
    if any(char.isdigit() for char in name):
        for i in phone:
            if i in name:
                if '动态' in name or '行程' in name or dong:
                    return phone[i]+'1'
                else:
                    return phone[i]
        if '动态' in name or '行程' in name:
            dong = True
    else:
        for i in person:
            if i in name:
                return i
    return False

def matchImg(imgsrc, imgobj,confidencevalue=0.8):  # imgsrc=原始图像，imgobj=待查找的图片
    imsrc = cv2.cvtColor(numpy.asarray(imgsrc),cv2.COLOR_RGB2BGR)
    imobj = cv2.cvtColor(numpy.asarray(Image.open(imgobj)),cv2.COLOR_RGB2BGR)
    match_result = ac.find_template(imsrc, imobj, confidencevalue)
    if match_result:
        return True
    return False

def Imgcheck(img):
    for i in os.listdir("people"):
        if matchImg(img,'people/'+i):
            return i.split(".")[0]
    return False

def auto(img,langs):
    text = image_to_string(img,lang=langs)
    text=list(filter(None,text.split("\n")))
    #print(text)
    for name in text:
        name = check_name(name)
        if name:
            return name
    return False

def huidu(img,th):
    img = img.convert('L')
    thres = th
    table = []
    for k in range(256):
        if k < thres:
            table.append(0)
        else:
            table.append(1)
    return img.point(table,'1')

global width,height,dong,person
person = ['刘涛','谢高明','李建林','汤达','田嘉伟','古涛龙','权志广','蒋海钢','朱志圣','祝薪宇','周志骏','廖志强','申弋杰','伍文彪','赵彦','彭正昌','马轩','张琦','戴劲','付涛','戴祥宇','骆超','钱之星','尹慧琪','李舒梦','谭慧','段云仙','黄数敏','张悦','罗彩云','蔡慧','杲嘉欣','刘慧','潘慧','彭师怡','肖舒晴','陈慧子','胡缅湘','陈丽容','雷志会','杨惠庭','余柳湘','赵玉芳','李柯瑾','欧润辉']
names = ' '
dong = False
r = 1
dong = 0
#num=0
#for i in os.listdir("image"):
#    num = num+1
#    os.rename('image/'+i,'image/'+str(num)+'.jpg')
size = len(os.listdir('image'))
for i in os.listdir("image"):
    img = Image.open("image/"+i)
    img = img.convert("RGB")
    img2 = img
    width,height = img.size
    x,y = find_px(img)
    #print(x,y)
    img3 = img.crop((x,y,x+800,y+320))
    #img3.show()
    names = auto(img3,langs='chi_sim')
    if not names:
        names = auto(img3,langs='eng')
        if not names:
            names = auto(img,langs='chi_sim')
    if not names:
        for t in (75,145):
            img = huidu(img3,t)
            #img.show()
            if names:
                break
        else:
            try:
                names = Imgcheck(img2)
                print("找图识别可能不准 请手动对比",end=' ')
                r = 0
            except:
                pass
    print(names,end=' ')      
    print(i)
    if names:
        if os.path.exists('images/'+names+'.jpg'):
            print("\033[1;32;43m 文件存在不保存不删除 \033[0m")
            r = 0
            os.rename('image/'+i,'image/'+names+'.jpg')
        elif r:
            img2.save('images/'+str(names)+'.jpg')
            os.remove("image/"+i)
        else:
            os.rename('image/'+i,'image/'+names+'.jpg')
        r = 1
        if '1' not in names:
            try:
                person.remove(names)
            except:
                print('删除名字失败，',names)
    else:
        print("\033[1;32;43m 失败！\033[0m",end='')
    dong = False
print("处理文件：",size)
print(person)