import requests
import re
import time
import os
import sys
import pymysql
from PIL import Image

def counttime():
    percent = num / total * 100
    keynum = round(percent / 2)
    a = "*" * keynum
    b = "." * (scale - keynum)
    dur = time.perf_counter() - start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(percent, a, b, dur), end="")
#获取首页HTML
url='https://safebooru.org/index.php?page=post&s=list&tags=1girl+'
url0='https://safebooru.org/'
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
web=requests.get(url,headers=headers)
dowm_lord_path="E:\project\AI绘图\训练集"
scale = 50 #进度条参数
start = time.perf_counter() #开始时间，用于计算运行时间的

#获取子页地址
sub_urls=[]
mat=re.search("\d*?\" alt=\"last page\"",web.text)
mat=re.search("\d+",mat.group())
page=int(mat.group())//40+1

#初始化数据库，建立数据库链接
database = pymysql.connect(host="localhost", user="root", db="pics", charset='utf8')
cursor = database.cursor()
sql = "INSERT INTO pictures VALUES (%s,%s)"

for i in range(page):#生成子页面链接
    sub_urls.append(url+f"&pid={i*40}")

#爬取图片下载链接
imgs_url=[]
detail_urls_all=[]
total = 0
for i in range(1):#爬取相应页数
    web=requests.get(sub_urls[i],headers=headers)
    mat=re.findall("<a id=\".*?\" href=\".*?\"",web.text)
    detail_urls = []
    for j in range(len(mat)):#爬取详细页地址
        mat_0=re.search("href=\"(.*?)\"",mat[j])
        detail_urls.append((url0+mat_0.group(1)).replace("amp;",""))
        total+=1
    detail_urls_all.append(detail_urls)
num = 0 #计数
valuelist = []
for i in detail_urls_all:#保存高清图片下载链接
    for j in i:
        web=requests.get(j,headers=headers)
        mat=re.search("alt=\"(.*?)\" src=\"(.*?)\"",web.text)
        tag = mat.group(1)
        img = requests.get(mat.group(2), headers=headers)
        img = img.content
        value = (tag,img)
        valuelist.append(value)
        num+=1
        counttime()
        time.sleep(0.1)
    cursor.executemany(sql, valuelist)
    database.commit()
