"""
ÇORLU LİHKAB - Web Sitesi Flask Uygulaması

Açıklama:
    Tekirdağ ilinde lisanslı harita kadastro bürosu ÇORLU LİHKAB'ın
    resmi web sitesi. 20+ hizmetin detaylı açıklamalarını, online
    başvuru formunu ve hizmet bilgilerini sunar.

Teknoloji Stack:
    - Framework: Flask 3.0.0
    - Compression: Flask-Compress 1.14.0
    - Template Engine: Jinja2
    - Server: Gunicorn (production)

PERFORMANCE OPTIMIZATIONS (Hız Iyileştirmeleri):
    1. GZIP Compression: Dosya boyutunu %70 küçültür
    2. Browser Caching: Static'ler 1 yıl, HTML 1 saat cache
    3. Script Defer: JavaScript parsing'i engelleme (async loading)
    4. DNS Prefetch: Harici domain'lere önceden bağlan
    5. Preconnect: Google Fonts'a TLS handshake'i önceden yap
    6. Font Display: FOIT/FOUT (Flash of Invisible/Unstyled Text) önle
    7. Security Headers: MIME sniffing, XSS, Clickjacking saldırılarına karşı

Versiyon: 1.1.0
Son Güncelleme: 2026-02-05
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_compress import Compress
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import os

# Flask uygulaması başlat
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'corlulihkab-secret-key-2026')

# Dosya yükleme ayarları
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 24 * 1024 * 1024  # 24MB
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'xlsx', 'xls'}

# Upload klasörü oluştur
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ============================================================
# PERFORMANCE OPTIMIZATION
# ============================================================

# GZIP compression etkinleştir - dosya boyutunu 70% kadar küçültür
# Tüm HTTP response'lar otomatik olarak sıkıştırılır (text, json, vb)
# Overhead minimal ve hız kazancı önemli (özellikle mobilde)
Compress(app)

# Jinja2 template caching - template'ler memory'de saklanır (hızlı render)
app.config['TEMPLATES_AUTO_RELOAD'] = False  # Production'da False


def allowed_file(filename):
    """Dosya uzantısı kontrol et"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def add_header(response):
    """
    Her HTTP response'a cache ve güvenlik headers ekle.
    
    CACHE STRATEGY (Tarayıcı Caching Stratejisi):
    
    Static Files (CSS, JS, Images):
    - Max-Age: 31536000 saniye (1 yıl)
    - Public: İçerik CDN ve proxy'lerde cache'lenebilir
    - Immutable Flag: Dosya asla değişmeyecek (webpack hash gibi)
    - Fayda: Tekrar ziyaret'lerde yükleme olmaz
    
    HTML Pages:
    - Max-Age: 3600 saniye (1 saat)
    - Public: CDN ve proxy'lerde cache'lenebilir
    - Fayda: Sunucu yükü azalır, sayfa hızlı sunar
    
    SECURITY HEADERS (Güvenlik Başlıkları):
    
    X-Content-Type-Options: nosniff
    - MIME sniffing saldırılarını engelle
    - Tarayıcı CSS dosyasını JavaScript olarak yorumlamaya çalışamaz
    
    X-Frame-Options: SAMEORIGIN
    - Clickjacking saldırılarını engelle
    - Site'nin sadece kendi iframe'lerinde gösterilmesine izin ver
    
    X-XSS-Protection: 1; mode=block
    - Eski tarayıcılarda XSS (Cross-Site Scripting) koruması
    - Modern tarayıcılar CSP kullanır
    
    PERFORMANCE TIP:
    - Static dosyalara hash ekle (webpack/asset pipeline)
    - Cache-busting: app.js?v=1.2.3 şeklinde
    """
    if 'static' in request.path:
        # Static dosyalar - uzun cache süresi (1 yıl = 31536000 saniye)
        response.cache_control.max_age = 31536000
        response.cache_control.public = True
        # Immutable flag (optional - tarayıcıya dosya asla değişmeyeceğini söyle)
        # response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
    else:
        # HTML sayfaları - kısa cache süresi (1 saat = 3600 saniye)
        # 1 saat sonra sunucu'dan yeni versiyonu kontrol et
        response.cache_control.max_age = 3600
        response.cache_control.public = True
    
    # ===== SECURITY HEADERS =====
    # MIME sniffing saldırılarını önle
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Clickjacking saldırılarını önle
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    
    # XSS koruması (eski tarayıcılar için)
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy (gelişmiş XSS koruması - gelecek)
    # response.headers['Content-Security-Policy'] = "default-src 'self'"
    
    return response


# ============================================================
# ANA SAYFA
# ============================================================

