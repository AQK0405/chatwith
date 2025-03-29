localStorage.setItem('serverAddress', 'http://127.0.0.1:8080')

async function http(obj){
    let result;
    if(obj.method == 'GET'){
        result = await fetch(obj.url).then(res => res);
    }else if(obj.method == 'POST'){
        result = await fetch(obj.url, {
            method: obj.method,
            headers: obj.headers,
            body: JSON.stringify(obj.body)
        }).then(res => res.json())
    }
    return result;
}

// obj参数说明
// obj = {
//     url: 'http://localhost:8080/api/userQuery',
//     method: 'GET'
// }
// obj = {
//     url: 'http://localhost:8080/api/userQuery',
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json'
//     },
//     body: {
//         'id': '00001'
//     }
// }

// const obj = {
//     url: 'http://localhost:8080/api/userQuery',
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json'
//     },
//     body: {
//         'id': '00001'
//     }
// }

// let res = await http(obj);
// console.log(res);