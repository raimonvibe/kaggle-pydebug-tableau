# 📊 Tableau Public Guide for pydebug-gold 150k 🚀
This guide helps you get strong dashboards quickly from the Kaggle dataset:
`pydebug-gold-150k-coding-fine-tuning-and-dpo-set`. 🧠

## 🪪 Dataset License

The dataset `pydebug-gold-150k-coding-fine-tuning-and-dpo-set` is licensed under **CC0 (Public Domain)**. ✅
You may copy, modify, and redistribute the dataset and derived CSV files (including on GitHub). 🌍

Source: https://www.kaggle.com/datasets/igormerlinicomposer/pydebug-gold-150k-coding-fine-tuning-and-dpo-set 🔗

## 1) 🛠️ Prepare the CSV (important)

Run: ▶️

```bash
python prepare_tableau_csv.py
```

This generates: 📦
- `python_expert_debug_150k_tableau_ready.csv` (full dataset) 🧾
- `python_expert_debug_150k_tableau_sample_20k.csv` (faster for Tableau Public) ⚡

If Tableau Public is slow, start with sample data: 🐢➡️🐇

```bash
python prepare_tableau_csv.py --sample-rows 10000
```

## 2) 🔌 Connect in Tableau Public

1. Open Tableau Public -> **Text file** 🗂️
2. Select `python_expert_debug_150k_tableau_sample_20k.csv` first 🎯
3. Confirm data types: 🧮
   - `Complexity` -> Number (Whole) 🔢
   - `Instruction_Words`, `Response_Words`, `Rejected_Words` -> Number (Whole) 📏
   - `Has_Rejected_Response` -> Boolean (or String if Tableau infers text) 🧷
4. Go to a worksheet 📄

## 3) 🧠 Recommended calculated fields

Create these calculated fields in Tableau: ✍️

### A) 📉 Response Quality Gap
```tableau
[Response_Words] - [Rejected_Words]
```

### B) 📊 Avg Words per Complexity
```tableau
AVG([Response_Words])
```

### C) 🧩 Distinct Errors
```tableau
COUNTD([System_Error])
```

### D) 🧾 Record Count
```tableau
COUNT([Instruction])
```

## 4) 🎨 Best first dashboards

## Dashboard 1: 🌋 Error Landscape
- **Rows**: `System_Error` 🧱
- **Columns**: `COUNT([Instruction])` 📐
- **Color**: `Environment` 🌈
- **Sort** descending by count 🔽

Use this to see which errors are most common and where. 🧭

## Dashboard 2: 🧮 Complexity Distribution
- **Columns**: `Complexity_Bucket` 🪣
- **Rows**: `COUNT([Instruction])` 🔢
- **Color**: `Category` 🎭
- Optional filter: `Environment` 🧪

Use this for distribution and audience-facing summary. 👥

## Dashboard 3: ⚖️ Response vs Rejected Length
- **Columns**: `AVG([Rejected_Words])` ⬅️
- **Rows**: `AVG([Response_Words])` ⬆️
- **Detail**: `Category` 🏷️
- **Color**: `Complexity_Bucket` 🎨
- **Filter**: `Environment`, `System_Error` 🔍

Use this to compare accepted/rejected verbosity patterns. 🧵

## Dashboard 4: 🧠 Category Performance Matrix
- **Rows**: `Category` 📚
- **Columns**: `AVG([Response_Minus_Rejected_Words])` ➗
- **Color**: `AVG([Complexity])` 🌡️
- **Label**: `COUNT([Instruction])` 🏷️

Use this to identify categories with richer final responses. 💡

## 5) 🕹️ Interactivity that makes dashboards better

Add these filters and set to **Apply to all worksheets**: 🧰
- `Environment` 🌍
- `Category` 🗃️
- `Complexity_Bucket` 📊
- `System_Error` 🚨

Add dashboard actions: 🎬
- **Filter action** from bar charts to detail tables 🎯
- **Highlight action** by `Category` ✨

## 6) 🗣️ Data storytelling tips for Tableau Public

- Start with one KPI strip at top: 🧱
  - Total Records 📌
  - Distinct Categories 🧭
  - Distinct Errors 🚩
  - Avg Complexity 📈
- Keep only 3-5 colors in your palette 🎨
- Use short titles that answer a question: ❓
  - "Which errors dominate by environment?" 🌐
  - "Do higher complexity prompts produce longer responses?" 📏
- Add a final "How to read this" text box for public viewers 📝

## 7) ⚡ Performance and publish tips

- Build using the 10k/20k sample first, then switch to full CSV 🚦
- Hide unused fields in Tableau Data pane 🧹
- Prefer extracts and avoid very large text tables on one sheet 🪶
- Use dashboard size **Automatic** or a common web size (e.g., 1200x800) 🖥️
- Before publish: check tooltips, filters, mobile layout, and title clarity ✅

## 8) 🧱 Suggested final Tableau Public project structure

- **Sheet 1**: KPI Summary 🧾
- **Sheet 2**: Error Landscape 🌋
- **Sheet 3**: Complexity Distribution 📊
- **Sheet 4**: Response vs Rejected Length ⚖️
- **Sheet 5**: Category Matrix 🧠
- **Dashboard**: Combine all with global filters 🧭

This structure gives a clean narrative: volume -> error patterns -> quality/complexity relationships. 🧬
