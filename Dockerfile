# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 设置环境变量，防止 Python 写入 .pyc 文件到容器中
ENV PYTHONDONTWRITEBYTECODE 1
# 设置 Python 输出不缓冲，直接打印到终端
ENV PYTHONUNBUFFERED 1

# 安装系统依赖
# Poppler-utils 包含 pdftoppm，是 pdf2image 的一个依赖
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ghostscript \
    tk \
    poppler-utils \
    # 清理 apt 缓存
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖
# 首先复制 requirements.txt 并安装，以便利用 Docker 的层缓存
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制项目文件到工作目录
COPY app.py .
COPY pdf_parser.py .
# 如果有其他需要复制的文件或目录，也在这里添加

# 暴露端口，Flask 默认运行在 5000 端口
EXPOSE 5000

# 定义容器启动时运行的命令
# 使用 gunicorn 作为生产级 WSGI 服务器，而不是 Flask 的开发服务器
# 需要将 gunicorn 添加到 requirements.txt
# CMD ["python", "app.py"]
# 使用 Gunicorn 启动应用。
# 'app:app' 指的是 app.py 文件中的 app Flask 实例。
# '-w 4' 表示 4 个 worker 进程。根据服务器资源调整。
# '-b 0.0.0.0:5000' 表示绑定到所有网络接口的 5000 端口。
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "app:app"]
```
