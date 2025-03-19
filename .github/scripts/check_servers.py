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
        is_running = "Ollama is running" in response.text
        print(f"Server {url}: {'Active' if is_running else 'Inactive'}")
        return is_running
    except Exception as e:
        print(f"Error checking {url}: {str(e)}")
        # 如果是连接错误，我们暂时认为服务器可能是临时不可用
        return True  # 改为 True，避免因为临时网络问题删除服务器

# 读取CSV文件
df = pd.read_csv('output_with_models.csv', header=None)

def process_server(row):
    server_url = row[0]
    models = row[1] if len(row) > 1 else ""
    
    print(f"Checking server: {server_url}")
    
    if check_server(server_url):
        return [server_url, models]
    return None

# 使用ThreadPoolExecutor进行并行处理
with ThreadPoolExecutor(max_workers=5) as executor:  # 减少并发数，避免过多请求
    results = list(executor.map(process_server, df.iterrows()))

# 收集活跃的服务器
active_servers = [result for result in results if result is not None]

# 确保我们不会意外删除所有服务器
if len(active_servers) < len(df) * 0.5:  # 如果活跃服务器少于总数的50%
    print("Warning: Too many servers appear to be inactive. Aborting update to prevent data loss.")
    exit(1)  # 退出并返回错误码

# 将活跃服务器保存到CSV
active_df = pd.DataFrame(active_servers)
if not active_df.empty:  # 只有在有活跃服务器时才更新文件
    active_df.to_csv('output_with_models.csv', header=False, index=False)
else:
    print("Error: No active servers found. Keeping existing server list.")
    exit(1) 