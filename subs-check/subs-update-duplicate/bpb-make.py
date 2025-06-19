'''功能说明
有一个原始数据 hosts.txt 文件内容如下
https://acc.moonfix.ir
https://de6.mamatune.top
https://www.speedtest.net
https://de4.mamatune.top
https://cfvless.betterman.xyz


并生成九个文件，生成顺序如下
bpb-vless-tls.txt
bpb-vless-tls-cfnat.txt
bpb-vless-tls-cloudflarest.txt
bpb-vless-notls.txt
bpb-vless-notls-cfnat.txt
bpb-vless-notls-cloudflarest.txt
bpb-trojan-tls.txt
bpb-trojan-tls-cfnat.txt
bpb-trojan-tls-cloudflarest.txt


根据链接数*文件数得到总数量 45 
根据总数得知两位数，单个数字前补上一个0，后面的升序序号是有用的，比如总量如果是100那么数字位数为3 单数字补2个0 双数字补1个0 一次类推，后面的需求需要

每个文件最终生成内容如下
其中 bpb-trojan-tls.txt bpb-trojan-tls-cfnat.txt bpb-trojan-tls-cloudflarest.txt 套用的模板字符串如下
trojan://bpb-trojan@visa.cn:443?security=tls&sni=这里填域名&type=ws&host=这里填域名&path=%2Ftr%3Fed%3D2560#BPB好人

bpb-trojan-tls.txt 文件生成内容如下保持 visa.cn:443 不变 并且将 `#BPB好人` 替换为 `#bpb-trojan-tls` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-trojan-tls` 最后附上升序数字编号，动态补0
trojan://bpb-trojan@visa.cn:443?security=tls&sni=acc.moonfix.ir&type=ws&host=acc.moonfix.ir&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls00
trojan://bpb-trojan@visa.cn:443?security=tls&sni=de6.mamatune.top&type=ws&host=de6.mamatune.top&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls01
trojan://bpb-trojan@visa.cn:443?security=tls&sni=www.speedtest.net&type=ws&host=www.speedtest.net&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls02
trojan://bpb-trojan@visa.cn:443?security=tls&sni=de4.mamatune.top&type=ws&host=de4.mamatune.top&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls03
trojan://bpb-trojan@visa.cn:443?security=tls&sni=cfvless.betterman.xyz&type=ws&host=cfvless.betterman.xyz&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls04


bpb-trojan-tls-cfnat.txt 文件生成内容如下并替换 visa.cn:443 为 192.168.255.253:1234 并且将 `#BPB好人` 替换为 `#bpb-trojan-tls-cfnat` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-trojan-tls-cfnat` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
trojan://bpb-trojan@192.168.255.253:1234?security=tls&sni=acc.moonfix.ir&type=ws&host=acc.moonfix.ir&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cfnat05
trojan://bpb-trojan@192.168.255.253:1234?security=tls&sni=de6.mamatune.top&type=ws&host=de6.mamatune.top&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cfnat06
trojan://bpb-trojan@192.168.255.253:1234?security=tls&sni=www.speedtest.net&type=ws&host=www.speedtest.net&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cfnat07
trojan://bpb-trojan@192.168.255.253:1234?security=tls&sni=de4.mamatune.top&type=ws&host=de4.mamatune.top&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cfnat08
trojan://bpb-trojan@192.168.255.253:1234?security=tls&sni=cfvless.betterman.xyz&type=ws&host=cfvless.betterman.xyz&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cfnat09


bpb-trojan-tls-cloudflarest.txt 文件生成内容如下并替换 visa.cn:443 为 104.27.4.153:443 并且将 `#BPB好人` 替换为 `#bpb-trojan-tls-cloudflarest` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-trojan-tls-cloudflarest` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
trojan://bpb-trojan@104.27.4.153:443?security=tls&sni=acc.moonfix.ir&type=ws&host=acc.moonfix.ir&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cloudflarest10
trojan://bpb-trojan@104.27.4.153:443?security=tls&sni=de6.mamatune.top&type=ws&host=de6.mamatune.top&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cloudflarest11
trojan://bpb-trojan@104.27.4.153:443?security=tls&sni=www.speedtest.net&type=ws&host=www.speedtest.net&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cloudflarest12
trojan://bpb-trojan@104.27.4.153:443?security=tls&sni=de4.mamatune.top&type=ws&host=de4.mamatune.top&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cloudflarest13
trojan://bpb-trojan@104.27.4.153:443?security=tls&sni=cfvless.betterman.xyz&type=ws&host=cfvless.betterman.xyz&path=%2Ftr%3Fed%3D2560%23bpb-trojan-tls-cloudflarest14


其中 bpb-vless-notls.txt bpb-vless-notls-cfnat.txt bpb-vless-notls-cloudflarest.txt 套用的模板字符串如下
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:80?encryption=none&security=none&type=ws&host=这里填域名&path=%3Fed%3D2560#BPB好人

bpb-vless-notls.txt 文件生成内容如下保持 visa.cn:443 不变 并且将 `#BPB好人` 替换为 `#bpb-vless-notls` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-vless-notls` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:80?encryption=none&security=none&type=ws&host=acc.moonfix.ir&path=%3Fed%3D2560%23bpb-vless-notls15
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:80?encryption=none&security=none&type=ws&host=de6.mamatune.top&path=%3Fed%3D2560%23bpb-vless-notls16
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:80?encryption=none&security=none&type=ws&host=www.speedtest.net&path=%3Fed%3D2560%23bpb-vless-notls17
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:80?encryption=none&security=none&type=ws&host=de4.mamatune.top&path=%3Fed%3D2560%23bpb-vless-notls18
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:80?encryption=none&security=none&type=ws&host=cfvless.betterman.xyz&path=%3Fed%3D2560%23bpb-vless-notls19


bpb-vless-notls-cfnat.txt 文件生成内容如下并替换 visa.cn:443 为 192.168.255.253:1234 并且将 `#BPB好人` 替换为 `#bpb-vless-notls-cfnat` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-vless-notls-cfnat` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=none&type=ws&host=acc.moonfix.ir&path=%3Fed%3D2560%23bpb-vless-notls-cfnat20
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=none&type=ws&host=de6.mamatune.top&path=%3Fed%3D2560%23bpb-vless-notls-cfnat21
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=none&type=ws&host=www.speedtest.net&path=%3Fed%3D2560%23bpb-vless-notls-cfnat22
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=none&type=ws&host=de4.mamatune.top&path=%3Fed%3D2560%23bpb-vless-notls-cfnat23
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=none&type=ws&host=cfvless.betterman.xyz&path=%3Fed%3D2560%23bpb-vless-notls-cfnat24


bpb-vless-notls-cloudflarest.txt 文件生成内容如下并替换 visa.cn:443 为 104.27.4.153:443 并且将 `#BPB好人` 替换为 `#bpb-vless-notls-cloudflarest` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-vless-notls-cloudflarest` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=none&type=ws&host=acc.moonfix.ir&path=%3Fed%3D2560%23bpb-vless-notls-cloudflarest25
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=none&type=ws&host=de6.mamatune.top&path=%3Fed%3D2560%23bpb-vless-notls-cloudflarest26
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=none&type=ws&host=www.speedtest.net&path=%3Fed%3D2560%23bpb-vless-notls-cloudflarest27
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=none&type=ws&host=de4.mamatune.top&path=%3Fed%3D2560%23bpb-vless-notls-cloudflarest28
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=none&type=ws&host=cfvless.betterman.xyz&path=%3Fed%3D2560%23bpb-vless-notls-cloudflarest29


其中 bpb-vless-tls.txt bpb-vless-tls-cfnat.txt bpb-vless-tls-cloudflarest.txt 套用的模板字符串如下
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:443?encryption=none&security=tls&sni=这里填域名&type=ws&host=这里填域名&path=%3Fed%3D2560#BPB好人

bpb-vless-tls.txt 文件生成内容如下保持 visa.cn:443 不变 并且将 `#BPB好人` 替换为 `#bpb-vless-tls` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-vless-tls` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:443?encryption=none&security=tls&sni=acc.moonfix.ir&type=ws&host=acc.moonfix.ir&path=%3Fed%3D2560%23bpb-vless-tls30
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:443?encryption=none&security=tls&sni=de6.mamatune.top&type=ws&host=de6.mamatune.top&path=%3Fed%3D2560%23bpb-vless-tls31
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:443?encryption=none&security=tls&sni=www.speedtest.net&type=ws&host=www.speedtest.net&path=%3Fed%3D2560%23bpb-vless-tls32
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:443?encryption=none&security=tls&sni=de4.mamatune.top&type=ws&host=de4.mamatune.top&path=%3Fed%3D2560%23bpb-vless-tls33
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@visa.cn:443?encryption=none&security=tls&sni=cfvless.betterman.xyz&type=ws&host=cfvless.betterman.xyz&path=%3Fed%3D2560%23bpb-vless-tls34


bpb-vless-tls-cfnat.txt 文件生成内容如下并替换 visa.cn:443 为 192.168.255.253:1234 并且将 `#BPB好人` 替换为 `#bpb-vless-tls-cfnat` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-vless-tls-cfnat` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=tls&sni=acc.moonfix.ir&type=ws&host=acc.moonfix.ir&path=%3Fed%3D2560%23bpb-vless-tls-cfnat35
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=tls&sni=de6.mamatune.top&type=ws&host=de6.mamatune.top&path=%3Fed%3D2560%23bpb-vless-tls-cfnat36
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=tls&sni=www.speedtest.net&type=ws&host=www.speedtest.net&path=%3Fed%3D2560%23bpb-vless-tls-cfnat37
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=tls&sni=de4.mamatune.top&type=ws&host=de4.mamatune.top&path=%3Fed%3D2560%23bpb-vless-tls-cfnat38
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@192.168.255.253:1234?encryption=none&security=tls&sni=cfvless.betterman.xyz&type=ws&host=cfvless.betterman.xyz&path=%3Fed%3D2560%23bpb-vless-tls-cfnat39


bpb-vless-tls-cloudflarest.txt 文件生成内容如下并替换 visa.cn:443 为 104.27.4.153:443 并且将 `#BPB好人` 替换为 `#bpb-vless-tls-cloudflarest` 并通过 `encodeURIComponent` 最终转换为 `%23bpb-vless-tls-cloudflarest` 最后附上升序数字编号，动态补0，并接上上个文件的数字编号结尾
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=tls&sni=acc.moonfix.ir&type=ws&host=acc.moonfix.ir&path=%3Fed%3D2560%23bpb-vless-tls-cloudflarest40
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=tls&sni=de6.mamatune.top&type=ws&host=de6.mamatune.top&path=%3Fed%3D2560%23bpb-vless-tls-cloudflarest41
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=tls&sni=www.speedtest.net&type=ws&host=www.speedtest.net&path=%3Fed%3D2560%23bpb-vless-tls-cloudflarest42
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=tls&sni=de4.mamatune.top&type=ws&host=de4.mamatune.top&path=%3Fed%3D2560%23bpb-vless-tls-cloudflarest43
vless://89b3cbba-e6ac-485a-9481-976a0415eab9@104.27.4.153:443?encryption=none&security=tls&sni=cfvless.betterman.xyz&type=ws&host=cfvless.betterman.xyz&path=%3Fed%3D2560%23bpb-vless-tls-cloudflarest44
'''

