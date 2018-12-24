#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys # 系统模块
import json
from flask import Response,Blueprint,request
sys.path.append("..")
from service.api_service import CrawlerService
import config #系统配置参数

# 使用 蓝图 定义 模块，
api_main = Blueprint(name='api',import_name="api" ,static_folder='./statics',template_folder='./templates')

searchUrlListKey= [{
                'name': '360',
                'searchSrc': 'https://www.so.com/s?ie=utf-8&shb=1&src=360sou_newhome&q='
            },
            {
                'name': 'baidu',
                'searchSrc': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd='
            },
            {
                'name': 'sogou',
                'searchSrc': 'https://www.sogou.com/web?query='
            }]

# 提供健康检查用接口
@api_main.route("/<to_do>/",methods=['POST','get'])
def search(to_do):

    keyword = ""
    if (request.method == "POST"):
        keyword = request.form.get("keyword")
    if (request.method == "get"):
        keyword = request.args.get("keyword")
        
    web_is = ""
    if (request.method == "POST"):
        web_is = request.form.get("web_is")
    if (request.method == "get"):
        web_is = request.args.get("web_is")
        
    result = {"code":1,"action":"api","to_do":to_do,"keyword":keyword,"web_is":web_is}
    
    for url in searchUrlListKey:
        print (url["name"],web_is) # 调试用
        if (url['name']==web_is):
        
            searchUrl = url['searchSrc']+keyword
            try:
                print ("crawler_url ---",searchUrl)
            except:
                pass
            
            crawlerService = CrawlerService()
            if (web_is == "baidu"):
                print("数据源",web_is)
                result = crawlerService.crawler_baidu(searchUrl=searchUrl,keyword=keyword,plant=web_is)
            if (web_is == "sogou"):
                print("数据源",web_is)
                result = crawlerService.crawler_sogou(searchUrl=searchUrl,keyword=keyword,plant=web_is)
            if (web_is == "360"):
                print("数据源",web_is)
                result = crawlerService.crawler_360(searchUrl=searchUrl,keyword=keyword,plant=web_is)
                
            break
            
    try:
        return Response(json.dumps(result,ensure_ascii=False), mimetype='application/json') # 采用json方式发送数据
    except:
        return Response(str(result).encode("utf-8"))

#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更","王滕辉"],
    "初创时间":["2018年10月"],
    "功能":["API功能模块 1.0"],
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
