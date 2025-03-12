import os
import re

# Readme.md 파일 경로
README_PATH = "Readme.md"

# GitHub Repository Base URL (네 리포지토리에 맞게 수정!)
BASE_URL = "https://github.com/jihostudy/TIL/blob/main/"

def get_target_dirs():
    """ 루트 디렉터리에서 README.md, .git 등을 제외한 폴더 목록 가져오기 """
    return [
        d for d in os.listdir(".")
        if os.path.isdir(d) and d not in [".git", ".github"]
    ]

def get_markdown_links(directory):
    """ 특정 디렉터리 내 모든 `.md` 파일의 링크를 생성 """
    links = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.join(root, file).replace("\\", "/")
                encoded_path = rel_path.replace(" ", "%20")
                links.append(f"[{file.replace('.md', '')}]({BASE_URL}{encoded_path})")

    return sorted(links)

def update_readme():
    """ Readme.md 파일을 최신화 """
    target_dirs = get_target_dirs()
    
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    for directory in target_dirs:
        section_title = f"## 📌 {directory.capitalize()}"
        if section_title in content:
            links = get_markdown_links(directory)
            section_pattern = rf"({re.escape(section_title)}\n\n### 📄 학습 내용\n\n)(.*?)(\n\n## |\Z)"
            new_section = section_title + "\n\n### 📄 학습 내용\n\n" + "\n".join(links) + "\n\n"
            content = re.sub(section_pattern, new_section, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
