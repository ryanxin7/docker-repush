## docker-repush 自动推送


### 步骤 1: 安装必要的依赖
在运行应用之前，确保已经安装了项目所需的依赖项，如 Flask、Flask-SocketIO、Docker SDK 等。
如果你还没有 requirements.txt 文件，你可以手动安装所需的 Python 包。你可以使用以下命令安装：

```bash
pip install flask flask-socketio docker eventlet
```


或者你可以创建一个 `requirements.txt` 文件，列出所有依赖项：

```bash
pip install flask flask-socketio docker eventlet
```

然后使用以下命令安装依赖：
```bash
pip install -r requirements.txt
```


### 步骤 2: 运行 Flask 应用
安装了必要的依赖后，你可以运行 Flask 应用。确保你的应用代码在一个文件中（例如 app.py），并且 Docker 客户端已经配置为连接远程 Docker 守护进程 (192.168.18.10:2375)。
执行以下命令启动 Flask 应用：

```bash
python app.py
```

Flask-SocketIO 应该会启动在 http://0.0.0.0:5000 上，允许外部访问。