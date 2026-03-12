import json
import os
import random
from typing import List, Dict, Optional


INSTRUCTION_TEMPLATES = [
    "མིང་ཚིག་འདིའི་ནང་དོན་ཅི་ཡིན།",
    "མིང་ཚིག་འདིར་དོན་འགྲེལ་བྱོས།",
    "མིང་ཚིག་འདིར་འོས་འཚམས་ཀྱི་འགྲེལ་བཤད་གནང་རོགས།",
    "ཐ་སྙད་འདིའི་གོ་དོན་ཤོད།",
]


def get_tibetan_letters(s: str) -> List[str]:
    """Return a list of Tibetan 'letters' (single codepoints) from the string, ignoring spaces and punctuation."""
    # This is a simple heuristic: we just keep non‑space chars and drop ASCII hyphen etc.
    return [ch for ch in s if ch not in {" ", "-", "།"}]


def get_tibetan_consonants(s: str) -> List[str]:
    """
    Return a list of Tibetan consonant letters (后加字) from the string.
    Tibetan consonants are in the range U+0F40-U+0F69.
    """
    # Tibetan consonant range: U+0F40 to U+0F69
    consonants = []
    for ch in s:
        code = ord(ch)
        # Tibetan consonants: ཀ (U+0F40) to ཀྵ (U+0F69)
        if 0x0F40 <= code <= 0x0F69:
            consonants.append(ch)
    return consonants


def get_last_syllable_suffixes(term: str) -> tuple:
    """
    获取最后一个音节的后加字和再后加字。
    在藏文中，音节通常以 ་（tsheg，U+0F0B）分隔。
    
    返回: (后加字, 再后加字)
    后加字是最后一个音节的最后一个辅音
    再后加字是最后一个音节的倒数第二个辅音（如果存在）
    """
    # 按 tsheg 分隔音节，获取最后一个音节
    syllables = term.split("་")
    last_syllable = syllables[-1] if syllables else ""
    
    if not last_syllable:
        return (None, None)
    
    # 获取最后一个音节中的所有辅音
    consonants = get_tibetan_consonants(last_syllable)
    if not consonants:
        return (None, None)
    
    # 后加字：最后一个辅音
    suffix = consonants[-1]
    # 再后加字：倒数第二个辅音（如果存在）
    second_suffix = consonants[-2] if len(consonants) >= 2 else None
    
    return (suffix, second_suffix)


def choose_connective(term: str) -> str:
    """
    Choose the proper 具指连词 according to the given rules,
    based on the last syllable's suffix (后加字) and second suffix (再后加字).

    规则:
      1) 后加字 in {ག, ད, བ} 或 再后加字 == ད  -> ཅེས
      2) 后加字 in {ང, ན, མ, འ, ར, ལ} 且 再后加字无 -> ཞེས
      3) 后加字 == ས 或 再后加字 == ས -> ཞེས
    其它情况默认用 ཞེས 。
    """
    # 获取最后一个音节的后加字和再后加字
    suffix, second_suffix = get_last_syllable_suffixes(term)
    
    if suffix is None:
        # 没有可分析的后加字，直接用 ཞེས
        return "ཞེས་པའི"

    # 规则3：后加字 == ས 或 再后加字 == ས -> ཞེས（优先检查规则3）
    if suffix == "ས" or second_suffix == "ས":
        return "ཞེས་པའི"

    # 规则1：后加字 in {ག, ད, བ} 或 再后加字 == ད -> ཅེས
    if suffix in {"ག", "ད", "བ"} or second_suffix == "ད":
        return "ཅེས་པའི"

    # 规则2：后加字 in {ང, ན, མ, འ, ར, ལ} 且 再后加字无 -> ཞེས
    if suffix in {"ང", "ན", "མ", "འ", "ར", "ལ"} and second_suffix is None:
        return "ཞེས་པའི"

    # 兜底：其他情况默认用 ཞེས
    return "ཞེས་པའི"


def build_instruction(term: str) -> str:
    """
    为给定的术语构建一条指令：
      [术语]་[具指连词]་[随机指令模板]
    """
    connective = choose_connective(term)
    template = random.choice(INSTRUCTION_TEMPLATES)
    # 在术语和具指连词之间、具指连词和指令模板之间添加 ་（tsheg），不保留空格
    return f"{term}་{connective}་{template}"


def process_line(line: str) -> Optional[Dict[str, str]]:
    """
    将原始的一行二元组数据转成一条指令样本。
    行格式示例：
      གྲོས་མོལ-གྲོས་མོལ་བྱེད་པའམ་གླེང་མོལ།
    """
    line = line.strip()
    if not line:
        return None

    # 只按第一个 '-' 切分
    if "-" not in line:
        # 不符合二元组格式时跳过
        return None

    term, definition = line.split("-", 1)
    term = term.strip()
    definition = definition.strip()

    if not term or not definition:
        return None

    # 去掉术语结尾的 །
    if term.endswith("།"):
        term = term[:-1]

    instruction = build_instruction(term)

    return {
        "instruction": instruction,
        "input": "",
        "output": definition,
        "task_type": None,  # 将在 main 函数中根据索引设置
    }


def main() -> None:
    # 获取项目根目录（script目录的父目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # 设置输入和输出路径
    raw_path = os.path.join(project_root, "data", "raw", "rawdata.txt")
    out_path = os.path.join(project_root, "data", "processed", "instructions.json")

    samples: List[Dict[str, str]] = []

    with open(raw_path, "r", encoding="utf-8") as f:
        for line in f:
            sample = process_line(line)
            if sample is not None:
                samples.append(sample)

    # 为每条数据设置 task_type 为 ID_explanation 格式（ID 从 1 开始）
    for idx, sample in enumerate(samples, start=1):
        sample["task_type"] = f"{idx}_explanation"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

