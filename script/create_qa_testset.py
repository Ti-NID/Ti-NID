import csv
import io
import json
import os
from typing import Dict, List


def process_qa_data(csv_content: str) -> List[Dict]:
    """Convert CSV Q&A data into instruction-format samples."""
    samples = []

    csv_file = io.StringIO(csv_content)
    reader = csv.DictReader(csv_file)

    for idx, row in enumerate(reader, start=1):
        question = row.get("question", "").strip()
        option_a = row.get("A", "").strip()
        option_b = row.get("B", "").strip()
        option_c = row.get("C", "").strip()
        option_d = row.get("D", "").strip()
        answer = row.get("answer", "").strip()

        if not question or not answer:
            continue

        answer_map = {
            "A": option_a,
            "B": option_b,
            "C": option_c,
            "D": option_d,
        }

        correct_answer = answer_map.get(answer, "")
        options_text = f"（A）{option_a}（B）{option_b}（C）{option_c}（D）{option_d}"
        instruction = f"{question} {options_text}"

        sample = {
            "instruction": instruction,
            "input": "",
            "output": correct_answer,
            "task_type": f"{idx}_qa",
        }

        samples.append(sample)

    return samples


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, "data", "raw", "qa_data.csv")

    if not os.path.exists(csv_path):
        print(f"Error: file not found: {csv_path}")
        print("Save CSV data to data/raw/qa_data.csv")
        print("Expected columns: question,A,B,C,D,answer")
        return

    print(f"Reading CSV file: {csv_path}")
    with open(csv_path, "r", encoding="utf-8") as f:
        csv_content = f.read()

    samples = process_qa_data(csv_content)
    print(f"Processed {len(samples)} samples")

    sft_dir = os.path.join(project_root, "data", "test", "sft_test")
    few_shot_dir = os.path.join(project_root, "data", "test", "few_shot_test")
    os.makedirs(sft_dir, exist_ok=True)
    os.makedirs(few_shot_dir, exist_ok=True)

    sft_path = os.path.join(sft_dir, "qa_test.json")
    sft_samples = samples[:50] if len(samples) >= 50 else samples

    with open(sft_path, "w", encoding="utf-8") as f:
        json.dump(sft_samples, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(sft_samples)} SFT test samples -> {sft_path}")

    few_shot_path = os.path.join(few_shot_dir, "qa_test.json")
    few_shot_samples = samples[:50] if len(samples) >= 50 else samples

    with open(few_shot_path, "w", encoding="utf-8") as f:
        json.dump(few_shot_samples, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(few_shot_samples)} few-shot test samples -> {few_shot_path}")


if __name__ == "__main__":
    main()
