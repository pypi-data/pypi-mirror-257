from lightningrobot_cli import install
import requests
import zipfile
import os
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
    install.main(1,adaptername)
    print("[信息]创建成功！")