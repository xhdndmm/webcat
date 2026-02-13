/*[https://github.com/xhdndmm/webcat]*/
let socket;
let currentUser = ""; // 用于存储当前登录的用户名

document.addEventListener('DOMContentLoaded', () => {
    checkAuth(); // 页面加载先查状态
});

// 检查登录状态
async function checkAuth() {
    const res = await fetch('/check_auth');
    const data = await res.json();
    
    if (data.is_logged_in) {
        currentUser = data.user_name; // 存下用户名
        initChat(data.user_name);
        setupLogout(); // 初始化退出按钮
    } else {
        document.getElementById('login_modal').style.display = 'flex';
    }
}

// 设置退出登录按钮逻辑
function setupLogout() {
    const logoutBtn = document.getElementById('logout_btn');
    if (logoutBtn) {
        logoutBtn.style.display = 'inline-block'; // 显示按钮
        logoutBtn.onclick = async () => {
            const res = await fetch('/logout');
            const data = await res.json();
            if (data.status === 'success') {
                location.reload(); // 退出后刷新，重新走 checkAuth 逻辑弹出登录框
            }
        };
    }
}

// 登录处理
async function handleLogin() {
    const username = document.getElementById('login_user').value;
    const password = document.getElementById('login_pwd').value;

    const res = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (data.status === 'success') {
        location.reload(); 
    } else {
        alert(data.message);
    }
}

// 初始化聊天 (WebSocket)
function initChat(username) {
    document.getElementById('user_status').innerText = `你好, ${username}`;
    document.getElementById('msg_input').disabled = false;
    document.getElementById('send_btn').disabled = false;
    
    // 连接服务器
    socket = io();

    // 监听消息接收
    socket.on('receive_msg', (data) => {
        appendMessage(data);
    });

    // 发送按钮点击
    document.getElementById('send_btn').onclick = sendMsg;
    // 回车键发送
    document.getElementById('msg_input').onkeypress = (e) => {
        if(e.key === 'Enter') sendMsg();
    };
}

function sendMsg() {
    const input = document.getElementById('msg_input');
    if (input.value.trim()) {
        socket.emit('send_msg', { msg: input.value });
        input.value = '';
    }
}

function appendMessage(data) {
    const list = document.getElementById('msg_list');
    const div = document.createElement('div');
    
    // 判断消息是否由当前用户发送
    const isMine = data.user === currentUser;
    
    // 如果是自己发的，添加 'mine' 类名
    div.className = `message ${isMine ? 'mine' : ''}`;
    
    div.innerHTML = `
        <div class="meta"><b>${data.user}</b> ${data.time || ''}</div>
        <div class="content">${data.msg}</div>
    `;
    list.appendChild(div);
    
    // 自动滚动到底部
    const chatWin = document.getElementById('chat_window');
    chatWin.scrollTop = chatWin.scrollHeight;
}