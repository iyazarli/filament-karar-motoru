# Filament Karar Motoru - Windows Kullanım Kılavuzu

## 🎯 Amaç
FDM 3D yazıcınız için en uygun filamenti seçmenize yardımcı olan akıllı karar destek sistemi.

---

## 📦 Windows'ta Kullanım (Python Yüklü Değilse)

### Yöntem 1: Hazır EXE Dosyası (ÖNERİLEN)

1. **filament_karar_motoru.exe** dosyasını masaüstüne kopyalayın
2. Çift tıklayın
3. Soruları yanıtlayın
4. Sonuçlar otomatik görüntülenir ve **filament_secim_sonucu.csv** dosyası oluşur

**NOT:** İlk açılış 5-10 saniye sürebilir (EXE paketi açılıyor).

---

### Yöntem 2: Python ile Çalıştırma

Eğer Python yüklüyse:

#### Adım 1: Python Kurulumu
- [Python.org](https://www.python.org/downloads/) adresinden Python 3.10+ indirin
- Kurulumda **"Add Python to PATH"** seçeneğini işaretleyin

#### Adım 2: Pandas Kütüphanesini Kurun
```cmd
pip install pandas
```

#### Adım 3: Çalıştırın
```cmd
python filament_karar_motoru.py
```

---

## 🛠️ Kendiniz EXE Oluşturmak İsterseniz

### Gereksinimler (Sadece Mac/Linux'ta build için):
```bash
pip install pyinstaller pandas
```

### Build Komutu:
```bash
python build_exe.py
```

Bu komut **dist/filament_karar_motoru.exe** dosyasını oluşturur.

**EXE Özellikleri:**
- ✅ Tek dosya (50-80 MB)
- ✅ Python kurulumu gerektirmez
- ✅ Tüm bağımlılıklar dahil (pandas, numpy)
- ✅ Windows 10/11 uyumlu

---

## 📊 Kullanım Adımları

### 1. Donanım Bilgileri
Programı çalıştırdığınızda yazıcınızın özelliklerini soracak:
- Kapalı kasa var mı?
- Filament kurutucusu var mı?
- Sertleştirilmiş nozzle var mı?
- Isıtmalı yatak sıcaklığı (°C)
- Nozzle maksimum sıcaklık (°C)
- Ekstruder tipi (Direct / Bowden)
- Nozzle ölçüleri (0.2, 0.4, 0.6, 0.8 mm) - birden fazla seçilebilir
- Tabla yüzeyleri (Cam, PEI Smooth, PEI Textured, BuildTak, Garolite, PP Sheet)

### 2. Kullanım Gereksinimleri
28 farklı kriter için 0-5 arası önem derecesi belirleyin:
- **0** = Hiç önemli değil
- **5** = Kritik öneme sahip

Örnek kriterler:
- Isı dayanımı
- Baskı kolaylığı
- Dayanıklılık
- Esneklik
- Şeffaflık
- vs.

### 3. Sonuçlar
Program size şunları verir:
- ✅ **En uygun filament sıralaması** (0-100% uyumluluk)
- ⚠️ **Uyarı mesajları** (basılamaz, tabla yetersiz, vs.)
- 📋 **Tabla bazlı öneriler** (her tabla için ayrı)
- 💾 **CSV dosyası** (Excel'de açılabilir)

---

## 📁 Çıktı Dosyası

**filament_secim_sonucu.csv** - Excel ile açın:

| Filament | Uyumluluk (%) | En İyi Tabla | Uyarılar |
|----------|---------------|--------------|----------|
| PLA+ | 100.0 | PEI Smooth | ✅ Sorunsuz |
| PETG | 95.3 | PEI Smooth | ✅ Sorunsuz |
| PEEK | 0.0 | PEI Textured | ❌ BASILAMAZ (Min 400°C gerekli) |

---

## 🚨 Sık Karşılaşılan Sorunlar

### "Python bulunamadı" hatası
**Çözüm:** Python yükleyin VEYA hazır .exe dosyasını kullanın

### "pandas modülü bulunamadı" hatası
**Çözüm:** `pip install pandas` komutunu çalıştırın

### EXE açılmıyor
**Çözüm:** 
1. Windows Defender'dan izin verin
2. Sağ tık → "Yönetici olarak çalıştır"
3. Antivirüs programını geçici devre dışı bırakın

### Terminal/cmd penceresi görünmüyor
**Çözüm:** EXE, `--noconsole` ile build edilmiş. Console görmek için:
```bash
# build_exe.py içindeki --noconsole satırını kaldırın
python build_exe.py
```

---

## 🎨 Özellikler

- 30 farklı filament tipi (PLA, PETG, ABS, Nylon, PC, PEEK, TPU, vs.)
- 40 farklı özellik değerlendirmesi
- 8 farklı uyarı tipi
- Çoklu nozzle desteği
- 6 farklı tabla yüzeyi desteği
- Akıllı ceza sistemi (donanım uyumsuzlukları)
- Min-Max normalizasyon (gerçekçi skorlama)
- CSV export (Excel/Google Sheets uyumlu)
- Türkçe/İngilizce bilingual dokümantasyon

---

## 📞 Destek

Sorun yaşarsanız:
1. Python sürümünüzü kontrol edin: `python --version` (3.10+ olmalı)
2. Pandas kurulu mu kontrol edin: `pip show pandas`
3. EXE dosyasını antivirüs beyaz listesine ekleyin

---

## 📝 Lisans

Bu yazılım eğitim ve kişisel kullanım içindir.

---

**Son Güncelleme:** 4 Şubat 2026
**Versiyon:** PRO++ v2.0
