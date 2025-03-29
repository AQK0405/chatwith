
const menu = document.getElementById("menu");
const userlist = document.getElementById("userList");
const addFriend_top = document.getElementById("addFriend");
(function(){
    addFriend_top.style.display = 'none';
    menu.style.right = '-20vw';
    userlist.style.right = '-25vw';
})()

// 如果本地存储存在userinfo则渲染页面
let userinfo = JSON.parse(localStorage.getItem('userinfo'));
if (userinfo){
    const login = document.getElementsByClassName('login')[0];
    const register = document.getElementsByClassName('register')[0];
    const user_username = document.getElementsByClassName('username')[0];
    const user_id = document.getElementsByClassName('id')[0];
    const chatbox_username = document.querySelector('#chatbox .myself');


    user_username.innerHTML = userinfo.username;
    user_id.innerHTML = `ID: ${userinfo.id}`;
    login.style.display = 'none';
    register.style.display = 'none';
}

// 点击头像
const user = document.getElementById("user");
user.onclick = () => {
    if(menu.style.right == '-20vw'){
        menu.style.right = '0';
    }else{
        menu.style.right = '-20vw';
    }
}


// 渲染聊天记录
async function renderChatHistory(){
    text = ''
    chatHistory = await getChatHistory();
    for (i = 0; i < chatHistory.length; i++) {
        if(chatHistory[i].send_id == userinfo.id){
            text += 
            `
                <div class="right">
                    <img class="avatar" src="../image/avatar.png" width="50px" height="50px" style="margin: 10px;" alt="avatar" title="${chatHistory[i].send_id}">
                    <div>
                        <h4 class="right myself">${userinfo.username}</h4>
                        <p class="right message">${chatHistory[i].content}</p>
                        <p class="right" id="sendTime" style="color: gray; font-size: 0.5em;">${chatHistory[i].send_time}</p>
                    </div>
                </div>
            `
        }else{
            text += 
            `
                <div class="left">
                    <img class="avatar" src="../image/avatar.png" width="50px" height="50px" style="margin: 10px;" alt="avatar" title="${chatHistory[i].send_id}">
                    <div>
                        <h4 class="left yourself">${chatHistory[i].friend_username}</h4>
                        <p class="left message">${chatHistory[i].content}</p>
                        <p class="left" id="sendTime" style="color: gray; font-size: 0.5em;">${chatHistory[i].send_time}</p>
                    </div>
                </div>
            `
        }
    }
    chatbox_window.innerHTML = text;
    chatbox_window.scrollTop = chatbox_window.scrollHeight;
}
// 渲染userlist数据
async function renderUserList(){
    let text = ''
    let friendlist = await getFriendList();
    for(i = 0; i < friendlist.length; i++){
        if(friendlist[i].accept == '1'){
            text +=
             `
                <div id="userListLine">
                    <img class="avatar" src="../image/avatar.png" width="50px" height="50px" title="${friendlist[i].friend_id}" alt="avatar">
                    <div>
                        <h4 class="username">${friendlist[i].friend_username}</h4>
                        <p class="status">在线</p>
                    </div>
                </div>
            `
        }
    }
    userlist.innerHTML = text;
    userlist.onclick = async (e)=>{
        let line = e.srcElement;
        let friend_id = line.children[0].getAttribute('title');
        localStorage.setItem('curtFriendId', friend_id);
        renderChatHistory();
    }
}


// 发送消息
const send_btn = document.querySelector('#typebox .button');
const send_input = document.querySelector('#typebox .input');
send_btn.onclick = async () => {
    res = await sendMsg(send_input.value, localStorage.getItem('curtFriendId'));
    if (res.code == 200){
        send_input.value = '';
    }else{
        console.log(res.msg);
        alert(res.msg);
    }
    renderChatHistory();
}
send_input.onkeydown = async (e) => {
    if (e.keyCode == 13){
        res = await sendMsg(send_input.value, localStorage.getItem('curtFriendId'));
        if (res.code == 200){
            send_input.value = '';
        }else{
            console.log(res.msg);
            alert(res.msg);
        }
        renderChatHistory();
    }
}
const renderChatHistoryInterval = setInterval(() => {
    if (localStorage.getItem('curtFriendId')){
        renderChatHistory();
    }else{
        clearInterval(renderChatHistoryInterval);
    }
    }, 3000);

// 收回userlist
const toggle = document.getElementById("toggle");
toggle.onclick = () => {
    renderUserList();
    
    if(userlist.style.right == '-25vw'){
        userlist.style.right = '0';
        userlist.style.boxShadow = '0 0 20px rgba(0, 0, 0, .5)';
        toggle.innerHTML = '&nbsp;&nbsp;&nbsp;〉'
        toggle.style.right = '25vw';
    }else{
        userlist.style.right = '-25vw';
        toggle.innerHTML = '〈&nbsp;&nbsp;&nbsp;'
        userlist.style.boxShadow = 0;
        toggle.style.right = '0';
    }
}


