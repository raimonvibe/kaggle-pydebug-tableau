# PyDebug Tableau Prep

Prepare and visualize the Kaggle dataset `pydebug-gold-150k-coding-fine-tuning-and-dpo-set` in Tableau Public.

## Files in this project

- `python_expert_debug_150k.csv` - source dataset
- `prepare_tableau_csv.py` - cleaning/enrichment script for Tableau
- `TABLEAU_PUBLIC_GUIDE.md` - Tableau dashboard and publishing playbook

## Quick start

Run from this folder:

```bash
python prepare_tableau_csv.py
```

This creates:

- `python_expert_debug_150k_tableau_ready.csv` (full)
- `python_expert_debug_150k_tableau_sample_20k.csv` (faster for Tableau Public)

Optional smaller sample:

```bash
python prepare_tableau_csv.py --sample-rows 10000
```

## Tableau Public workflow

1. Open Tableau Public and connect to the sample CSV first.
2. Build and test dashboards with the sample.
3. Switch the data source to the full CSV for final publishing.

See full guidance in `TABLEAU_PUBLIC_GUIDE.md`.

## Code License

This repository's code and documentation are licensed under the **MIT License**.
See `LICENSE`.

## Dataset License

The dataset `pydebug-gold-150k-coding-fine-tuning-and-dpo-set` is licensed under **CC0 (Public Domain)**.
You may copy, modify, and redistribute the dataset and derived CSV files, including on GitHub.

Source: https://www.kaggle.com/datasets/igormerlinicomposer/pydebug-gold-150k-coding-fine-tuning-and-dpo-set
