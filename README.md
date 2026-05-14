# Ti-NID: Tibetan Instruction-Finetuning Dataset

藏语指令微调数据集构建

## 项目简介

本项目提供了一个完整的藏语指令数据集构建流程，包括原始数据处理、指令化转换算法、以及多种测试集的生成。项目旨在为藏文自然语言处理任务提供高质量的指令数据集。

## 项目结构

```
Ti-NID/
├── data/                          # 数据目录
│   ├── raw/                       # 原始数据
│   │   ├── rawdata.txt            # 二元组原始数据（字词-释义）
│   │   └── README_QA.md           # QA数据说明文档
│   ├── processed/                 # 处理后的数据
│   │   └── instructions.json     # 转换后的指令数据集
│   ├── test_sets/                 # 测试集目录
│   │   ├── sft_test/              # SFT测试集
│   │   ├── instruction_diversity_test/  # 指令多样性增益验证测试集
│   │   ├── few_shot_test/         # 少样本学习测试集
│   │   └── multi_task_test/       # 多任务测试测试集
│   └──train/                      # 部分训练数据
│       ├── essay_generation_500.json
│       ├── explanation_generation_500.json
│       ├── news_generation_500.json
│       ├── qa_instructions_500.json
│       ├── summarization_500.json
│       ├── text_classification_test_500.json
│       └── title_generation_500.json
├── script/                        # 脚本目录
│   ├── instruction_generator.py  # 指令化转换算法
│   ├── create_qa_testset.py      # QA测试集生成脚本
│   └── process_qa.py              # QA数据处理脚本
├── README.md                      # 项目说明文档
├── requirements.txt               # Python依赖包
└── LICENSE                        # 开源许可证

```

## 数据格式

### 原始数据格式

原始数据文件 `data/raw/rawdata.txt` 采用二元组格式，每行一个词条：

```
术语-释义
```

示例：
```
གྲོས་མོལ-གྲོས་མོལ་བྱེད་པའམ་གླེང་མོལ།
བསབ་པ-གསོབ་པའི་མ་འོངས་པ།
```

### 转换后数据格式

转换后的指令数据集采用JSON格式，每条数据包含以下字段：

```json
{
  "instruction": "术语་具指连词་指令模板",
  "input": "",
  "output": "释义内容",
  "task_type": "ID_explanation"
}
```

示例：
```json
{
  "instruction": "གྲོས་མོལ་ཞེས་པའི་མིང་ཚིག་འདིར་འོས་འཚམས་ཀྱི་འགྲེལ་བཤད་གནང་རོགས།",
  "input": "",
  "output": "གྲོས་མོལ་བྱེད་པའམ་གླེང་མོལ།",
  "task_type": "1_explanation"
}
```

## 使用方法

### 环境要求

- Python 3.7+
- 依赖包见 `requirements.txt`

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行转换脚本

```bash
python script/instruction_generator.py
```

运行后会在 `data/processed/` 目录下生成 `instructions.json` 文件。

## 指令化算法说明

### 具指连词选择规则

算法根据藏文语法规则自动选择适当的具指连词（ཅེས་པའི、ཞེས་པའི）：

1. **规则1**：后加字为 ག/ད/བ 或再后加字为 ད → 使用 `ཅེས་པའི`
2. **规则2**：后加字为 ང/ན/མ/འ/ར/ལ 且没有再后加字 → 使用 `ཞེས་པའི`
3. **规则3**：后加字为 ས 或再后加字为 ས → 使用 `ཞེས་པའི`

### 指令模板

系统随机选择以下指令模板之一：

- `མིང་ཚིག་འདིའི་ནང་དོན་ཅི་ཡིན།`（这个词语的含义是什么？）
- `མིང་ཚིག་འདིར་དོན་འགྲེལ་བྱོས།`（请对这个词语进行释义。）
- `མིང་ཚིག་འདིར་འོས་འཚམས་ཀྱི་འགྲེལ་བཤད་གནང་རོགས།`（请对这个词语给出恰当的解释。）
- `ཐ་སྙད་འདིའི་གོ་དོན་ཤོད།`（说出这个术语的意思。）

## 训练集说明

### SFT训练集 (`train/`)

用于监督微调（Supervised Fine-Tuning）的基础训练数据。为方便开源社区进行模型微调与效果复现，本项目针对涵盖的 7 大核心任务类别，**每类精选并开源了 500 条高质量指令数据**（共计 3500 条）。

具体包含以下子任务文件：
- `essay_generation_500.json`：作文生成（智能生成）指令数据
- `explanation_generation_500.json`：词语释义/名词解释指令数据
- `news_generation_500.json`：新闻生成指令数据
- `qa_instructions_500.json`：常识问答/知识解答指令数据
- `summarization_500.json`：文本摘要生成指令数据
- `text_classification_test_500.json`：文本分类指令数据
- `title_generation_500.json`：文章标题生成指令数据

## 测试集说明

### SFT测试集 (`data/test_sets/sft_test/`)

用于监督微调（Supervised Fine-Tuning）的测试集，包含标准格式的指令数据。

### 指令多样性增益验证测试集 (`data/test_sets/instruction_diversity_test/`)

用于验证指令多样性对模型性能的影响，通常包含更多样本（如400条）。

### 少样本学习测试集 (`data/test_sets/few_shot_test/`)

用于少样本学习（Few-shot Learning）评估，包含少量示例数据。

### 多任务测试测试集 (`data/test_sets/multi_task_test/`)

用于多任务学习评估，包含多种任务类型的数据。

## 贡献指南

欢迎提交Issue和Pull Request来改进本项目。
