// 获取好友申请列表
async function getFriendList(){
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/getFriendList', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            id: userinfo.id
        }
    })
    return res.user_list;
}

// 获取聊天记录
async function getChatHistory(){
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/chatHistory', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            id: userinfo.id,
            friend_id:localStorage.getItem('curtFriendId')
        }
    })
    return res.history;
}

// 发送消息
async function sendMsg(msg, friend_id){

    if(msg.trim() == ''){
        alert('请输入内容');
        return 0;
    }
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/sendMsg', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            id: userinfo.id,
            friend_id: friend_id,
            content: msg
        }
    })
    return res;
}

// 获取所有用户
async function getAllUser(){
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/getAllUser', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            key: localStorage.getItem('key')
        }
    })
    return res.userList;
}

// 模糊查询
async function getRelativeUser(key_word){
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/queryRelativeUser', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            key_word: key_word
        }
    })
    return res.userList;
}