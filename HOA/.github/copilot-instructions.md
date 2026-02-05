# ÇORLU LİHKAB Web Sitesi - Geliştirici Kılavuzu

Bu dosya ÇORLU LİHKAB web sitesinin geliştirmesi ve deployment'ı hakkında özel talimatlar içerir.

## Proje Açıklaması

Bu proje, Tekirdağ ilinde hizmet veren lisanslı harita kadastro bürosu ÇORLU LİHKAB'ın resmi web sitesidir. Toplam 20+ hizmetin ayrıntılı açıklamalarını, online başvuru formunu, personel ve ücret bilgilerini içermektedir.

## Teknoloji Stack

- **Backend:** Python 3.9+ ile Flask 3.0.0
- **Frontend:** HTML5, CSS3, JavaScript
- **Sunucu:** Gunicorn (Production)
- **Deployment:** Render.com, Heroku, veya özel VPS

## Proje Yapısı

```
corlulihkab/
├── app.py                         # Ana Flask uygulaması
├── requirements.txt               # Python bağımlılıkları
├── Procfile                       # Deployment konfigürasyonu
├── README.md                      # Proje dökümantasyonu
├── .gitignore                     # Git ignore kuralları
├── templates/                     # Jinja2 HTML şablonları
│   ├── base.html                  # Ana şablon (header, nav, footer)
│   ├── index.html                 # Anasayfa
│   ├── online-basvuru.html        # Online başvuru formu
│   ├── iletisim.html              # İletişim sayfası
│   ├── personelimiz.html          # Personel bilgileri
│   ├── islem-ucretleri.html       # Hizmet ücretleri
│   ├── service_template.html      # Hizmet detail şablonu
│   └── services/                  # Hizmet detay sayfaları (20+)
│       ├── aplikasyon.html
│       ├── cins-degisikligi.html
│       ├── birlestirme.html
│       ├── ... (17 daha)
│       └── harita-plan-ornegi.html
├── static/                        # Statik dosyalar
│   ├── css/
│   │   └── style.css              # Ana stil dosyası
│   ├── js/                        # JavaScript dosyaları (isteğe bağlı)
│   └── img/                       # Resim varlıkları
└── .github/
    └── copilot-instructions.md    # Bu dosya
```

## Yerel Geliştirme

### 1. Ortamı Hazırla
```bash
# Depoyu klonla
git clone https://github.com/yourusername/corlulihkab.git
cd corlulihkab

# Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\Scripts\activate     # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. Uygulamayı Çalıştır
```bash
# Development modu ile
python3 app.py

# veya
flask run

# Farklı port kullanmak için
flask run --port 5001
```

Tarayıcıda http://localhost:5000 (ya da http://localhost:5001) adresine gidin.

### 3. Test Et
- Anasayfa yüklüyor mu?
- Menü dropdown'ları çalışıyor mu?
- Hizmetler sekmesi açılıyor mu?
- Online başvuru formu çalışıyor mu?
- İletişim bilgileri gösteriliyor mu?

## Stil Kustomizasyonu

### Renkler
Ana renkler `static/css/style.css` dosyasında tanımlıdır:
- **Primary Blue:** `#4A90E2`
- **Dark Blue:** `#357ABD`
- **Subtitle Orange:** `#FF8C00`
- **Dark Text:** `#2c3e50`

### Yazı Tipi
- **Font:** Open Sans
- Fallback: Helvetica Neue, Arial

Değişiklik yapmak için `style.css` dosyasını düzenleyin.

## Flask Rotaları

Ana rotalar `app.py` dosyasında tanımlıdır:

```python
@app.route('/')                              # Anasayfa
@app.route('/aplikasyon')                    # Hizmet detail sayfaları
@app.route('/online-basvuru', methods=['GET', 'POST'])  # Başvuru formu
@app.route('/iletisim', methods=['GET', 'POST'])        # İletişim
@app.route('/personelimiz')                  # Personel
@app.route('/islem-ucretleri')               # Ücretler
```

Yeni rota eklemek için `app.py` dosyasına ekleme yapın.

## Deployment

### Render.com'da Deploy
1. GitHub'a push yapın
2. [Render.com](https://render.com) hesabı açın
3. "New" → "Web Service" seçin
4. GitHub deponuzu seçin
5. Settings:
   - **Name:** corlulihkab (ya da tercih ettiğiniz ad)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3
6. "Create Web Service" seçin

### Heroku'da Deploy
1. GitHub'a push yapın
2. [Heroku](https://heroku.com) hesabı açın
3. "New" → "Create new app" seçin
4. App adını girin
5. "Deployment method" → "GitHub" seçin
6. Depo bağlayın
7. "Enable Automatic Deploys" seçin (isteğe bağlı)
8. "Deploy Branch" seçin

### Özel VPS'de Deploy
1. SSH ile bağlanın
2. Python ve pip yükleyin
3. Depoyu klonlayın
4. Sanal ortam oluşturun
5. Gunicorn kurun
6. Systemd service dosyası oluşturun
7. Nginx proxy yapılandırın

## Orjinal Domaine Bağlama

Deployment tamamlandıktan sonra:

1. Domain sağlayıcıda DNS kayıtlarını güncelleyin
2. Render.com/Heroku'daki custom domain ayarlarını yapılandırın
3. SSL sertifikasını etkinleştirin

## Sorun Giderme

### CSS yüklenmiyorsa
- Flask'ın `static` klasörüne erişimini kontrol edin
- Cache temizleyin (Ctrl+Shift+Delete)
- Development modunda debug modu açın

### Formlar çalışmıyor
- Flask'ın `secret_key` ayarlanmış mı kontrol edin
- Request method doğru mu kontrol edin (GET/POST)
- Network tab'ında hata mesajını kontrol edin

### Port zaten kullanılıyor
```bash
# Port kontrol
lsof -i :5000

# Farklı port kullan
flask run --port 5001
```

## Kontribüsyon Rehberi

1. Branch oluşturun: `git checkout -b feature/yeni-ozellik`
2. Değişiklik yapın
3. Test edin
4. Commit yapın: `git commit -am 'Açıklama'`
5. Push yapın: `git push origin feature/yeni-ozellik`
6. Pull request açın

## İletişim

- **Telefon:** (282) 654-0544
- **E-posta:** bilgi@corlulihkab.com
- **Web:** www.corlulihkab.com

## Lisans

Tüm hakları saklıdır © 2024 ÇORLU LİHKAB
