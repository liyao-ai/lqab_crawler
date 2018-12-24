  #!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import os # 操作系统模块
import sys # 操作系统模块1
import datetime # 系统时间模块1
import time # 系统时间模块2
import json # json处理模块

#-----系统外部需安装库模块引用-----

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options


#-----DIY自定义库模块引用-----
sys.path.append("..")
import config #系统配置参数
import diy.inc_sys as inc_sys #自定义系统级功能模块 
import diy.inc_conn as inc_conn #自定义数据库操作模块
import diy.inc_hash as inc_hash # 基本自定义hash模块
import diy.inc_file as inc_file # 基本自定义文件模块
from service.api_service import CrawlerService
 
#-----DIY自定义库模块引用-----

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# ---本模块内部类或函数定义区

# web服务基础模块
class BaseHandler(tornado.web.RequestHandler):

    # 获得浏览器传递参数
    def browser_argument(self,name_p=""):
        
        value_p = ""
        
        if (name_p != ""):
        
            try:
                if (name_p in self.request.arguments):
                    value_p = self.request.arguments[name_p][0].decode('utf-8')
            except:
                pass
                
        print ("输入参数名：",name_p,"返回参数值：",value_p)
        
        return value_p
        
    # 动态调用模块
    def import_do(self,file_p="",args_p=""):
        
        result = ""
        
        run_model =__import__(file_p)
        result = run_model.run_it(args_p)
        #try:
            #run_model =__import__(file_p)
            #result = run_model.run_it(args_p)
        #except:
            #result = "模块不存在或调用接口错误"
            
        return result

# 主页模块
class IndexHandler(tornado.web.RequestHandler):
    
    def get(self,*args):
        
        # 访问日志处理
        dic_login_p = {}
        dic_t = {}
        txt_log = "" # 日志的文本内容
        path_p = config.path_main + "\\data\\log\\z_log_web_index.csv"
        file_file = inc_file.File_file()
        dic_t["time_v"] = inc_sys.str_split(datetime.datetime.now()) # 访问时间
        dic_t["ip"] = self.request.remote_ip # 获得IP
        dic_t["id"] = 0
        # 获得用户cookie资料
        try:
            
            str_t = self.get_secure_cookie("session_lqab_user")
            str_t = str_t.decode('utf-8')
            # 解密session字典
            str_t = secret_lqab(str_t,key_p=config.dic_config["secret_key"],salt_p = config.dic_config["secret_salt"],secret_if="no")
            dic_login_p = eval(str_t)
            if ("id" in dic_login_p):
                dic_t["id"] = dic_login_p["id"]
            
        except:
        
            pass
        
        #print ("日志参数",path_p,dic_t) # 调试用
        
        # 将访问日志字典转化为csv格式
        if (dic_t):
            txt_log = str(dic_t["id"]) + "," + dic_t["ip"] + "," + dic_t["time_v"] + "\n"
            
        # 写入访问日志
        try:
            file_file.write_add(path_p=path_p,renew_if=0,content_p=txt_log)
        except:
            pass
            
        # 渲染首页
        self.render('index.html',
        name_soft=config.dic_config["name_soft"],
        type_soft=config.dic_config["type_soft"],
        vol_soft=config.dic_config["vol_soft"],
        authority_soft=config.dic_config["authority_soft"],
        author_soft=config.dic_config["author_soft"],
        qq_group=config.dic_config["qq_group"],
        tel_lqab=config.dic_config["tel_lqab"],
        url_lqab=config.dic_config["url_lqab"],
        sys_time=str(datetime.datetime.now())
        ) #渲染首页
        
