from lightningrobot_cli import install
import requests
import zipfile
import os
import pip._internal

def main():
    print("[询问]项目名称")
    name = input()
    # 下载模板文件并解压到指定目录
    requests.get("https://github.com/LightningRobot/template/archive/refs/heads/main.zip", stream=True)
    zipfile.ZipFile("template-main.zip")
    os.rename("template-main",name)
    # 安装适配器包并创建适配器目录
    print("[询问]要使用哪个适配器")
    adaptername = input()
    adapter = f"lighteningrobot-adapter-" + name
    pip._internal.main(['install', adapter])
    path = f"{name}adapters/{adaptername}"
    os.makedirs(path)
    adapter_url = install.get_package_config(adapter)
    requests.get(adapter_url, stream=True)
    print(f"[信息]成功安装适配器包 {adaptername}！（来源：PyPI）")
    print("[信息]创建成功！")