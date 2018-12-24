#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import sys # 操作系统模块

#-----系统外部需安装库模块引用-----
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

from tornado.options import define, options

#-----DIY自定义库模块引用-----
from service.handler import * #导入web路由
import config # 主配置参数
import diy.inc_sys as inc_sys # 自定义系统功能函数模块

#--------- 外部模块处理<<结束>> ---------#

#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理
###config_web_start###

#mvc配置_start
settings = {
    "template_path": './statics/views',    #前台渲染模板文件路径
    "static_path": './statics/',    #静态文件路径
    "static_url_prefix": '/statics/',  #静态文件前缀
    "cookie_secret": "bZJc2derneeos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",    #构造函数中指定cookie_secret参数
    "login_url": "/login",
    "autoreload":True,
    #"xsrf_cookies": True,    #防止cookie的跨站访问攻击
    #"xheaders":True,
    }
#mvc配置_end

#web路由配置_start
handler_list=[
    (r"/", IndexHandler),    #主页
    (r'/api', Api),    #API服务
    (r'/script', ScriptHandler),    #寄生脚本处理
    ]
#web路由配置_end

###config_web_end###

# ---本模块内部类或函数定义区

# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更","王滕辉"],
"初创时间":["2018年10月"],
"功能":["基于tornado的web服务 1.0"],
}

def web_start():

    inc_sys.version(dic_p=dic_note) # 打印版本
    define("port", default=config.dic_config["web_port"], help="run on the given port", type=int)
    tornado.options.parse_command_line()
    app = tornado.web.Application(handler_list, **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print ("Note: Running on http://" + config.dic_config["ip"] + ":" + config.dic_config["web_port"] + " (Press Ctrl+Break to quit)")
    tornado.ioloop.IOLoop.instance().start()

#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():

    web_start() #启动网站伺服主程序

if __name__ == "__main__":
    
    main()
    
#---------- 主过程<<结束>> -----------#