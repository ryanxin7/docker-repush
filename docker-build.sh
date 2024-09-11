#!/bin/bash

# 获取当前日期，格式为 YYYYMMDD
DATE=$(date +"%Y%m%d")

# 设置镜像名称，带日期后缀
IMAGE_NAME="repush:$DATE"

# 输出构建信息
echo "Building Docker image: $IMAGE_NAME"

# 构建 Docker 镜像
docker build -t "$IMAGE_NAME" .

# 输出完成信息
echo "Docker image $IMAGE_NAME built successfully"
