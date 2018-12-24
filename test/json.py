#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年10月"],
"功能":["调用测试"],
}

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import sys # 操作系统模块1
import os # 操作系统模块2
import types # 数据类型
import time # 时间模块
import datetime # 日期模块
import re # 正则表达式
import chardet # 编码处理
import requests
import urllib

#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----


#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理---
def args2dic(args_list_p=[]):
    
    dic_p = {}
    
    if args_list_p:
        
        i = 0
        
        for x in args_list_p:

            if (i > 0):
                if (x.split("=")):
                    dic_p[x.split("=")[0]] = x.split("=")[1]
                    #print (i,x,type(x)) # 调试用
            i += 1
        
    return dic_p
# shell模式下参数处理
dic_args = {} # 参数字典
dic_args = args2dic(sys.argv)

# ---全局变量处理---

# ---提交参数处理

# 申请ip
if ("ip" in dic_args):
    ip = dic_args["ip"]
else:
    ip = "http://localhost"
    
# 申请端口
if ("port" in dic_args):
    port = dic_args["port"]
else:
    port = "80"
    
# 调用行为
if ("action" in dic_args):
    action = dic_args["action"]
else:
    action = "api"
    
# 提交文本
if ("keyword" in dic_args):
    keyword = dic_args["keyword"]
else:
    keyword = ""
    
# 用户id
if ("uid" in dic_args):
    uid = dic_args["uid"]
else:
    uid = "0"
    
# 语义提交网站
if ("web_is" in dic_args):
    web_is = dic_args["web_is"]
else:
    web_is = "url"
    
#print ("基本参数",ip,port,action,keyword,uid,web_is) # 调试用

# ---本模块内部类或函数定义区

# 版本说明
def version(dic_p={}):
    print ("-----------------------------")
    [print("\n",x," --- ",re.sub("[\[,\],\',\,]", "", str(dic_p[x])),"\n") for x in dic_p] # 调试用
    print ("-----------------------------")

#--------- 内部模块处理<<结束>> ---------#

#---------- 过程<<开始>> -----------#

# 快捷爬虫类
class Crawler_fast(object):

    def __init__(self):
    
        self.headers = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/56.0.2924.87 Safari/537.36")}

    # 判断是否是已知编码标准
    def code_standard_is(self,chartset_p=""):
        result = False
        list_p = [
        "gb2312",
        "GB2312",
        "gbk",
        "GBK",
        "utf-8",
        "UTF-8",
        "iso-8859-1",
        "ISO-8859-1"
        ]
        #print ("待处理的编码标准：",chartset_p) # 调试用
        if (chartset_p.strip() in list_p):
            result = True
        
        return result

    # 获取网页字符默认编码
    def get_encodings_from_content(self,content):
        
        charset = re.compile(r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I).findall(content)
        if len(charset) == 0:
            charset = re.compile(r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I).findall(content)
            if len(charset) == 0:
                charset = re.compile(r'^<\?xml.*?encoding=["\']*(.+?)["\'>]').findall(content)
                if len(charset) == 0:
                    charset = ['n/a']
        return charset[0]
                          
    # post爬取
    def get_html_post(self,url_p="",dic_p={},timeout_p=28,headers_p="",chartset_p="utf-8"):
        
        chartset_get = ""
        if (headers_p == ""):
            headers_p = self.headers
        
        #将字典格式化成能用的形式
        data_p = urllib.parse.urlencode(dic_p).encode('utf-8')
        #创建一个request,放入我们的地址、数据、头
        request = urllib.request.Request(url_p, data_p, headers_p)
        #访问
        txt = urllib.request.urlopen(request).read()

        chartset_get = self.get_encodings_from_content(txt.decode(chartset_p, "ignore")) # 尝试编码 获得内部编码信息
        if (self.code_standard_is(chartset_p=chartset_get)):
            print ("<<原文编码识别[通过]>>")
            txt = txt.decode(chartset_get, "ignore")
        else:
            # 进行编码判别
            print ("<<原文编码识别[未通过]>>")
            code_is = chardet.detect(txt)
            if ("encoding" in code_is):
                chartset_get = code_is["encoding"]
                txt = txt.decode(code_is["encoding"], "ignore")
                        
        print ("<<<快捷爬虫>>>过程："," ","原文编码：",chartset_get)
    
        return txt,chartset_get
    
# 加密类
class Secret():

    def secret_lqab(self,text_p="",secret_if="yes",key_p="lqabisgood",salt_p = b'llqqaabbiissookk'):

        import base64 # base64加密模块
        import hashlib # hashlib加密模块
        import psutil # 系统库
        from cryptography.fernet import Fernet
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        #预处理
        password=bytes(key_p, encoding="utf-8")
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt_p,iterations=100000,backend=default_backend())
        jey = base64.urlsafe_b64encode(kdf.derive(password))
        key = Fernet(jey)
        result = text_p
    
        #加密
        if (secret_if == "yes"):
        
            try:
                result = result.encode("utf-8")
                result = str(key.encrypt(result)) # 加密
                result = result.replace("b'","")
                result = result.replace("'","")
            except:
                pass
        #解密
        if (secret_if == "no"):
        
            try:
                result = result.encode("utf-8")
                result = key.decrypt(result)
                result = result.decode("utf-8")

            except:
                pass
    
        return result

# 主过程函数
def main():

    chartset_code = ""
    version(dic_p=dic_note) # 打印版本
    code_html = ""
    url_p = ip + ":" + port + "/" + action
    print ("提交地址：",url_p)
    
    # 内部调用自定义简化爬虫 获得API端爬取内容
    values = {
             "keyword":keyword,
             "uid":uid,
             "web_is":web_is
                    }
    crawler_fast = Crawler_fast()
    code_html,chartset_code  = crawler_fast.get_html_post(url_p=url_p,dic_p=values)

    #try:
        #code_html,chartset_code  = crawler_fast.get_html_post(url_p=url_p,dic_p=values)
    #except Exception as e:
        #print (e)
        #pass
    
    # 解密可以采取多种手段 本解密代码仅为示例用，有精力的客户可自编程自用的解码模块
    
    secret = Secret() # 加解密类实例化
    if (code_html.strip() != ""):
       print ("密文长度:",len(code_html))
       code_html = secret.secret_lqab(text_p=code_html,secret_if="no",key_p="fbc37fe869960998c7da80da4e936ad2",salt_p = b'llqqaabbiissookk')
    # 写入获得的测试结果
    # print ("明文结果",code_html) #调试用
    with open("result.json", 'w', encoding="utf-8") as f:
        print ("明文长度:",len(code_html))
        print ("返回值类型",type(code_html))
        if (type(code_html) is str):
            f.write(code_html)
        if (type(code_html) is bytes):
            txt = code_html.decode("utf-8")
            f.write(txt)
    
if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#