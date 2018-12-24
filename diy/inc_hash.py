#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年10月"],
"功能":["散列函数模块 1.0"],
}

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import sys # 操作系统模块1
import os # 操作系统模块2
import types # 数据类型
import time # 时间模块
import datetime # 日期模块
import re # 正则表达式
import hashlib #哈希模块

#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理---

# ---全局变量处理---


# ---本模块内部类或函数定义区

def hash_make(str_hash,action_p="md5"):
    
    hash_last = ""
    
    # md5
    if (action_p == "md5"):
        str_hash = str_hash.encode("utf-8")
        hash = hashlib.md5()
        hash.update(str_hash)
        hash_last = hash.hexdigest()
        
    return hash_last
    
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

# 主过程子函数
def run_it():
    
    # 版本说明
    def version(dic_p={}):
        print ("-----------------------------")
        [print("\n",x," --- ",re.sub("[\[,\],\',\,]", "", str(dic_p[x])),"\n") for x in dic_p] # 调试用
        print ("-----------------------------")
        
    result_p = "hello world!"
    version(dic_p=dic_note) # 打印版本
    
    return result_p # 调试用

#--------- 内部模块处理<<结束>> ---------#

#---------- 过程<<开始>> -----------#

# 过程函数
def main():

    #1 过程一
    print(run_it())
    #2 过程二
    #3 过程三
    
if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#