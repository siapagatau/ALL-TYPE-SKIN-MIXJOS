# Prompt: Buat Skin Mixer Lebih Mirip Foto Asli

> **v3.0 LANDSCAPE**: viewBox kini **1600 x 1000**. Tata letak tetap sama dengan foto, tetapi kotak/plat/panel/garis diregangkan ke samping (SX), sedangkan benda bulat (kenop, jack, sekrup, RCA, logo) memakai skala seragam SR sehingga tetap bulat. Konversi di bagian 2 di bawah berlaku untuk versi portrait lama; untuk v3 pakai fungsi X()/Y()/LX()/LY()/LR() di generator.

Salin semua isi di bawah garis ke AI (Claude), lalu lampirkan: **foto referensi**, **zip ALL-TYPE-SKIN-MIXJOS terbaru**, dan (kalau ada) screenshot hasil render skin saat ini.

---

Kamu adalah desainer skin SVG presisi tinggi. Tugasmu: perbaiki skin **Yamaha MG12XUK** (`tools/gen_skin_01.py`) supaya **ukuran, bentuk, proporsi, posisi, dan warna** sedekat mungkin dengan foto referensi yang saya lampirkan. Jangan merombak fungsi, hanya tampilan.

## 1. Aturan wajib (jangan dilanggar)
1. Hasil akhir harus lolos `python3 tools/validate.py skins/skin-01` dengan **0 ERROR**. Usahakan 0 WARN juga.
2. Jangan ubah id kontrol, isi `mapping`, `indicators`, dan struktur `skin.json`. Semua 25 kontrol dan 14 LED harus tetap ada.
3. Dilarang di SVG: `script`, `foreignObject`, `image`, `use`, `audio`, `video`, `iframe`, atribut `on*`, `href`, dan URL `http(s)://`. Hindari `filter` dan `mask` (tidak dirender).
4. Id hanya huruf kecil, angka, dan tanda hubung. Tidak boleh ada id ganda.
5. Grup knob `knob-*` wajib punya `data-cx`, `data-cy`, `data-angle-min`, `data-angle-max`, `data-value-default`. **Lingkaran pertama** di dalam grup adalah badan knob (dipakai validator untuk radius), dan harus muat di dalam hit rect.
6. Tombol toggle wajib punya `-normal` dan `-active`. Kotak hit tidak boleh tumpang tindih lebih dari 10% dan tidak boleh keluar viewBox.
7. Koordinat harus ditulis langsung di atribut (jangan pakai `transform` di grup pembungkus kontrol), karena hit-test aplikasi membaca atribut apa adanya.
8. Setelah selesai jalankan `python3 tools/gen_skin_01.py`, `python3 tools/validate.py skins/skin-01`, lalu `python3 tools/index.py .`.

## 2. Geometri acuan (satuan: piksel foto 800x800)
- Bodi mixer: x 40..759, y 70..729, yaitu **720 x 660 px, rasio 1,09 : 1** (hampir persegi, bukan lebar memanjang).
- Skin memakai skala 4/3, jadi viewBox = **960 x 880**. Konversi: `X=(x-40)*4/3`, `Y=(y-70)*4/3`.
- Pusat kanal 1-6: x = 108 + 54,8 x (n-1). Garis biru pembatas: x = 82, 137, 192, 246, 301, 356, 421.
- Pusat strip stereo 7/8, 9/10, 11/12 (kenop): x = 458, 511, 563. Jack atas: x = 444, 487, 529.
- Baris vertikal (pusat kenop): GAIN 308, COMP 365, HIGH 432, MID 474, LOW 515, FX 557, PAN 600, LEVEL 657.
- Jack combo y = 135 (r luar ±26). Plat PAD/HPF y 194..229. Jack stereo y = 173 dan 214 (r ±12,6).
- Panel SPX: 592..708 x 318..468. Daftar efek: 593..712 x 473..600. Panel biru bawah: FX RTN 593..649 x 601..717, Monitor 651..712 x 539..626, Stereo 651..712 x 628..717.
- Warna: muka #272828, biru #0265d3, kenop EQ #12bf97, kenop PAN #e3412e, cap putih #f4f5f0, cap COMP #efe6b6, teks label #a3a8ab / #d3d6d8.

