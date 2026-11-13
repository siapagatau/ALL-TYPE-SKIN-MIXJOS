# ALL-TYPE-SKIN-MIXJOS

SATU repo untuk semua skin APK MIXJOS. Menggantikan tiga repo lama: skin mixer (`MIXDTX-SKIN` / `SKIN-MIXER`), `MIXDTX-COMPSKIN`, dan `MIXDTX-EQSKIN`.

URL index (diatur di `assets/config/skin-repo.json`, `eq-skin-repo.json`, `comp-skin-repo.json` — ketiganya sama):
`https://raw.githubusercontent.com/siapagatau/ALL-TYPE-SKIN-MIXJOS/master/index.json`

## Tipe skin
Tiap skin di `index.json` punya field `type`. Tab pemilih skin di APK hanya menampilkan skin bertipenya.

| type | tab di APK | function | skin saat ini |
|---|---|---|---|
| `mixer` | MIXER | `mic.*`, `reverb.*`, `echo.*`, `eqmic.*`, `eqaudio.*`, `sysreverb.*` (REVERB AUDIO) | `skin-01` Yamaha MG12XUK (v3.1, 10 kolom, 45 kontrol, 21 LED), `skin-02` dB Voice 602-RV (v4.2: 10 kolom, 51 kontrol, 21 LED, lampu meter diperbaiki (rect pertama); EQ 4 slider berlabel SUB/LOW/MID/HIGH, layar mati, knob cincin) |
| `comp` | KOMPRESOR | `comp.*` | `comp-dbx234` DBX 234 Kompresor |
| `eq` | EQUALIZER | `eq31.*` | `eq31-dbx1231` dbx 1231 EQ (v1.1) |
| `stage` | PANGGUNG (di atas mixer) | tanpa function; `stage.json` + gambar scene | `stage-festival` Panggung Festival |

`id` unik lintas tipe (hanya `A-Z a-z 0-9 _ -`, maks 64). Skin tanpa `type` dianggap `mixer`.

## Struktur
```
index.json            katalog (sha256 + size + type), dibuat tools/index.py
skins/<id>/           skin.json  skin.svg  preview.svg
prompts/              aturan membuat skin (MIXER, KOMPRESOR, EQUALIZER, MIRIP, UNIVERSAL)
tools/                generator, validator, index.py
```

## Alur menambah / mengubah skin
1. Buat atau ubah `skins/<id>/` (salin skin contoh sesuai tipenya; aturan di `prompts/`).
2. Validasi: `python3 tools/validate.py skins/<id>` (mixer), `python3 tools/validate_comp.py <id>` (kompresor), `python3 tools/validate_eq.py <id>` (equalizer), `python3 tools/validate_stage.py <id>` (panggung).
3. Bangun ulang index: `python3 tools/index.py` — tipe dibaca otomatis dari function di `skin.json` (`comp.*` -> comp, `eq31.*` -> eq, selain itu mixer).
4. Upload seluruh isi folder ini ke root repo GitHub `ALL-TYPE-SKIN-MIXJOS` (branch master).

## Skin PANGGUNG (type `stage`)
Folder `skins/<id>/` berisi `stage.json` + gambar scene (WebP). Tiap scene = satu gambar panggung yang layar green screen-nya SUDAH transparan
(dibuat `tools/gen_stage_festival.py` dari gambar hijau asli), sehingga media pengguna digambar DI BELAKANG gambar dan muncul tepat di dalam layar.
- `scenes.<cerah|sunset|malam>`: `image`, `lightGain` (kekuatan lampu per scene; siang redup, malam penuh), `slots` (kotak layar, 0..1 terhadap gambar).
- `schedule`: jam mulai tiap scene menurut jam lokal HP (bawaan: 00:00 malam, 06:00 cerah, 17:00 sunset, 18:30 malam). Pengguna juga bisa mengunci scene manual.
- `defaultLights`: lampu bawaan. `type` `beam` (sorot) / `lamp` (biasa); `motion` `diam|ayun|sapu` + `angle`, `angleTo`, `period` (detik); `blink` `tetap|kedip|denyut` + `bpm`.
Pengguna mengisi tiap layar dengan foto/GIF/video (video diputar berulang, tanpa suara), mengatur posisi & ukuran, serta menambah/mengubah lampu langsung di APK (tombol PANGGUNG -> EDIT).
Gambar scene maksimal 4 MB per berkas (batas unduh APK).

Generator skin contoh: `tools/gen_skin_01.py`, `gen_skin_02.py`, `gen_comp_dbx234.py`, `gen_eq31_dbx1231.py` (hasilnya identik dengan file di `skins/`), `gen_stage_festival.py <folder gambar CERAH/SUNSET/MALAM.png>`.
