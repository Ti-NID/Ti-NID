# Project Submission Checklist

## Documentation

- [x] README.md — Main project documentation
- [x] CHECKLIST.md — Submission checklist
- [x] LICENSE — MIT open-source license
- [x] .gitignore — Git ignore configuration

## Code

- [x] script/instruction_generator.py — Bi-tuple to instruction conversion
- [x] script/create_qa_testset.py — QA test set generation
- [x] script/process_qa.py — QA data processing

## Data Files

- [x] data/raw/rawdata.txt — Raw bi-tuple data
- [x] data/raw/README_QA.md — QA data documentation
- [x] data/processed/instructions.json — Processed instruction dataset

## Test Sets

- [x] data/test/sft_test/ — SFT test set
  - [x] 3_explanation_test.json
- [x] data/test/instruction_diversity_test/ — Instruction diversity test set
  - [x] 3_explanation_test_400.json
- [x] data/test/few_shot_test/ — Few-shot test set
  - [x] 3_explanation_test.json
- [x] data/test/multi_task_test/ — Multi-task test set
  - [x] Multiple test files

## Path Consistency

- [x] README.md paths point to `script/instruction_generator.py`
- [x] Test set paths use `data/test/`
- [x] QA scripts reference `script/create_qa_testset.py`

## Code Verification

- [x] script/instruction_generator.py runs successfully
- [x] Path configuration in scripts is correct

## Pre-Submission Notes

1. **Processed data**: Ensure `data/processed/instructions.json` is up to date
2. **Test sets**: Verify test set file formats
3. **Documentation**: All path references are consistent
4. **Dependencies**: requirements.txt includes necessary notes

## Push Commands

```bash
git add .
git commit -m "docs: convert project documentation to English"
git push origin main
```
