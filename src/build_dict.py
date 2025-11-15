import json
import yaml
from pathlib import Path

def build_core_dictionary(data_path: Path, dicts_dir: Path, lua_dir: Path):
    """
    处理主词典文件，生成 rime 词典和 lua 使用的元数据文件。
    """
    print("Building core dictionary files...")
    
    # 1. 加载原始 JSON 数据
    with open(data_path / 'words_with_frequency_and_translation_and_ipa.json', 'r', encoding='utf-8') as f:
        words_data = json.load(f)

    rime_dict_lines = []
    lua_meta_data = {}

    # Rime 词典文件头
    rime_dict_header = {
        'name': 'hallelujah_english',
        'version': '1.0',
        'sort': 'by_weight',
        'use_preset_vocabulary': True,
    }
    rime_dict_lines.append(yaml.dump(rime_dict_header, allow_unicode=True, sort_keys=False))
    rime_dict_lines.append('...\n')

    # 2. 遍历数据，生成 Rime 词典行和 Lua 元数据
    for word, data in words_data.items():
        frequency = data.get('frequency', 0)
        
        # 格式: 文本<Tab>编码<Tab>词频
        rime_dict_lines.append(f"{word}\t{word}\t{frequency}")

        # 为 Lua 创建元数据
        meta = {}
        if 'ipa' in data and data['ipa']:
            meta['ipa'] = data['ipa']
        if 'translation' in data and data['translation']:
            # 将多行翻译处理成列表
            meta['trans'] = [t.strip() for t in data['translation'] if t.strip()]
        
        if meta:
            lua_meta_data[word] = meta

    # 3. 写入文件
    dicts_dir.mkdir(parents=True, exist_ok=True)
    lua_dir.mkdir(parents=True, exist_ok=True)
    # 写入 Rime 词典文件
    dict_file_path = dicts_dir / 'english.dict.yaml'
    dict_file_path.write_text('\n'.join(rime_dict_lines), encoding='utf-8')    
    
    # 写入 Lua 使用的元数据 JSON 文件
    meta_file_path = lua_dir / 'english_meta.json'
    with open(meta_file_path, 'w', encoding='utf-8') as f:
        json.dump(lua_meta_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully created '{dict_file_path}' and '{meta_file_path}'")

