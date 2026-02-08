# 🗺️ Bilecik LIHKAB - Harita Mühendislik Web Sitesi

**Bilecik ve ilçelerinde (Osmaneli, Pazaryeri, Gölpazarı, Söğüt, Bozüyük, İnhisar, Yenipazar) profesyonel harita kadastro mühendislik hizmetleri.**

## 📋 Proje Hakkında

Bilecik LIHKAB (Lisanslı Harita Kadastro Bürosu) web sitesi, Flask framework kullanılarak geliştirilmiş modern ve performanslı bir web uygulamasıdır. 24+ harita mühendislik hizmeti sunar ve müşterilerin online başvuru yapmasını sağlar.

### 🎯 Özellikler

- ✅ **24+ Profesyonel Hizmet**: Aplikasyon, cins değişikliği, birleştirme, parselasyon ve daha fazlası
- ✅ **Online Başvuru Sistemi**: Dosya yükleme ile 7/24 başvuru imkanı
- ✅ **Responsive Tasarım**: Mobil, tablet ve masaüstü uyumlu
- ✅ **SEO Optimize**: Bilecik ve ilçeleri için Google arama optimizasyonu
- ✅ **Performans**: GZIP compression, browser caching, lazy loading
- ✅ **Güvenlik**: XSS, clickjacking ve MIME sniffing koruması
- ✅ **Yapay Zeka Chatbot**: 7/24 müşteri desteği ve hizmet bilgilendirme

## 🛠️ Teknoloji Stack

- **Backend**: Flask 3.0.0 (Python)
- **Template Engine**: Jinja2
- **Compression**: Flask-Compress (GZIP)
- **Server**: Gunicorn (Production)
- **Frontend**: HTML5, CSS3, JavaScript
- **SEO**: robots.txt, sitemap.xml, meta tags, structured data

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- pip
- virtualenv (önerilir)

### Adımlar

```bash
# 1. Projeyi klonla
git clone https://github.com/iyazarli/HOA_website.git
cd HOA_website

# 2. Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Uygulamayı çalıştır
python app.py
```

Tarayıcıda `http://localhost:5000` adresine gidin.

## 📦 Deployment

### Heroku

```bash
# Heroku CLI ile
heroku create bilecik-lihkab
git push heroku main
heroku open
```

### Render / Railway

1. GitHub repo'nuzu bağlayın
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`

### VPS (Ubuntu)

```bash
# Nginx + Gunicorn setup
sudo apt update
sudo apt install python3-pip python3-venv nginx
git clone https://github.com/iyazarli/HOA_website.git
cd HOA_website
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:8000 app:app
```

## 📂 Proje Yapısı

```
HOA/
├── app.py                  # Ana Flask uygulaması
├── requirements.txt        # Python bağımlılıkları
├── robots.txt             # SEO - arama motoru yönergeleri
├── sitemap.xml            # SEO - site haritası
├── .gitignore             # Git ignore dosyası
├── README.md              # Proje dokümantasyonu
├── static/
│   ├── css/
│   │   └── style.css      # Ana CSS dosyası
│   └── img/               # Görseller ve logolar
├── templates/
│   ├── base.html          # Ana şablon
│   ├── index.html         # Anasayfa
│   ├── online-basvuru.html # Online başvuru formu
│   ├── islem-ucretleri.html # Ücret tarifesi
│   ├── iletisim.html      # İletişim sayfası
│   ├── personelimiz.html  # Personel bilgileri
│   ├── referanslarimiz.html # Referanslar
│   └── services/          # Hizmet detay sayfaları (24 adet)
└── uploads/               # Yüklenen dosyalar
```

## 🎨 Hizmetlerimiz

### Ana Hizmetler
- Aplikasyon
- Cins Değişikliği
- Birleştirme
- İrtifak Hakkı Tesisi/Terkini
- Bağımsız Bölüm Yer Gösterme

### Diğer Hizmetler
- Parsel Yer Gösterme
- Röperli Kroki
- Yola Terk/Yoldan İhdas/Ayırma
- Parselasyon
- Sınırlandırma Haritaları
- Hatalı Bağımsız Bölüm/Blok Düzeltme
- İmar Planı Uygulamaları
- Yapı Aplikasyonu/Vaziyet Planı
- TUS Uygulamaları
- Konum Belirleme
- Halihazır Harita Yapımı
- Plankote
- Yol Profil Çalışmaları
- Harita Plan Örnekleri

## 🔍 SEO Optimizasyonu

### Hedef Kelimeler

**Bilecik ve İlçeleri:**
- Bilecik harita mühendisi
- Osmaneli kadastro bürosu
- Pazaryeri LIHKAB
- Gölpazarı harita hizmetleri
- Söğüt aplikasyon
- Bozüyük parselasyon
- İnhisar imar planı
- Yenipazar röperli kroki

**Hizmet Bazlı:**
- Bilecik aplikasyon fiyatları
- Bilecik cins değişikliği
- Bilecik parsel birleştirme
- Bilecik irtifak hakkı
- Bilecik halihazır harita

### Yapılanlar
✅ Meta title ve description optimizasyonu  
✅ robots.txt ve sitemap.xml  
✅ Structured data (JSON-LD)  
✅ Open Graph tags (sosyal medya)  
✅ Canonical URLs  
✅ Image alt texts  

## 🤖 Yapay Zeka Chatbot

Web sitesine entegre edilen AI chatbot:

- 7/24 müşteri desteği
- Hizmet bilgilendirme
- Fiyat teklifi
- Randevu yönlendirme
- Sık sorulan sorular

## 📊 Performans

- **GZIP Compression**: %70 dosya boyutu azaltma
- **Browser Caching**: Static files 1 yıl, HTML 1 saat
- **Lazy Loading**: Görseller gerektiğinde yüklenir
- **CDN Ready**: Cloudflare entegrasyonu hazır
- **Lighthouse Score**: 90+ (Performance, SEO, Accessibility)

## 🔒 Güvenlik

- XSS koruması
- Clickjacking koruması
- MIME sniffing koruması
- Secure file upload
- Input validation
- HTTPS ready

## 📞 İletişim

**Bilecik LIHKAB**  
📍 Bilecik, Türkiye  
📧 info@bileciklihkab.com  
📱 [Telefon numarası]

**Hizmet Verdiğimiz Bölgeler:**  
Bilecik Merkez, Osmaneli, Pazaryeri, Gölpazarı, Söğüt, Bozüyük, İnhisar, Yenipazar

## 📝 Lisans

© 2026 Bilecik LIHKAB. Tüm hakları saklıdır.

## 🔄 Güncellemeler

- **v1.0.0** (2026-02-08): İlk versiyon
  - 24 hizmet sayfası
  - Online başvuru sistemi
  - SEO optimizasyonu
  - AI chatbot entegrasyonu

---

**Geliştirici:** [İsim]  
**GitHub:** https://github.com/iyazarli/HOA_website
