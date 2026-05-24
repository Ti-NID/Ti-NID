# QA Data File Guide

Save your complete CSV-format Q&A data as `qa_data.csv`.

## Format

The CSV file must include the following columns:

- `question` — Question text
- `A` — Option A
- `B` — Option B
- `C` — Option C
- `D` — Option D
- `answer` — Correct answer (`A`, `B`, `C`, or `D`)

## Example

```csv
question,A,B,C,D,answer
Question 1,Option A1,Option B1,Option C1,Option D1,A
Question 2,Option A2,Option B2,Option C2,Option D2,B
```

## Usage

1. Save the CSV file to `data/raw/qa_data.csv`
2. Run the processing script: `python script/create_qa_testset.py`
3. Generated test sets are saved to:
   - `data/test/sft_test/qa_test.json`
   - `data/test/few_shot_test/qa_test.json`
