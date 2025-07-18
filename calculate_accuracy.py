import json
import re
import os

def calculate_accuracy(file_path):
    """
    Parses a JSON file to calculate the accuracy of a model's answers using a more flexible parsing strategy.

    Args:
        file_path (str): The absolute path to the JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误：在 {file_path} 未找到文件")
        return
    except json.JSONDecodeError:
        print(f"错误：无法从文件 {file_path} 解码JSON")
        return

    correct_count = 0
    total_count = 0
    unparsable_model_answers = 0

    for item in data:
        if not isinstance(item, dict):
            continue

        total_count += 1
        
        ground_truth = None
        # Extract ground truth answer from 'output'
        if 'output' in item and isinstance(item['output'], str):
            gt_match = re.search(r'<answer>(.*?)</answer>', item['output'])
            if gt_match:
                ground_truth = gt_match.group(1).strip()
        if ground_truth is None:
            ground_truth = item['output']

        model_answer = None
        # Extract model's answer from 'Output'
        if 'Output' in item and isinstance(item['Output'], str):
            output_text = item['Output']
            # New strategy: Look for the final choice (A, B, or C) in the text.
            # This regex looks for "The answer is A", "My final answer is B.", "Therefore, the correct option is C", etc.
            # It also looks for a single letter A, B, or C at the end of the string, possibly surrounded by punctuation.
            # ma_match = re.search(r'(?:answer is|option is|is:|is)\s*([A-D])|\b([A-D])\.?$', output_text, re.IGNORECASE)
            # if ma_match:
            #     model_answer = next((g for g in ma_match.groups() if g is not None), None)
            #     if model_answer:
            #         model_answer = model_answer.strip().upper()
            # mathc \n\n**ANSWER: A/B/C/D**
            ma_match = re.search(r'\*\*ANSWER:\s*([A-D])', output_text, re.IGNORECASE)
            if ma_match:
                model_answer = next((g for g in ma_match.groups() if g is not None), None)
                if model_answer:
                    model_answer = model_answer.strip().upper()
            print(f"Model answer found: {model_answer}", "Ground Truth: ",ground_truth)

        if ground_truth is not None and model_answer is not None:
            if model_answer == ground_truth:
                correct_count += 1
        else:
            unparsable_model_answers += 1
            # For debugging: print the output that couldn't be parsed
            # print(f"Could not parse answer from: {item.get('Output', 'No Output field')}")


    parsable_count = total_count - unparsable_model_answers
    accuracy = (correct_count / parsable_count) * 100 if parsable_count > 0 else 0

    print(f"计算结果:")
    print(f"--------------------")
    print(f"已处理的总项目数: {total_count}")
    print(f"正确答案数: {correct_count}")
    print(f"模型答案未找到或无法解析的数量: {unparsable_model_answers}")
    print(f"准确率 (基于 {parsable_count} 个可解析的项目): {accuracy:.2f}%")

if __name__ == "__main__":
    json_file_path = '/Users/zrwang/Desktop/medqa_filtered_test.7.18,0:13.54.json'
    calculate_accuracy(json_file_path)