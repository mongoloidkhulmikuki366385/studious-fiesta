# -*- coding: utf-8 -*-
__author__ = 'Simon Liu'


import pymysql
from sqltest.Configfile import *


class MysqlOperate(object):
    def __init__(self):
        self.conn = None
        self.cur = None
        self.init()
        self.connect()

    def init(self):
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.db = DB
        self.port = PORT
        self.charset = CHARSET

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                 db=self.db, port=self.port, charset=self.charset)
            if self.conn.open:
                self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
            else:
                raise Exception, "Mysql connect fail!"
        except Exception as e:
            raise e

    def insert_to_table(self):
        try:
            cmd = [
                'insert into `user` value(16,"Peter","goudang","male")',
                'insert into `user`(`name`,`nickname`,`sex`) value("Lisa","混元霹雳手","male")',
                'insert into `user`(`name`,`nickname`,`sex`) value("Kangkang","隔壁村的富贵","male"),("CH","唐伯虎点翠花","female")'
            ]
            for value in cmd:
                self.cur.execute(value)
                self.conn.commit()
        except Exception as e:
            raise e
        self.cur.close()
        self.close()

    def query_from_table(self):
        cmd = [
            'select * from `user` where `sex`="female"',
            'select * from `user` where `sex`="male" Order BY "id" desc limit 4,2'
            ]
        try:
            for value in cmd:
                self.cur.execute(value)
                results = self.cur.fetchall()
                for row in results:
                    print row
        except Exception as e:
            raise e

    def update_table_info(self):
        cmd = 'update `user` set `sex`="female" where `id`<5'
        self.cur.execute(cmd)
        self.conn.commit()

    def delete_table_info(self):
        cmd = 'delete from `user` where `name`="zhou"'
        self.cur.execute(cmd)
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    sql = MysqlOperate()
    sql.delete_table_info()


