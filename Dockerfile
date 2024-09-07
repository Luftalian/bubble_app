# Goのベースイメージ
FROM golang:1.23-alpine AS go-builder

# 作業ディレクトリを設定
WORKDIR /app

# Goモジュールの依存関係をコピー
COPY go.mod go.sum ./
RUN go mod download

# アプリケーションのソースコードをコピー
COPY . .

# テンプレートファイルをコピー
COPY templates/ /app/templates/

# Goアプリケーションをビルド
RUN go build -o server .

# Pythonのベースイメージ
FROM python:3.10-slim AS python-builder

# Pythonの作業ディレクトリを設定
WORKDIR /app

# Pythonのrequirements.txtをコピー
COPY python/requirements.txt .

# Pythonの依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# GoアプリケーションとPythonスクリプトを組み合わせた最終的なイメージ
FROM python:3.10-slim AS final

# 作業ディレクトリを設定
WORKDIR /app

# Goビルダーからバイナリをコピー
COPY --from=go-builder /app/server /app/server

# PythonビルダーからPythonパッケージとスクリプトをコピー
COPY --from=python-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=python-builder /app /app

# テンプレートファイルを最終イメージにもコピー
COPY --from=go-builder /app/templates /app/templates

COPY python/script.py /app/python/script.py
COPY python/circle.py /app/python/circle.py
RUN mkdir /app/processed_files /app/uploaded_files /app/with_circle_img /app/circle_info
COPY how_to_use/how_to_use.png /app/how_to_use/how_to_use.png

# アプリケーションのポートを公開
EXPOSE 8080

# サーバーを起動
CMD ["./server"]
