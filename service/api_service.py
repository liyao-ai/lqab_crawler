#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import time
from bs4 import BeautifulSoup as bs_4
import uuid

sys.path.append("..")
from diy.inc_conn import Conn_mysql
from diy.inc_html import HtmlSource
import config #系统配置参数

# API模式下的爬虫
class CrawlerService():
    
    def __init__(self):
        pass
        
    # 标准爬虫采集程序
    def crawler_url(self,url_p=""):
        
        chartset_code = ""
        code_html = "" # html格式原码
        # 使用自定义获取源码脚本获取 网页
        source = HtmlSource()
        code_html,chartset_code = source.get_html(url_p=url_p,type_p='rg')
        return code_html,chartset_code
        
    # 搜狗爬虫采集程序
    def crawler_sogou(self,searchUrl,keyword,plant,data_if=0):
        
        # 通用数据库连接 全局接口
        conn = Conn_mysql(
        host=config.dic_config["host_mysql"], 
        port=int(config.dic_config["port_mysql"]), 
        user=config.dic_config["user_mysql"], 
        passwd=config.dic_config["pwd_mysql"], 
        db="lqab_basedata_" + config.dic_config["name_mysql_after"]
        )
        chartset_code = ""
        # 使用自定义获取源码脚本获取 网页
        source = HtmlSource()

        html,chartset_code = source.get_html(url_p=searchUrl,type_p='rg')
        #使用beautifulSoup 解析html 字符串，'lxml' 原理还是xPath
        soup = bs_4(html,'lxml')
        # beautifulSoup 写法解析获取列表 区别 find  与 findAll
        result_list = soup.find("div", id="main").find("div", class_="results").findAll("div",class_="vrwrap")
        
        dic_t = {}
        url = ""
        i = 1
        for result in result_list:
        
            print ("\n\n<",i,">步子处理。")
            #print(result)
            content = b""
            dic_t[i] = {"title":"","url":"","summary":"","snapshot":"","content":"","chartset":""}
            
            try:
                
                if(result.find("h3",class_="vrTitle")!=None):
                    title = result.find("h3",class_="vrTitle").get_text()
                else:
                    title = ''
                dic_t[i]["title"] = title
            
                if(result.find("div",class_="fb")!=None):
                
                    if(result.find("div",class_="fb").find("a")!=None):
                        snapshot = result.find("div",class_="fb").find("a").get("href")
                    else:
                        snapshot=''
                else:
                    snapshot=''
                dic_t[i]["snapshot"] = snapshot
                content,chartset_code = source.get_html(url_p=snapshot,type_p='rg_byte')
                
                if(result.find("h3")!=None):
                    url = "https://www.sogou.com"+result.find("h3").find("a").get("href")
                else:
                    url=''
                
                dic_t[i]["url"] = url
            
                if (content.strip() == ""):
                    content,chartset_code = source.get_html(url_p=url,type_p='rg')
                    dic_t[i]["chartset"] = chartset_code
                
                if(result.find(class_="str_info")!=None):
                    summary = result.find(class_="str_info").get_text()
                else:
                    if(result.find(class_="str-text-info")!=None):
                        summary = result.find(class_="str-text-info").get_text()
                    else:
                        summary = ''
            
                if (content == b""):
                    content,chartset_code = source.get_html(url_p=url,type_p='rg_byte')
            
                if (content != b""):
            
                    # 利用识别的编码进行解码
                    if (source.code_standard_is(chartset_p=chartset_code)):
                        print ("<<原文编码识别[通过]>>")
                    
                        try:
                            content = content.decode(chartset_code)
                        except Exception as e:
                            print ("二次爬取编码错误：",e)
                        chartset_code += "_fail" 
                        content = str(content)
                
                else:
                
                    chartset_code += "_fail" 
                    content = str(content)
                    
                dic_t[i]["chartset"] = chartset_code
                dic_t[i]["content"] = content  # 提取纯文本
            
            except Exception as e:
                
                print (e)
                
            time.sleep(1) # 间隔一秒钟
            i +=1 
            
        conn.close()
        
        return dic_t
        
    # 百度爬虫采集程序
    def crawler_baidu(self,searchUrl,keyword,plant,data_if=0):
        
        # 通用数据库连接 全局接口
        conn = Conn_mysql(
        host=config.dic_config["host_mysql"], 
        port=int(config.dic_config["port_mysql"]), 
        user=config.dic_config["user_mysql"], 
        passwd=config.dic_config["pwd_mysql"], 
        db="lqab_basedata_" + config.dic_config["name_mysql_after"]
        )
        chartset_code = ""
        # 使用自定义获取源码脚本获取 网页
        source = HtmlSource()
        html,chartset_code = source.get_html(url_p=searchUrl,type_p='rg')
        #使用beautifulSoup 解析html 字符串，'lxml' 原理还是xPath
        soup = bs_4(html,'lxml')
        # beautifulSoup 写法解析获取列表 区别 find  与 findAll
        result_list = soup.find("div",id="content_left").findAll("div",srcid="1599",tpl="se_com_default")
        dic_t = {}
        i = 1
        for result in result_list:
        
            print ("\n\n<",i,">步子处理。")
            #print(result)
            content = b""
            dic_t[i] = {"title":"","url":"","summary":"","snapshot":"","content":"","chartset":""}
            
            title = result.find("h3").get_text()
            dic_t[i]["title"] = title
            
            try:
            
                snapshot = result.find("div", class_="f13").find("a", class_="m").get("href")
                dic_t[i]["snapshot"] = snapshot
                content,chartset_code = source.get_html(url_p=snapshot,type_p='rg_byte')
                
            except Exception as e:
                print (e)
            
            url = result.find("h3").find("a").get("href")
            dic_t[i]["url"] = url
            if (content.strip() == ""):
                content,chartset_code = source.get_html(url_p=url,type_p='rg')
                dic_t[i]["chartset"] = chartset_code
                
            summary = result.find("div", class_="c-abstract").get_text()
            dic_t[i]["summary"] = summary
            
            if (content == b""):
                content,chartset_code = source.get_html(url_p=url,type_p='rg_byte')
            
            if (content != b""):
            
                # 利用识别的编码进行解码
                if (source.code_standard_is(chartset_p=chartset_code)):
                    print ("<<原文编码识别[通过]>>")
                    
                    try:
                        content = content.decode(chartset_code)
                    except Exception as e:
                        print ("二次爬取编码错误：",e)
                        chartset_code += "_fail" 
                        content = str(content)
                
                else:
                
                    chartset_code += "_fail" 
                    content = str(content)
                    
            dic_t[i]["chartset"] = chartset_code
            dic_t[i]["content"] = content  # 提取纯文本
            
            time.sleep(1) # 间隔一秒钟
            i +=1 
            
        conn.close()
        
        return dic_t
        
    # 360爬虫采集程序
    def crawler_360(self,searchUrl,keyword,plant,data_if=0):
        
        # 通用数据库连接 全局接口
        conn = Conn_mysql(
        host=config.dic_config["host_mysql"], 
        port=int(config.dic_config["port_mysql"]), 
        user=config.dic_config["user_mysql"], 
        passwd=config.dic_config["pwd_mysql"], 
        db="lqab_basedata_" + config.dic_config["name_mysql_after"]
        )
        chartset_code = ""
        # 使用自定义获取源码脚本获取 网页
        source = HtmlSource()
        html,chartset_code = source.get_html(url_p=searchUrl,type_p='rg')
        #使用beautifulSoup 解析html 字符串，'lxml' 原理还是xPath
        soup = bs_4(html,'lxml')
        # beautifulSoup 写法解析获取列表 区别 find  与 findAll
        result_list = soup.find("div", id="container").find("ul", class_="result").findAll("li")
        dic_t = {}
        i = 1
        for result in result_list:
        
            print ("\n\n<",i,">步子处理。")
            content = b""
            
            dic_t[i] = {"title":"","url":"","summary":"","snapshot":"","content":"","chartset":""}
            
            if(result.get("data-urlfp") != None):
            
                title = result.find("h3").get_text()
                dic_t[i]["title"] = title
                
                url = result.find("h3").find("a").get("href")
                dic_t[i]["url"] = url
                
                if(result.find("p", class_="res-desc")!=None):
                    summary = result.find("p", class_="res-desc").get_text()
                else:
                    summary = ''
                dic_t[i]["summary"] = summary
                
                if(result.find("p", class_="res-linkinfo").find("a", class_="m")!=None):
                    snapshot = result.find("p", class_="res-linkinfo").find("a", class_="m").get("href")
                else:
                    snapshot=''
                dic_t[i]["snapshot"] = snapshot
                
                if (content.strip() == "" and summary != ''):
                    content,chartset_code = source.get_html(url_p=url,type_p='rg')
                    dic_t[i]["chartset"] = chartset_code

                if (content == b"" and url != ''):
                    content,chartset_code = source.get_html(url_p=url,type_p='rg_byte')
            
                if (content != b""):
            
                    # 利用识别的编码进行解码
                    if (source.code_standard_is(chartset_p=chartset_code)):
                        print ("<<原文编码识别[通过]>>")
                    
                        try:
                            content = content.decode(chartset_code)
                        except Exception as e:
                            print ("二次爬取编码错误：",e)
                            chartset_code += "_fail" 
                            content = str(content)
                
                    else:
                
                        chartset_code += "_fail" 
                        content = str(content)
                    
            dic_t[i]["chartset"] = chartset_code
            dic_t[i]["content"] = content  # 提取纯文本
            
            time.sleep(1) # 间隔一秒钟
            if (i > 20):
                break # 加入空地址熔断
            else:
                i +=1 
            
        conn.close()
        
        return dic_t
        
#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更","王滕辉"],
    "初创时间":["2018年10月"],
    "功能":["API服务功能模块 1.0"],
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


