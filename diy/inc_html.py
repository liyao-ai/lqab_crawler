#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# develop 514840279

#-----系统自带必备模块引用-----
import os
import requests
import re #正则处理
import urllib
import chardet
import hashlib
import sys

from bs4 import BeautifulSoup as bs_4
from selenium import webdriver # 浏览器引擎webdriver模块
from lxml import etree
from selenium.webdriver.chrome.options import Options 
from lxml import html
sys.path.append("..")
import config #系统配置参数

# 编码类
class HtmlCode(object):
    
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
        
    # 字符串编码转化
    def charset_to_each(self,txt_p="",charset_self="",charset_want=""):
        str_t = ""
        
        if (charset_self == "ISO-8859-1" and charset_want == "utf-8"):
            print ("原编码：",charset_self,"目的编码：",charset_want)
            str_t = txt_p.encode('ISO-8859-1','ignore')
        
        return str_t

# 特殊规则
class HtmlRule(object):
    # 计算MD5值
    def get_md5_value(self,src):
        myMd5 = hashlib.md5()
        myMd5.update(src.encode("utf8"))
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    # 读取网站域名
    def get_url_root(self, url):
        http = ''
        https = ''
        url_root = ''
        if 'http://' in url or 'http:/' in url:
            http = 'http://'
            url = url.replace('http://', '').replace('http:/', '').strip()
        elif 'https://' in url or 'https:/' in url:
            https = 'https://'
            url = url.replace('https://', '').replace('httpss:/', '').strip()
        else:
            pass
        url_root = url.split('/')[0]
        return (http + https + url_root)

     # 解析页面

    # 数据提取详细页的
    def html_content_analysis_detial(self,html_text, column,url):
        md5 = self.get_md5_value(src=html_text)
        tree = html.fromstring(html_text)
        column_context = []
        #column_context = [("md5", [md5])]
        # column_context.append(("标题链接", [url]))
        for a in column:
            if 'l' == a[2]:
                # 进行lxml方式解析
                text = tree.xpath(a[1])
                column_context.append((a[0], text))
            elif 'n' == a[2]:
                # 返回 做补位处理
                column_context.append((a[0], [a[1]]))
            elif 'sp' == a[2]:
                # 二次处理
                text = tree.xpath(a[1])
                if len(text)>0:
                    column_context.append((a[0], [(text[0].split(a[3])[a[4]]).strip()]))
                else:
                    column_context.append((a[0], []))
            elif 'sab' == a[2]:
                # 二次处理 字符串前拼接
                # 赶集网读取联系电话完整图片地址 处理过程
                text = tree.xpath(a[1])
                list = []
                for path in text:
                    list.append(a[3] + path.strip())
                column_context.append((a[0], list))
            elif 'sr' == a[2]:
                # 二次处理 字符串前拼接
                # 赶集网读取联系电话完整图片地址 处理过程
                text = tree.xpath(a[1])
                list = []
                for path in text:
                    list.append(self.get_url_root(url) + path.strip())
                column_context.append((a[0], list))
            elif 'arr' == a[2]:
                # 二次处理 几个中的一个
                text = tree.xpath(a[1])
                column_context.append((a[0], text[a[3]].strip()))
            elif 'sarr' == a[2]:
                # 二次处理 几个中的和成一个
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    #print(item)
                    if item.strip() == '':
                        pass
                    else:
                        st = st +item.strip()
                column_context.append((a[0], [st.strip()]))
            elif 'sarra' == a[2]:
                # 二次处理 几个中的和成一个
                text = tree.xpath(a[1])
                st = ''
                for item in text:
                    #print(item)
                    if item.strip() == '':
                        pass
                    else:
                        st = st +item.strip()+a[3]
                column_context.append((a[0], [st.strip()]))
            elif 'nsp' == a[2]:
                # 二次处理 非固定列 ul处理
                # 应届生网最后的不固定信息
                text = tree.xpath(a[1])
                list = []
                column = []
                for item in text:

                    if item.strip() == '':
                        pass
                    else:
                        list.append(item.strip())
                for item in range(len(list)):
                    if item % 2 == 1:
                        column.append((list[item - 1], [list[item]]))
                column_context.append((a[0], column))
            elif 'nspa' == a[2]:
                # 二次处理 非固定列 ul处理
                # 拉钩网企业信息不固定
                text = tree.xpath(a[1])
                list = []
                column = []
                for item in text:
                    if item.strip() == '':
                        pass
                    else:
                        list.append(item.strip())
                for item in range(len(list)):
                    if item % 2 == 1:
                        column.append(([list[item]], list[item - 1]))
                column_context.append((a[0], column))
                # print(a[0]+a[1]+a[2])
        return column_context

    # 数据提取列表页处理方式
    def html_content_analysis_list(self,html_text, column,url):
        column_content = self.html_content_analysis_detial(html_text, column, url)
        le = len(column_content)
        c = column_content[0][1]
        lista = []
        for i in range(len(c)):
            listb=[]
            for a in column_content:
                if a[0] == '标题链接':
                    continue
                if len(a[1]) < len(c):
                    listb.append(a)
                else:
                    listb.append((a[0], a[1][i]))
            lista.append(listb)
        return lista
        
