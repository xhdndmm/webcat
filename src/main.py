#[https://github.com/xhdndmm/webcat]

from flask import Flask, render_template, request, jsonify, session
import json
import base64
import sqlite3
import logging

#==========配置区==========
DB_PATH = "webcat.db"
DATA_PATH = "webcat.json"
LOG_PATH = "webcat.log"
LOG_LEVEL = "logging.INFO"
#====================

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_PATH, level=LOG_LEVEL)

#初始化数据库
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        logger.info("数据库打开成功")
    except Exception as e:
        logger.error("数据库无法打开",e)
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS USERINFO
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT UNIQUE NOT NULL,
                            PWD TEXT NOT NULL)''')
        logger.info("数据库创建成功")
    except Exception as e:
        logger.error("数据库创建失败",e)
    conn.commit()
    conn.close()

#Flask路由
#主页
@app.route('/')
def index():
    return render_template('index.html')

# 注册
@app.route('/register', methods=['GET,POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        pwd = request.form['password']

        #base64加密密码
        original_str = str(pwd)
        bytes_data = original_str.encode('utf-8')
        encoded_bytes = base64.b64encode(bytes_data)
        encoded_str = encoded_bytes.decode('utf-8')

        try:
            with sqlite3.connect(DB_PATH) as conn:
                c = conn.cursor()
                c.execute("INSERT INTO USERINFO (NAME, PWD) VALUES (?,?)", (name, encoded_str))
                conn.commit()
            return "注册成功！<a href='/'>去登录</a>"
        except sqlite3.IntegrityError:
            return "用户名已存在！"
    return render_template('register.html')

#登陆
@app.route('/login', methods=['POST'])
def login():
    # 获取 JS 发送的 JSON 数据
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "未接收到数据"}), 400
        
    username = data.get('username')
    password = data.get('password')

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM USERINFO WHERE NAME = ?", (username,))
        user = c.fetchone()

        decoded_bytes = base64.b64decode(password)
        decoded_str = decoded_bytes.decode('utf-8')

        if user and decoded_str(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return jsonify({
                "status": "success", 
                "message": "登录成功",
                "user_name": user[1]
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "用户名或密码错误"
            }), 401

#登陆状态监测
@app.route('/check_auth')
def check_auth():
    if 'user_name' in session:
        return jsonify({"is_logged_in": True, "user_name": session['user_name']})
    return jsonify({"is_logged_in": False})