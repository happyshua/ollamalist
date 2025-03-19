import pandas as pd
import requests
import json
from urllib.parse import urljoin
import time

def get_models(server_url):
    try:
        response = requests.get(urljoin(server_url, 'api/tags'))
        if response.status_code == 200:
            models = response.json()
            return ', '.join([model['name'] for model in models['models']])
    except:
        pass
    return ""

# 读取现有的CSV文件
existing_df = pd.read_csv('output_with_models.csv', header=None)
existing_servers = set(existing_df[0].tolist())

# 获取服务器列表
try:
    response = requests.get('https://raw.githubusercontent.com/forrany/Awesome-Ollama-Server/refs/heads/main/public/data.json')
    servers_data = json.loads(response.text)
    
    # 筛选TPS在20-350之间的服务器
    new_servers = []
    for server in servers_data:
        if 20 <= float(server.get('tps', 0)) <= 350:
            server_url = server['server']
            if server_url + '/v1' not in existing_servers:
                models = server.get('models', [])
                models_str = ', '.join([str(model) for model in models])
                new_servers.append([server_url + '/v1', models_str])
    
    # 将新服务器添加到现有列表
    if new_servers:
        new_df = pd.DataFrame(new_servers)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_csv('output_with_models.csv', header=False, index=False)

except Exception as e:
    print(f"Error updating servers: {str(e)}") 