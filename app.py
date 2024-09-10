from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import docker
import eventlet

# 初始化 Flask 和 Flask-SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# 创建 Docker 客户端，连接远程 Docker 守护进程
docker_client = docker.DockerClient(base_url='tcp://192.168.18.10:2375')

# 添加认证信息 (如有需要)
auth_config = {
    'username': 'username',  # 替换为你的用户名
    'password': 'password'   # 替换为你的密码
}

@app.route('/')
def index():
    return render_template('index.html')  # 渲染前端页面

@socketio.on('clearLog')
def handle_clear_log():
    """
    清除日志的处理逻辑
    """
    # 向前端发送清除日志的信号
    socketio.emit('logCleared')

@socketio.on('startPush')
def handle_push(data):
    source_image = data['sourceImage']
    private_repo_url = data['privateRepoUrl']  # 例如 registry.cn-beijing.aliyuncs.com/xxk8s
    project_name = data['projectName']  # 项目名，例如 alpine
    version = data['version']  # 镜像版本，例如 3.20.3

    # 生成目标镜像名称（确保路径正确）
    target_image = f"{private_repo_url}/{project_name}:{version}"

    try:
        # 打印拉取镜像的日志，使用 low-level API 捕获详细日志
        socketio.emit('log', f"Pulling image {source_image}")
        pull_log_stream = docker_client.api.pull(source_image, stream=True, decode=True)

        # 逐行输出拉取镜像的日志
        for log_line in pull_log_stream:
            socketio.emit('log', f"Pull log: {log_line}")
            if 'status' in log_line:
                socketio.emit('log', f"Pull status: {log_line['status']}")
            if 'progress' in log_line:
                socketio.emit('log', f"Progress: {log_line.get('progress', '')}")
            if 'error' in log_line:
                socketio.emit('log', f"Error: {log_line['error']}")

        # 打印标记镜像的日志
        socketio.emit('log', f"Tagging image {source_image} as {target_image}")
        image = docker_client.images.get(source_image)
        image.tag(target_image)

        # 使用高级别 API 推送镜像
        socketio.emit('log', f"Pushing image {target_image} using high-level API")

        # 推送镜像，使用 auth_config 来确保认证信息
        push_log_stream = docker_client.images.push(
            target_image, 
            stream=True, 
            decode=True, 
            auth_config=auth_config  # 使用认证信息
        )

        # 逐行输出推送日志
        for log_line in push_log_stream:
            socketio.emit('log', f"Push log: {log_line}")
            if 'status' in log_line:
                socketio.emit('log', f"Push status: {log_line['status']}")
            if 'progress' in log_line:
                socketio.emit('log', f"Progress: {log_line.get('progress', '')}")
            if 'error' in log_line:
                socketio.emit('log', f"Error: {log_line['error']}")

        # 完成操作
        socketio.emit('log', "All operations completed successfully using high-level API")
    except docker.errors.APIError as e:
        socketio.emit('log', f"Error: {str(e)}")
    except Exception as e:
        socketio.emit('log', f"Unexpected Error: {str(e)}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
