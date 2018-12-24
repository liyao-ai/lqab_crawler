#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import sys
import os
#-----系统外部需安装库模块引用-----
import sqlite3
import pymysql
#-----DIY自定义库模块引用-----

sys.path.append("..")
from config import dic_config #系统配置参数

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# ---本模块内部类或函数定义区
# sqlite3数据库对象
class Conn_sqlite3():

    def __init__(self,path_data,memory_if=0,cached_statements=100,timeout=5):
        
        # 如果数据库路径为空，则赋值为默认路径
        if (path_data == ""):
            self.path_data =  config.path_main + "data\\sqlite\\main_sqlite.db"
        else:
            self.path_data = path_data
            
        try:
        
            if (memory_if == 0):
                self.conn = sqlite3.connect(self.path_data,cached_statements,timeout)
                
                #print("sqllite文件型调用:[{}]".format(self.path_data)) # 调试用
            else:
                self.conn = sqlite3.connect(':memory:')
                
                #print("sqlite内存型调用:[:memory:]") # 调试用
        
        except Exception as e:
        
            print('事务处理失败', e)

    # 全表读数据方法
    def read_sql(self, sql):
        res = 0
        data = ()
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            res = len(data)
        except:
            pass
        self.cur.close()
        return res, data
        
    # 数据写操作方法
    def write_sql(self, sql, *args):
        res = 0
        self.cur = self.conn.cursor()
        try:
        
            self.cur.execute(sql, *args)
            self.conn.commit()
            res = self.cur.rowcount
            
        except:
        
            res = -1
            
        self.conn.commit()
        self.cur.close()
        return res
        
        
    #利用脚本批量操作的方法
    def script(self,script_p):
        
        result = 1
        self.cur = self.conn.cursor()
        try:
            self.cur.executescript(script_p)
        except:
            result =0
        self.cur.close()
        return result
    
    # 传递连接对象
    def get_conn(self):
        return self.conn
        
    # 关闭游标
    def close_cur(self):
        self.cur.close()
    
    # 关闭连接对象
    def close(self):
        self.conn.commit()
        self.conn.close()

# mysql数据库对象
class Conn_mysql():

    def __init__(self, host='localhost', user='root', passwd='', db=dic_config['db'], port=3306, charset="utf8",cursorclass = pymysql.cursors.Cursor):
        
        #print ("host=",host," user=",user," passwd=",passwd," db=",db," port=",port," charset=",charset) # 调试用
        try:
            self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset,cursorclass = cursorclass)
            self.cur = self.conn.cursor()
        except Exception as e:
            print ("host=",host," user=",user," passwd=",passwd," db=",db," port=",port," charset=",charset) # 调试用
            print('数据库打开事务处理失败', e)
    
    # 全表读数据方法
    def read_sql(self, sql):
        res = 0
        data = ()
        self.cur = self.conn.cursor()
        try:
            res = self.cur.execute(sql)
            data = self.cur.fetchall()
        except:
            pass
        self.cur.close()
        return res, data
        
    # 分页读数据方法
    def read_sql_page(self, sql, values_p):
        res = 0
        data = ()
        self.cur = self.conn.cursor()
        try:
            res = self.cur.execute(sql)
            if (values_p < res):
                self.cur.scroll(values_p,'relative')
            data = self.cur.fetchall()
        except:
            pass
        self.cur.close()
        return res, data
    
    # 数据写操作方法
    def write_sql(self, sql, *args):
        try:
            self.cur = self.conn.cursor()
            
            if ("update " in sql):
                
                effect_row = self.cur.execute(sql, *args)
                #print("update_effect_row=",effect_row) # 调试用
                if (effect_row > 0):
                    return True
                else:
                    return False
                    
            if ("insert " in sql):
                effect_row = self.cur.execute(sql, *args)
                #print("insert_effect_row=",effect_row) # 调试用
                if (effect_row > 0):
                    return True
                else:
                    return False
                
            self.cur.execute(sql, *args)
            self.conn.commit()
            self.cur.close()
            return True
        except:
            return False
            pass
        
    # 传递连接对象
    def get_conn(self):
        return self.conn
    
    # 关闭游标
    def close_cur(self):
        try:
            self.cur.close()
        except Exception as e:
            print('数据库关闭游标处理失败', e)
            
    # 关闭连接对象
    def close(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print('数据库关闭连接处理失败', e)
            
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#
def main():

    import re #正则处理
    # 说明字典
    dic_note = {
    "版权":["LQAB工作室"],
    "作者":["集体","吉更"],
    "初创时间":["2018年10月"],
    "功能":["数据库功能模块 1.0"],
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