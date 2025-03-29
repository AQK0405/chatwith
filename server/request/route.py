import json
from request.mysql import MySql

with open('server.init', mode='r', encoding='utf-8') as init:
    init = json.loads(init.read())
    host = init['host']
    port = init['database_port']
    user = init['user']
    password = init['password']
    database = init['database']

mysql = MySql(host=host, port=port, user=user, password=password, database=database)


def getID():
    try:
        with open('server.init', mode='r', encoding='utf-8') as init:
            init = json.loads(init.read())
            startID = int(init['startID'])
            newId = startID + 1
            with open('server.init', mode='w', encoding='utf-8') as file:
                init['startID'] = newId
                file.write(json.dumps(init, indent=4))
            return startID
    except Exception as e:
        print('--> route读取初始ID错误' + str(e))


def getKey():
    try:
        with open('server.init', mode='r', encoding='utf-8') as init:
            init = json.loads(init.read())
            key = init['key']
        return key
    except Exception as e:
        print('--> route读取key错误' + str(e))
        return ''


def userQuery(id, password):
    try:
        data = mysql.userQuery(f"id = '{id}'")[0]
        if data[2] == password:
            user_info = {"id": id, "username": data[1], "register_time": f"{data[4]}"}
            msg = {"code": 200, "msg": "成功", "user_info": user_info}
        else:
            msg = {"code": 404, "msg": "密码错误"}
    except Exception as e:
        msg = {"code": 404, "msg": "账号不存在"}
        print('--> route查找用户异常' + str(e))
    return json.dumps(msg)


def userAdd(username, password):
    id = getID()
    try:
        data = mysql.userAdd([{"id": str(id), "username": username, "password": password}])
        if data:
            data = json.loads(userQuery(id, password))['user_info']
            user_info = {"id": data['id'], "username": data['username'], "register_time": f"{data['register_time']}"}
            msg = {"code": 200, "msg": "成功", "user_info": user_info}
        else:
            msg = {"code": 505, "msg": "注册失败"}
    except Exception as e:
        msg = {"code": 505, "msg": "注册失败"}
        print('--> route添加用户异常' + str(e))
    return json.dumps(msg)


def friendApply(id, friend_id):
    try:
        # 未添加accept = None, 0
        try:
            accept = str(mysql.getFriendApplyStatus(id, friend_id)[2])
        except TypeError:
            accept = "None"
        # 是否存在id为friend_id的用户
        status = mysql.userQuery(f"id = '{friend_id}'")
        # 判断friend_id是否为自己
        if id == friend_id:
            status = 0

        if status:
            # 如果重复申请好友则data = 0
            if accept == 1:
                msg = {"code": 404, "msg": "你们已经是好友了"}
            else:
                data = mysql.friendApply(id, friend_id)
                if data:
                    msg = {"code": 200, "msg": "已发送好友申请"}
                else:
                    msg = {"code": 404, "msg": "别加了"}
        else:
            msg = {"code": 404, "msg": "id不正确"}
    except Exception as e:
        msg = {"code": 505, "msg": "错误"}
        print('--> route申请添加好友异常' + str(e))
    return json.dumps(msg)


def getFriendList(id):
    try:
        user_list = []
        data = mysql.getFriendList(id)
        for friend in data:
            # 如果friend[0]等于id,说明friend[0]是自己id,friend[1]是朋友id
            if friend[0] == id:
                friend_id = friend[1]
            else:
                friend_id = friend[0]
            friend_username = mysql.userQuery(f"id = '{friend_id}'")[0][1]
            apply_id = friend[0]

            info = {"apply_id": f"{apply_id}", "friend_id": f"{friend_id}", "friend_username": f"{friend_username}",
                    "accept": f"{friend[2]}", "apply_time": f"{friend[3]}"}
            user_list.append(info)
        msg = {"code": 200, "msg": "成功", "user_list": user_list}
    except Exception as e:
        msg = {"code": 505, "msg": "错误"}
        print('--> route获取好友列表异常' + str(e))

    return json.dumps(msg)