from pathlib import Path
from urllib.parse import quote

# 🧩 参数集中定义
UUID = "89b3cbba-e6ac-485a-9481-976a0415eab9"
TROJAN_PWD = "bpb-trojan"

ADDRS = {
    "visa_tls": "visa.cn:443",
    "visa_notls": "visa.cn:80",
    "cfnat": "192.168.255.253:1234",
    "cloudflare": "104.16.38.129:443",
}

SECURITY = {
    "tls": "security=tls",
    "notls": "security=none",
}

# ✨ 模板生成器（VLESS / Trojan）
def make_vless(addr_key, sec_key, tag_name):
    return (
        f"vless://{UUID}@{ADDRS[addr_key]}?encryption=none&{SECURITY[sec_key]}"
        f"&sni={{d}}&type=ws&host={{d}}&path=%3Fed%3D2560#{{tag}}"
    ), tag_name

def make_trojan(addr_key, tag_name):
    return (
        f"trojan://{TROJAN_PWD}@{ADDRS[addr_key]}?security=tls"
        f"&sni={{d}}&type=ws&host={{d}}&path=%2Ftr%3Fed%3D2560#{{tag}}"
    ), tag_name

# 📁 所有输出目标与模板组合
configurations = [
    ("bpb-vless-tls.txt",               *make_vless("visa_tls", "tls", "bpb-vless-tls")),
    ("bpb-vless-tls-cfnat.txt",         *make_vless("cfnat", "tls", "bpb-vless-tls-cfnat")),
    ("bpb-vless-tls-cloudflarest.txt", *make_vless("cloudflare", "tls", "bpb-vless-tls-cloudflarest")),
    ("bpb-vless-notls.txt",            *make_vless("visa_notls", "notls", "bpb-vless-notls")),
    ("bpb-vless-notls-cfnat.txt",      *make_vless("cfnat", "notls", "bpb-vless-notls-cfnat")),
    ("bpb-vless-notls-cloudflarest.txt",*make_vless("cloudflare", "notls", "bpb-vless-notls-cloudflarest")),
    ("bpb-trojan-tls.txt",              *make_trojan("visa_tls", "bpb-trojan-tls")),
    ("bpb-trojan-tls-cfnat.txt",        *make_trojan("cfnat", "bpb-trojan-tls-cfnat")),
    ("bpb-trojan-tls-cloudflarest.txt", *make_trojan("cloudflare", "bpb-trojan-tls-cloudflarest")),
]

# 🌐 读取域名
with open("hosts.txt", "r", encoding="utf-8") as f:
    domains = [line.strip().replace("https://", "") for line in f if line.strip()]

# 🚀 生成配置
total = len(domains) * len(configurations)
width = len(str(total))
index = 0

for filename, template, tag in configurations:
    lines = []
    for domain in domains:
        tag_encoded = quote(f"#{tag}{str(index).zfill(width)}")
        lines.append(template.format(d=domain, tag=tag_encoded))
        index += 1
    Path(filename).write_text("\n".join(lines), encoding="utf-8")

print("✔️ 所有配置生成完毕")