> **v3.1**: skin-01 kini punya 10 kolom (viewBox 1940 x 900). Kolom 6-10 = REVERB AUDIO (fungsi `sysreverb.*`, lihat tabel kolom 6-10 di `PROMPT-SKIN-UNIVERSAL.md`); kolom 1-5 tidak berubah, panel kanan bergeser +54,8 satuan foto ke kanan. Semua angka "25 kontrol / 14 LED" di bawah berlaku untuk kolom 1-5 saja; total skin kini 45 kontrol dan 21 LED.

## 3. Pemetaan fungsi (jangan diubah) - v2.1: satu fitur aplikasi per channel
| Channel | Judul | Kontrol (baris -> fungsi) | Tombol ON/OFF |
|---|---|---|---|
| CH1 | MIC | GATE (atas) = mic.gate, VOLUME (bawah) = mic.volume | mic.toggle |
| CH2 | EQ MIC | HIGH / MID / LOW = eqmic.high / eqmic.mid / eqmic.low | eqmic.toggle |
| CH3 | ECHO | DELAY = echo.delay, FEEDBACK = echo.feedback, MIX (bawah) = echo.mix | echo.toggle |
| CH4 | REVERB | ROOM, DAMP, WIDTH, PARAM, WET, DRY = reverb.room / damp / width / cess / wet / dry | reverb.toggle |
| CH5 | EQ AUDIO | GAIN, SUB, HIGH, MID, LOW = eqaudio.gain / sub / high / mid / low | eqaudio.toggle |
| (CH6) | - | kolom CADANGAN dan strip stereo 7/8-11/12 dihapus total, bodi dipotong | - |
| Layar SPX | - | kosong (teks oranye dan slot-display dihapus) | - |
| Meter L / R | - | led-mic-1..7 / led-out-1..7 | - |

Strip 7/8-11/12, FX RTN, STEREO, MONITOR, SPX PARAMETER hanya hiasan (tanpa fungsi).

## 4. Cara kerja (wajib berulang sampai mirip)
1. Hitung ulang posisi dan ukuran komponen langsung dari foto: zoom per area (kiri-atas, kanan-atas, kiri-bawah, kanan-bawah), catat pusat dan radius tiap kenop, jack, tombol, dan teks. Jangan menebak.
2. Render skin ke PNG, lalu jalankan `python3 tools/compare.py foto.jpg skins/skin-01/skin.svg` untuk membuat `_overlay.png` (tumpang 50%) dan `_sbs.png` (berdampingan).
3. Cari selisih terbesar dulu: **bentuk bodi dan rasio, ukuran kotak panel, ukuran kenop/jack, posisi teks, ukuran font, warna**. Perbaiki di generator, ulangi.
4. Ulangi minimal 3 putaran. Di tiap putaran sebutkan 5 selisih terbesar yang kamu temukan dan apa yang kamu ubah.
5. Terakhir, cek lagi dengan checklist di bawah.

## 5. Checklist kemiripan
- [ ] Rasio bodi 1,09 : 1, sudut membulat, lis atas terang tipis, sisi kanan dan bawah gelap.
- [ ] 6 jack combo hitam besar + 2 sekrup tiap jack; plat PAD abu-abu terang.
- [ ] Kenop GAIN (hitam bergerigi + cap putih), COMP (cap krem + cincin abu 3 segmen), EQ hijau, FX putih, PAN merah.
- [ ] Strip stereo hanya punya HIGH dan LOW (tanpa MID), dengan label BAL / PAN/BAL.
- [ ] Panel biru kanan-atas: FOOT SW, FX SEND, MONITOR OUT, 2 XLR, STEREO OUT, PHONES, lis bergaris.
- [ ] Modul SPX: layar "24" oranye, logo SPX, POWER, PROGRAM, PARAMETER, meter L/R 7 level.
- [ ] Daftar 24 efek dalam 2 kolom (bentuk L), 3 panel biru bawah-kanan.
- [ ] Ukuran dan ketebalan font tiap label sama dengan foto; tidak ada teks yang menimpa kenop.
- [ ] Validator 0 ERROR.

Keluaran yang saya minta: zip ALL-TYPE-SKIN-MIXJOS terbaru (generator, skin.svg, preview.svg, skin.json, index.json) + ringkasan selisih yang tersisa.
