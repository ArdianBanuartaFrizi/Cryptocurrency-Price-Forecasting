# Cryptocurrency Price Forecasting — BTC, ETH, dan SOL

Project analisis deret waktu (*time series analysis*) untuk mempelajari pola harga historis dan membandingkan hasil peramalan tiga aset cryptocurrency: **Bitcoin (BTC), Ethereum (ETH), dan Solana (SOL)**.

Project ini menggunakan Python dan dua metode utama, yaitu **SARIMA** dan **Holt-Winters Exponential Smoothing**. Analisis dilakukan pada data harian, bulanan, dan tahunan.

> **Penting:** Repository ini mendokumentasikan dan menata ulang notebook analisis yang diberikan. Sebelum menggunakan angka evaluasi sebagai bukti performa model, baca bagian [Catatan Validasi Metodologi](#catatan-validasi-metodologi) dan `docs/TECHNICAL_REVIEW.md`. Metrik pada notebook awal belum seluruhnya merupakan evaluasi out-of-sample yang valid.

## Tujuan Project

1. Mengamati perkembangan harga BTC, ETH, dan SOL berdasarkan data historis.
2. Melakukan eksplorasi pola dan karakteristik data time series.
3. Menerapkan SARIMA dan Holt-Winters untuk peramalan harga.
4. Membandingkan proyeksi dari kedua metode pada tiga skala waktu.
5. Menyajikan hasil analisis melalui grafik dan metrik evaluasi.

## Cryptocurrency yang Dianalisis

| Aset | Simbol | Fokus analisis |
|---|---|---|
| Bitcoin | BTC | Harga historis dan proyeksi harga |
| Ethereum | ETH | Harga historis dan proyeksi harga |
| Solana | SOL | Harga historis dan proyeksi harga |

## Sumber Dataset

Dataset yang dicantumkan pada project awal:

**Cryptocurrency Historical Prices — Kaggle**  
https://www.kaggle.com/datasets/sudalairajkumar/cryptocurrencypricehistory

Dataset perlu diunduh secara manual dari Kaggle. File mentah tidak disertakan di repository ini agar repository tetap ringan dan pengguna dapat mengikuti ketentuan distribusi dataset dari sumber aslinya.

### Catatan kesesuaian format data

Notebook awal menggunakan empat kolom berikut:

- `snapped_at`: tanggal observasi
- `price`: harga cryptocurrency
- `market_cap`: kapitalisasi pasar
- `total_volume`: volume perdagangan

Sementara file CSV Kaggle yang umum didistribusikan menggunakan kolom seperti `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, dan `Marketcap`. Karena itu, repository ini menyediakan script untuk mengubah file Kaggle menjadi format yang diharapkan notebook.

**Ada perbedaan provenance yang perlu dikonfirmasi:** output yang tersimpan di notebook awal menunjukkan data BTC, ETH, dan SOL sampai 10 Desember 2025. Rentang tersebut tidak otomatis dapat direproduksi hanya dengan file Kaggle versi historis yang lebih lama. Pastikan file yang digunakan dalam analisis awal memang berasal dari dataset yang dicantumkan atau merupakan data yang telah diperbarui/ditransformasi dari sumber lain.

## Bagaimana Project Ini Bekerja?

Alur analisis pada notebook:

1. **Data acquisition** — membaca CSV Bitcoin, Ethereum, dan Solana.
2. **Preprocessing** — memeriksa tipe data, missing values, mengubah kolom tanggal, dan memilih harga sebagai variabel utama.
3. **Exploratory Data Analysis (EDA)** — melihat tren harga, moving average, decomposition, correlation matrix, serta uji stasioneritas ADF dan grafik ACF/PACF.
4. **Modeling** — menerapkan SARIMA dan Holt-Winters.
5. **Forecasting** — membuat proyeksi pada skala harian, bulanan, dan tahunan.
6. **Evaluation and visualization** — membandingkan hasil model menggunakan MAE, RMSE, dan MAPE serta menampilkan grafik hasil peramalan.

### Metode yang digunakan

**SARIMA (Seasonal Autoregressive Integrated Moving Average)**

SARIMA merupakan metode peramalan deret waktu yang menggabungkan komponen autoregressive, differencing, moving average, dan komponen musiman. Metode ini digunakan untuk menangkap pola historis dan pola musiman pada harga.

**Holt-Winters Exponential Smoothing**

Holt-Winters menggunakan pemulusan eksponensial dengan komponen level, tren, dan musiman. Dalam notebook awal, model menggunakan tren aditif dan konfigurasi musiman yang disesuaikan menurut interval data.

### Periode forecasting pada notebook awal

| Interval data | Horizon proyeksi |
|---|---:|
| Harian | 12 hari ke depan |
| Bulanan | 6 bulan ke depan |
| Tahunan | 3 tahun ke depan |

### Metrik evaluasi

| Metrik | Kegunaan |
|---|---|
| MAE | Rata-rata nilai absolut selisih prediksi dan aktual |
| RMSE | Akar rata-rata kuadrat kesalahan; lebih sensitif terhadap error besar |
| MAPE | Rata-rata persentase kesalahan absolut |

## Struktur Repository

```text
cryptocurrency-price-forecasting/
├── README.md
├── requirements.txt
├── requirements-optional.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── README.md
│   └── processed/
│       └── README.md
│
├── notebooks/
│   ├── 01_crypto_price_forecasting.ipynb
│   └── archive/
│       └── projectstatistik_btc_original.ipynb
│
├── src/
│   └── prepare_kaggle_data.py
│
├── docs/
│   └── TECHNICAL_REVIEW.md
│
└── outputs/
    ├── figures/
    └── tables/
```

## Cara Menjalankan Project

### 1. Clone repository

```bash
git clone https://github.com/USERNAME/cryptocurrency-price-forecasting.git
cd cryptocurrency-price-forecasting
```

Ganti `USERNAME` dengan username GitHub pemilik repository.

### 2. Buat virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Unduh dataset dari Kaggle

Unduh dan ekstrak dataset, kemudian tempatkan tiga file berikut di `data/raw/`:

```text
data/raw/
├── coin_Bitcoin.csv
├── coin_Ethereum.csv
└── coin_Solana.csv
```

Nama file harus sesuai. Jika nama file berbeda, sesuaikan nama file atau parameter script.

### 5. Transformasi dataset

Jalankan dari root repository:

```bash
python src/prepare_kaggle_data.py
```

Script akan menghasilkan:

```text
data/processed/
├── Bitcoin.csv
├── Ethereum.csv
└── Solana.csv
```

Kolom hasil transformasi mengikuti format yang dibutuhkan notebook: `snapped_at`, `price`, `market_cap`, dan `total_volume`.

### 6. Jalankan notebook

```bash
jupyter notebook
```

Buka `notebooks/01_crypto_price_forecasting.ipynb`, kemudian jalankan cell secara berurutan.

Jika ingin menjalankan bagian Prophet opsional, install dependensinya:

```bash
pip install -r requirements-optional.txt
```

## Catatan Validasi Metodologi

Notebook awal masih memerlukan beberapa perbaikan sebelum hasilnya dapat dijadikan kesimpulan ilmiah atau klaim performa model:

1. **Evaluasi belum menggunakan pasangan periode aktual-prediksi yang tepat.** Pada bagian forecasting utama, prediksi periode mendatang dibandingkan dengan nilai aktual periode historis terakhir. Evaluasi seharusnya menggunakan chronological holdout atau rolling-origin backtesting.
2. **Konfigurasi musiman SARIMA masih disamaratakan.** Parameter musiman 12 digunakan untuk data harian, bulanan, dan tahunan, padahal makna 12 observasi berbeda pada setiap frekuensi.
3. **Data tahunan relatif terbatas.** SARIMA musiman dengan periode 12 pada data tahunan membutuhkan observasi yang jauh lebih banyak daripada yang tersedia pada data awal.
4. **Penanganan missing values perlu ditinjau.** Mengganti harga yang hilang dengan angka 1 dapat menciptakan observasi harga artifisial. Variabel hasil pengisian pada notebook awal juga belum digunakan secara konsisten.
5. **Beberapa nama variabel grafik tidak konsisten.** Jalankan notebook dari kernel bersih dan periksa kembali seluruh cell agar tidak bergantung pada variabel dari sesi sebelumnya.
6. **Sumber dan rentang data perlu dikonfirmasi.** Output notebook mencapai Desember 2025, sedangkan format dan cakupan file Kaggle yang dicantumkan perlu dicocokkan dengan file yang benar-benar digunakan.

Rincian temuan dan rekomendasi perbaikannya tersedia di `docs/TECHNICAL_REVIEW.md`.

## Batasan Interpretasi

- Harga cryptocurrency sangat volatil dan dipengaruhi banyak faktor eksternal yang tidak dimodelkan dalam notebook ini.
- SARIMA dan Holt-Winters hanya menggunakan pola historis harga; keduanya tidak memasukkan sentimen pasar, kebijakan, berita, atau indikator makroekonomi.
- Prediksi merupakan hasil model statistik, bukan jaminan harga aktual.
- Project ini dibuat untuk tujuan pembelajaran dan analisis data, bukan rekomendasi investasi.

## Teknologi

- Python
- Pandas dan NumPy
- Matplotlib, Seaborn, dan Plotly
- Statsmodels
- Scikit-learn
- Jupyter Notebook

---

**Project focus:** Time Series Analysis · Statistical Forecasting · Cryptocurrency · Python · Data Visualization
