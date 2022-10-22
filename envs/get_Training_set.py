import requests
import re
import time

#获取首页HTML
class geturl():#生成网页
    def __init__(self,headers,url):#输入信息头与初始页URL
        self.headers=headers
        self.url=url[0]
        self.pattern=url[1]
        mat=re.search("((http.?://.*?/).*?\..*?)\?",self.url)
        self.url0=mat.group(2)
        self.url1=mat.group(1)
    filenum=0
    start = time.perf_counter()  # 开始时间，用于计算运行时间的
    tags_list=[]#储存tags
    def Trunpages(self):#翻页
        web = requests.get(self.url, headers=self.headers)
        mat = re.search("<div class=.*?> <b>(\d*?)</b> (<a href=.*?>.*?</a>)*?</div>", web.text)
        mat_0 = re.findall("href=\"(.*?)\">(.*?)<", mat.group())
        mat_0 = re.match("(.*?)\"", mat_0[-2][0])
        if mat_0==None:
            return 0
        self.url=self.url1+mat_0.group(1).replace("amp;","")
        self.counttime()#显示进度
        return 1

    def getDetailUrl(self):#爬取并返回详情页URL列表
        detail_urls = []
        web = requests.get(self.url, headers=self.headers)
        mat = re.findall("<a id=\".*?\" href=\"(.*?)\"", web.text)
        for i in mat:
            detail_urls.append((self.url0+i).replace("amp;",""))
        # print("getDetailUrl complete\n")
        return detail_urls

    def getImgUrl(self):# 获取高清图片下载链接和相应的标签
        global tags_list
        url_list=self.getDetailUrl()
        img_url_list=[]
        self.tags_list=[]
        for i in range(len(url_list)):
            web = requests.get(url_list[i], headers=self.headers)
            mat = re.search(self.pattern, web.text)
            mat_0=re.search("(.*?)\" height=.*?",mat.group(1))
            self.tags_list.append(mat_0.group(1))
            img_url_list.append(mat.group(2))
        # print("get Img url complete\n")
        return img_url_list

    def dowmLord(self,url_list,downLordPath,sql=None):#传入下载路径和图片URL列表，下载图片
        global filenum
        path = []

        for i in range(len(url_list)):  # 下载到本地
            path.append(downLordPath + "\\" + str(self.filenum+i) + ".jpg")
            if sql==None:#下载路径储存到mysql数据库
                img = requests.get(url_list[i], headers=self.headers)
                with open(path[i], "wb") as f:
                    f.write(img.content)
                # print(f"start DownLord:{i}\n")
            else:#下载成文件
                img = requests.get(url_list[i], headers=self.headers)
                with open(path[i], "wb") as f:
                    # print(f"start DownLord:{path[i]}\n")
                    f.write(img.content)

            time.sleep(0.1)
        self.filenum = self.filenum + len(url_list)
        return path

    def getSomePageImg(self,num,downLordPath,cursor=None,database=None,sql=None):#下载num页图像至对应路径
        for i in range(num):
            if sql!=None:
                self.savesql(downLordPath,cursor,database,sql)
                judge = self.Trunpages()
            else:
                print(f"DownLording {self.url}")
                self.dowmLord(self.getImgUrl(),downLordPath)
                judge=self.Trunpages()
            print(f"the {i+1} page DownLord complete,start next page now...\n")
            if judge==0:
                print("last page")
                break
            time.sleep(1)
        print("end\n")

    def getAllPageImg(self,downLordPath,cursor=None,database=None,sql=None):#下载该页至最后一页
        i=1
        while 1:
            if sql!=None:
                self.savesql(downLordPath,cursor,database,sql)
                time.sleep(1)
                judge=self.Trunpages()
            else:
                self.dowmLord(self.getImgUrl(), downLordPath)
                time.sleep(1)
                judge=self.Trunpages()

            # print(f"the {i} page downlord complete,start next page now...\n")
            if judge==0:
                print("last page")
                break
            time.sleep(1)
            i=i+1
        print("end\n")

    def savesql(self,path,cursor,database,sql):#储存为mysql文件
        value_list=[]
        path_list=self.dowmLord(self.getImgUrl(),path,sql)
        for i in range(len(path_list)):
            value = (self.tags_list[i], path_list[i])
            value_list.append(value)
        cursor.executemany(sql, value_list)
        database.commit()

    def get_last_page(self):#获取最后一页url
        web = requests.get(self.url, headers=self.headers)
        mat = re.search("<div class=.*?> <b>(\d*?)</b> (<a href=.*?>.*?</a>)*?</div>", web.text)
        mat_0 = re.findall("href=\"(.*?)\">(.*?)<", mat.group())
        mat_0 = re.match("(.*?)\"", mat_0[-1][0])
        if mat_0 == None:
            return 0
        self.url_lastpage = self.url1 + mat_0.group(1).replace("amp;", "")
        return self.url_lastpage

    def getpage(self,url):#获取当前页码
        web = requests.get(url, headers=self.headers)
        mat = re.search("<div class=.*?> <b>(\d*?)</b> (<a href=.*?>.*?</a>)*?</div>", web.text)
        return mat.group(1)

    def counttime(self):#记录当前下载进度对应到最后一页
        scale=50
        pagenum=int(self.getpage(self.url))
        percent=pagenum/int(self.getpage(self.get_last_page()))*100
        keynum = round(percent / 2)
        a = "*" * keynum
        b = "." * (scale - keynum)
        dur = time.perf_counter() - self.start
        print("\r{:^3.2f}%[{}->{}]{:.2f}s\n".format(percent, a, b, dur)+f"the {pagenum} page ，{self.filenum}Img downlord complete,start next page now...\n"
                                                                        f"{self.url}\n", end="")