@app.route('/')
def index():
    """Anasayfa - Hero slider, hizmetler ve bilgi sayfası."""
    return render_template('index.html')


# ============================================================
# SEO ROUTES - robots.txt ve sitemap.xml
# ============================================================

@app.route('/robots.txt')
def robots():
    """SEO - robots.txt dosyasını sun"""
    return app.send_static_file('robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    """SEO - sitemap.xml dosyasını sun"""
    return app.send_static_file('sitemap.xml')


# ============================================================
# HİZMETLER SAYFASI ROTALARI (HİZMETLERİMİZ)
# ============================================================

@app.route('/aplikasyon')
def aplikasyon():
    """Aplikasyon hizmeti detay sayfası."""
    return render_template('services/aplikasyon.html')

@app.route('/cins-degisikligi')
def cins_degisikligi():
    """Cins Değişikliği hizmeti detay sayfası."""
    return render_template('services/cins-degisikligi.html')

@app.route('/birlestirme')
def birlestirme():
    """Birleştirme hizmeti detay sayfası."""
    return render_template('services/birlestirme.html')

@app.route('/irtifak-hakki-tesisi')
def irtifak_hakki_tesisi():
    """İrtifak Hakkı Tesisi hizmeti detay sayfası."""
    return render_template('services/irtifak-hakki-tesisi.html')

@app.route('/irtifak-hakki-terkini')
def irtifak_hakki_terkini():
    return render_template('services/irtifak-hakki-terkini.html')

@app.route('/bagimsiz-bolum-yer-gosterme')
def bagimsiz_bolum_yer_gosterme():
    return render_template('services/bagimsiz-bolum-yer-gosterme.html')

# Hizmet sayfaları - DİĞER HİZMETLERİMİZ
@app.route('/parsel-yer-gosterme')
def parsel_yer_gosterme():
    return render_template('services/parsel-yer-gosterme.html')

@app.route('/roperli-kroki')
def roperli_kroki():
    return render_template('services/roperli-kroki.html')

@app.route('/yola-terk-yoldan-ihdas-ayirma')
def yola_terk():
    return render_template('services/yola-terk-yoldan-ihdas-ayirma.html')

@app.route('/parselasyon')
def parselasyon():
    return render_template('services/parselasyon.html')

@app.route('/sinirlandirma-haritalari')
def sinirlandirma_haritalari():
    return render_template('services/sinirlandirma-haritalari.html')

@app.route('/hatali-bagimsiz-bolum')
def hatali_bagimsiz_bolum():
    return render_template('services/hatali-bagimsiz-bolum-duzeltme.html')

@app.route('/hatali-blok')
def hatali_blok():
    return render_template('services/hatali-blok-duzeltmesi.html')

@app.route('/imar-plani')
def imar_plani():
    return render_template('services/imar-plani-uygulamalari.html')

@app.route('/yapi-aplikasyonu')
def yapi_aplikasyonu():
    return render_template('services/yapi-aplikasyonu-vaziyet-plani.html')

@app.route('/tus-uygulamalari')
def tus_uygulamalari():
    return render_template('services/tus-uygulamalari.html')

@app.route('/konum-belirleme')
def konum_belirleme():
    return render_template('services/konum-belirleme.html')

@app.route('/halihazir-harita')
def halihazir_harita():
    return render_template('services/halihazir-harita-yapimi.html')

@app.route('/plankote')
def plankote():
    return render_template('services/plankote.html')

@app.route('/yol-profil')
def yol_profil():
    return render_template('services/yol-profil-calismalari.html')

@app.route('/harita-plan-ornegi')
def harita_plan_ornegi():
    return render_template('services/harita-plan-ornegi.html')

# ============================================================
# ONLINE BAŞVURU FORMU
# ============================================================

@app.route('/online-basvuru', methods=['GET', 'POST'])
def online_basvuru():
    """
    Online başvuru formu sayfası.
    
    GET: Boş formu göster
    POST: Form verisini al ve dosya kontrol et, başarı mesajı göster
    
    Form Alanları:
    - ad_soyad: Müşterinin adı soyadı (str)
    - telefon: İletişim telefon numarası (str)
    - email: E-posta adresi (str)
    - hizmet: Talep edilen hizmet türü (str)
    - dosya: İsteğe bağlı dosya ekli (file, max 1MB)
    
    Dosya Validasyonu:
    - Max boyut: 1MB (mail gönderim limiti)
    - İzin verilen formatlar: PDF, DOC, DOCX, JPG, PNG, XLSX, XLS
    """
    if request.method == 'POST':
        # HTML form'dan gönderilen verileri al
        ad_soyad = request.form.get('ad_soyad')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        hizmet = request.form.get('hizmet')
        
        # Dosya kontrol et
        dosya_adi = None
        if 'dosya' in request.files:
            file = request.files['dosya']
            
            # Dosya seçildiyse kontrol et
            if file and file.filename != '':
                # Dosya boyutu kontrol
                if file.content_length and file.content_length > MAX_FILE_SIZE:
                    flash(f'Dosya boyutu çok büyük! Maksimum 1MB olmalıdır.', 'error')
                    return redirect(url_for('online_basvuru'))
                
                # Dosya uzantısı kontrol
                if not allowed_file(file.filename):
                    flash('Dosya türü desteklenmiyor! İzin verilen: PDF, DOC, DOCX, JPG, PNG, XLSX, XLS', 'error')
                    return redirect(url_for('online_basvuru'))
                
                # Dosya adı güvenli hale getir ve kaydet
                dosya_adi = secure_filename(file.filename)
                # Dosya adına timestamp ekle (benzersiz yap)
                dosya_adi = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{dosya_adi}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], dosya_adi))
        
        # TODO: Veritabanına kaydet veya email'e gönder
        # db.session.add(Basvuru(ad_soyad=ad_soyad, telefon=telefon, email=email, hizmet=hizmet, dosya=dosya_adi))
        # db.session.commit()
        # send_email(email, "Başvurunuz Alındı", template="basvuru_onayi.html", attachment=dosya_adi)
        
        # Başarı mesajı göster ve sayfayı yenile
        flash('Başvurunuz başarıyla alınmıştır. En kısa sürede sizinle iletişime geçilecektir.', 'success')
        return redirect(url_for('online_basvuru'))
    
    return render_template('online-basvuru.html')

