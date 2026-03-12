# 项目结构说明

## 目录结构

```
Ti-IFD/
├── data/                          # 数据目录
│   ├── raw/                       # 原始数据目录
│   │   └── rawdata.txt            # 二元组原始数据文件
│   │                               # 格式：术语-释义（每行一条）
│   └── processed/                 # 处理后的数据目录
│       └── instructions.json      # 转换后的指令数据集
│                                   # JSON格式，包含instruction、input、output、task_type字段
│
├── script/                        # 脚本目录
│   ├── instruction_generator.py   # 指令化转换算法主文件
│   │                               # 功能：将二元组数据转换为指令格式
│   ├── create_qa_testset.py       # QA测试集生成脚本
│   └── process_qa.py              # QA数据处理脚本
│
├── data/
│   └── test_sets/                 # 测试集目录
│       ├── sft_test/              # SFT（Supervised Fine-Tuning）测试集
│       │                           # 用于监督微调的测试数据
│       │
│       ├── instruction_diversity_test/  # 指令多样性增益验证测试集
│       │                               # 包含多种指令模板的测试数据
│       │                               # 用于验证指令多样性对性能的影响
│       │
│       ├── few_shot_test/         # 少样本学习测试集
│       │                           # 包含少量示例的测试数据
│       │                           # 用于评估模型的少样本学习能力
│       │
│       └── multi_task_test/       # 多任务测试测试集
│                                   # 包含多种任务类型的测试数据
│                                   # 用于评估模型的多任务学习能力
│
├── README.md                      # 项目主说明文档
├── PROJECT_STRUCTURE.md           # 项目结构说明文档（本文件）
├── requirements.txt               # Python依赖包列表
├── LICENSE                        # 开源许可证（MIT）
└── .gitignore                     # Git忽略文件配置

```

## 文件说明

### 数据文件

- **data/raw/rawdata.txt**: 原始二元组数据，格式为 `术语-释义`，每行一条记录
- **data/processed/instructions.json**: 转换后的指令数据集，JSON格式

### 代码文件

- **script/instruction_generator.py**: 指令化转换算法，包含以下主要功能：
  - 读取原始二元组数据
  - 根据藏文语法规则选择具指连词
  - 随机选择指令模板
  - 生成标准格式的指令数据
  - 输出JSON格式的处理结果

### 测试集文件

所有测试集文件均为JSON格式，包含以下字段：
- `instruction`: 指令文本
- `input`: 输入内容（通常为空字符串）
- `output`: 期望输出
- `task_type`: 任务类型（格式：ID_explanation）

## 使用流程

1. **准备原始数据**：将二元组数据放入 `data/raw/rawdata.txt`
2. **运行转换脚本**：执行 `python script/instruction_generator.py`
3. **获取结果**：处理后的数据保存在 `data/processed/instructions.json`
4. **使用测试集**：根据需求选择相应的测试集进行评估

## 注意事项

- 确保原始数据文件使用UTF-8编码
- 运行代码前确保已安装所需依赖（当前版本仅使用Python标准库）
- 测试集文件为示例文件，实际使用时需要根据具体需求调整数据量
