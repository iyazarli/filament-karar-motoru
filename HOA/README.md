# ÇORLU LİHKAB Web Sitesi

Tekirdağ ilinde hizmet veren lisanslı harita kadastro bürosu ÇORLU LİHKAB'ın resmi web sitesidir.

## Teknoloji

- **Framework:** Flask 3.0.0
- **Frontend:** HTML5, CSS3, JavaScript
- **Sunucu:** Gunicorn (Production)
- **Database:** Statik Content (gerekli değil)

## Kurulum

### Gereksinimler
- Python 3.9 veya üstü
- pip (Python package manager)

### Adımlar

1. **Depoyu klonlayın:**
```bash
git clone https://github.com/yourusername/corlulihkab.git
cd corlulihkab
```

2. **Sanal ortam oluşturun:**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ya da
venv\Scripts\activate  # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

## Çalıştırma

### Geliştirme Ortamında
```bash
python3 app.py
```
Tarayıcıda `http://localhost:5000` adresine gidin.

### Production Ortamında (Gunicorn ile)
```bash
gunicorn app:app
```

## Dosya Yapısı

```
corlulihkab/
├── app.py                    # Ana Flask uygulaması
├── requirements.txt          # Python bağımlılıkları
├── Procfile                  # Deployment konfigürasyonu
├── templates/
│   ├── base.html             # Ana template
│   ├── index.html            # Anasayfa
│   ├── online-basvuru.html   # Online başvuru formu
│   ├── iletisim.html         # İletişim sayfası
│   ├── personelimiz.html     # Personel sayfası
│   ├── islem-ucretleri.html  # Ücret tablosu
│   ├── service_template.html # Hizmet detail sayfası
│   └── services/             # Hizmet detay sayfaları (20+)
├── static/
│   ├── css/
│   │   └── style.css         # Ana stil dosyası
│   ├── js/                   # JavaScript dosyaları
│   └── img/                  # Resim varlıkları
└── README.md
```

## Hizmetler

ÇORLU LİHKAB aşağıdaki hizmetleri sağlamaktadır:

### HİZMETLERİMİZ
- Aplikasyon
- Cins Değişikliği
- Birleştirme
- İrtifak Hakkı Tesisi
- İrtifak Hakkı Terkini
- Bağımsız Bölüm Yer Gösterme

### DİĞER HİZMETLERİMİZ
- Parsel Yer Gösterme
- Röperli Kroki
- Yola Terk / Yoldan İhdas / Ayırma
- Parselasyon
- Sınırlandırma Haritaları
- Hatalı Bağımsız Bölüm Düzeltme
- Hatalı Blok Düzeltmesi
- İmar Planı Uygulamaları
- Yapı Aplikasyonu / Vaziyet Planı
- TUS Uygulamaları
- Konum Belirleme
- Halihazır Harita Yapımı
- Plankote
- Yol Profil Çalışmaları
- Harita Plan Örneği (Kadastro Çapı)

## Deployment

### Render.com Deployment
1. GitHub'a push yapın
2. [Render.com](https://render.com) üzerinde yeni Web Service oluşturun
3. GitHub deponuzu bağlayın
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`

### Heroku Deployment
1. GitHub'a push yapın
2. [Heroku](https://heroku.com) üzerinde yeni app oluşturun
3. Deploy seçeneğini seçin
4. GitHub deponuzu bağlayın
5. Otomatik deployment etkinleştirin

## İletişim

- **Telefon:** (282) 654-0544
- **E-posta:** bilgi@corlulihkab.com
- **Adres:** Çorlu, Tekirdağ

## Lisans

Tüm hakları saklıdır © 2024 ÇORLU LİHKAB