# 获取网页源码 重要
class HtmlSource(HtmlCode,HtmlRule):
    
    def get_html(self,url_p="",dic_p={},type_p='rg',chartset_p='utf-8',timeout_p=10):
        
        chartset_get = "n/a" # 爬取数据的字符形式编码
        headers_p = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
        txt = "nothing"
                
        # 获取网页源码
        try:
        
            # request_get的方法
            if (type_p == 'rg'):
            
                html = requests.get(url=url_p,timeout=timeout_p,headers=headers_p)
                chartset_get = self.get_encodings_from_content(html.text) # 用英文字符匹配法重新识别编码
                
                if (self.code_standard_is(chartset_p=chartset_get)):
                
                    print ("<<原文编码识别[通过]>>")
                    
                    if (chartset_get.lower() == "iso-8859-1"):
                    
                        print ("rg模式，<<原文编码iso-8859-1特殊处理")
                        try:
                            txt = html.content.decode("GBK")
                        except:
                            txt = html.content.decode("gb2312")
                            
                    else:
                    
                        print ("rg模式，按照识别的" + chartset_get + "特殊处理")
                        txt = html.content.decode(chartset_get)
                    
                else:
                
                    print ("<<原文编码识别[未通过]>>")
                    
                    txt = ""
                    
                print ("<<<rg>>>过程："," ","原文编码：",chartset_get)
                html.close()
            
            # request_get的方法 只输出字节码
            if (type_p == 'rg_byte'):
                txt = b""
                html = requests.get(url=url_p,timeout=timeout_p,headers=headers_p)
                chartset_get = self.get_encodings_from_content(html.text) # 用英文字符匹配法重新识别编码
                txt = html.content
                print ("<<<rg_byte>>>过程："," ","原文编码：",chartset_get)
                html.close()
            
            # request_post的方法
            if (type_p == 'rp'):
            
                conn_p = requests.session()
                rep_p = conn_p.post(url=url_p,data=dic_p,timeout=timeout_p,headers=headers_p)
                txt = rep_p.content
                chartset_get = self.get_encodings_from_content(txt.decode(chartset_p, "ignore"))
                if (self.code_standard_is(chartset_p=chartset_get)):
                    print ("<<原文编码识别[通过]>>")
                    txt = txt.decode(chartset_get, "ignore")
                else:
                    print ("<<原文编码识别[未通过]>>")
                    code_is = chardet.detect(txt)
                    if ("encoding" in code_is):
                        chartset_get = code_is["encoding"]
                        txt = txt.decode(code_is["encoding"], "ignore")
                    
                print ("<<<rp>>>过程："," ","原文编码：",chartset_get)
                
            # urllib的get方法
            if (type_p == 'ug'):

                html = urllib.request.urlopen(url=url_p)
                txt = html.read()
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
                        
                print ("<<<ug>>>过程："," ","原文编码：",chartset_get)
            
            # urllib的post方法
            if (type_p == 'up'):
                
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
                        
                print ("<<<up>>>过程："," ","原文编码：",chartset_get)

                
            # session的方法
            if (type_p == 'ss'):
                res_addr = self.session.get(url_p, timeout=timeout_p, headers=headers_p)
                res_addr.encoding = chardet.detect(res_addr.content)["encoding"]
                txt = bs_4(res_addr.text, "lxml")
                print ("<<<ss>>>过程："," ","原文编码：",chartset_get)

            # Selenium的方法 待完善
            if (type_p == 'se'):
                self.driver.get(url_p)
                js = "var q=document.body.scrollTop=100000"
                self.driver.execute_script(js)
                self.driver.implicitly_wait(30)  # 据说此方法是智能等待，看效果还不错，数据加载完就返回了 30 代表等待秒
                txt = self.driver.page_source
                chartset_get = self.get_encodings_from_content(txt)
                print ("<<<se>>>过程："," ","原文编码：",chartset_get)

            # login的方法 待完善
            if (type_p == 'lg'):
                print ("<<<lg>>>过程："," ","原文编码：",chartset_get)

        except Exception as e:
            
            print("html爬虫处理失败", e)
            
            html = requests.get(url=url_p, headers=headers_p)
            chartset_get = "n/a"
            print ("爬虫的最后处理，按照默认的" + chartset_p + "编码输出")
            try:
                txt = html.content.decode(chartset_p)
            except:
                txt = html.content.decode("gbk")
                
            html.close()
            
        return txt,chartset_get # 返回文本型html编码 加上自定义编码头

    #  获取网页原文 （ulib）
    def get_html_ulib(self,url_p, type_p='rp', chartset_p='utf-8'):
        html = urllib.request.urlopen(url=url_p)
        txt = html.read().decode(chartset_p)
        html.close()
        return txt

    #  获取网页原文 （selenium）
    def get_html_selenium(self,url_p):
        driver = webdriver.Chrome("../driver/chromedriver.exe")

        driver.get(url_p)
        js = "document.documentElement.scrollTop=1000000"
        driver.execute_script(js)
        driver.implicitly_wait(30)  # 据说此方法是智能等待，看效果还不错，数据加载完就返回了 30 代表等待秒
        print(driver)
        txt = driver.page_source
        return txt,driver

    # 获取网页字符集
    def get_encodings_from_content(self,content):
        
        charset = re.compile(r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I).findall(content)
        if len(charset) == 0:
            charset = re.compile(r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I).findall(content)
            if len(charset) == 0:
                charset = re.compile(r'^<\?xml.*?encoding=["\']*(.+?)["\'>]').findall(content)
                if len(charset) == 0:
                    charset = ['n/a']
        return charset[0]

    # 获取html原码的地址列表信息1
    def get_url_list(self, html=''):

        all_a_url = re.findall("href=[\"'](.*?)[\"']", html)
        return all_a_url

    # 获取html原码的地址列表信息2
    def get_url_list_xpath(self, html=''):
        # print(html)
        # 取得列表块
        doc = etree.HTML(html)
        # 网页上所有a标签的href地址
        all_a_url = doc.xpath('//a/@href')
        # all_img_url = doc.xpath('//img/@src')[0]

        # 地址
        return all_a_url

    # 获取超链接内容
    def get_a_text(self, html=""):
        a_text_p = ()
        try:
            a_text_p = re.findall("href=[\"'](.*?)[\"'](.*?)>(.*?)</a>", html)
        except:
            pass
        return a_text_p

    # 去除噪点
    def addr_clear(self, all_a_url_p):
        list_url = []
        for url in all_a_url_p:
            # 先去除 噪点
            if "javascript" not in url and url.replace('#', '') != "":
                # 去除重复
                if url not in list_url:
                    list_url.append(url.strip())
        return list_url

    # 截取相对路径
    def current_url_get(self, url_p=""):
        url_t = ""
        if ("://" in url_p):
            url_t = url_p.split('://')[0]
            url_p = url_p.replace(url_t + "://", "")
            # 如果存在二级及以上的虚拟目录
            if ("/" in url_p):
                url_p = url_p.replace('/' + url_p.split('/')[-1], '/')
        else:
            return url_t
        return url_p

    # 计算完整的路径
    def addr_reckon(self, url, url_root):
        first_charate = url[0:1]
        second_charate = url[1:2]
        # print(first_charate)
        if first_charate == '/':
            # 根路径拼接
            url_root_temp = self.get_url_root(url=url_root)
            url = url_root_temp + "/" + url
            if second_charate == '/':
                url = url
        elif first_charate == '.':
            if second_charate == '/':
                # 当前路径下拼接
                url = url_root + url[1:]
            elif second_charate == '.':
                # 递归上层路径
                url = url[3:]
                # print(url)
                current_url = self.current_url_get(url_p=url_root)
                # print(url_root)
                url = self.addr_reckon(url=url, url_root=current_url)
        elif '//' in url:
            url = '//' + url.split('//')[1]
        elif ':' in url:
            url = '//' + url.split(':')[1]
        elif url[0:1] in ['?', '~', '+']:
            url = url
        if (url[0:5] == "http:" and url[0:7] != "http://"):
            url = url[0:5] + "//" + url[6:len(url)]
        elif(url[0:5] == "https:" and url[0:7] != "https://"):
            url = url[0:6] + "//" + url[7:len(url)]
        elif(url[0:2] =="//"):
            url = "http:"+url

        return url

    # 读取网站域名
    def get_url_root(self, url):
        http = ''
        https = ''
        url_root = ''
        if 'http://' in url or 'http:/' in url:
            http = 'http://'
            url = url.replace('http://', '').replace('http:/', '').strip()
        elif 'https://' in url or 'https:/' in url:
            https = 'https://'
            url = url.replace('https://', '').replace('httpss:/', '').strip()
        else:
            pass
        url_root = url.split('/')[0]
        return (http + https + url_root)

    # 补全完整路径/
    def addr_whole(self, all_a_url, url_root, url_key=""):
        url_temp = []
        current_url = self.current_url_get(url_p=url_root)
        for url in all_a_url:
            if "http" not in url:
                # 计算完整路径
                url = self.addr_reckon(url, url_root=current_url)
            # 简单验证地址的正确性
            if self.addr_validate(url=url):
                url_temp.append(url.strip())
        all_a_url = url_temp
        return all_a_url

    # 简单验证地址的正确性
    def addr_validate(self,url=''):
        url_head = url.split(':')[0]
        if url_head not in ['http','https','ftp']:
            if url[0:2] == '//':
                return True
            if url[0:1] == '/':
                return True
            return False
        else:
            return True

    def main(self):
        print("")

#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更"],
    "初创时间":["2018年10月"],
    "功能":["html功能模块 1.0"],
    }
    #0 版本说明
    def version(dic_p={}):
        print ("\n")
        print ("-----------------------------")
        [print("\n",x," --- ",re.sub("[\[,\],\',\,]", "", str(dic_p[x])),"\n") for x in dic_p] # 调试用
        print ("-----------------------------")
        print ("")  # 防止代码外泄 只输出一个空字符
        
    version(dic_p=dic_note) # 打印版本
    print ("hello world!")

if __name__ == '__main__':
    main()
#---------- 主过程<<结束>> -----------#