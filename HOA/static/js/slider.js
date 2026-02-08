// Hero Slider JavaScript - Bilecik LIHKAB

let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides ? slides.length : 0;

function showSlide(index) {
    if (totalSlides === 0) return;
    
    // Index sınırlarını kontrol et
    if (index >= totalSlides) {
        currentSlide = 0;
    } else if (index < 0) {
        currentSlide = totalSlides - 1;
    } else {
        currentSlide = index;
    }
    
    // Tüm slide'ları gizle
    slides.forEach(slide => {
        slide.style.display = 'none';
    });
    
    // Aktif slide'ı göster
    if (slides[currentSlide]) {
        slides[currentSlide].style.display = 'block';
    }
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

function prevSlide() {
    showSlide(currentSlide - 1);
}

// Otomatik slider (5 saniyede bir)
function autoSlide() {
    if (totalSlides > 0) {
        setInterval(nextSlide, 5000);
    }
}

// Sayfa yüklendiğinde başlat
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        showSlide(0);
        autoSlide();
    });
} else {
    showSlide(0);
    autoSlide();
}
