#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import sys # 操作系统模块
import json
import os

#-----系统外部需安装库模块引用-----
from flask import Flask, Response,render_template,request,redirect

# 引入 模块
from service.Search import dosearch as search_blueprinit
from service.Crawler import crawler as crawler_blueprinit
from service.Api import api_main as api_blueprinit

#-----DIY自定义库模块引用-----
import config # 主配置参数
import diy.inc_sys as inc_sys # 自定义系统功能函数模块

#--------- 外部模块处理<<结束>> ---------#

#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# BASE_DIR建立一个基础路径，用于静态文件static，views的调用
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#web路由配置_start

app=Flask(__name__,template_folder='templates',static_folder='statics')
# 使用 蓝图 注册不同模块
app.register_blueprint(crawler_blueprinit,url_prefix='/crawler')
app.register_blueprint(search_blueprinit,url_prefix='/search')
app.register_blueprint(api_blueprinit,url_prefix='/api')

# 当访问 "/"，"/index"，"/home","incex.hltml" 默认跳转到 "/index.hmtl" 模板中渲染首页
@app.route("/")
@app.route("/home")
@app.route("/index")
@app.route("/index.html")

#web路由配置_end

# ---本模块内部类或函数定义区

def findhell():
    result = {'username': 'python', 'password': 'python'}
    return render_template('index.html', name=result) # 采用模板方式解析页面

# 提供健康检查用接口
@app.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json') # 采用json方式发送数据

# 测试接口
@app.route("/test")
def getUser():
    result = {'username': 'python', 'password': 'python'}
    return Response(json.dumps(result), mimetype='application/json')


######################################
#           错误控制中心             #
######################################

# 统一错误返回配置方法
def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(404) 
def page_not_found(error): 
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(400) 
def page_not_found(error): 
    content = json.dumps({"error_code": "400"})
    # resp = Response(content)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    resp = Response_headers(content)
    return resp
    # return "error_code:400"

@app.errorhandler(410) 
def page_not_found(error): 
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(500) 
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp

# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更","王滕辉"],
"初创时间":["2018年12月"],
"功能":["基于flask的web服务 1.0"],
}

#---------- 主过程<<开始>> -----------#

def main():

    inc_sys.version(dic_p=dic_note) # 打印版本
    # 端口号默认值自增一 防止与tornado冲突
    app.run(port=str(int(config.dic_config["web_port"]) + 1), host=config.dic_config["ip"])

if __name__ == "__main__":
    
    main()
    
#---------- 主过程<<结束>> -----------#
