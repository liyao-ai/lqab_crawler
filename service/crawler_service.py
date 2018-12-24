#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import os
import uuid
import pymysql
import chardet

from bs4 import BeautifulSoup as bs_4

sys.path.append("..")
from diy.inc_conn import Conn_mysql
from diy.inc_html import HtmlSource

import config #系统配置参数


# 爬虫服务
class CrawlerService():
    
    def __init__(self):
        pass
    
    # 爬虫采集程序
    def crawler(self,searchUrl,keyword,plant):
        
        dic_p = {} # 请求参数字典
        url_p = "" # post提交主网址
        code_html = "" # 返回的网址编码
        # 通用数据库连接 全局接口
        conn = Conn_mysql(
        host=config.dic_config["host_mysql"], 
        port=int(config.dic_config["port_mysql"]), 
        user=config.dic_config["user_mysql"], 
        passwd=config.dic_config["pwd_mysql"], 
        db="lqab_basedata_" + config.dic_config["name_mysql_after"],
        cursorclass = pymysql.cursors.DictCursor
        )
        # 使用自定义获取源码脚本获取 网页
        source = HtmlSource()
        
        # --- 各种网页爬虫内核提交方式 ---
        code_html,chartset_code = source.get_html(url_p=searchUrl,type_p='rg') # 调用request的get提交模式
        
        #if (len(searchUrl.split("?")) > 0):
            #url_p = searchUrl.split("?")[0]
            #list_t= searchUrl.split("?")[1].split("&")
            #for x in list_t:
                #dic_p[x.split("=")[0]] = x.split("=")[1]
            #print ("提交网址:",url_p,"参数字典：",dic_p) # 调试用
            #code_html,chartset_code = source.get_html(url_p=searchUrl,dic_p=dic_p,type_p='rp') # 调用request的post提交模式
        
        #code_html,chartset_code  = source.get_html(url_p=searchUrl,type_p='ug') # 调用urllib的get提交模式
        
        #if (len(searchUrl.split("?")) > 0):
            #url_p = searchUrl.split("?")[0]
            #list_t= searchUrl.split("?")[1].split("&")
            #for x in list_t:
                #dic_p[x.split("=")[0]] = x.split("=")[1]
            #print ("提交网址:",url_p,"参数字典：",dic_p) # 调试用
            #code_html,chartset_code  = source.get_html(url_p=searchUrl,dic_p=dic_p,type_p='up') # 调用urllib的post提交模式
        
        #使用beautifulSoup 解析html 字符串，'lxml' 原理还是xPath
        # beautifulSoup 写法解析获取列表 区别 find  与 findAll
        soup = bs_4(code_html,'lxml')
        if "百度" == plant:
            result_list =soup.find("div",id="content_left").findAll("div",srcid="1599",tpl="se_com_default")
            for result in result_list:
                #print(result)
                title = result.find("h3").get_text()
                url = result.find("h3").find("a").get("href")
                summary = result.find("div", class_="c-abstract").get_text()
                if(result.find("div", class_="f13").find("a", class_="m")!=None):
                    snapshot = result.find("div", class_="f13").find("a", class_="m").get("href")
                else:
                    snapshot=''
                sql = "insert into search_local_temp(uuid,title,url,summary,snapshot,search_keyword,search_plant,create_user) values('%s','%s','%s','%s','%s','%s','%s','%s') " % (uuid.uuid1(),title,url,summary,snapshot,keyword,plant,'wth')
                #print(sql)
                conn.write_sql(sql=sql)
        elif "360" == plant:
            result_list = soup.find("div", id="container").find("ul", class_="result").findAll("li")
            for result in result_list:
                print(result.get("data-urlfp"))
                if(result.get("data-urlfp")!=None):
                    # print(result)
                    title = result.find("h3").get_text()
                    url = result.find("h3").find("a").get("href")
                    if(result.find("p", class_="res-desc")!=None):
                        summary = result.find("p", class_="res-desc").get_text()
                    else:
                        summary=''
                    if(result.find("p", class_="res-linkinfo").find("a", class_="m")!=None):
                        snapshot = result.find("p", class_="res-linkinfo").find("a", class_="m").get("href")
                    else:
                        snapshot=''
                    sql = "insert into search_local_temp(uuid,title,url,summary,snapshot,search_keyword,search_plant,create_user) values('%s','%s','%s','%s','%s','%s','%s','%s') " % (
                    uuid.uuid1(), title, url, summary, snapshot, keyword, plant, 'wth')
                    # print(sql)
                    conn.write_sql(sql=sql)
        elif "搜狗" == plant:
            result_list = soup.find("div", id="main").find("div", class_="results").findAll("div",class_="vrwrap")
            for result in result_list:
                # print(result)
                if(result.find("h3",class_="vrTitle")!=None):
                    title = result.find("h3",class_="vrTitle").get_text()
                else:
                    title = ''
                if(result.find("h3")!=None):
                    url = "https://www.sogou.com"+result.find("h3").find("a").get("href")
                else:
                    url=''
                if(result.find(class_="str_info")!=None):
                    summary = result.find(class_="str_info").get_text()
                else:
                    if(result.find(class_="str-text-info")!=None):
                        summary = result.find(class_="str-text-info").get_text()
                    else:
                        summary = ''
                if(result.find("div",class_="fb")!=None):
                    if(result.find("div",class_="fb").find("a")!=None):
                        snapshot = result.find("div",class_="fb").find("a").get("href")
                    else:
                        snapshot=''
                else:
                    snapshot=''
                sql = "insert into search_local_temp(uuid,title,url,summary,snapshot,search_keyword,search_plant,create_user) values('%s','%s','%s','%s','%s','%s','%s','%s') " % (
                    uuid.uuid1(), title, url, summary, snapshot, keyword, plant, 'wth')
                # print(sql)
                conn.write_sql(sql=sql)


            
        conn.close()


#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更","王滕辉"],
    "初创时间":["2018年10月"],
    "功能":["爬虫服务功能模块 1.0"],
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

