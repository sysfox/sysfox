#!/usr/bin/env python3
"""
GitHub Stats Auto-updater
自动更新 README.md 中的 GitHub 统计信息
"""

import os
import re
import json
import requests
from datetime import datetime


def get_github_stats(username, token):
    """获取 GitHub 统计信息"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    try:
        # 获取用户信息
        user_url = f'https://api.github.com/users/{username}'
        user_response = requests.get(user_url, headers=headers)
        user_data = user_response.json()
        
        # 获取仓库列表
        repos_url = f'https://api.github.com/users/{username}/repos?per_page=100'
        repos_response = requests.get(repos_url, headers=headers)
        repos_data = repos_response.json()
        
        # 计算总星标数
        total_stars = sum(repo['stargazers_count'] for repo in repos_data)
        
        # 获取 PR 和 Issues 数量 (使用搜索 API)
        search_prs_url = f'https://api.github.com/search/issues?q=author:{username}+type:pr'
        prs_response = requests.get(search_prs_url, headers=headers)
        prs_count = prs_response.json()['total_count']
        
        search_issues_url = f'https://api.github.com/search/issues?q=author:{username}+type:issue'
        issues_response = requests.get(search_issues_url, headers=headers)
        issues_count = issues_response.json()['total_count']
        
        return {
            'stars': total_stars,
            'prs': prs_count,
            'issues': issues_count,
            'commits': 1886,  # 可以替换为实际的提交数获取逻辑
            'contributed': 32  # 可以替换为实际的贡献仓库数获取逻辑
        }
        
    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")
        return None


def update_readme(stats):
    """更新 README.md 文件"""
    readme_path = 'README.md'
    
    if not os.path.exists(readme_path):
        print("README.md not found!")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 更新 GitHub Stats 部分
    stats_pattern = r'(GitHub Stats:\s*\n(?:\s*[├└]─[^\n]*\n)*)'
    new_stats = f"""GitHub Stats:
  ├─ Stars Earned: {stats['stars']}
  ├─ Commits (This Year): {stats['commits']}
  ├─ Total PRs: {stats['prs']}
  ├─ Total Issues: {stats['issues']}
  └─ Contributed to (Last Year): {stats['contributed']}
"""
    
    content = re.sub(stats_pattern, new_stats, content)
    
    # 写回文件
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("README.md updated successfully!")
    print(f"Stats: Stars={stats['stars']}, PRs={stats['prs']}, Issues={stats['issues']}")
    return True


def main():
    """主函数"""
    username = 'sysfox'
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("GITHUB_TOKEN environment variable not found!")
        return
    
    print("Fetching GitHub stats...")
    stats = get_github_stats(username, token)
    
    if stats:
        print("Updating README.md...")
        update_readme(stats)
    else:
        print("Failed to fetch GitHub stats!")


if __name__ == '__main__':
    main()
