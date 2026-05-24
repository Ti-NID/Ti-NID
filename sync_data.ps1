# Sync dataset files from the Ti-NID GitHub repository.
# Documentation and scripts are English-only; Tibetan data files are copied as-is.

$ErrorActionPreference = "Stop"
$BaseUrl = "https://raw.githubusercontent.com/Ti-IDF/Ti-NID/main"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

$Files = @(
    "data/raw/rawdata.txt",
    "data/processed/instructions.json",
    "data/test/sft_test/3_explanation_test.json",
    "data/test/instruction_diversity_test/3_explanation_test_400.json",
    "data/test/few_shot_test/3_explanation_test.json",
    "data/test/multi_task_test/1_title_generation_test.json",
    "data/test/multi_task_test/2_essay_generation_test.json",
    "data/test/multi_task_test/3_explanation_test.json",
    "data/test/multi_task_test/3_explanation_test_400.json",
    "data/test/multi_task_test/4_news_generation_dup_test.json",
    "data/test/multi_task_test/5_summarization_test.json",
    "data/test/multi_task_test/6_text_classification_test.json",
    "data/test/multi_task_test/7_other_or_qa_test_400.json",
    "data/train/essay_generation_500.json",
    "data/train/explanation_generation_500.json",
    "data/train/news_generation_500.json",
    "data/train/qa_instructions_500.json",
    "data/train/summarization_500.json",
    "data/train/text_classification_test_500.json",
    "data/train/title_generation_500.json"
)

foreach ($rel in $Files) {
    $dest = Join-Path $Root $rel
    $dir = Split-Path $dest -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $url = "$BaseUrl/$rel"
    Write-Host "Downloading $rel ..."
    Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
}

Write-Host "Done. All dataset files synced."
