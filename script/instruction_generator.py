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
    """Return Tibetan codepoints from the string, ignoring spaces and punctuation."""
    return [ch for ch in s if ch not in {" ", "-", "།"}]


def get_tibetan_consonants(s: str) -> List[str]:
    """Return Tibetan consonant letters (suffix candidates) in the range U+0F40-U+0F69."""
    consonants = []
    for ch in s:
        code = ord(ch)
        if 0x0F40 <= code <= 0x0F69:
            consonants.append(ch)
    return consonants


def get_last_syllable_suffixes(term: str) -> tuple:
    """
    Return the syllable suffix and second suffix of the last syllable.

    Tibetan syllables are separated by tsheg (་, U+0F0B).
  """
    syllables = term.split("་")
    last_syllable = syllables[-1] if syllables else ""

    if not last_syllable:
        return (None, None)

    consonants = get_tibetan_consonants(last_syllable)
    if not consonants:
        return (None, None)

    suffix = consonants[-1]
    second_suffix = consonants[-2] if len(consonants) >= 2 else None

    return (suffix, second_suffix)


def choose_connective(term: str) -> str:
    """
    Choose the demonstrative connective based on Tibetan grammar rules.

    Rules:
    1) suffix in {ག, ད, བ} or second_suffix == ད -> ཅེས་པའི
    2) suffix in {ང, ན, མ, འ, ར, ལ} and no second_suffix -> ཞེས་པའི
    3) suffix == ས or second_suffix == ས -> ཞེས་པའི
    Default: ཞེས་པའི
    """
    suffix, second_suffix = get_last_syllable_suffixes(term)

    if suffix is None:
        return "ཞེས་པའི"

    if suffix == "ས" or second_suffix == "ས":
        return "ཞེས་པའི"

    if suffix in {"ག", "ད", "བ"} or second_suffix == "ད":
        return "ཅེས་པའི"

    if suffix in {"ང", "ན", "མ", "འ", "ར", "ལ"} and second_suffix is None:
        return "ཞེས་པའི"

    return "ཞེས་པའི"


def build_instruction(term: str) -> str:
    """Build an instruction: [term] + [connective] + [random template]."""
    connective = choose_connective(term)
    template = random.choice(INSTRUCTION_TEMPLATES)
    return f"{term}་{connective}་{template}"


def process_line(line: str) -> Optional[Dict[str, str]]:
    """
    Convert one raw bi-tuple line into an instruction sample.

    Example line:
    གྲོས་མོལ-གྲོས་མོལ་བྱེད་པའམ་གླེང་མོལ།
    """
    line = line.strip()
    if not line:
        return None

    if "-" not in line:
        return None

    term, definition = line.split("-", 1)
    term = term.strip()
    definition = definition.strip()

    if not term or not definition:
        return None

    if term.endswith("།"):
        term = term[:-1]

    instruction = build_instruction(term)

    return {
        "instruction": instruction,
        "input": "",
        "output": definition,
        "task_type": None,
    }


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    raw_path = os.path.join(project_root, "data", "raw", "rawdata.txt")
    out_path = os.path.join(project_root, "data", "processed", "instructions.json")

    samples: List[Dict[str, str]] = []

    with open(raw_path, "r", encoding="utf-8") as f:
        for line in f:
            sample = process_line(line)
            if sample is not None:
                samples.append(sample)

    for idx, sample in enumerate(samples, start=1):
        sample["task_type"] = f"{idx}_explanation"

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
