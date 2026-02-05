/**
 * HERO SLIDER - Anasayfa Resim Döngüsü
 * ============================================================
 * 
 * AMAÇ:
 * Anasayfada dinamik resim carousel'ı (slider) oluşturur.
 * Ziyaretçilerin gözünü çeken resimleri otomatik olarak değiştirir.
 * 
 * ÖZELLIKLERI:
 * ✓ Otomatik ilerleme: Her 5 saniyede bir resimleri değiştirir
 * ✓ Manuel kontrol: Sonraki/Önceki butonları ile elle gezinme
 * ✓ Dot göstergeleri: Kaçıncı slide'da olduğunu gösterir
 * ✓ Responsive: Mobil ve masaüstünde sorunsuz çalışır
 * ✓ Performans: DOM caching, IIFE pattern ile optimize
 * 
 * KULLANILAN TEKNOLOJİ:
 * - IIFE (Immediately Invoked Function Expression): Global scope'u kirletmeden izole
 * - 'use strict': Sıkı hata kontrolü
 * - CSS classes: DOM manipülasyonunu optimize eder
 * - setInterval: Otomatik ilerleme timer'ı
 * 
 * VERSIYON: 2.0
 * SON GÜNCELLEME: 2026-02-05
 * 
 * HTML STRUKTUR:
 * <div class="slider-container">
 *   <div class="slider">
 *     <div class="slide">
 *       <img src="..." alt="...">
 *     </div>
 *     <!-- Daha fazla .slide öğeleri -->
 *   </div>
 *   <button class="prev" onclick="previousSlide()">❮</button>
 *   <button class="next" onclick="nextSlide()">❯</button>
 *   <div class="dots">
 *     <span class="dot" onclick="currentSlide(0)"></span>
 *     <!-- Daha fazla .dot öğeleri -->
 *   </div>
 * </div>
 * 
 * CSS CLASSLAR (style.css'de tanımlı):
 * - .slider: Slider container'ı
 * - .slide.active: Gösterilmesi gereken slide
 * - .dot.active: Aktif slide'ın göstergesi
 * 
 * ============================================================
 */

