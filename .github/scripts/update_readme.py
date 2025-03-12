import os
import re

# 현재 스크립트가 실행되는 위치를 기준으로 경로 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))  # 루트 디렉터리로 이동
README_PATH = os.path.join(ROOT_DIR, "README.md")  # Readme.md의 절대경로 설정

# GitHub Repository Base URL
BASE_URL = "https://github.com/jihostudy/TIL/blob/main/"

def get_target_dirs():
    """ 루트 디렉터리에서 README.md, .git 등을 제외한 폴더 목록 가져오기 """
    return [
        d for d in os.listdir(ROOT_DIR)
        if os.path.isdir(os.path.join(ROOT_DIR, d)) and d not in [".git", ".github"]
    ]

def get_markdown_links(directory):
    """ 특정 디렉터리 내 모든 `.md` 파일의 링크를 생성 """
    links = []
    
    for root, _, files in os.walk(os.path.join(ROOT_DIR, directory)):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), ROOT_DIR).replace("\\", "/")
                encoded_path = rel_path.replace(" ", "%20")
                links.append(f"[{file.replace('.md', '')}]({BASE_URL}{encoded_path})")

    return sorted(links)

def update_readme():
    """ Readme.md 파일을 최신화 """
    target_dirs = get_target_dirs()
    
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    updated_content = content  # 변경 내용을 저장할 변수
    changes_detected = False  # 변경 사항 확인 변수

    for directory in target_dirs:
        section_title = f"## 📌 {directory.replace('_', ' ')}"
        
        if section_title in content:
            links = get_markdown_links(directory)
            new_section = f"{section_title}\n\n### 📄 학습 내용\n\n" + "\n".join(links) + "\n\n"
            section_pattern = rf"({re.escape(section_title)}\n\n### 📄 학습 내용\n\n)(.*?)(\n\n## |\Z)"
            
            updated_content, num_subs = re.subn(section_pattern, new_section, updated_content, flags=re.DOTALL)

            if num_subs > 0:
                print(f"🔄 {directory} 섹션 업데이트됨.")
                changes_detected = True

    if changes_detected:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("✅ README.md 파일이 변경되었습니다.")
    else:
        print("⚠️ README.md 파일에 변경 사항이 없습니다.")

if __name__ == "__main__":
    update_readme()
