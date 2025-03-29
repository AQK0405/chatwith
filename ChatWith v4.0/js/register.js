const windows = document.getElementById("window");
const button = document.getElementsByClassName("button")[0];
const username = document.getElementsByClassName("username")[0];
const password = document.getElementsByClassName("password")[0];


(function(){
    windows.style.transform = 'translateY(-80vh)'
})();

window.onload = () => {
    windows.style.transform = 'translateY(0)';
}
button.onclick = async () => {
    if(username.value.trim() == '' || password.value.trim() == ''){
        alert("请输入账号和密码");
        return 0;
    }
    res = await http({
        url: localStorage.getItem('serverAddress') + '/api/userAdd', 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {
            username: username.value,
            password: password.value
        }
    })
    

    if (res.code == 200){
        localStorage.setItem('userinfo', `${JSON.stringify(res.user_info)}`)
        alert(res.msg);
        window.history.go(-1);
    }else{
        alert(res.msg);
    }
}