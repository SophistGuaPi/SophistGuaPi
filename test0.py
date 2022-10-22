import re
import pymysql
import get_Training_set as gts
dowm_lord_path="G:\\db\\img"
urlAndPattern=['https://safebooru.org/index.php?page=post&s=list&tags=1girl&pid=16040',re.compile("alt=\"(.*?)\" src=\"(.*?)\"")]
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}

database = pymysql.connect(host="localhost", user="root", db="pics", charset='utf8')
cursor = database.cursor()
sql = "INSERT INTO pictures VALUES (%s,%s)"

x=gts.geturl(headers,urlAndPattern)
x.filenum=16040 #重新开始时的图片编码，必须从中断的那一页开始。
while 1:
    try:
        x.getAllPageImg(dowm_lord_path,cursor=cursor,database=database,sql=sql)

    except BaseException:
        print(BaseException,"restart...\n")
        filenum=x.filenum
        urlAndPattern[0]=x.url
    if x.getpage(x.get_last_page()) == x.url:
        break