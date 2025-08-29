import os
import re

# 목차를 생성할 기본 경로
root_dir = "." 
# 제외할 폴더 및 파일 목록
exclude_list = ['.git', '.github', 'scripts', 'README.md', '.DS_Store']

# 디렉토리 구조를 저장할 딕셔너리
dir_structure = {}

# 파일 이름에서 날짜나 숫자 프리픽스를 제거하는 함수 (필요시 수정)
def clean_filename(filename):
    # 예: '1.31. javascript reduce.md' -> 'javascript reduce'
    name_without_ext = os.path.splitext(filename)[0]
    # 숫자, 점, 공백으로 시작하는 부분 제거
    cleaned_name = re.sub(r'^\d+[\.\s]*', '', name_without_ext).strip()
    return cleaned_name

# 디렉토리 순회
for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
    # 제외 목록에 있는 디렉토리는 건너뛰기
    dirnames[:] = [d for d in dirnames if d not in exclude_list]
    
    # 루트 디렉토리는 건너뛰고 하위 디렉토리만 처리
    if dirpath != root_dir:
        # 현재 디렉토리(카테고리) 이름 가져오기
        category = os.path.basename(dirpath)
        
        # 마크다운 파일만 필터링하고 이름 정리
        md_files = sorted([
            f for f in filenames if f.endswith('.md')
        ])
        
        if md_files:
            dir_structure[category] = []
            for md_file in md_files:
                file_path = os.path.join(dirpath, md_file).replace('\\', '/')
                file_title = clean_filename(md_file)
                dir_structure[category].append(f"[{file_title}]({file_path})")


# 마크다운 목차 텍스트 생성
markdown_text = ""
sorted_categories = sorted(dir_structure.keys())

for category in sorted_categories:
    markdown_text += f"### 📂 {category}\n"
    for item in dir_structure[category]:
        markdown_text += f"- {item}\n"
    markdown_text += "\n"


# README.md 파일 읽기
with open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()

# README.md에서 기존 목차 영역 찾아 교체
# 정규표현식을 사용하여 주석 사이의 내용을 찾음
pattern = r"(.*?)"
new_readme_content = re.sub(
    pattern,
    f"\n{markdown_text}",
    readme_content,
    flags=re.DOTALL
)

# 변경된 내용으로 README.md 파일 쓰기
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme_content)

print("README.md has been updated successfully.")
