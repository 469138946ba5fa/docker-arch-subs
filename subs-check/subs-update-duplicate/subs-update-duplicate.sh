#!/usr/bin/env bash
set -euo pipefail

export IP=192.168.255.253 H_P=7890 S_P=7890 ; export HTTP_PROXY=http://${IP}:${H_P} HTTPS_PROXY=http://${IP}:${H_P} ALL_PROXY=socks5://${IP}:${S_P} http_proxy=http://${IP}:${H_P} https_proxy=http://${IP}:${H_P} all_proxy=socks5://${IP}:${S_P} 

curl -I www.google.com
python update-json-v1.0.py
python duplicate-data-v3.0.py
cat ../config/config.yaml
cp -fv sub_list.json sub_list.json.bak

unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy

# 定义变量
HTTP_PORT=8001
TIMESTAMP=$(TZ='Asia/Shanghai' date '+%Y-%m-%d %T')

# 函数：更新本地文件
update_files() {
  echo "开始更新本地文件……"
  # 删除旧文件
  rm -frv bpb*.txt
  # 拷贝更新后的文件
  python3 bpb-make.py
  echo "所有文件均已处理完成。"
}

# 函数：重启 HTTP 服务
restart_http_server() {
  echo "开始重启 HTTP 服务……"
  # 优雅关闭已有服务，避免使用 sudo kill -9（也可用 pkill）
  pkill -f "python3 -m http.server -b 0.0.0.0 -d" || true
  sleep 1
  nohup python3 -m http.server -b 0.0.0.0 -d . "$HTTP_PORT" > "http-server.log" 2>&1 &
  echo "HTTP 服务已重启。"
}

# 主流程
update_files
restart_http_server
chmod -Rv a+x .
