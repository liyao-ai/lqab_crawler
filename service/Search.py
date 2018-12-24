#!/usr/bin/python3
import sys
import os
import json
from flask import Response,Blueprint
sys.path.append("..")
from service.search_service import SearchService
import config #系统配置参数
# 使用 蓝图 定义 模块，
dosearch = Blueprint(name='dosearch',import_name="dosearch" ,static_folder='./statics',template_folder='./templates')

# 提供健康检查用接口
@dosearch.route("/<type>/<keyword>",methods=['POST','get'])
def search(type,keyword):
    result = {'type': 'keyword'}
    searchService =  SearchService()
    data = searchService.findAll(page_number=1,page_size=10,search_keyword=keyword,search_plant=type)
    return Response(json.dumps(data), mimetype='application/json') # 采用json方式发送数据
    
#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更","王滕辉"],
    "初创时间":["2018年10月"],
    "功能":["搜索功能模块 1.0"],
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