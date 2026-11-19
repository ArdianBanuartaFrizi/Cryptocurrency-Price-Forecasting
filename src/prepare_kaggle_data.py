#!/usr/bin/env python3
"""Convert Kaggle cryptocurrency CSV files into the schema used by the notebook."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


COINS = {
    "Bitcoin": "coin_Bitcoin.csv",
    "Ethereum": "coin_Ethereum.csv",
    "Solana": "coin_Solana.csv",
}


def normalize_column_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def find_column(df: pd.DataFrame, candidates: list[str], required: bool = True):
    lookup = {normalize_column_name(col): col for col in df.columns}
    for candidate in candidates:
        key = normalize_column_name(candidate)
        if key in lookup:
            return lookup[key]
    if required:
        raise ValueError(
            f"Kolom tidak ditemukan. Kandidat: {candidates}. "
            f"Kolom tersedia: {list(df.columns)}"
        )
    return None


def convert_one(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {input_path}")

    df = pd.read_csv(input_path)

    date_col = find_column(df, ["Date", "snapped_at", "timestamp"])
    price_col = find_column(df, ["Close", "price", "closing_price"])
    market_cap_col = find_column(
        df, ["Marketcap", "Market Cap", "market_cap", "marketcap_usd"], required=False
    )
    volume_col = find_column(
        df, ["Volume", "total_volume", "volume_usd"], required=False
    )

    dates = pd.to_datetime(df[date_col], errors="coerce", utc=True).dt.tz_localize(None)
    prices = pd.to_numeric(df[price_col], errors="coerce")

    market_caps = (
        pd.to_numeric(df[market_cap_col], errors="coerce")
        if market_cap_col is not None
        else pd.Series(float("nan"), index=df.index)
    )
    volumes = (
        pd.to_numeric(df[volume_col], errors="coerce")
        if volume_col is not None
        else pd.Series(float("nan"), index=df.index)
    )

    cleaned = pd.DataFrame(
        {
            "snapped_at": dates,
            "price": prices,
            "market_cap": market_caps,
            "total_volume": volumes,
        }
    )

    # A row without a valid date or closing price cannot be used as a price observation.
    cleaned = cleaned.dropna(subset=["snapped_at", "price"])
    cleaned = cleaned.sort_values("snapped_at")
    cleaned = cleaned.drop_duplicates(subset=["snapped_at"], keep="last")

    if cleaned.empty:
        raise ValueError(f"Tidak ada observasi tanggal/harga valid pada {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned["snapped_at"] = cleaned["snapped_at"].dt.strftime("%Y-%m-%d")
    cleaned.to_csv(output_path, index=False)

    print(
        f"[OK] {input_path.name} -> {output_path} "
        f"({len(cleaned):,} baris; {cleaned['snapped_at'].iloc[0]} "
        f"s.d. {cleaned['snapped_at'].iloc[-1]})"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Ubah CSV Kaggle menjadi format yang digunakan notebook."
    )
    parser.add_argument(
        "--raw-dir",
        default="data/raw",
        help="Folder CSV mentah (default: data/raw)",
    )
    parser.add_argument(
        "--processed-dir",
        default="data/processed",
        help="Folder keluaran (default: data/processed)",
    )
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    processed_dir = Path(args.processed_dir)

    missing = [filename for filename in COINS.values() if not (raw_dir / filename).exists()]
    if missing:
        expected = "\n".join(f"  - {raw_dir / name}" for name in missing)
        raise SystemExit(
            "File dataset belum lengkap. Letakkan file berikut di folder data/raw:\n"
            f"{expected}\n\n"
            "Unduh dan ekstrak dataset dari Kaggle terlebih dahulu."
        )

    for coin, filename in COINS.items():
        convert_one(raw_dir / filename, processed_dir / f"{coin}.csv")

    print("\nSelesai. Notebook dapat membaca file dari data/processed/.")


if __name__ == "__main__":
    main()
