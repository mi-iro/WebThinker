import json

# --- 配置 ---
input_filename = '/mnt/public/lianghao/wzr/WebThinker/outputs/Med/test_medqa..webthinker/test.7.18,0:13.54.json'
output_filename = '/mnt/public/lianghao/wzr/WebThinker/outputs/Med/test_medqa..webthinker/filtered_test.7.18,0:13.54.json'
keys_to_keep = ["id", "question", "options", "output", "prompt", "Output", "WebExplorer"] # 修改这里以指定需要保留的字段

# --- 脚本主体 ---

try:
    # 使用 'with' 语句安全地打开和读取文件
    with open(input_filename, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    # 核心处理逻辑（与之前相同）
    filtered_data = [
        {key: obj[key] for key in keys_to_keep if key in obj}
        for obj in original_data
    ]

    # 使用 'with' 语句安全地写入新文件
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"处理完成！已从 '{input_filename}' 读取数据。")
    print(f"已将筛选后的数据写入 '{output_filename}'。")
    print(f"保留的字段: {keys_to_keep}")

except FileNotFoundError:
    print(f"错误：输入文件 '{input_filename}' 未找到。")
except json.JSONDecodeError:
    print(f"错误：输入文件 '{input_filename}' 不是有效的JSON格式。")
except Exception as e:
    print(f"发生未知错误: {e}")