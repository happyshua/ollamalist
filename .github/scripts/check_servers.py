import pandas as pd
import requests
from urllib.parse import urlparse
import time
from concurrent.futures import ThreadPoolExecutor

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

def process_server(row):
    server_url = row[0]
    models = row[1] if len(row) > 1 else ""
    
    print(f"Checking server: {server_url}")
    
    if check_server(server_url):
        return [server_url, models]
    return None

# 使用ThreadPoolExecutor进行并行处理
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(process_server, df.iterrows())

# 收集活跃的服务器
active_servers = [result for result in results if result is not None]

# 将活跃服务器保存到CSV
active_df = pd.DataFrame(active_servers)
active_df.to_csv('output_with_models.csv', header=False, index=False) 
