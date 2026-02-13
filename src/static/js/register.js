/*[https://github.com/xhdndmm/webcat]*/
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // 阻止表单默认提交行为

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const re_password = document.getElementById('re_password').value;

    // 1. 简单的客户端校验
    if (password !== re_password) {
        alert("两次输入的密码不一致！");
        return;
    }

    // 2. 构造表单数据
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
        // 3. 发送请求到后端 /register 路由
        const response = await fetch('/register', {
            method: 'POST',
            body: formData
        });

        const result = await response.json(); // 我们之前把后端改成了返回 JSON

        if (result.status === 'success') {
            alert("注册成功！点击确定返回登录。");
            window.location.href = '/'; // 跳转回主页
        } else {
            alert("注册失败：" + result.message);
        }
    } catch (error) {
        console.error("请求出错:", error);
        alert("服务器响应错误，请稍后再试");
    }
});