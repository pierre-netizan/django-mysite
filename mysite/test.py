# class Xxx:
#     def __init__(self,title):
#         self.title=title
#     def __str__(self):
#         return f"{self.__class__.__name__}({self.title})"

# print(Xxx('ooo'))


import requests

def get_public_ip():
    try:
        # 使用免费的公共 API
        response = requests.get('https://api.ipify.org', params={'format': 'text'}, timeout=5)
        return response.text.strip()
    except requests.RequestException as e:
        return f"无法获取IP: {e}"

# 调用函数
public_ip = get_public_ip()
print(f"本机外网IP: {public_ip}")

    