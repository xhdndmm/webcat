#[https://github.com/xhdndmm/webcat]

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from pathlib import Path
import base64
import sqlite3
import logging
import time
import os
import json
import sys

# 配置部分
CONFIG_PATH = Path("wc_cfg.json")
DEFAULT_CONFIG = {
    "log_path": "wc_log.log",
    "db_path": "wc_db.db",
    "secret_key": "123"
}

if not CONFIG_PATH.exists():
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    print(f"已生成默认配置文件 {CONFIG_PATH}，请填写后重试。")
    sys.exit(0)

cfg = json.load(open(CONFIG_PATH, "r", encoding="utf-8"))
#==========

app = Flask(__name__)
app.secret_key = cfg["secret_key"]
socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(filename=cfg["log_path"], level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化数据库
def init_db():
    with sqlite3.connect(cfg["db_path"]) as conn:
        c = conn.cursor()
        #用户信息表
        c.execute('''CREATE TABLE IF NOT EXISTS USERINFO
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT UNIQUE NOT NULL,
                            PWD TEXT NOT NULL)''')
        #聊天记录表
        c.execute('''CREATE TABLE IF NOT EXISTS MSGDATA
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT UNIQUE NOT NULL,
                            MSG TEXT NOT NULL,
                            TIME TEXT NOT NULL)''')            
        conn.commit()

if not os.path.exists(cfg["db_path"]):
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 兼容 Form 提交和 JSON 提交
        data = request.get_json() if request.is_json else request.form
        name = data.get('username')
        pwd = data.get('password')

        # Base64 编码
        encoded_str = base64.b64encode(str(pwd).encode('utf-8')).decode('utf-8')

        try:
            with sqlite3.connect(cfg["db_path"]) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO USERINFO (NAME, PWD) VALUES (?,?)", (name, encoded_str))
                conn.commit()
            return jsonify({"status": "success", "message": "注册成功"})
        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "用户名已存在"}), 400
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "未接收到数据"}), 400
        
    username = data.get('username')
    password = data.get('password')

    # 将输入的密码进行同样的编码用于比对
    encoded_input = base64.b64encode(str(password).encode('utf-8')).decode('utf-8')

    with sqlite3.connect(cfg["db_path"]) as conn:
        c = conn.cursor()
        c.execute("SELECT ID, NAME, PWD FROM USERINFO WHERE NAME = ?", (username,))
        user = c.fetchone()

        # 修正比对逻辑
        if user and user[2] == encoded_input:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return jsonify({"status": "success", "user_name": user[1]})
        else:
            return jsonify({"status": "error", "message": "用户名或密码错误"}), 401

@app.route('/check_auth')
def check_auth():
    if 'user_name' in session:
        return jsonify({"is_logged_in": True, "user_name": session['user_name']})
    return jsonify({"is_logged_in": False})

@app.route('/logout')
def logout():
    session.clear()
    return jsonify({"status": "success", "message": "已退出登录"})

# 确保用户在没有登录的状态下不会连接socket
@socketio.on('connect')
def handle_connect():
    if 'user_name' not in session:
        return False

# 消息收发
@socketio.on('send_msg')
def handle_message(data):
    user = session.get('user_name', '游客')
    msg_content = data.get('msg', '')
    msg_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    # 写入数据库
    with sqlite3.connect(cfg["db_path"]) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO MSGDATA (NAME, MSG, TIME) VALUES (?,?,?)", (user,msg_content,msg_time))
        conn.commit()

    # 构造消息对象
    chat_data = {
        'user': user,
        'msg': msg_content,
        'time': msg_time,
    }
    
    # 广播给所有人
    emit('receive_msg', chat_data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=False, port=5000)