// 退出登录
const logout = document.getElementsByClassName('logout')[0];
logout.onclick = ()=>{
    if (userinfo){
        localStorage.removeItem('userinfo');
    }else{
        alert('未登录');
    }
}
// 点击首页
const chatbox_window = document.querySelector('#chatbox .window');
const index = document.getElementById("index");
const chatbox_title = document.querySelector('#chatbox .title');
index.onclick = (e)=>{
    e.preventDefault();
    addFriend_top.style.display = 'none';
    chatbox_window.innerHTML = '';
    chatbox_title.innerHTML = '<h3 style="margin-left: 10px;">> 首页</h3>';
    typebox.style.transform = 'translateY(0)';
    chatbox_window.style.height = '50vh'
}



// 点击联系人
const myfriend = document.getElementById("myfriend");
const typebox = document.getElementById("typebox");
// 渲染好友申请列表
async function renderFriendApply(){
    let text = '';
    let friendlist = await getFriendList();
    for(i = 0; i < friendlist.length; i++){
        if(friendlist[i].accept == '0'){
            if (friendlist[i].apply_id == userinfo.id){
                text += 
            `
                <div id="myFriendApply">
                    <img class="avatar" src="../image/avatar.png" width="80px" height="80px" alt="avatar">
                    <div class="info">
                        <h4 class="username">${friendlist[i].friend_username}</h4>
                        <p class="id">ID: ${friendlist[i].friend_id}</p>
                        <p class="applytime">申请时间: ${friendlist[i].apply_time}</p>
                    </div>
                    <div class="nobutton">待同意···</div>
                </div>
            `
            }else{
                text += 
                `
                    <div id="myFriendApply">
                        <img class="avatar" src="../image/avatar.png" width="80px" height="80px" alt="avatar">
                        <div class="info">
                            <h4 class="username">${friendlist[i].friend_username}</h4>
                            <p class="id">ID: ${friendlist[i].friend_id}</p>
                            <p class="applytime">申请时间: ${friendlist[i].apply_time}</p>
                        </div>
                        <div class="button">同意</div>
                    </div>
                `
            }
        }
    }
    chatbox_window.innerHTML = text;
    const btn = document.querySelectorAll('#myFriendApply .button');
    for(i = 0; i < btn.length; i++){
        chatbox_window.onclick = async (e)=>{
            click_btn = e.srcElement
            friend_id = click_btn.previousElementSibling.children[1].innerHTML.split(':')[1].trim();
            res = await http({
                url: localStorage.getItem('serverAddress') + '/api/acceptApply', 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: {
                    apply_id: friend_id,
                    receive_id: userinfo.id,
                    accept: '1'
                }
            })
            alert(res.msg);
            renderFriendApply();
        }
    }
}


myfriend.onclick = (e)=>{
    e.preventDefault();
    // 关闭聊天记录轮询
    // clearInterval(renderChatHistoryInterval);
    // 删除curtFriendId
    localStorage.removeItem('curtFriendId');
    chatbox_title.innerHTML = '<h3 style="margin-left: 10px;">> 联系人</h3>';
    typebox.style.transform = 'translateY(100%)';
    chatbox_window.style.height = '70vh';
    addFriend_top.style.display = 'flex';
    addFriend_top.style.backgroundColor = '#b4c2dc';
    addFriend_top.innerHTML = 
    `
        <input class="input" type="text" placeholder="请输入ID：">
        <div class="button" onclick="addFriend()">添加</div>
    `
    renderFriendApply();
}

// 添加朋友
async function addFriend(){
    const input = document.querySelector('#addFriend .input');
    if (input.value.trim() == ''){
        alert('请输入ID');
        return 0;
    }
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/friendApply', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            id: userinfo.id,
            friend_id: input.value
        }
    })
    alert(res.msg);
    renderFriendApply();
    if(res.code == 200)
        await sendMsg(`我是${userinfo.username}`, input.value);
}

(function(){
    if(userinfo.id == 'admin'){
        const sidebar = document.getElementById('sidebar');
        let background = document.createElement('a');
        background.innerHTML = '<div id="background">后台</div>';
        sidebar.appendChild(background);


        background.onclick = async () => {
            key = prompt('请输入密钥：');
            if (key == null){
                return 0;
            }
            localStorage.setItem('key', key);
            res = await http({
                url: localStorage.getItem('serverAddress') + '/api/getBackgroundPermission', 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: {
                    id: userinfo.id,
                    key: key
                }
            })
            if(res.code == 200){
                window.location.href = '../html/backManager.html';
            }else{
                alert(res.msg);
            }
        }
    }
})();



const setting = document.getElementById('setting');
console.log(setting);

setting.onclick = (e)=>{
    let text = '';
    e.preventDefault();
    // 关闭聊天记录轮询
    // clearInterval(renderChatHistoryInterval);
    // 删除curtFriendId
    localStorage.removeItem('curtFriendId');
    addFriend_top.style.display = 'none';
    chatbox_title.innerHTML = '<h3 style="margin-left: 10px;">> 设置</h3>';
    typebox.style.transform = 'translateY(100%)';
    chatbox_window.style.height = '70vh';

    const window = document.querySelector('#chatbox .window');
    text += 
    `
        <div id="setting">
            <div class="setting-item">
                <h4>avatar</h4> <input type="file" placeholder="avatar">
            </div>
            <div class="setting-item">
                <h4>username</h4> <input class="input" type="text" placeholder="username">
            </div>
            <div class="setting-item">
                <h4>password</h4> <input class="input" type="password" placeholder="password">
            </div>
            <div class="save">保存</div>
        </div>
    `
    window.innerHTML = text;
}