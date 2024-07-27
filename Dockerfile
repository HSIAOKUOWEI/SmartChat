# 使用官方的 Python 运行环境作为基础镜像
FROM python:3.10-slim

# 设置容器内的工作目录
WORKDIR /app

# 复制当前目录内容到容器的 /app 目录
COPY . /app

# 安装 requirements.txt 中指定的依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露容器的 5000 端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 当容器启动时运行 app.py
CMD ["flask", "run", "--host=0.0.0.0"]
