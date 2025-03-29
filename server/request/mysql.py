import json

import pymysql


class MySql:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        try:
            self.connect = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password)
            self.cursor = self.connect.cursor()
            self.init()
        except Exception as e:
            print('--> mysql数据库异常！' + str(e))

    def init(self):
        # 初始化
        createDatabase = 'create database if not exists chatwith'
        self.cursor.execute(createDatabase)
        try:
            self.connect = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                           database=self.database)
            self.cursor = self.connect.cursor()
            # 创建用户表
            self.cursor.execute(
                'CREATE TABLE if not exists tb_user(id CHAR(10) primary key, username VARCHAR(10) NOT NULL, password VARCHAR(20) NOT NULL,permission_back ENUM("1","0") NOT NULL DEFAULT "0", register_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)')
            # 默认添加管理员账号
            self.__addAdmin()
            # 创建好友表
            self.cursor.execute(
                'CREATE TABLE if not exists friend (apply_id CHAR(10) NOT NULL,receive_id CHAR(10) NOT NULL, accept ENUM("1","0") NOT NULL DEFAULT "0", apply_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)')
            # 创建聊天记录表
            self.cursor.execute(
                'CREATE TABLE if not exists chat_history (send_id CHAR(10) NOT NULL, receive_id CHAR(10) NOT NULL, content TEXT DEFAULT NULL, send_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)')
            return 1
        except Exception as e:
            print('--> mysql数据库初始化失败！' + str(e))
            return 0

    def __addAdmin(self):
        try:
            with open('server.init', mode='r', encoding='utf-8') as init:
                init = json.loads(init.read())
                self.cursor.execute(
                    f"""insert into tb_user(id, username, password, permission_back) values("{init['ADMIN_ID']}", "{init['ADMIN_USERNAME']}", "{init['ADMIN_PASSWORD']}", "1")""")
            return self.cursor.rowcount
        except Exception as e:
            print('--> mysql添加管理员账号失败' + str(e))
            return 0

    # 用户表操作
    def userAdd(self, users):
        rowcount = 0
        try:
            for user in users:
                sentence = f"insert into tb_user(id, username, password) values('{user['id']}', '{user['username']}', '{user['password']}')"
                self.cursor.execute(sentence)
                rowcount = rowcount + self.cursor.rowcount
                return rowcount
        except Exception as e:
            print('--> mysql添加用户失败' + str(e))
            return 0

    def userDelete(self, id):
        sentence = f'DELETE FROM tb_user WHERE id = "{id}"'
        self.cursor.execute(sentence)
        return self.cursor.rowcount

    def userChange(self, id, username, password):
        sentence = f'UPDATE tb_user SET username = "{username}", password="{password}" WHERE id = "{id}"'
        self.cursor.execute(sentence)
        return self.cursor.rowcount

    def userQuery(self, where):
        sentence = f'select * from tb_user where {where}'
        self.cursor.execute(sentence)
        return self.cursor.fetchall()

    # 好友申请表操作
    def friendApply(self, id, friend_id):
        # 查找是否有重复申请
        sentence_extra = f'select * from friend where (apply_id = "{id}" and receive_id = "{friend_id}") or (apply_id = "{friend_id}" and receive_id = "{id}")'
        self.cursor.execute(sentence_extra)
        if self.cursor.fetchall():
            return 0
        else:
            sentence = f'insert into friend(apply_id, receive_id) values("{id}", "{friend_id}")'
            self.cursor.execute(sentence)
            return self.cursor.rowcount

    def deleteFriend(self):
        pass

    def acceptApply(self, apply_id, receive_id, accept):
        sentence = f'UPDATE friend SET accept = "{accept}" WHERE apply_id = "{apply_id}" AND receive_id = "{receive_id}"'
        self.cursor.execute(sentence)
        return self.cursor.rowcount

    def getFriendList(self, id):
        sentence = f'SELECT * FROM friend WHERE apply_id = "{id}" OR receive_id = "{id}"'
        self.cursor.execute(sentence)
        return self.cursor.fetchall()

    def getFriendApplyStatus(self, id, friend_id):
        sentence = f'SELECT * FROM friend WHERE (apply_id = "{id}" AND receive_id = "{friend_id}") OR (apply_id = "{friend_id}" AND receive_id = "{id}")'
        self.cursor.execute(sentence)
        return self.cursor.fetchone()

    # 聊天记录表操作
    def sendMsg(self, id, friend_id, content):
        sentence = f'INSERT INTO chat_history (send_id, receive_id, content) VALUES ("{id}", "{friend_id}", "{content}")'
        self.cursor.execute(sentence)
        return self.cursor.rowcount

    def getChatHistory(self, id, friend_id):
        sentence = f'SELECT * FROM chat_history WHERE (send_id = "{id}" AND receive_id = "{friend_id}") OR (send_id = "{friend_id}" AND receive_id = "{id}") ORDER BY send_time ASC'
        self.cursor.execute(sentence)
        return self.cursor.fetchall()
