# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import DBUtils
import pymysql
from DBUtils.PooledDB import PooledDB


class db_tool(object):
    """将采集的数据插入数据库"""
    def __init__(self):
        """"""
        self.pool = None
        self.mysql_connect = self.get_connect_nlp()

    def get_connect_nlp(self):
        conn = None
        if self.pool == None:
            self.pool = PooledDB(MySQLdb, 50, host='127.0.0.1', user='root', passwd='jingxin', db='nlp', port=3306,charset = "utf8")  # 5为连接池里的最少连接数
            conn = self.pool.connection()
        else:
            conn = self.pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了

        return conn

    def insert_data_long_query(self, body):
        """插入数据"""
        body = body.strip()
        value_list = [body]
        self.conn = self.mysql_connect
        sql = ("insert into nlp.article(body) values(%s)")
        cur = self.conn.cursor()
        cur.execute(sql,value_list)
        self.conn.commit()
        # res = cur.fetchone()
        cur.close()



class P1Pipeline(object):

    def __init__(self):
        self.tool = db_tool()

    def process_item(self, item, spider):

        speak = item["speak"]
        if len(speak.strip()) > 0:
            self.tool.insert_data_long_query(speak)
        return item
