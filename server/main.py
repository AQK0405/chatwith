import socket
import time

from request.httpRequestBody import HttpRequestBody
from request.route import *

try:
    with open('server.init', mode='r', encoding='utf-8') as init:
        init = json.loads(init.read())
        serverAdress = init['server_address']
        serverPort = init['server_port']
except Exception:
    print('-->配置文件读取失败！')
    exit(0)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('0.0.0.0', serverPort))
socket.listen()
print(f'--> 服务器已在 {serverAdress}:{serverPort}/ 开启')
while True:
    conn, addr = socket.accept()
    request = conn.recv(1024)
    requestBody = HttpRequestBody(request.decode())
    currentTime = time.strftime('%Y-%m-%d_%H:%M:%S')
    print(f'[{currentTime}]', requestBody.method, requestBody.path, requestBody.body)

    # 处理GET请求
    if requestBody.method == 'GET':
        if requestBody.path == '/':
            response_headers = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: text/html\r\n\r\n"
            conn.sendall(response_headers.encode())
            with open('html/index.html', mode='rb') as html:
                conn.sendall(html.read())
            conn.close()

    # 处理POST请求
    elif requestBody.method == 'POST':
        response_headers = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: application/json\r\n\r\n"
        conn.sendall(response_headers.encode())
        # 查询用户的api
        if requestBody.path == '/api/userQuery':
            resp = userQuery(requestBody.body['id'], requestBody.body['password'])
            conn.sendall(resp.encode())
        # 获取所有用户的api
        elif requestBody.path == '/api/getAllUser':
            resp = getAllUser(requestBody.body['key'])
            conn.sendall(resp.encode())
        # 添加用户的api
        elif requestBody.path == '/api/userAdd':
            resp = userAdd(requestBody.body['username'], requestBody.body['password'])
            conn.sendall(resp.encode())
        # 添加好友的api
        elif requestBody.path == '/api/friendApply':
            resp = friendApply(requestBody.body['id'], requestBody.body['friend_id'])
            conn.sendall(resp.encode())
        # 获取好友列表的api
        elif requestBody.path == '/api/getFriendList':
            resp = getFriendList(requestBody.body['id'])
            conn.sendall(resp.encode())
        # 同意好友申请的api
        elif requestBody.path == '/api/acceptApply':
            resp = acceptApply(requestBody.body['apply_id'], requestBody.body['receive_id'], requestBody.body['accept'])
            conn.sendall(resp.encode())
        # 获取聊天记录的api
        elif requestBody.path == '/api/chatHistory':
            resp = chatHistory(requestBody.body['id'], requestBody.body['friend_id'])
            conn.sendall(resp.encode())
        # 发送消息的api
        elif requestBody.path == '/api/sendMsg':
            resp = sendMsg(requestBody.body['id'], requestBody.body['friend_id'], requestBody.body['content'])
            conn.sendall(resp.encode())
        # 获取后台权限的api
        elif requestBody.path == '/api/getBackgroundPermission':
            resp = getBackgroundPermission(requestBody.body['id'], requestBody.body['key'])
            conn.sendall(resp.encode())
        # 更改用户信息的api
        elif requestBody.path == '/api/userChange':
            resp = userChange(requestBody.body['id'], requestBody.body['username'], requestBody.body['password'], requestBody.body['key'])
            conn.sendall(resp.encode())
        # 删除用户的api
        elif requestBody.path == '/api/deleteUser':
            resp = userDelete(requestBody.body['id'], requestBody.body['key'])
            conn.sendall(resp.encode())
        elif requestBody.path == '/api/queryRelativeUser':
            resp = queryRelativeUser(requestBody.body['key_word'])
            conn.sendall(resp.encode())

    # 处理跨域预检
    elif requestBody.method == 'OPTIONS':
        response = [
            'HTTP/1.1 204 No Content',
            'Access-Control-Allow-Origin: *',
            'Access-Control-Allow-Methods: POST, GET, OPTIONS',
            'Access-Control-Allow-Headers: Content-Type',
            'Access-Control-Max-Age: 86400',
            ''
        ]
        conn.sendall('\r\n'.join(response).encode())
    conn.close()

socket.close()
