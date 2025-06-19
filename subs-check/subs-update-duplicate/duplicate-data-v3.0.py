import os
import json
# python -m pip install ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

'''功能说明
比如指定 source.json 文件位置内容如下
[
  {
    "id": 0,
    "remarks": "test0",
    "site": "test0",
    "url": "https://a.txt|https://b.txt|https://c.txt",
    "update_method": "change_date",
    "enabled": true
  },
  {
    "id": 1,
    "remarks": "test1",
    "site": "test1",
    "url": "https://d.txt|httpx://a.txt|https://a.txt|https://e.txt",
    "update_method": "change_date",
    "enabled": true
  },
  {
    "id": 2,
    "remarks": "test2",
    "site": "test2",
    "url": "https://f.txt|httpx://g.txt|https://b.txt",
    "update_method": "change_date",
    "enabled": true
  }
]
比如指定 result.yaml 文件位置内容如下
other1:
  - '21'
  - '121'
other2:
  - '21'
  - '121'
  - '121'
  - '121'
other3:
  - '121'
  - '121'
  - '121'
sub-urls:
  - http://192.168.255.150:8001/sub_merge.txt
other4:
  - '121'
  - '121'
去重之后效果就是 result.yaml 文件中的 sub-urls: 下
other1:
  - '21'
  - '121'
other2:
  - '21'
  - '121'
  - '121'
  - '121'
other3:
  - '121'
  - '121'
  - '121'
sub-urls:
  - "https://a.txt"
  - "httpx://b.txt"
  - "https://c.txt"
  - "https://d.txt"
  - "httpx://a.txt"
  - "https://e.txt"
  - "https://f.txt"
  - "httpx://g.txt"
other4:
  - '121'
  - '121'
'''

def main():
    # -------------------------------
    # 用户输入路径
    # -------------------------------
    # source_json_path = input("请输入 source.json 文件的路径: ").strip()
    # result_yaml_path = input("请输入保存 result.yaml 文件的路径: ").strip()
    source_json_path = 'sub_list.json'
    result_yaml_path = '../config/config.yaml'
    # 检查 source.json 文件是否存在
    if not os.path.exists(source_json_path):
        print(f"错误：文件 {source_json_path} 不存在。")
        return

    # -------------------------------
    # 第一步：加载 source.json 文件并提取 URL
    # -------------------------------
    # 读取 source.json 文件
    try:
        with open(source_json_path, "r", encoding="utf-8") as f:
            source_data = json.load(f)
    except Exception as e:
        print(f"读取 JSON 文件时出错: {e}")
        return

    # 提取 URL 字段并去重
    seen = set()
    unique_urls = []

    for entry in source_data:
        url_field = entry.get("url", "")
        urls = url_field.split("|")  # 按 "|" 分割 URL
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)

    # -------------------------------
    # 第二步：加载/创建 result.yaml 文件
    # -------------------------------
    yaml = YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    # 加载或初始化 YAML 数据
    if os.path.exists(result_yaml_path):
        try:
            with open(result_yaml_path, "r", encoding="utf-8") as f:
                yaml_data = yaml.load(f)
                if yaml_data is None:
                    yaml_data = {}
        except Exception as e:
            print(f"读取 YAML 文件时出错: {e}")
            return
    else:
        print(f"文件 {result_yaml_path} 不存在，将创建一个新的文件。")
        yaml_data = {}

    # 更新 "sub-urls" 节点，确保每个 URL 被双引号包裹
    yaml_data["sub-urls"] = [DoubleQuotedScalarString(url) for url in unique_urls]

    # -------------------------------
    # 第三步：写回 result.yaml 文件
    # -------------------------------
    try:
        with open(result_yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(yaml_data, f)
        print(f"成功更新 {result_yaml_path} 文件中的 sub-urls 节点！")
    except Exception as e:
        print(f"写入 YAML 文件时出错: {e}")

if __name__ == "__main__":
    main()