#APi模块 强调速度 系统核心服务模块
class Api(BaseHandler):
    
    # 爬虫语义意图form处理
    def crawler_intention_form(self,web_is_p="",keyword_p=""):
        
        searchUrl_p = "" #form提交地址
        
        searchUrlListKey = [{
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
        
        for url in searchUrlListKey:

            if (url['name']==web_is_p):
        
                searchUrl_p = url['searchSrc']+keyword_p
                try:
                    print ("crawler_url ---",searchUrl)
                except:
                    pass
                    
        return searchUrl_p
        
    # 爬虫意图识别
    def crawler_intention(self,txt_p):
        result = False
        import re
        pattern = re.compile(r'([a-z][a-z0-9+\-.]*)://([a-zA-Z0-9\-._~%]+|\[[a-zA-Z0-9\-._~%!$&\'()*+,;=:]+\])(:[0-9]+)?([a-zA-Z0-9\-\/._~%!$&\'()*+]+)?(\?[a-zA-Z0-9&=]+)?')    # 匹配模式
        url = re.findall(pattern,txt_p)
        if (url != []):
            result = True
        return result
    
    # 主执行过程
    def do_it(self):
        
        crawlerService = CrawlerService()
        result = ""
        args_p = {}
        uid = ""
        ckey = ""
        keyword = ""
        web_is = "url"
        dic_t = self.request.arguments
        rs_basedata_mysql = inc_conn.Conn_mysql(config.dic_config["host_mysql"],config.dic_config["user_mysql"],config.dic_config["pwd_mysql"], "lqab_basedata_" + config.dic_config["name_mysql_after"], int(config.dic_config["port_mysql"]))
        secret = inc_hash.Secret() # 加解密类实例化
        dic_result = {}
        chartset_code = ""
        url_intention = True
        dic_result = {} #最后的结果字典
        txt_last = "" # 最后的返回文本
        
        for x in dic_t:
            try:
                args_p[x]= dic_t[x][0].decode('utf-8')
            except:
                pass
        if ("keyword" in args_p):
            keyword = args_p["keyword"]
            if (keyword.strip() == ""):
                self.write("关键词不能为空！")
                return ""
        # 获得密钥
        if ("uid" in args_p):
            uid = args_p["uid"]
            sql = "select ckey from crawler_key where id=" + uid
            res, rows = rs_basedata_mysql.read_sql(sql)
            if (res < 1):
                self.write("用户未被识别！")
                return ""
            else:
                ckey = rows[0][0]
                print ("双向密钥：",ckey)
        else:
            self.write("UID不能为空！")
            return ""
        
        dic_result["time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        url_intention = self.crawler_intention(txt_p=keyword)
        if (url_intention):
        
            print("<<<网址爬取意图>>>")
            result,chartset_code = crawlerService.crawler_url(url_p=keyword)
            print("html原码长度：",len(result))
            dic_result["action"] = "url"
            dic_result["code"] = result
            dic_result["chartset"] = chartset_code
            
        else:
        
            print("<<<语义搜索意图>>>")
            if ("web_is" in args_p):
                web_is = args_p["web_is"]
            else:
                web_is = "intention"
            
            searchUrl = self.crawler_intention_form(web_is_p=web_is,keyword_p=keyword) #获得form地址 
            print ("提交站点：",web_is," form地址：",searchUrl)
            
            if (web_is == "baidu"):
                dic_result["main"] = crawlerService.crawler_baidu(searchUrl=searchUrl,keyword=keyword,plant=web_is)
                
            if (web_is == "sogou"):
                dic_result["main"] = crawlerService.crawler_sogou(searchUrl=searchUrl,keyword=keyword,plant=web_is)
                
            if (web_is == "360"):
                dic_result["main"] = crawlerService.crawler_360(searchUrl=searchUrl,keyword=keyword,plant=web_is)
        
        # 处理结果回写

        # 加密处理
        if (dic_result):
            try:
                txt_last = json.dumps(dic_result,ensure_ascii=False)
            except:
                pass
            if (ckey != "n/a"):
                txt_last = secret.secret_lqab(text_p=txt_last,secret_if="yes",key_p=ckey,salt_p = b'llqqaabbiissookk')
        
        self.write(txt_last)
        
    # get方式登录
    def get(self):
        self.do_it()
    
    # post方式登录
    def post(self):
        self.do_it()

# 寄生脚本处理 模仿文件型脚本调用调用
class ScriptHandler(BaseHandler):
    
    # 权限检查
    def roles_chk(self,file_p="",code_p="",roles_p=""):
        
        pass_if = False
        
        rs_sqlite_file = Conn_sqlite3(config.path_main + config.dic_config["path_sqlite"],0)
        sql = "select id from menu_list "
        sql += "where file_name ='" + file_p + "." + code_p + "' "
        sql += "and admin like '%-"+ roles_p + "-%' "
        res, rows = rs_sqlite_file.read_sql(sql)
        print("权限查询语句：",sql) #调试用
        if (res > 0):
            pass_if = True
            
        rs_sqlite_file.close_cur() # 关闭数据库游标
        rs_sqlite_file.close() # 关闭数据库连接
            
        return pass_if
    
    # 动态执行内容获取
    def content_get(self,roles_p="",file_p="",code_p="",args_p=""):
        
        result = ""
        pass_if =  True
        #1 权限检查
        pass_if = self.roles_chk(file_p=file_p,code_p=code_p,roles_p=roles_p)
        if (pass_if is False):
            result = "管理员操作权限不匹配或权限表故障"
            return result
        
        # 获得脚本文件名    
        try:
            file_p = self.browser_argument(name_p="file")
            #self.write (file) #调试用
        except:
            pass
        try:
            print ("脚本文件路径：",file_p,"参数字典：",args_p) # 调试用
        except:
            pass
            
        result = self.import_do(file_p=file_p,args_p=args_p) # 获得动态执行模块结果
            
        return result
        
    # 主执行过程
    def do_it(self,*args):
        
        roles_p = "" # 权限值初始化
        file_p = "" # 请求功能模块名
        code_p = "" # 请求功能模块名
        output = "" # 请求结果的输出方式
        time_now_p = str_split(datetime.datetime.now()) # 请求时间
        path_p = config.path_main + "\\data\\log\\"
        dic_t = {}
        str_log = ""
        args_p = {}
        
        # 取得web端提交参数
        dic_t = self.request.arguments
        for x in dic_t:
            try:
                args_p[x] = dic_t[x][0].decode('utf-8')
            except:
                pass
            
        
        # 登录校验
        pass_if,dic_login_p = self.admin_login_check(time_alive_p=config.dic_config["time_alive"])
        
        if (pass_if is False):
        
            self.render('login_admin.html',
            name_soft=config.dic_config["name_soft"],
            type_soft=config.dic_config["type_soft"],
            vol_soft=config.dic_config["vol_soft"],
            )
            
        # 参数处理
        
        roles_p = dic_login_p["roles"]
        try:
            file_p = self.browser_argument(name_p="file")
            code_p = self.browser_argument(name_p="code")
            output = self.browser_argument(name_p="output")
        except:
            pass
        print ("脚本调用参数",roles_p,file_p,code_p,output) # 调试用
        
        # 业务处理
        args_p["roles"] = roles_p # 追加操作权限参数
        if ("aid" in dic_login_p):
            args_p["aid"] = str(dic_login_p["aid"]) # 追加管理员ID
            
        content = self.content_get(roles_p=roles_p,file_p=file_p,code_p=code_p,args_p=args_p)
        
        # 写入操作日志
        if (config.dic_config["log_if"] == "1"):
        
            path_p += "z_log_script.csv"
            args_p["time_run"] = str_split(datetime.datetime.now()).encode('utf_8')
            file_file = inc_file.File_file()
            
            # 将访问日志字典转化为csv格式
            txt_log = ""
            
            #print ("基础参数字典",args_p) # 调试用
            print ("日志路径",path_p) # 调试用
            
            if (args_p):

                try:
                    txt_log = args_p["file"][0] + "," + args_p["code"][0] + "," + args_p["output"][0] + "," + args_p["roles"] + "," +  args_p["time_run"] +  "\n"
                    file_file.write_add(path_p=path_p,renew_if=0,content_p=txt_log)
                except:
                    pass
                    
        # 结果展示
        if (output == "html"):
            self.write(content) # 调试用
        
    def get(self,*args):
    
        self.do_it()
        
    def post(self,*args):

        self.do_it()
# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年10月"],
"功能":["主执行句柄模块"],
}
# 主过程子函数
def run_it():
    
    result_p = "hello world!"
    inc_sys.version(dic_p=dic_note) # 打印版本
    
    return result_p # 调试用

#--------- 内部模块处理<<结束>> ---------#

#---------- 过程<<开始>> -----------#
def main():
    
    #1 过程一
    print(run_it())
    #2 过程二
    #3 过程三

if __name__ == "__main__":
    main()
#---------- 主过程<<结束>> -----------#