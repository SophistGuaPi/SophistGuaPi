import requests
import re
import time
import os

#获取首页HTML
url='https://safebooru.org/index.php?page=post&s=list&tags=1girl+'
url0='https://safebooru.org/'
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
web=requests.get(url,headers=headers)
dowm_lord_path="E:\project\AI绘图\训练集"

#获取子页地址
sub_urls=[]
mat=re.search("\d*?\" alt=\"last page\"",web.text)
mat=re.search("\d+",mat.group())
page=int(mat.group())//40+1

for i in range(page):#生成子页面链接
    sub_urls.append(url+f"&pid={i*40}")

#爬取图片下载链接
imgs_url=[]
detail_urls=[]
for i in range(1):#爬取相应页数
    web=requests.get(sub_urls[i],headers=headers)
    mat=re.findall("<a id=\".*?\" href=\".*?\"",web.text)
    for j in range(len(mat)):#爬取详细页地址
        mat_0=re.search("href=\"(.*?)\"",mat[j])
        detail_urls.append((url0+mat_0.group(1)).replace("amp;",""))

for i in range(len(detail_urls)):#保存高清图片下载链接
    web=requests.get(detail_urls[i],headers=headers)
    mat=re.search("alt=\"(.*?)\" src=\"(.*?)\"",web.text)
    print(mat.group(1))
    imgs_url.append(mat.group(2))
    print(imgs_url)
    print(i)
    time.sleep(0.01)


# path=[]
# for i in range(len(imgs_url)):#自动生成文件名
#     path.append(dowm_lord_path+"\\"+str(i)+".jpg")
#
# for i in range(len(imgs_url)):#下载到本地
#     img=requests.get(imgs_url[i],headers=headers)
#     with open(path[i],"wb") as f:
#         f.write(img.content)
#     time.sleep(0.1)

# print(web.text)