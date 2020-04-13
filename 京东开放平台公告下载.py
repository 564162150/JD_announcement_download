#网页调用
import requests

#数据解析
import json

#sqlite数据库引用
import sqlite3

#时间引用，方便设置间隔
import time

#本地目录引用
from os import path

#加载邮件发送引用
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr



#查询公告主页面
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
url='https://open.jd.com/doc/getNewJosChannelInfo?channelId=&pageIndex='
html = requests.get(url, headers=headers)
jsob = json.loads(html.text)
responseData = jsob.get('responseData')
josCmsArticle = responseData['josCmsArticle']

# 打开数据库连接
#打开本地数据库
d = path.dirname(__file__)
db = sqlite3.connect(path.abspath(d)+'\jd.db')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

#开始循环插入本地数据库首页所有公告
for i in range(len(josCmsArticle)):
    sqlselect = 'SELECT count(1) FROM JDJOSChannel where indexid=%s' % (
        josCmsArticle[i]['id'])
    cursor.execute(sqlselect)
    db.commit()
    selectid = cursor.fetchall()

    if selectid[0][0]==0:#判断当前公告ID是否已经插入数据表
        ids = josCmsArticle[i]['id']
        articleTitle = josCmsArticle[i]['articleTitle']
        articleChannelId = josCmsArticle[i]['articleChannelId']
        created = josCmsArticle[i]['created']
        modified = josCmsArticle[i]['modified']
        # SQL 插入语句
        sql = 'INSERT INTO JDJOSChannel(indexid,articleTitle, articleChannelId, created, modified,status,mailtext)VALUES (%s,\'%s\',%s,\'%s\',\'%s\',0,\'\')' % (
            ids, articleTitle, articleChannelId, created, modified)
        cursor.execute(sql)
        db.commit()
    else:
        pass

#开始获取具体页面数据并发邮件


#邮件相关参数准备
my_sender = 'xxxx@xx.com'    # 发件人邮箱账号
my_pass = 'xxxx'              # 发件人邮箱密码(当时申请smtp给的口令)
my_user = 'xxxx@xx.com'      # 收件人邮箱账号，我这边发送给自己

#创建发送邮件方法
def mail(articleTitle, mailtext):
    ret = True
    try:
        msg = MIMEText(mailtext, 'html', 'utf-8')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr(["京东开放平台", my_sender])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr(["公告机器人", my_user])
        # 邮件的主题，也可以说是标题
        msg['Subject'] = articleTitle

        # 发件人邮箱中的SMTP服务器，端口是465
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


#查询数据库中现在有几条公告未发送记录
sqlmailcount = 'SELECT count(1) FROM JDJOSChannel where status=0'
cursor.execute(sqlmailcount)
db.commit()
mailcount = cursor.fetchall()
count = mailcount[0][0]

#查询数据库中未发送的日志行
sqlmail = 'SELECT indexid,articleTitle,mailtext FROM JDJOSChannel where status=0'
cursor.execute(sqlmail)
db.commit()
mailitem = cursor.fetchall()

#开始按未发送的公告数循环发邮件
for i in range(count):
    #获取该发送邮件的ID值
    mailid=mailitem[i-1][0]
    articleTitleset = mailitem[i-1][1]

    #开始获取详情页面的html
    urlitem = 'https://open.jd.com/doc/getArticleDetailInfo?articleId=%s' % (mailid)
    jsobitem = json.loads(requests.get(urlitem, headers=headers).text)
    mailtextset = jsobitem['responseData']['articleContent']
    #mailtextset = mailitem[i][2]    # 邮件内容
    ret = mail(articleTitleset, mailtextset)
    if ret:
        sqlupdatestatus = 'UPDATE JDJOSChannel set `status`=1 where indexid=%s' % (mailid)
        cursor.execute(sqlupdatestatus)
        db.commit()
        print("主题：【%s】%s 邮件发送成功" % (mailid, articleTitleset))
    else:
        print("主题：【%s】%s 邮件发送失败" % (mailid, articleTitleset))
    #由于某些邮箱服务会查看发送频率，所以设置间隔时间可以提高多封连续发送成功率
    time.sleep(100)

# 关闭数据库连接
db.close()
