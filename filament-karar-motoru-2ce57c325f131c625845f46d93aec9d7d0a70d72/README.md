# 📦 Filament Karar Motoru - Windows Paketi

## İçindekiler

Bu klasörde 5 dosya bulunuyor:

1. **filament_karar_motoru.py** - Ana program (Python script)
2. **build_exe.py** - Mac/Linux'ta EXE oluşturma script'i
3. **build_exe_windows.bat** - Windows'ta EXE oluşturma (opsiyonel)
4. **KULLANIM_KILAVUZU.md** - Detaylı kullanım kılavuzu
5. **HIZLI_BAŞLANGIÇ.md** - Hızlı başlangıç talimatları

---

## 🎯 Ne İşe Yarar?

3D yazıcınız için **30 farklı filament** arasından **en uygun olanı** seçmenize yardımcı olur.

- ✅ Yazıcınızın donanımını kontrol eder
- ✅ İhtiyaçlarınıza göre puanlar
- ✅ Uyarılar verir (basılamaz, tabla yetersiz, vs.)
- ✅ Sonuçları CSV'ye kaydeder

---

## 🚀 Windows Kullanıcısı İçin 3 Seçenek

### Seçenek A: Hazır EXE (Hiçbir Kurulum Yok) ⭐ ÖNERİLEN

**Sen yapacaksın (Mac'te):**
```bash
pip3 install pyinstaller
python3 build_exe.py
```

Sonra `dist/filament_karar_motoru.exe` dosyasını Windows'a gönder.

**Windows kullanıcısı:**
- Çift tıkla → Kullan → Bitti!

---

### Seçenek B: Python Script (Python Kurulu Olmalı)

**Windows kullanıcısı:**
1. Python kur: https://python.org
2. Terminal'de: `pip install pandas`
3. Çalıştır: `python filament_karar_motoru.py`

---

### Seçenek C: Online Çalıştırma

**Google Colab'da çalıştır:**
1. https://colab.research.google.com/ aç
2. Script'i yükle
3. Çalıştır

---

## 📁 Dosya Boyutları

- `filament_karar_motoru.py`: ~50 KB
- `filament_karar_motoru.exe`: ~50-80 MB (pandas dahil)

**EXE neden büyük?**
Tüm Python + pandas + numpy kütüphaneleri içinde!

---

## 💡 Önerilen Gönderme Yöntemi

**En basit:**
1. Mac'te EXE oluştur
2. Google Drive / WeTransfer ile gönder
3. "Çift tıkla, kullan" de

**Alternatif (küçük dosya):**
1. Sadece `.py` dosyasını gönder
2. Python + pandas kurmasını söyle
3. `python filament_karar_motoru.py` yazsın

---

## ❓ SSS

**S: EXE Mac'te çalışır mı?**
Hayır, sadece Windows. Mac'te `.py` scriptini kullan.

**S: Antivirüs EXE'yi engellerse?**
"Engeli kaldır" / "Yine de çalıştır" de. EXE virüs değil, sadece imzasız.

**S: Hangi Windows sürümleri?**
Windows 10/11. Windows 7 denenmedi.

---

## 📞 Destek

Sorun olursa:
1. `KULLANIM_KILAVUZU.md` dosyasına bak
2. Python sürümünü kontrol et: `python --version`
3. Pandas kurulu mu: `pip show pandas`

---

**Versiyon:** PRO++ v2.0  
**Tarih:** 4 Şubat 2026  
**Geliştirici:** İhsan
