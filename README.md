<div align="center">
    <h1>WebCat --- 一个网页聊天工具</h1>
    <a href="https://github.com/xhdndmm/webcat/stargazers"><img src="https://img.shields.io/github/stars/xhdndmm/webcat" alt="Stars"></a>
    <a href="https://github.com/xhdndmm/webcat/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
    <a href="https://www.python.org/download"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Version"></a>
    <a href="https://github.com/xhdndmm/webcat/releases"><img src="https://img.shields.io/github/downloads/xhdndmm/webcat/total" alt="Downloads"></a>
    <br>
    <img src="https://skillicons.dev/icons?i=py,flask,sqlite,html,js,css" loading="lazy"/>
    <br>
    <img src="./doc/img/屏幕截图_20260213_164404.jpg" width="600"><img>
</div>

## 项目结构
```
.
├── doc
│   └── img
│       └── 屏幕截图_20260213_164404.jpg
├── LICENSE
├── README.md
├── requirements.txt
├── src
│   ├── app.py
│   ├── static
│   │   ├── css
│   │   │   ├── index.css
│   │   │   └── register.css
│   │   └── js
│   │       ├── index.js
│   │       └── register.js
│   └── templates
│       ├── index.html
│       └── register.html
└── TODO.txt

8 directories, 12 files
```

## 使用说明
### 1.先决条件
首先你需要准备好[python3](https://www.python.org/downloads/)环境，然后下载[源代码](https://github.com/xhdndmm/webcat/releases)并解压。
- 建议使用linux系统运行。
### 2.准备运行环境
#### 2.1创建python虚拟环境
```shell
cd /path/to/webcat
python -m venv .venv
```
#### 2.2 安装依赖包
```shell
.venv/bin/pip install -r requirements.txt
```
### 3.运行程序
```shell
cd src/
.venv/bin/python app.py
```
运行后会生成默认配置。
```json
{
  "log_path": "wc_log.log",
  "db_path": "wc_db.db",
  "secret_key": "123"
}
```
其中
- `log_path`是日志路径
- `db_path`是数据库路径
- `secret_key`是socket安全密钥

请按需修改配置文件，修改后即可正常运行。

## 技术说明
目前采用python+flask的后端，使用sqlite数据库存储用户信息，并将聊天记录存储在一个json文件中。前后端使用websocket保持连接来确保信息按时收发。

## 问题反馈
如果在使用中遇到问题，请在[Issues](https://github.com/xhdndmm/webcat/issues)页面反馈。

## 贡献
我们非常欢迎你来贡献代码等，但是请遵守以下几点：
- 1.请将pr提交到dev分支。
- 2.不要提交没有意义的代码及相关内容。
- 3.不要提交未经测试的代码。

## 协议
本程序使用[MIT](./LICENSE)许可证。