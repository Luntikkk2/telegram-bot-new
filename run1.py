import os
import requests
import subprocess

# Ваши данные
GITHUB_USERNAME = "Luntikkk2"
GITHUB_TOKEN = "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"
REPO_NAME = "telegram-bot-new"
OPENAI_API_KEY = "sk-proj-RB8AU0adiI4SNkUoFtiST3BlbkFJmWeDM6T4Nm9fLnYabzZf"
TELEGRAM_BOT_TOKEN = "7231687026:AAGjcMaY-tjF-JiP8WLiL9mpzKuuTN_hd7g"
REQUIRED_FILES = [".gitattributes", "render.yaml"]
OUTPUT_FILE = "check_repo_output.txt"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result

# Создание нового репозитория на GitHub
def create_github_repo():
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    data = {
        "name": REPO_NAME,
        "private": True
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"Repository '{REPO_NAME}' created successfully.")
    else:
        print(f"Failed to create repository: {response.json()}")

# Создание и добавление .gitattributes файла
def create_gitattributes():
    with open(".gitattributes", "w") as file:
        file.write("* text=auto\n")

# Создание render.yaml
render_yaml = f"""
services:
- type: web
  name: telegram-bot
  env: python
  plan: free
  repo: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}
  buildCommand: pip install -r requirements.txt
  startCommand: python bot.py
  envVars:
  - key: OPENAI_API_KEY
    value: {OPENAI_API_KEY}
  - key: TELEGRAM_BOT_TOKEN
    value: {TELEGRAM_BOT_TOKEN}
"""

def create_render_yaml():
    with open("render.yaml", "w") as file:
        file.write(render_yaml)

# Инициализация репозитория и первый коммит
def init_and_commit():
    run_command("git init")
    create_gitattributes()
    create_render_yaml()
    run_command("git add .")
    run_command('git commit -m "Initial commit"')

# Загрузка кода в репозиторий на GitHub
def push_to_github():
    remote_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    run_command(f"git remote add origin {remote_url}")
    run_command("git branch -M main")
    run_command("git push -u origin main")

# Функция для проверки файлов в репозитории
def check_files_in_repo():
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    with open(OUTPUT_FILE, "w") as file:
        if response.status_code == 200:
            repo_files = [item['name'] for item in response.json()]
            missing_files = [file for file in REQUIRED_FILES if file not in repo_files]
            
            if not missing_files:
                file.write(f"All required files are present in the repository '{REPO_NAME}'.\n")
            else:
                file.write(f"Missing files in the repository '{REPO_NAME}': {', '.join(missing_files)}\n")
        else:
            file.write(f"Failed to access the repository: {response.json()}\n")

# Основной скрипт
if __name__ == "__main__":
    # Настройка глобальных параметров Git
    run_command('git config --global user.name "Luntikkk2"')
    run_command('git config --global user.email "you@example.com"')
    
    create_github_repo()
    init_and_commit()
    push_to_github()
    check_files_in_repo()
