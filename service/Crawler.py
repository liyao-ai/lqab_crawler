#!/usr/bin/python3
import sys
import json
from flask import Response,Blueprint,redirect
sys.path.append("..")
from service.crawler_service import CrawlerService
import config #系统配置参数
# 使用 蓝图 定义 模块，
crawler = Blueprint(name='crawler',import_name="crawler" ,static_folder='./statics',template_folder='./templates')

searchUrlListKey= [{
                'name': '360',
                'searchSrc': 'https://www.so.com/s?ie=utf-8&shb=1&src=360sou_newhome&q='
            },
            {
                'name': '百度',
                'searchSrc': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd='
            },
            {
                'name': '搜狗',
                'searchSrc': 'https://www.sogou.com/web?query='
            }]

# 提供健康检查用接口
@crawler.route("/<type_web>/<keyword>",methods=['POST','get'])
def search(type_web,keyword):
    result = {"code":1}
    for url in searchUrlListKey:
        try:
            print(url)
        except:
            pass
        if (url['name']==type_web):
            searchUrl = url['searchSrc']+keyword
            crawlerService = CrawlerService()
            crawlerService.crawler(searchUrl=searchUrl,keyword=keyword,plant=type_web)

                
    return Response(json.dumps(result), mimetype='application/json') # 采用json方式发送数据
    
#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更","王滕辉"],
    "初创时间":["2018年10月"],
    "功能":["爬虫功能模块 1.0"],
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
