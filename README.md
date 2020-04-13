# 京东开放平台公告下载与邮件提醒

#### 介绍
京东开放平台公告时常会发布影响接口调用的公告信息，对于产品经历的我，需要及时了解这些信息，以便调整对接方案。所以业余时间拼装了这么一个可自动发送公告信息邮件的脚本程序。（初学者，代码质量一般）

#### 软件架构
主程序通过python实现

调用了第三方库有：

requests,json,sqlite3,smtplib,email等

数据库使用了免安装的sqlite

#### 安装教程
1.拷贝.py和.db文件，放在同一目录下

2.修改.py文件中的邮件

[收件邮箱]

[发件人邮箱]

[发件邮箱密码（授权码）]QQ邮箱获取方式如下：

![输入图片说明](https://images.gitee.com/uploads/images/2020/0413/132732_2c8d4c7e_5444155.png "FE73F542-D222-4786-80AE-56982791251B.png")

![输入图片说明](https://images.gitee.com/uploads/images/2020/0413/132746_62a69713_5444155.png "E0DF33D3-2157-426e-AC15-B0DD6E6E948B.png")

![](https://images.gitee.com/uploads/images/2020/0413/142009_3eb31ee9_5444155.png "7237FD34-06E8-4d91-AAC4-7E7AB2EB467C.png")


#### 使用说明
直接运行.py文件即可

![运行结果](https://images.gitee.com/uploads/images/2020/0413/132635_6507c2dc_5444155.jpeg "{0932997A-F4CE-4A02-A332-12D15FB59B4D}_20200413125752.jpg")


![输入图片说明](https://images.gitee.com/uploads/images/2020/0413/142017_2b67c37c_5444155.jpeg "{C6CC6FAF-56D9-45C8-90E7-94E2A50F71DF}_20200413141828.jpg")
