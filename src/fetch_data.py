import os
import requests
from pathlib import Path

# --- 配置信息 ---
# hallelujahIM 仓库信息
REPO_OWNER = 'dongyuwei'
REPO_NAME = 'hallelujahIM'
REPO_BRANCH = 'master'
REPO_DICT_PATH = 'dictionary'

# 需要下载的原始词典文件列表
REQUIRED_FILES = [
    'words_with_frequency_and_translation_and_ipa.json',
    'phonex_encoded_words.json',
    'fuzzy_soundex_encoded_words.json',
]

def fetch_source_files(data_dir: Path):
    """
    检查并下载所需的原始词典文件。
    该函数具有幂等性，只有当文件不存在时才会下载。
    """
    print("Checking for source dictionary files...")
    data_dir.mkdir(parents=True, exist_ok=True)

    # 检查是否所有文件都已存在
    missing_files = []
    for filename in REQUIRED_FILES:
        if not (data_dir / filename).exists():
            missing_files.append(filename)

    if not missing_files:
        print(f"All source files already exist in '{data_dir}'. Skipping download.")
        return

    print(f"Missing files: {', '.join(missing_files)}. Starting download from GitHub...")

    # 使用 requests 库下载缺失的文件
    # 参考: [Download single files from GitHub - Stack Overflow](https://stackoverflow.com/questions/4604663/download-single-files-from-github){target="_blank" class="gpt-web-url"}
    # 构造 GitHub raw 内容的基础 URL
    base_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/refs/heads/{REPO_BRANCH}/{REPO_DICT_PATH}"

    for filename in missing_files:
        file_url = f"{base_url}/{filename}"
        target_path = data_dir / filename
        
        try:
            print(f"Downloading {filename}...")
            response = requests.get(file_url, stream=True, timeout=60)
            response.raise_for_status()  # 如果请求失败 (如 404), 则抛出异常

            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Successfully saved to '{target_path}'")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename}: {e}")
            # 如果下载失败，删除可能已创建的不完整文件
            if target_path.exists():
                target_path.unlink()
            # 抛出异常，中断整个构建过程，因为缺少源文件无法继续
            raise IOError(f"Failed to download required source file: {filename}") from e