def acceptApply(apply_id, receive_id, accept):
    try:
        data = mysql.acceptApply(apply_id, receive_id, accept)
        if data:
            msg = {"code": 200, "msg": "成功"}
        else:
            msg = {"code": 404, "msg": "重复"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route同意好友申请异常' + str(e))
    return json.dumps(msg)


def sendMsg(id, friend_id, content):
    try:
        data = mysql.sendMsg(id, friend_id, content)
        if data:
            msg = {"code": 200, "msg": "发送成功"}
        else:
            msg = {"code": 404, "msg": "发送失败"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route发送消息异常' + str(e))
    return json.dumps(msg)


def chatHistory(id, friend_id):
    try:
        history = []
        data = mysql.getChatHistory(id, friend_id)
        friend_username = mysql.userQuery(f'id = "{friend_id}"')[0][1]
        if data:
            for info in data:
                message = {"send_id": f"{info[0]}", "friend_id": f"{info[1]}", "friend_username": f"{friend_username}",
                           "content": f"{info[2]}", "send_time": f"{info[3]}"}
                history.append(message)
            msg = {"code": 200, "msg": "成功", "history": history}
        else:
            msg = {"code": 404, "msg": "未查询到数据"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route查找聊天记录异常' + str(e))
    return json.dumps(msg)


def getBackgroundPermission(id, key):
    try:
        KEY = getKey()
        permission_back = mysql.userQuery(f'id = "{id}"')[0][3]
        if (key == KEY and permission_back == '1'):
            msg = {"code": 200, "msg": "成功"}
        else:
            msg = {"code": 404, "msg": "密钥不正确"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route获取后台权限异常' + str(e))
    return json.dumps(msg)


def getAllUser(key):
    try:
        userList = []
        KEY = getKey()
        if key == KEY:
            data = mysql.userQuery('id LIKE "%" ORDER BY id ASC')
            for user in data:
                temp = {"id": f"{user[0]}", "username": f"{user[1]}", "password": f"{user[2]}",
                        "permission_back": f"{user[3]}", "register_time": f"{user[4]}"}
                userList.append(temp)
            msg = {"code": 200, "msg": "成功", "userList": userList}
        else:
            msg = {"code": 404, "msg": "密钥不正确"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route获取所有用户异常' + str(e))
    return json.dumps(msg)


def userChange(id, username, password, key):
    try:
        KEY = getKey()
        data = mysql.userChange(id, username, password)
        if key == KEY:
            if data:
                msg = {"code": 200, "msg": "成功"}
            else:
                msg = {"code": 404, "msg": "失败"}
        else:
            msg = {"code": 404, "msg": "密钥不正确"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route更改用户异常' + str(e))
    return json.dumps(msg)


def userDelete(id, key):
    try:
        KEY = getKey()
        with open('server.init', mode='r', encoding='utf-8') as init:
            init = json.loads(init.read())
        if id == init['ADMIN_ID']:
            msg = {"code": 404, "msg": "管理员账号不可删除"}
        else:
            data = mysql.userDelete(id)
            if key == KEY:
                if data:
                    msg = {"code": 200, "msg": "成功"}
                else:
                    msg = {"code": 404, "msg": "失败"}
            else:
                msg = {"code": 404, "msg": "密钥不正确"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route删除用户异常' + str(e))
    return json.dumps(msg)


def queryRelativeUser(key_word):
    try:
        userList = []
        data = mysql.userQuery(f'id LIKE "%{key_word}%" OR username LIKE "%{key_word}%" OR password LIKE "%{key_word}%" OR permission_back = "{key_word}" OR register_time LIKE "%{key_word}%" ')
        if data:
            for user in data:
                temp = {"id": f"{user[0]}", "username": f"{user[1]}", "password": f"{user[2]}","permission_back": f"{user[3]}", "register_time": f"{user[4]}"}
                userList.append(temp)
            msg = {"code": 200, "msg": "成功", "userList": userList}
        else:
            msg = {"code": 404, "msg": "未查询到数据"}
    except Exception as e:
        msg = {"code": 505, "msg": "服务器异常"}
        print('--> route查找相关用户异常' + str(e))
    return json.dumps(msg)
