#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
from diy.inc_conn import Conn_mysql
import config
import pymysql
# 本地缓存服务
class SearchService():

    def __init__(self):
        pass
    def findAll(self,page_number=1,page_size=10,search_keyword="",search_plant=""):
        # 通用数据库连接 全局接口
        conn = Conn_mysql(
        host=config.dic_config["host_mysql"], 
        port=int(config.dic_config["port_mysql"]), 
        user=config.dic_config["user_mysql"], 
        passwd=config.dic_config["pwd_mysql"], 
        db="lqab_basedata_" + config.dic_config["name_mysql_after"],
        cursorclass = pymysql.cursors.DictCursor
        )
        sql  ="select uuid,title,url,summary,snapshot,search_keyword,search_plant,create_user from search_local_temp where search_plant='%s' and search_keyword='%s' limit %d,%d" %(search_plant,search_keyword,(page_number-1)*page_size,page_size)
        res,data = conn.read_sql(sql=sql)
        #try:
            #print(data)
        #except:
            #pass
        conn.close()
        return data

#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更","王滕辉"],
    "初创时间":["2018年10月"],
    "功能":["搜索服务功能模块 1.0"],
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
