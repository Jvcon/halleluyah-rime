import json
from pathlib import Path

def _convert_dict_to_lua_table_str(py_dict: dict) -> str:
    """将 Python 字典转换为 Lua table 字符串。"""
    lines = []
    for key, value in py_dict.items():
        # Lua 字符串需要用双引号包裹，并转义特殊字符
        key_str = json.dumps(key) 
        # value 是一个单词列表，同样处理
        lua_array_items = [json.dumps(item) for item in value]
        val_str = "{" + ", ".join(lua_array_items) + "}"
        lines.append(f"  [{key_str}] = {val_str},")
    return "{\n" + "\n".join(lines) + "\n}"


def build_fuzzy_sound_resources(data_path: Path, lua_dir: Path):
    """
    处理模糊音文件，生成 lua 可用的资源文件。
    """
    print("Building fuzzy sound resources for Lua...")

    lua_dir.mkdir(parents=True, exist_ok=True)

    files_to_process = {
        'phonex_encoded_words.json': 'phonex_encoded.lua',
        'fuzzy_soundex_encoded_words.json': 'fuzzy_soundex_encoded.lua'
    }

    for in_file, out_file in files_to_process.items():
        # 1. 加载原始 JSON
        with open(data_path / in_file, 'r', encoding='utf-8') as f:
            fuzzy_data = json.load(f)

        # 2. 转换为 Lua table 字符串
        lua_table_str = _convert_dict_to_lua_table_str(fuzzy_data)
        
        # 3. 包装成一个返回 table 的 Lua 模块
        lua_module_content = f"-- This file is auto-generated.\nreturn {lua_table_str}"
        
        # 4. 写入 .lua 文件
        output_path = lua_dir / out_file
        output_path.write_text(lua_module_content, encoding='utf-8')
        print(f"Successfully created '{output_path}'")

