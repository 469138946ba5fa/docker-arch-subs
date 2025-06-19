#!/usr/bin/env python3
import os
import json
import re
# python -m pip install requests
import requests
import time
import logging
import argparse
from datetime import datetime

'''功能说明
更新json文件上某些特殊的链接，比如页面获取，日期更新这种需要时时请求更新的链接，并持续性的挂载间隔一段时间就更新
脚本指定json文件，并读取，内容如下 
[
    {
      "id": 0,
      "remarks": "crazygeeky",
      "site": "https://www.crazygeeky.com/",
      "url": "https://crazygeeky.com/wp-content/uploads/attachment/20250403.txt|https://crazygeeky.com/wp-content/uploads/attachment/20250403.yaml",
      "update_method": "change_date",
      "enabled": true
    },
    {
      "id": 1,
      "remarks": "Fukki-Z/nodefree",
      "site": "https://nodefree.org/f/freenode|Fukki-Z/nodefree|FiFier/v2rayShare",
      "url": "https://nodefree.githubrowcontent.com/2025/04/20250403.yaml|https://nodefree.githubrowcontent.com/2025/04/20250403.txt",
      "update_method": "change_date",
      "enabled": true
    },
    {
      "id": 2,
      "remarks": "nexthiddify.github.io",
      "site": "https://nexthiddify.github.io",
      "url": "https://node.freeclashnode.com/uploads/2025/04/0-20250403.txt|https://node.freeclashnode.com/uploads/2025/04/1-20250403.txt|https://node.freeclashnode.com/uploads/2025/04/2-20250403.txt",
      "update_method": "change_date",
      "enabled": true
    },
    {
      "id": 3,
      "remarks": "www.freev2raynode.com",
      "site": "https://www.freev2raynode.com/",
      "url": "https://node.freev2raynode.com/uploads/2025/04/0-20250403.txt|https://node.freev2raynode.com/uploads/2025/04/1-20250403.txt",
      "update_method": "change_date",
      "enabled": true
    },
    {
      "id": 4,
      "remarks": "gooooooooooooogle/collectSub",
      "site": "https://github.com/gooooooooooooogle/collectSub",
      "url": "https://paste.gg/p/anonymous/6e1b3f2aec804d80b4dd73a691fbd635/files/deb8313f637c44bd981786e3e4c75e95/raw|https://sub.scp-nsc.top/clash",
      "update_method": "page_release",
      "enabled": true
    },
    {
      "id": 5,
      "remarks": "github.com/beck-8",
      "site": "https://github.com/beck-8/subs-check/raw/refs/heads/master/config/config.example.yaml",
      "url": "https://fastly.jsdelivr.net/gh/Alvin9999/PAC@latest/backup/img/1/2/ip/clash.meta2/2/config.yaml|https://fastly.jsdelivr.net/gh/Alvin9999/PAC@latest/backup/img/1/2/ip/clash.meta2/4/config.yaml",
      "update_method": "page_release",
      "enabled": true
    }
  ]
然后执行这个脚本根据日期或页面更新有效链接，保持json文件时时最新
'''

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Update:
    def __init__(self, json_file):
        self.json_file = json_file
        self.session = requests.Session()  # 创建请求会话

    def load_json(self):
        with open(self.json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, data):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=False, indent=2, ensure_ascii=False)

    def url_updated(self, url):
        """判断远程链接是否已更新（返回 True 表示请求成功）"""
        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()  # 若状态码为4xx、5xx，则抛出异常
            logging.info("Status code for {}: {}".format(url, resp.status_code))
            return True
        except requests.RequestException as e:
            logging.error("Error fetching {}: {}".format(url, e))
            return False

    def get_valid_urls_joined(self, urls):
        """传入形如用 | 分隔的 URL 字符串，检查每个链接，返回用 | 拼接的有效链接字符串"""
        url_list = urls.split('|')
        valid_urls = []
        for url in url_list:
            if self.url_updated(url):
                valid_urls.append(url)
            else:
                logging.error("URL {} failed or is invalid.".format(url))
        joined_urls = '|'.join(valid_urls)
        logging.info("Valid URLs joined: {}".format(joined_urls))
        return joined_urls if valid_urls else urls

    def update_json(self):
        """加载 JSON，更新各记录的链接，并写回文件"""
        # 获取当前日期信息
        today = datetime.today()
        this_year = today.strftime('%Y')
        this_month_str = today.strftime('%m')      # 带前导零月份
        this_month_int = str(today.month)          # 去掉前导零的月份
        this_today = today.strftime('%Y%m%d')
        this_day_str = today.strftime('%d')        # 带前导零日
        this_day_int = str(today.day)            # 去掉前导零的日
        data = self.load_json()
        updated = False

        for sub in data:
            try:
                # 仅对 enabled 为 True 且 update_method 不是 'auto' 的记录进行更新
                if sub.get('enabled', False) and sub.get('update_method') != 'auto':
                    id = sub.get('id')
                    current_url = sub.get('url')
                    logging.info("Processing ID {}.".format(id))
                    if sub.get('update_method') == 'change_date':
                        new_url = self.change_date(id, current_url, this_year, this_month_str, this_today)
                    elif sub.get('update_method') == 'page_release':
                        new_url = self.find_link(id, current_url, this_year, this_month_str, this_month_int, this_day_int)
                    else:
                        new_url = current_url
                    if new_url != current_url:
                        sub['url'] = new_url
                        updated = True
                        logging.info("ID {} url updated to {}".format(id, new_url))
                    else:
                        logging.info("No available update for ID {}".format(id))
            except KeyError as e:
                logging.error("KeyError {} for record. Please check update method settings.".format(e))
        if updated:
            self.save_json(data)
            logging.info("JSON file updated successfully.")
        else:
            logging.info("No updates were made to the JSON file.")

    def change_date(self, id, current_url, this_year, this_month_str, this_today):
        """更新 URL 地址，基于日期"""
        if id == 0:
            new_url = f'https://crazygeeky.com/wp-content/uploads/attachment/{this_today}.txt|https://crazygeeky.com/wp-content/uploads/attachment/{this_today}.yaml'
        elif id == 1:
            new_url = f'https://nodefree.githubrowcontent.com/{this_year}/{this_month_str}/{this_today}.yaml|https://nodefree.githubrowcontent.com/{this_year}/{this_month_str}/{this_today}.txt'
        elif id == 2:
            new_url = f'https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/0-{this_today}.txt|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/1-{this_today}.txt|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/2-{this_today}.txt|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/3-{this_today}.txt|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/4-{this_today}.txt|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/0-{this_today}.yaml|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/1-{this_today}.yaml|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/2-{this_today}.yaml|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/3-{this_today}.yaml|https://node.freeclashnode.com/uploads/{this_year}/{this_month_str}/4-{this_today}.yaml'
        elif id == 3:
            new_url = f'https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/0-{this_today}.txt|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/1-{this_today}.txt|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/2-{this_today}.txt|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/3-{this_today}.txt|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/4-{this_today}.txt|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/0-{this_today}.yaml|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/1-{this_today}.yaml|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/2-{this_today}.yaml|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/3-{this_today}.yaml|https://node.freev2raynode.com/uploads/{this_year}/{this_month_str}/4-{this_today}.yaml'
        else:
            new_url = current_url
        valid_urls = self.get_valid_urls_joined(new_url)
        return valid_urls if valid_urls else current_url

    def process_links(self, url, exclusion_patterns, pattern):
        """提取并处理链接"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            # 提取链接并移除双引号
            all_links = [link.replace('"', '') for link in re.findall(pattern, response.text)]
            # 根据排除规则过滤链接并附加参数
            links = []
            for link in all_links:
                if any(re.search(exclusion, link) for exclusion in exclusion_patterns):
                    continue
                if 'sub.xn--4gqvd492adjr.com' in link:  # 检查域名匹配
                    links.append(f"{link}/?flag=clash.meta")  # 添加参数
                else:
                    links.append(link)
            return "|".join(links) if links else None
        except requests.RequestException as e:
            logging.error(f"Failed to fetch links from {url}: {e}")
            return None

    def find_link(self, id, current_url, this_year, this_month_str, this_month_int, this_day_int):
        """根据 ID 查找更新的链接"""
        # 定义更加泛化的排除规则
        exclusion_patterns = [
            r"//github\.com/.+/releases/download",  # GitHub Releases 下载链接
            r"//127\.0\.0\.1:\d+/",  # 本地链接 (支持 http/https)
            r"//notify\..+?/",  # 通知服务
            r"//github\.com/.+/apprise",  # Apprise 服务
            r"//slink\.ltd/.+?",  # Slink 重定向链接
            r"//example\.com/.+?",  # 示例域名 (支持所有路径)
            r"//example\.worker\.dev",  # 匹配 example.worker.dev
            r"HTTP_PROXY|HTTPS_PROXY",  # 环境变量相关
            r"\{[^\}]+\}",  # 排除带有花括号的模板（例如 {Ymd} 或 {Y}-{m}-{d}）的链接
            r"https://ghfast\.top/",  # github-proxy 链接排除规则
        ]
        pattern = r'https?://[^\s"]+'

        # 根据 ID 确定 URL
        if id == 4:
            url = f'https://github.com/gooooooooooooogle/collectSub/raw/refs/heads/main/sub/{this_year}/{this_month_int}/{this_month_int}-{this_day_int}.yaml'
        elif id == 5:
            url = f'https://github.com/beck-8/subs-check/raw/refs/heads/master/config/config.example.yaml'
        elif id == 6:
            url = f'https://github.com/yitong2333/proxy-minging/raw/refs/heads/main/latest.yaml'
        else:
            return current_url

        logging.info(f'{url}')
        links = self.process_links(url, exclusion_patterns, pattern)
        return links if links else current_url


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="实时更新 JSON 文件中的有效链接。")
#     parser.add_argument("--json-file", required=True, help="指定待更新 JSON 文件路径")
#     parser.add_argument("--interval", type=int, default=300, help="更新间隔（秒），默认为300秒")
#     args = parser.parse_args()

#     updater = Update(json_file=args.json_file)
#     while True:
#         updater.update_json()
#         logging.info("等待 {} 秒后进行下一次更新...".format(args.interval))
#         time.sleep(args.interval)

if __name__ == '__main__':
    updater = Update(json_file='sub_list.json')
    updater.update_json()
