import re
import time
import urllib.parse

from pymysql import *

url_mapping = dict()

#数据库事务支持
def dao_transaction(db, sql, params):
    conn = connect(host='localhost', port=3306, database=db, user='root', password='123456', charset='utf8')

    cs = conn.cursor()

    res = cs.execute(sql, params)

    conn.commit()
    # 关闭Cursor对象
    cs.close()
    # 关闭Connection对象
    conn.close()
    return res

#查询所有
def fetch_all(db, sql, params):
    conn = connect(host="localhost", port=3306, user='root', password='123456', database=db, charset='utf8')
    cs = conn.cursor()
    cs.execute(sql, params)
    records = cs.fetchall()

    cs.close()
    conn.close()
    return records

#查询一条
def fetch_one(db, sql, params):
    conn = connect(host="localhost", port=3306, user='root', password='123456', database=db, charset='utf8')
    cs = conn.cursor()
    cs.execute(sql, params)
    record = cs.fetchone()

    cs.close()
    conn.close()
    return record


#路由装饰器
def route(pre):
    def regist(func):
        url_mapping[pre] = func

        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped_func

    return regist

#自定义的处理器
@route('/index')
def index(params):
    return "主页面"
@route('/index/about')
def about(params):
    return "主页面下的关于页面"

#处理器映射器
def mapper(env, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html;charset=UTF-8')]
    start_response(status, response_headers)
    if env['url'][4:] in url_mapping:
        print('url='+env['url'][4:])
        try:
            return url_mapping[env['url'][4:]](env['params'])
        except Exception as e:
            print(e)
            return "系统异常，请稍后再试"
    else:
            return "请求的路径无效!"
