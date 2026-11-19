# Processed dataset

Folder ini berisi CSV hasil transformasi yang dibaca notebook:

- `Bitcoin.csv`
- `Ethereum.csv`
- `Solana.csv`

Kolom standar:

- `snapped_at`
- `price`
- `market_cap`
- `total_volume`

Jalankan `python src/prepare_kaggle_data.py` dari root repository untuk membuat file-file tersebut dari dataset Kaggle di `data/raw/`.
