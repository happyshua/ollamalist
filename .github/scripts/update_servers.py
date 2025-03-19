name: Update Ollama Servers

on:
  schedule:
    - cron: '0 * * * *'  # 每小时运行一次
  workflow_dispatch:  # 允许手动触发

jobs:
  update-servers:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests pandas
          
      - name: Update server list
        run: python .github/scripts/update_servers.py
        
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add output_with_models.csv
          git commit -m "Update server list: add new servers" || exit 0
          git push