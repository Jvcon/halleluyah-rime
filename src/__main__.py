import argparse
from pathlib import Path
from src.fetch_data import fetch_source_files
from src.build_dict import build_core_dictionary
from src.build_fuzzy import build_fuzzy_sound_resources

def main():
    parser = argparse.ArgumentParser(description="Build Rime dictionary files from hallelujahIM data.")
    
    # 使用相对路径，方便在 GitHub Actions 中运行
    repo_root = Path(__file__).parent.parent
    
    parser.add_argument('--data-dir', type=Path, default=repo_root / 'data',
                        help='Directory containing the source JSON files.')
    parser.add_argument('--dicts-dir', type=Path, default=repo_root / 'dicts',
                        help='Output directory for Rime dictionary files.')
    parser.add_argument('--lua-dir', type=Path, default=repo_root / 'lua',
                        help='Output directory for Lua resource files.')
    
    args = parser.parse_args()

    try:
        fetch_source_files(args.data_dir)
    except IOError as e:
        print(f"\nBuild failed: Could not obtain source files. Error: {e}")
        return # 如果文件获取失败，则终止程序

    # 确保输出目录存在
    args.dist_dir.mkdir(parents=True, exist_ok=True)

    # 执行构建任务
    build_core_dictionary(args.data_dir, args.dicts_dir, args.lua_dir)
    build_fuzzy_sound_resources(args.data_dir, args.lua_dir)
    
    print("\nAll tasks completed successfully!")

if __name__ == '__main__':
    main()
