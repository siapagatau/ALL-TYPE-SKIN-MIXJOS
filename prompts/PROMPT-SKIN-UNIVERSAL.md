# Prompt: Buat Skin Mixer Baru dari Foto Referensi (gaya "remake rapi" seperti skin Yamaha)

Salin semua isi di bawah garis ke AI (Claude), lalu lampirkan: **foto mixer baru**, **zip ALL-TYPE-SKIN-MIXJOS terbaru** (berisi skin-01 Yamaha dan skin-02 dB Voice sebagai contoh), dan nama mixernya.

---

Kamu desainer skin SVG. Tugasmu: buat skin baru dari foto mixer yang saya lampirkan, **langsung jadi tanpa tanya balik**, dengan prinsip yang sama seperti `skin-01` (Yamaha MG12XUK) dan `skin-02` (dB Voice 602-RV). Pelajari kedua contoh itu dulu (`tools/gen_skin_01.py`, `tools/gen_skin_02.py`) lalu tiru pendekatannya.

## 1. Filosofi: bukan salinan foto, tapi remake sederhana yang tetap terasa mereknya
- **STRUKTUR WAJIB MIRIP FOTO.** Sebelum menggambar, tulis dulu daftar blok dari foto (mana panel atas, panel bawah, panel samping, urutan komponen dari kiri ke kanan dan atas ke bawah) lalu ikuti persis urutan dan pembagian itu. Contoh dB Voice: panel atas hitam berisi jack dan tombol PHANTOM di bawah tiap jack (jadi toggle ON/OFF), panel bawah lebih sempit dan bertingkat, ring knob merah/putih/oranye, EQ 7-band dengan bar judul terang, panel abu-abu dengan XLR. Contoh Yamaha: panel biru kanan atas, daftar efek bentuk L. Kalau hasilnya tidak langsung dikenali sebagai mixer di foto, berarti struktur belum benar.
- Yang disederhanakan hanya **detail kecil** (tekstur, bayangan, tulisan mikro), bukan susunan blok.
- Jangan menjiplak foto piksel demi piksel. Ambil **ciri khas merek** saja: warna panel (Yamaha = biru, dB Voice = garis merah), jenis jack, logo dan tulisan model, bentuk blok besar (panel jack, layar, EQ, meter, fader).
- Hasilnya harus **simpel, rapi, konsisten, enak dilihat di layar HP**. Tidak ada detail kecil yang tidak terbaca di layar 6 inci.
- Satu ukuran untuk semua knob fungsi, jarak antar baris sama, label rata tengah di atas knob, tidak ada teks yang menimpa knob atau saling bertabrakan.
- Tata letak dibaca dari foto (posisi relatif blok), tapi diatur ulang ke grid rapi: kolom kanal sama lebar, baris knob jarak sama.

## 2. Pemetaan fungsi (tetap, jangan diubah)
Aplikasi punya 5 fitur mic + fitur REVERB AUDIO (v1.4+), tiap fitur = 1 kolom kanal (urut kiri ke kanan, total 10 kolom):

| Kolom | Judul | Knob (urut dari atas) | Toggle |
|---|---|---|---|
| 1 | MIC | mic.gate (GATE), mic.volume (VOLUME) | mic.toggle |
| 2 | EQ MIC | eqmic.high, eqmic.mid, eqmic.low | eqmic.toggle |
| 3 | ECHO | echo.delay, echo.feedback, echo.mix | echo.toggle |
| 4 | REVERB | reverb.room, damp, width, cess, wet, dry | reverb.toggle |
| 5 | EQ AUDIO | eqaudio.gain, sub, high, mid, low | eqaudio.toggle |
| 6 | REVERB AUDIO (sub "Suara app lain") | sysreverb.gain (GAIN); baris knob lain dim seperti kolom lain | sysreverb.toggle (id `tg-sysreverb`) |
| 7 | REVERB (sub "Reverb audio") | sysreverb.wet, room, damp, width, cess, predelay (PRE-DLY) | sysreverb.reverb.toggle (id `tg-sysreverb-reverb`) |
| 8 | DELAY (sub "Delay audio") | sysreverb.delay, feedback, mix | sysreverb.echo.toggle (id `tg-sysreverb-echo`) |
| 9 | KIRIM (sub "Ke reverb") | sysreverb.rsend.sub, low, mid, high | - (plat dim, tanpa fungsi) |
| 10 | KIRIM (sub "Ke delay") | sysreverb.esend.sub, low, mid, high | - (plat dim, tanpa fungsi) |

Total **37 knob + 8 toggle = 45 kontrol** dan **21 LED** meter (`led-mic-1..7` = meter.mic, `led-out-1..7` = meter.output, `led-sys-1..7` = meter.sysreverb).
Meter SYS (REVERB AUDIO) diletakkan di blok meter yang sama dengan MIC/OUT (bar ketiga, label "SYS"), BUKAN di dalam kolom channel.
**Kolom 6-10 = kolom BARU di sebelah kanan EQ AUDIO**; kolom 1-5 dan blok lain (panel kanan, display, meter L/R) tidak berubah, panel kanan hanya bergeser ke kanan. Jangan menumpangkan kontrol REVERB AUDIO ke kolom lama.
Nilai awal knob kolom 6-10 = nilai awal APK (`SysReverbSettings`): wet 0.5, room 0.6, damp 0.4, width 1.0, cess 0.4, predelay 0.2, delay 0.45, feedback 0.45, mix 0.4, gain 0.5, rsend sub/low/mid/high 0/0.3/0.8/1.0, esend 0/0/0.7/0.7.
Id saklar sysreverb WAJIB berbeda (jangan pakai pola `tg-<fungsi pertama>`, ketiganya akan bentrok jadi `tg-sysreverb`).
Kalau mixer di foto punya kurang dari 10 kanal, kolom fitur boleh diletakkan di area kenop terbesar; kalau lebih, kanal sisanya jadi hiasan.

