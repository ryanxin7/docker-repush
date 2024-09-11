# 使用官方的 Python 镜像作为基础镜像
FROM registry.cn-beijing.aliyuncs.com/xxk8s/python:3.8-slim

# 设置工作目录
WORKDIR /app

# 复制项目的依赖文件 requirements.txt 到镜像中
COPY requirements.txt .

# 使用国内的镜像源安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt \
    --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目的所有文件到工作目录中
COPY . .

# 设置环境变量，防止 Python 缓存文件
ENV PYTHONUNBUFFERED=1

# 暴露应用运行的端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python", "app.py"]