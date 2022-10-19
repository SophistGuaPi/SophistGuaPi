import requests
import re
import time

#获取首页HTML
class geturl():#生成网页
    def __init__(self,headers,url=None):#输入信息头与初始页URL
        self.headers=headers
        self.url=url
        mat=re.search("((http.?://.*?/).*?\..*?)\?",url)
        self.url0=mat.group(2)
        self.url1=mat.group(1)
    filenum=0

    def Trunpages(self):#翻页
        web = requests.get(self.url, headers=self.headers)
        mat = re.search("<div class=.*?> <b>(\d*?)</b> (<a href=.*?>.*?</a>)*?</div>", web.text)
        mat_0 = re.findall("href=\"(.*?)\">(.*?)<", mat.group())
        mat_0 = re.match("(.*?)\"", mat_0[-2][0])
        if mat_0==None:
            return 0
        self.url=self.url1+mat_0.group(1).replace("amp;","")
        return 1

    def getDetailUrl(self):#爬取并返回详情页URL列表
        detail_urls = []
        web = requests.get(self.url, headers=self.headers)
        mat = re.findall("<a id=\".*?\" href=\"(.*?)\"", web.text)
        for i in mat:
            detail_urls.append((self.url0+i).replace("amp;",""))
        print("getDetailUrl complete\n")
        return detail_urls

    def getImgUrl(self):# 获取高清图片下载链接和相应的标签
        url_list=self.getDetailUrl()
        img_url_list=[]
        tags_list=[]
        for i in range(len(url_list)):
            web = requests.get(url_list[i], headers=self.headers)
            mat = re.search("alt=\"(.*?)\" src=\"(.*?)\"", web.text)
            tags_list.append(mat.group(1))
            img_url_list.append(mat.group(2))
        print("get Img url complete\n")
        return img_url_list,tags_list

    def dowmLord(self,url_list,downLordPath):#传入下载路径和图片URL列表，下载图片
        path = []
        global filenum
        for i in range(self.filenum,self.filenum+len(url_list)):  # 自动生成文件名
            path.append(downLordPath + "\\" + str(i) + ".jpg")

        for i in range(len(url_list)):  # 下载到本地
            img = requests.get(url_list[i], headers=self.headers)
            with open(path[i], "wb") as f:
                print(f"start DownLord:{path[i]}\n")
                f.write(img.content)
            time.sleep(0.1)
        self.filenum = self.filenum + len(url_list)

    def getSomePageImg(self,num,downLordPath):#下载num页图像至对应路径
        for i in range(num):
            print(f"DownLording {self.url}")
            self.dowmLord(self.getImgUrl()[0],downLordPath)
            self.Trunpages()
            print(f"the {i+1} page DownLord complete,start next page now...\n")
            time.sleep(1)
        print("end\n")

    def getAllPageImg(self,downLordPath):
        i=1
        while 1:
            self.dowmLord(self.getImgUrl()[0], downLordPath)
            time.sleep(1)
            judge=self.Trunpages()
            print(f"the {i} page downlord complete,start next page now...\n")
            if judge==0:
                break
            i=i+1
        print("end\n")