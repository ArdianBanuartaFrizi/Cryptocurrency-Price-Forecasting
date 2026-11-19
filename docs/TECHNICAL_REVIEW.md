# Technical Review — Cryptocurrency Price Forecasting

Dokumen ini merangkum pemeriksaan terhadap notebook awal `projectstatistik_btc.ipynb`. Tujuannya menjaga dokumentasi repository tetap jujur terhadap kondisi kode dan hasil yang tersimpan.

## 1. Kesesuaian sumber data

Notebook membaca file `Bitcoin.csv`, `Ethereum.csv`, dan `Solana.csv` dengan kolom:

- `snapped_at`
- `price`
- `market_cap`
- `total_volume`

Output notebook menunjukkan rentang:
- BTC: 28 April 2013–10 Desember 2025 (4.608 baris).
- ETH: 7 Agustus 2015–10 Desember 2025 (3.778 baris).
- SOL: 11 April 2020–10 Desember 2025 (2.070 baris).

Dataset Kaggle yang dicantumkan umumnya disajikan sebagai CSV historis per koin dengan kolom OHLCV dan market capitalization. File sumber tersebut perlu ditransformasikan agar sesuai dengan schema notebook. Rentang sampai Desember 2025 pada output notebook juga perlu ditelusuri: jangan menganggap hasil tersebut berasal dari file Kaggle yang sama tanpa memeriksa file mentah dan versi dataset.

## 2. Masalah evaluasi forecasting utama

Pada fungsi SARIMA, model dipasang pada seluruh seri data dan kemudian menghasilkan nilai in-sample serta forecast ke depan. Bagian akhir forecast kemudian dibandingkan dengan enam atau dua belas nilai aktual terakhir. Pada Holt-Winters, model juga dipasang pada seluruh seri, lalu forecast masa depan dibandingkan dengan nilai historis terakhir.

Perbandingan ini tidak memasangkan prediksi dengan nilai aktual pada tanggal yang sama. Oleh karena itu, MAE, RMSE, dan MAPE dari bagian forecasting utama tidak boleh dipresentasikan sebagai ukuran akurasi out-of-sample yang valid.

### Rancangan evaluasi yang disarankan

1. Urutkan data berdasarkan tanggal.
2. Tentukan horizon uji sesuai frekuensi (misalnya 12 hari, 6 bulan, atau 3 tahun).
3. Pisahkan data secara kronologis menjadi training dan testing.
4. Fit model hanya pada training set.
5. Forecast sepanjang horizon testing.
6. Bandingkan prediksi dan aktual pada tanggal yang sama.
7. Hitung MAE, RMSE, dan MAPE dari pasangan tersebut.
8. Setelah evaluasi, fit ulang model terpilih pada seluruh data untuk membuat forecast masa depan.
9. Untuk hasil yang lebih kuat, gunakan rolling-origin backtesting dan bandingkan dengan baseline naïve.

## 3. Konfigurasi SARIMA

Fungsi `sarima_forecast()` menggunakan seasonal order `(1, 1, 1, 12)` pada semua frekuensi. Parameter musiman 12 berarti:

- Data harian: pola 12 hari.
- Data bulanan: pola 12 bulan.
- Data tahunan: pola 12 tahun.

Satu nilai parameter tidak otomatis sesuai untuk ketiga frekuensi. Selain itu, data tahunan pada notebook hanya memiliki sekitar belasan observasi, sehingga seasonal period 12 tidak didukung oleh panjang seri yang memadai. Warning statsmodels tentang terlalu sedikit observasi juga muncul pada hasil yang tersimpan.

Rekomendasi:
- Tentukan periode musiman berdasarkan karakteristik data dan bukti EDA.
- Untuk data harian, evaluasi pola mingguan (7) atau pola lain yang didukung data.
- Untuk data bulanan, periode 12 dapat diuji untuk pola tahunan.
- Untuk data tahunan yang pendek, pertimbangkan model non-musiman dan nyatakan keterbatasan sampel.

## 4. Penanganan missing values

Notebook membuat salinan dataset dengan `fillna(1)`. Mengganti harga yang hilang menjadi 1 bukan imputasi yang netral karena dapat menghasilkan lonjakan atau penurunan artifisial. Selain itu, salinan yang sudah diisi tidak digunakan secara konsisten pada langkah berikutnya.

Rekomendasi:
- Periksa missing values pada kolom tanggal dan harga.
- Jangan mengganti missing price dengan angka arbitrer.
- Tentukan apakah baris perlu dihapus, diinterpolasi, atau dipertahankan sebagai missing berdasarkan penyebab dan frekuensi data.
- Dokumentasikan setiap keputusan imputasi.

## 5. Konsistensi kode dan reproducibility

Notebook awal menggunakan Google Colab Drive dan lokasi folder khusus. Salinan kerja repository mengganti bagian pembacaan file agar memakai `data/processed/`, tetapi beberapa bagian analisis masih berasal dari notebook awal.

Temuan tambahan:
- Ada label “weekly” atau “weeks” pada bagian yang sebenarnya menggunakan observasi harian.
- Parameter `freq` pada fungsi SARIMA tidak digunakan untuk menentukan konfigurasi model.
- Sejumlah cell grafik merujuk pada nama variabel prediksi yang tidak konsisten dengan nama variabel yang dibuat pada cell sebelumnya. Kernel lama mungkin menyimpan variabel dari eksekusi sebelumnya sehingga masalah tidak selalu tampak.
- Beberapa grafik dan evaluasi perlu dijalankan ulang dari kernel bersih.

## 6. Prioritas perbaikan

| Prioritas | Perbaikan | Alasan |
|---|---|---|
| 1 | Konfirmasi file sumber dan rentang tanggal | Menjamin provenance data |
| 2 | Perbaiki chronological holdout | Menghasilkan metrik evaluasi yang valid |
| 3 | Atur seasonal period per frekuensi | Menghindari spesifikasi musiman yang tidak sesuai |
| 4 | Benahi missing-value handling | Menghindari harga artifisial |
| 5 | Rapikan variabel dan grafik | Menjamin notebook berjalan dari kernel bersih |
| 6 | Tambahkan rolling-origin backtesting | Menguji kestabilan performa model |

## Kesimpulan audit

Project sudah memiliki kerangka analisis yang jelas: EDA, pengujian karakteristik time series, penerapan SARIMA dan Holt-Winters, serta visualisasi hasil. Namun, hasil evaluasi forecasting utama belum dapat dianggap valid sebelum pemisahan training-testing dan kesesuaian tanggal aktual-prediksi diperbaiki. Dokumentasi repository sengaja menyatakan keterbatasan ini agar pembaca tidak salah menafsirkan hasil.
