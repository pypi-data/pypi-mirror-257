from lightningrobot_cli import install
import requests
import zipfile
import os
import pip

def main():
    print("[询问]项目名称")
    name = input()
    
    # 下载模板文件并保存到本地
    response = requests.get("https://github.com/LightningRobot/template/archive/refs/heads/main.zip", stream=True)
    with open("template-main.zip", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    # 解压到指定目录
    with zipfile.ZipFile("template-main.zip", 'r') as zip_ref:
        zip_ref.extractall(name)
    os.rename(f"{name}/template-main", name)

    # 安装适配器包并创建适配器目录
    print("[询问]要使用哪个适配器")
    adaptername = input()
    adapter_package = f"lighteningrobot-adapter-{adaptername}"  # 修正适配器包名计算
    pip.main(['install', adapter_package])  # 使用pip.main代替pip._internal

    path = f"{name}/adapters/{adaptername}"
    os.makedirs(path, exist_ok=True)  # 添加exist_ok=True以避免已存在的错误

    adapter_url = install.get_package_config(adapter_package)['download_url']  # 假设get_package_config返回包含download_url的字典

    response = requests.get(adapter_url, stream=True)
    adapter_zip_file = f"{adaptername}-main.zip"
    with open(adapter_zip_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

    # 解压适配器文件到指定目录
    with zipfile.ZipFile(adapter_zip_file, 'r') as zip_ref:
        zip_ref.extractall(path)

    # 删除临时的zip文件
    os.remove(adapter_zip_file)

    print(f"[信息]成功安装适配器包 {adaptername}！（来源：PyPI）")
    print("[信息]创建成功！")