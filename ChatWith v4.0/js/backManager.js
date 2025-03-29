const userList = document.getElementById("userlist");
async function renderUserList() {
    text = 
    `
        <tr class="title">
            <th>ID</th>
            <th>用户名</th>
            <th>密码</th>
            <th>操作</th>
        </tr>
    `
    res = await getAllUser();
    for(i = 0; i < res.length; i++){
        text += 
        `
            <tr>
                <td>${res[i].id}</td>
                <td><input type="text" value="${res[i].username}"></td>
                <td><input type="text" value="${res[i].password}"></td>
                <td>
                    <button id="change">修改</button>
                    <button id="delete">删除</button>
                </td>
            </tr>
        `
    }
    userList.innerHTML = text;
}
renderUserList();

async function changeUser(id, username, password){
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/userChange', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            id: id,
            username: username,
            password: password,
            key: localStorage.getItem('key')
        }
    })
    return res;
}

async function deleteUser(id){
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/deleteUser', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            id: id,
            key: localStorage.getItem('key')
        }
    })
    return res;
}

userList.onclick = async (e)=>{
    click_btn = e.srcElement
    let res;
    if(click_btn.id == 'change'){
        id = click_btn.parentElement.parentElement.children[0].innerHTML;
        username = click_btn.parentElement.previousElementSibling.previousElementSibling.children[0].value;
        password = click_btn.parentElement.previousElementSibling.children[0].value;
        res = await changeUser(id, username, password);
    }
    if(click_btn.id == 'delete'){
        id = click_btn.parentElement.parentElement.children[0].innerHTML;
        res = await deleteUser(id);
    }
    alert(res.msg);
    renderUserList();
}

const search_btn = document.querySelector("#searchbox .search-btn");
const search = document.querySelector("#searchbox .search");
search_btn.onclick = async ()=>{
    res = await getRelativeUser(search.value);
    text = 
    `
        <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>密码</th>
            <th>操作</th>
        </tr>
    `
    for(i = 0; i < res.length; i++){
        text += 
        `
            <tr>
                <td>${res[i].id}</td>
                <td><input type="text" value="${res[i].username}"></td>
                <td><input type="text" value="${res[i].password}"></td>
                <td>
                    <button id="change">修改</button>
                    <button id="delete">删除</button>
                </td>
            </tr>
        `
    }
    userList.innerHTML = text;
    
    
}
search.onkeydown = (e)=>{
    if(e.keyCode == 13){
        search_btn.click();
    }
}