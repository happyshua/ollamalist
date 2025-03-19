import pandas as pd
import requests
from urllib.parse import urlparse
import time

def check_server(url):
    try:
        # 从完整URL中提取基础URL
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        response = requests.get(base_url, timeout=10)
        return "Ollama is running" in response.text
    except:
        return False

# 读取CSV文件
df = pd.read_csv('output_with_models.csv', header=None)

# 创建一个新的DataFrame来存储活跃的服务器
active_servers = []

# 检查每个服务器
for index, row in df.iterrows():
    server_url = row[0]
    models = row[1] if len(row) > 1 else ""
    
    print(f"Checking server: {server_url}")
    
    if check_server(server_url):
        active_servers.append([server_url, models])
    
    # 添加延迟以避免过快请求
    time.sleep(1)

# 将活跃服务器保存到CSV
active_df = pd.DataFrame(active_servers)
active_df.to_csv('output_with_models.csv', header=False, index=False) 