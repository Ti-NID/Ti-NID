# TI-NID: GRAMMAR-AWARE NATIVE INSTRUCTION CONSTRUCTION FOR TIBETAN---A REPRODUCIBLE SIMULATION STUDY

## Overview

This project provides a complete pipeline for constructing Tibetan instruction datasets. It releases a subset of native Tibetan instruction data, including:

- Native bi-tuple construction
- Normalized rules for attaching demonstrative connectives
- Bi-tuple-to-instruction formatting algorithms
- Multiple instruction test sets

The goal is to provide high-quality instruction data for Tibetan natural language processing tasks.

## Project Structure

```
Ti-NID/
├── data/                              # Data directory
│   ├── raw/                           # Raw data
│   │   ├── rawdata.txt                # Native bi-tuple data (term-definition)
│   │   └── README_QA.md               # QA data documentation
│   ├── processed/                     # Processed data
│   │   └── instructions.json          # Converted instruction dataset
│   ├── test/                          # Test sets
│   │   ├── sft_test/                  # SFT test set
│   │   ├── instruction_diversity_test/  # Instruction diversity evaluation set
│   │   ├── few_shot_test/             # Few-shot learning test set
│   │   └── multi_task_test/           # Multi-task evaluation set
│   └── train/                         # Sample training data
│       ├── essay_generation_500.json
│       ├── explanation_generation_500.json
│       ├── news_generation_500.json
│       ├── qa_instructions_500.json
│       ├── summarization_500.json
│       └── title_generation_500.json
├── script/                            # Scripts
│   ├── instruction_generator.py       # Bi-tuple to instruction conversion
│   ├── create_qa_testset.py           # QA test set generation
│   └── process_qa.py                  # QA data processing
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
└── LICENSE                            # Open-source license
```

## Data Format

### Raw Data Format

The raw file `data/raw/rawdata.txt` uses a bi-tuple format with one entry per line:

```
term-definition
```

Example:

```
གྲོས་མོལ-གྲོས་མོལ་བྱེད་པའམ་གླེང་མོལ།
བསབ་པ-གསོབ་པའི་མ་འོངས་པ།
```

### Converted Instruction Format

The converted dataset is stored in JSON. Each record contains:

```json
{
  "instruction": "term + connective + instruction template",
  "input": "",
  "output": "definition content",
  "task_type": "ID_explanation"
}
```

Example:

```json
{
  "instruction": "གྲོས་མོལ་ཞེས་པའི་མིང་ཚིག་འདིར་འོས་འཚམས་ཀྱི་འགྲེལ་བཤད་གནང་རོགས།",
  "input": "",
  "output": "གྲོས་མོལ་བྱེད་པའམ་གླེང་མོལ།",
  "task_type": "1_explanation"
}
```

## Usage

### Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Conversion Script

```bash
python script/instruction_generator.py
```

This generates `data/processed/instructions.json`.

## Instruction Formatting Algorithm

### Demonstrative Connective Selection Rules

The algorithm selects the appropriate demonstrative connective (`ཅེས་པའི` or `ཞེས་པའི`) according to Tibetan grammar:

1. **Rule 1**: If the syllable suffix is ག/ད/བ, or the second suffix is ད → use `ཅེས་པའི`
2. **Rule 2**: If the syllable suffix is ང/ན/མ/འ/ར/ལ and there is no second suffix → use `ཞེས་པའི`
3. **Rule 3**: If the syllable suffix is ས, or the second suffix is ས → use `ཞེས་པའི`

### Instruction Templates

The system randomly selects one of the following Tibetan instruction templates:

- `མིང་ཚིག་འདིའི་ནང་དོན་ཅི་ཡིན།` — What is the meaning of this word?
- `མིང་ཚིག་འདིར་དོན་འགྲེལ་བྱོས།` — Please define this word.
- `མིང་ཚིག་འདིར་འོས་འཚམས་ཀྱི་འགྲེལ་བཤད་གནང་རོགས།` — Please provide an appropriate explanation for this word.
- `ཐ་སྙད་འདིའི་གོ་དོན་ཤོད།` — State the meaning of this term.

## Training Data

### SFT Training Set (`data/train/`)

Supervised fine-tuning (SFT) sample data. To support community fine-tuning and reproducibility, this repository releases **500 high-quality instruction samples per task type** across 7 core task categories (3,500 samples in total).

Included files:

- `essay_generation_500.json` — Essay generation
- `explanation_generation_500.json` — Word/term definition
- `news_generation_500.json` — News generation
- `qa_instructions_500.json` — Knowledge QA
- `summarization_500.json` — Text summarization
- `title_generation_500.json` — Title generation

## Test Sets

### SFT Test Set (`data/test/sft_test/`)

Standard instruction-format data for supervised fine-tuning evaluation.

### Instruction Diversity Test Set (`data/test/instruction_diversity_test/`)

Used to evaluate the impact of instruction diversity on model performance (typically ~400 samples).

### Few-Shot Test Set (`data/test/few_shot_test/`)

Used for few-shot learning evaluation with a small number of examples.

### Multi-Task Test Set (`data/test/multi_task_test/`)

Used for multi-task evaluation across several task types.

## Contributing

Issues and pull requests are welcome.

## Citation

If you use Ti-NID in your research, please cite this repository:

```bibtex
@misc{ti-nid2025,
  title={Ti-NID: A Tibetan Instruction Dataset Based on Native Bi-tuples and Grammatical Constraints},
  author={},
  year={2025},
  url={https://github.com/Ti-IDF/Ti-NID}
}
```

## License

See [LICENSE](LICENSE) for details.
