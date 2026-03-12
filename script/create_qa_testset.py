import json
import os
import csv
import io
from typing import List, Dict

def process_qa_data(csv_content: str) -> List[Dict]:
    """处理CSV数据，转换为指令格式"""
    samples = []
    
    # 使用StringIO和csv模块解析
    csv_file = io.StringIO(csv_content)
    reader = csv.DictReader(csv_file)
    
    for idx, row in enumerate(reader, start=1):
        question = row.get('question', '').strip()
        option_a = row.get('A', '').strip()
        option_b = row.get('B', '').strip()
        option_c = row.get('C', '').strip()
        option_d = row.get('D', '').strip()
        answer = row.get('answer', '').strip()
        
        if not question or not answer:
            continue
        
        # 根据答案选择对应的选项内容
        answer_map = {
            'A': option_a,
            'B': option_b,
            'C': option_c,
            'D': option_d
        }
        
        correct_answer = answer_map.get(answer, '')
        
        # 构建选项文本
        options_text = f"（A）{option_a}（B）{option_b}（C）{option_c}（D）{option_d}"
        
        # 构建指令
        instruction = f"{question} {options_text}"
        
        sample = {
            "instruction": instruction,
            "input": "",
            "output": correct_answer,
            "task_type": f"{idx}_qa"
        }
        
        samples.append(sample)
    
    return samples

def main():
    # 获取项目根目录
    code_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(code_dir)
    csv_path = os.path.join(project_root, "data", "raw", "qa_data.csv")
    
    # 读取CSV文件
    if not os.path.exists(csv_path):
        print(f"错误：找不到文件 {csv_path}")
        print("请将CSV数据保存到 data/raw/qa_data.csv")
        print("数据格式：question,A,B,C,D,answer")
        return
    
    print(f"正在读取CSV文件: {csv_path}")
    with open(csv_path, 'r', encoding='utf-8') as f:
        csv_content = f.read()
    
    # 处理数据
    samples = process_qa_data(csv_content)
    print(f"共处理 {len(samples)} 条数据")
    
    # 确保目录存在
    sft_dir = os.path.join(project_root, "test_sets", "sft_test")
    few_shot_dir = os.path.join(project_root, "test_sets", "few_shot_test")
    os.makedirs(sft_dir, exist_ok=True)
    os.makedirs(few_shot_dir, exist_ok=True)
    
    # 保存SFT测试集（前50条）
    sft_path = os.path.join(sft_dir, "qa_test.json")
    sft_samples = samples[:50] if len(samples) >= 50 else samples
    
    with open(sft_path, 'w', encoding='utf-8') as f:
        json.dump(sft_samples, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已生成 {len(sft_samples)} 条SFT测试集数据 -> {sft_path}")
    
    # 保存少样本学习测试集（前50条）
    few_shot_path = os.path.join(few_shot_dir, "qa_test.json")
    few_shot_samples = samples[:50] if len(samples) >= 50 else samples
    
    with open(few_shot_path, 'w', encoding='utf-8') as f:
        json.dump(few_shot_samples, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已生成 {len(few_shot_samples)} 条少样本学习测试集数据 -> {few_shot_path}")

if __name__ == "__main__":
    main()
