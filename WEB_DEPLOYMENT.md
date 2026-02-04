# 🌐 Web Deployment Kılavuzu

Bu doküman filament_karar_motoru.py programını web sitesi olarak nasıl yayınlayacağınızı açıklar.

## 🚀 Hızlı Başlangıç (Yerel Test)

```bash
# Streamlit'i kur
pip install streamlit pandas

# Uygulamayı başlat
streamlit run app_streamlit.py
```

Tarayıcınızda `http://localhost:8501` açılacak.

---

## ☁️ Ücretsiz Cloud Deployment Seçenekleri

### 1️⃣ STREAMLIT CLOUD (ÖNERİLEN - EN KOLAY)

**장점:**
- ✅ Tamamen ücretsiz
- ✅ GitHub'dan otomatik deploy
- ✅ SSL sertifikası dahil
- ✅ Kurulum gerektirmiyor

**Adımlar:**

1. **GitHub Repository Oluştur**
   - https://github.com adresine git
   - "New repository" tıkla
   - İsim ver: `filament-karar-motoru`
   - Public seç, Create

2. **Dosyaları Yükle**
   ```bash
   cd /Users/ihsan/Downloads
   git init
   git add app_streamlit.py filament_karar_motoru.py requirements.txt
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/KULLANICI_ADIN/filament-karar-motoru.git
   git push -u origin main
   ```

3. **Streamlit Cloud'da Deploy Et**
   - https://share.streamlit.io adresine git
   - GitHub hesabınla giriş yap
   - "New app" tıkla
   - Repository seç: `filament-karar-motoru`
   - Main file: `app_streamlit.py`
   - Deploy!

4. **✨ Hazır!**
   - URL: `https://KULLANICI-filament-karar-motoru.streamlit.app`
   - Herkesle paylaşabilirsin

---

### 2️⃣ HUGGING FACE SPACES (AI FRIENDLY)

**장점:**
- ✅ Ücretsiz
- ✅ Streamlit desteği
- ✅ Güçlü sunucular

**Adımlar:**

1. https://huggingface.co/spaces adresine git
2. "Create new Space" tıkla
3. Space SDK: **Streamlit** seç
4. Dosyaları yükle:
   - `app_streamlit.py` → `app.py` olarak yükle
   - `filament_karar_motoru.py` yükle
   - `requirements.txt` yükle
5. Otomatik deploy olur

**URL:** `https://huggingface.co/spaces/KULLANICI/filament-karar`

---

### 3️⃣ RENDER (PROFESYONEL)

**장점:**
- ✅ 750 saat/ay ücretsiz
- ✅ Otomatik SSL
- ✅ GitHub entegrasyonu

**Adımlar:**

1. https://render.com adresine git, kaydol
2. "New +" → "Web Service"
3. GitHub repository'ni bağla
4. Settings:
   - **Name:** filament-karar-motoru
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0`
5. Create Web Service

**URL:** `https://filament-karar-motoru.onrender.com`

**⚠️ Not:** Ücretsiz plan 15 dakika kullanılmazsa uyur, ilk açılış yavaş olabilir.

---

### 4️⃣ RAILWAY (HIZLI)

**장점:**
- ✅ $5 ücretsiz kredi/ay
- ✅ Çok hızlı deployment
- ✅ Uyumuyor

**Adımlar:**

1. https://railway.app adresine git
2. GitHub ile giriş yap
3. "New Project" → "Deploy from GitHub repo"
4. Repository seç
5. Settings → Generate Domain

**URL:** `https://filament-karar-motoru-production.up.railway.app`

---

## 📦 Kendi Sunucunda Hosting

### VPS/Dedicated Server (Ubuntu)

```bash
# Sunucuya bağlan
ssh kullanici@sunucu-ip

# Gereklilikleri kur
sudo apt update
sudo apt install python3-pip nginx

# Dosyaları yükle
git clone https://github.com/KULLANICI/filament-karar-motoru.git
cd filament-karar-motoru

# Paketleri kur
pip3 install -r requirements.txt

# Streamlit'i systemd service olarak çalıştır
sudo nano /etc/systemd/system/filament.service
```

**filament.service içeriği:**
```ini
[Unit]
Description=Filament Karar Motoru
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/filament-karar-motoru
ExecStart=/usr/local/bin/streamlit run app_streamlit.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Service'i başlat
sudo systemctl enable filament
sudo systemctl start filament

# Nginx reverse proxy kur
sudo nano /etc/nginx/sites-available/filament
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name filament.sendomainin.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/filament /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🔒 SSL Sertifikası (HTTPS)

```bash
# Let's Encrypt ile ücretsiz SSL
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d filament.sendomainin.com
```

---

## 📊 Deployment Karşılaştırması

| Platform | Ücretsiz | Kurulum | Hız | SSL | Uyumuyor |
|----------|----------|---------|-----|-----|----------|
| **Streamlit Cloud** | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ❌ |
| **Hugging Face** | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ❌ |
| **Render** | 750h/ay | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ❌ |
| **Railway** | $5/ay | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| **Kendi VPS** | ❌ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⚙️ | ✅ |

---

## 🎨 Özelleştirme

### Logo Ekle
`app_streamlit.py` dosyasında:
```python
st.set_page_config(
    page_title="Filament Karar Motoru",
    page_icon="🔧",  # Buraya emoji veya logo.png yolu
    layout="wide"
)
```

### Tema Değiştir
`.streamlit/config.toml` dosyası oluştur:
```toml
[theme]
primaryColor="#FF4B4B"
backgroundColor="#0E1117"
secondaryBackgroundColor="#262730"
textColor="#FAFAFA"
font="sans serif"
```

---

## 🐛 Troubleshooting

**Problem:** Port hatası
```
OSError: [Errno 98] Address already in use
```
**Çözüm:**
```bash
streamlit run app_streamlit.py --server.port=8502
```

**Problem:** ModuleNotFoundError: No module named 'filament_karar_motoru'
**Çözüm:** İki dosya aynı klasörde olmalı:
- `app_streamlit.py`
- `filament_karar_motoru.py`

**Problem:** Streamlit Cloud'da deploy hatası
**Çözüm:** `requirements.txt` dosyasını kontrol et, GitHub'da olmalı.

---

## 📞 Destek

- Streamlit Dokümanları: https://docs.streamlit.io
- Streamlit Forum: https://discuss.streamlit.io
- GitHub Issues: Repository'nizdeki Issues sekmesi

---

## ✅ Kontrol Listesi

Deployment öncesi:
- [ ] `app_streamlit.py` çalışıyor (yerel test)
- [ ] `requirements.txt` hazır
- [ ] GitHub repository oluşturuldu
- [ ] Dosyalar yüklendi
- [ ] Platform seçildi
- [ ] Deploy edildi
- [ ] Test edildi (tarayıcıda açıldı mı?)
- [ ] URL paylaşıldı

---

**🎉 Artık web siteniz hazır! Herkesle paylaşabilirsiniz.**