## 3. Aturan tampilan (inti "remake rapi")
1. **Komponen tanpa fungsi digelapkan 50%** (kalikan semua warna hex dengan 0,5; fungsi `dim()` di generator). Ini berlaku untuk: knob kosong, fader, slider EQ, display, tombol transport, knob master/phones, dan hiasan lain. Komponen fungsi tampil terang penuh, jadi mata langsung tahu mana yang bisa disentuh.
2. **Label tetap terang** walau komponennya digelapkan.
3. Knob fungsi: badan hitam bergerigi + cap putih + garis penunjuk, 11 tick putih di sekelilingnya. Knob hiasan: sama persis tapi dim 50% dan diputar acak (-140 derajat).
4. Toggle: plat abu-abu terang bertuliskan "ON / OFF" dan nama fitur, tombol kotak di tengah, nyala **oranye** saat aktif.
5. Baris knob kosong di kolom yang knob-nya lebih sedikit tetap digambar (dim) supaya semua kolom tinggi dan rapi sama.
6. Blok non-fungsi dari foto diringkas: EQ 7-band jadi 7 slider sederhana, layar jadi kotak hitam dengan angka oranye, daftar efek cukup dibuang kalau tidak muat.
7. Meter L/R: 7 segmen per sisi (3 hijau, 3 kuning/oranye, 1 merah/abu PEAK), segmen mati = warna sama dengan opasitas 30%, segmen nyala = grup `led-*-on` yang `display="none"` secara bawaan.
8. Jack, XLR, sekrup tetap digambar sederhana tapi mirip jenisnya (combo, TRS perak, XLR emas). Jangan terlalu detail.
9. Warna dasar: muka gelap (#232426 atau sesuai merek), teks #a3a8ab / #d3d6d8, cap putih #f4f5f0, aksen merek (biru #0265d3 Yamaha, merah #e0342b dB Voice). Pilih satu warna aksen dari foto.
10. Logo dan nama model ditulis sebagai teks (Arial / Georgia), bukan gambar.

## 4. Aturan teknis wajib
1. Lolos `python3 tools/validate.py skins/skin-NN` dengan **0 ERROR** (usahakan 0 WARN).
2. Jangan ubah id kontrol dan isi `mapping`. Id hanya huruf kecil, angka, tanda hubung, tidak boleh ganda.
3. Dilarang di SVG: `script`, `foreignObject`, `image`, `use`, `audio`, `video`, `iframe`, atribut `on*`, `href`, URL `http(s)://`. Hindari `filter` dan `mask`.
4. Grup `knob-*` wajib punya `data-cx`, `data-cy`, `data-angle-min=-135`, `data-angle-max=135`, `data-value-default=0.5`. **Lingkaran pertama** di dalam grup = badan knob dan harus muat di dalam hit rect.
5. Toggle punya `-normal` dan `-active` (aktif `display="none"`). Hit rect tidak boleh tumpang tindih lebih dari 10% dan tidak boleh keluar viewBox.
6. Koordinat ditulis langsung di atribut, **tanpa `transform` di grup kontrol fungsi** (hit-test membaca atribut apa adanya). `transform` hanya boleh di knob hiasan.
7. Ukuran kanvas bebas, tapi pakai landscape sekitar 1241 x 900 supaya pas di layar HP.
8. Buat generator baru `tools/gen_skin_NN.py` (salin gen_skin_02.py sebagai kerangka), jalankan, lalu `validate.py`, lalu `python3 tools/index.py`.

## 5. Cara kerja (ulangi sampai rapi)
1. Lihat foto dan catat: merek, warna aksen, jenis jack, blok-blok besar di kiri/kanan/atas/bawah.
2. Susun kerangka: bodi, 5 kolom kanal, panel kanan (jack, logo, EQ, display, meter, fader).
3. Render ke PNG (playwright/chromium), lihat hasilnya, **cari tabrakan teks, teks menimpa knob, ketidakrataan jarak**, perbaiki. Minimal 3 putaran, di tiap putaran sebut 3 masalah terbesar dan apa yang diubah.
4. Cek checklist akhir.

## 6. Checklist akhir
- [ ] Terlihat jelas merek dan modelnya (logo, warna aksen, jenis jack) tapi tetap sederhana.
- [ ] 37 knob fungsi sama besar, jarak baris sama, label di atas tiap knob, tidak ada teks bertabrakan.
- [ ] 8 toggle oranye saat aktif (5 lama + 3 REVERB AUDIO), plat ON/OFF terbaca.
- [ ] Semua komponen tanpa fungsi gelap 50%.
- [ ] 21 LED meter ada dan berfungsi (mic, output, sysreverb).
- [ ] Validator 0 ERROR.
- [ ] Rapi dan terbaca di layar HP.

Keluaran yang saya minta: zip ALL-TYPE-SKIN-MIXJOS terbaru (generator baru, skin.svg, preview.svg, skin.json, index.json) + 3 baris ringkasan hal yang masih bisa diperbaiki.