# ============================================================
# İLETİŞİM SAYFASI
# ============================================================

# İletişim
@app.route('/iletisim', methods=['GET', 'POST'])
def iletisim():
    """
    İletişim formu sayfası - Ziyaretçilerin mesaj göndermesini sağlar.
    
    GET: İletişim formunu göster
    POST: Mesajı al ve başarı mesajı göster
    
    Not: Gerçek uygulamada mesajlar veritabanına kaydedilmeli
    veya direkt yöneticiye email'e gönderilmelidir.
    """
    if request.method == 'POST':
        # TODO: Mesajı email'e gönder veya veritabanına kaydet
        # send_email(admin_email, "Yeni İletişim Mesajı", template="iletisim_maili.html")
        
        flash('Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapılacaktır.', 'success')
        return redirect(url_for('iletisim'))
    
    return render_template('iletisim.html')

# Personelimiz
@app.route('/personelimiz')
def personelimiz():
    """Personel bilgileri sayfası - Büro çalışanlarının bilgilerini gösterir."""
    return render_template('personelimiz.html')


# Referanslarımız
@app.route('/referanslarimiz')
def referanslarimiz():
    """Referanslarımız sayfası - Çalıştığımız büyük şirketlerin logolarını gösterir."""
    return render_template('referanslarimiz.html')


# ============================================================
# İŞLEM ÜCRETLERİ
# ============================================================

# İşlem Ücretleri
@app.route('/islem-ucretleri')
def islem_ucretleri():
    """
    İşlem ücretleri sayfası - Hizmetlerin tarifelerini gösterir.
    
    Her hizmete ait ücretler, ödeme koşulları ve 
    özel durumlar bu sayfada açıklanır.
    """
    return render_template('islem-ucretleri.html')


if __name__ == '__main__':
    """
    Flask uygulamasını başlat.
    
    Ortam Değişkenleri:
    - PORT: Sunucunun çalışacağı port (varsayılan: 5000)
    - FLASK_ENV: 'development' veya 'production' (varsayılan: development)
    - SECRET_KEY: Flask session'ları imzalamak için kullanılan gizli anahtar
    
    Çalıştırma Örnekleri:
    $ python3 app.py  # Varsayılan (localhost:5000, debug=True)
    $ PORT=5001 python3 app.py  # Custom port
    $ FLASK_ENV=production python3 app.py  # Production modu (debug=False)
    $ FLASK_ENV=development python3 app.py  # Development modu (debug=True, auto-reload)
    """
    port = int(os.environ.get('PORT', 5000))
    # Production'da debug=False kullan (güvenlik için)
    # Development'da debug=True kullan (hata ayıklama ve auto-reload için)
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    # host='0.0.0.0': Tüm ağ arayüzlerinden erişime izin ver (Heroku, Render gibi platformlar için gerekli)
    # port: Ortam değişkeninden veya varsayılan 5000'den al
    # debug: Debug modu aç/kapat
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
