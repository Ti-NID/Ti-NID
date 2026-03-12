# QA数据文件说明

请将完整的CSV格式问答数据保存为 `qa_data.csv` 文件。

## 数据格式

CSV文件应包含以下列：
- question: 问题
- A: 选项A
- B: 选项B  
- C: 选项C
- D: 选项D
- answer: 正确答案（A、B、C或D）

## 示例

```csv
question,A,B,C,D,answer
问题1,选项A1,选项B1,选项C1,选项D1,A
问题2,选项A2,选项B2,选项C2,选项D2,B
```

## 使用方法

1. 将CSV数据保存到 `data/raw/qa_data.csv`
2. 运行处理脚本：`python code/create_qa_testset.py`
3. 生成的测试集将保存在 `test_sets/sft_test/qa_test.json` 和 `test_sets/few_shot_test/qa_test.json`