(function() {
    'use strict';
    
    /* ============================================================
       SLIDE DURUMU DEĞIŞKENLERI
       ============================================================ */
    
    // Şu anda gösterilen slide'ın indexi (0'dan başlar)
    let currentSlideIndex = 0;
    
    // Tüm slide öğelerine referans (DOM caching performans için)
    let slides = [];
    
    // Tüm dot (gösterge) öğelerine referans
    let dots = [];
    
    // Otomatik ilerleme timer referansı (durdurabilmek için)
    let autoAdvanceTimer = null;
    
    /* ============================================================
       SLIDER FONKSİYONLARI
       ============================================================ */
    
    /**
     * Belirtilen indexteki slide'ı göster ve diğerlerini gizle
     * 
     * @param {number} index - Gösterilecek slide'ın sıra numarası (0-indexed)
     * 
     * NASIL ÇALIŞIR:
     * 1. Index'i kontrol et (sınırlar içinde kalması için)
     * 2. Tüm slide'ların active class'ını kaldır
     * 3. Seçilen slide'a active class ekle
     * 4. Dot'ları da güncelle (hangi slide aktif göstermek için)
     * 
     * ÖRNEK:
     * showSlide(2) → 3. slide'ı göster (0,1,2 ← 3. slide)
     */
    function showSlide(index) {
        // Slide yoksa fonksiyondan çık
        if (slides.length === 0) return;
        
        /* Circular navigation: Son slide'ın sonuna gelirse başa dön */
        if (index >= slides.length) {
            currentSlideIndex = 0;  // Son slide'tan sonra 1. slide'a dön
        } else if (index < 0) {
            currentSlideIndex = slides.length - 1;  // İlk slide'tan önce sonuncuya dön
        } else {
            currentSlideIndex = index;
        }
        
        /* CSS classes kullanarak DOM manipülasyonunu optimize et */
        // Tüm slide'ları gez
        slides.forEach((slide, i) => {
            // Eğer i === currentSlideIndex ise active class ekle, yoksa çıkar
            slide.classList.toggle('active', i === currentSlideIndex);
        });
        
        /* Dot göstergelerini de güncelle */
        if (dots.length > 0) {
            dots.forEach((dot, i) => {
                // Aktif slide'ın dot'ı vurgulanır
                dot.classList.toggle('active', i === currentSlideIndex);
            });
        }
    }
    
    /**
     * Slide'ları ileri/geri kaydır
     * 
     * @param {number} direction - Kaydırma yönü (+1: sonraki, -1: önceki)
     * 
     * KULLANIM:
     * changeSlide(1) → Sonraki slide
     * changeSlide(-1) → Önceki slide
     */
    function changeSlide(direction) {
        showSlide(currentSlideIndex + direction);
        // Otomatik ilerleme timer'ını sıfırla (kullannıcı müdahalesi)
        resetAutoAdvance();
    }
    
    /**
     * Doğrudan belirtilen slide'ı göster
     * 
     * @param {number} index - Gösterilecek slide indexi
     * 
     * KULLANIM:
     * <span class="dot" onclick="currentSlide(0)"></span> → İlk slide'ı göster
     */
    function currentSlide(index) {
        showSlide(index);
        resetAutoAdvance();
    }
    
    /**
     * Otomatik ilerlemeyi başlat - Her 5 saniyede bir sonraki slide
     */
    function startAutoAdvance() {
        autoAdvanceTimer = setInterval(() => {
            changeSlide(1);
        }, 5000);  // 5000ms = 5 saniye
    }
    
    /**
     * Otomatik ilerleme timer'ını sıfırla
     * 
     * Ne zaman çağrılır:
     * - Kullanıcı Sonraki/Önceki butonu tıkladığında
     * - Kullanıcı dot'a tıkladığında
     * - Timer'ı durdur ve yeniden başlat (aralık sıfırlanır)
     */
    function resetAutoAdvance() {
        clearInterval(autoAdvanceTimer);
        startAutoAdvance();
    }
    
    /* ============================================================
       BAŞLATMA (INITIALIZATION)
       ============================================================
       Sayfa tamamen yüklendikten sonra slider'ı ayarla.
    */
    
    /**
     * DOM hazır olduğunda slider'ı başlat
     * 
     * NE YAPILIR:
     * 1. HTML'deki tüm .slide öğelerini bul ve sakla
     * 2. HTML'deki tüm .dot öğelerini bul ve sakla
     * 3. İlk slide'ı göster (showSlide(0))
     * 4. Otomatik ilerlemeyi başlat (startAutoAdvance)
     * 
     * NE ZAMAN ÇALIŞIR:
     * - Sayfa tamamen yüklendiğinde (DOMContentLoaded event'inde)
     */
    document.addEventListener('DOMContentLoaded', () => {
        // Tüm slide öğelerini seç ve sakla
        slides = document.querySelectorAll('.slide');
        
        // Tüm dot öğelerini seç ve sakla
        dots = document.querySelectorAll('.dot');
        
        // Eğer en az bir slide varsa
        if (slides.length > 0) {
            // İlk slide'ı göster (index: 0)
            showSlide(0);
            
            // Otomatik ilerlemeyi başlat
            startAutoAdvance();
        }
    });
    
    /* ============================================================
       GLOBAL FONKSIYONLARI AÇIĞA ÇIKAR
       ============================================================
       HTML'deki onclick event'leri kullanabilmek için
       fonksiyonları window object'ine ata.
       
       KULLANIM:
       <button onclick="changeSlide(1)">Sonraki</button>
       <span class="dot" onclick="currentSlide(0)"></span>
    */
    
    // Sonraki/Önceki butonu için
    window.changeSlide = changeSlide;
    
    // Dot indicator'leri için
    window.currentSlide = currentSlide;
    
})();  // IIFE sonu - scope izolasyonunu kapat
