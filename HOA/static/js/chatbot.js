// AI Chatbot JavaScript - Bilecik LIHKAB

// Chatbot açma/kapatma
function toggleChatbot() {
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    
    if (chatbotWindow.style.display === 'none') {
        chatbotWindow.style.display = 'flex';
        chatbotToggle.style.display = 'none';
    } else {
        chatbotWindow.style.display = 'none';
        chatbotToggle.style.display = 'flex';
    }
}

// Enter tuşuna basınca mesaj gönder
function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

// Hızlı mesaj gönderme
function sendQuickMessage(message) {
    document.getElementById('chatbot-input').value = message;
    sendChatMessage();
}

// Mesaj gönderme
function sendChatMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Kullanıcı mesajını göster
    addMessage(message, 'user');
    input.value = '';
    
    // Bot düşünüyor göstergesi
    addTypingIndicator();
    
    // Simüle edilmiş bot yanıtı (gerçek AI entegrasyonu için API çağrısı yapılabilir)
    setTimeout(() => {
        removeTypingIndicator();
        const response = generateBotResponse(message);
        addMessage(response, 'bot');
    }, 1500);
}

// Mesaj ekleme
function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = text;
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Yazıyor göstergesi
function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatbot-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message bot-message';
    typingDiv.innerHTML = '<div class="message-content typing"><span></span><span></span><span></span></div>';
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

// Bot yanıtı oluşturma (Basit AI simülasyonu - gerçek entegrasyon için OpenAI/Claude API kullanılabilir)
function generateBotResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Hizmet sorguları
    if (lowerMessage.includes('aplikasyon')) {
        return `
            <strong>📍 Aplikasyon Hizmeti</strong><br><br>
            Aplikasyon, taşınmazların kadastro müdürlüğüne gerçek yerlerinin gösterilmesidir.<br><br>
            <strong>Gerekli Belgeler:</strong><br>
            • Tapu fotokopisi<br>
            • Kimlik fotokopisi<br><br>
            <strong>Süre:</strong> 3-5 iş günü<br><br>
            Detaylı bilgi için: <a href="/aplikasyon">Aplikasyon Sayfası</a><br>
            Fiyat teklifi için: <a href="/online-basvuru">Online Başvuru</a>
        `;
    }
    
    if (lowerMessage.includes('cins değişikliği') || lowerMessage.includes('cins degisikligi')) {
        return `
            <strong>🏗️ Cins Değişikliği Hizmeti</strong><br><br>
            Taşınmaz cinsinin (arsa/arazi) değiştirilmesi işlemidir.<br><br>
            <strong>Ne Zaman Gerekir?</strong><br>
            • Tarla/arazi üzerine bina yapıldığında<br>
            • İmar planı değişikliğinde<br><br>
            Detaylar: <a href="/cins-degisikligi">Cins Değişikliği Sayfası</a>
        `;
    }
    
    if (lowerMessage.includes('birleştirme') || lowerMessage.includes('birlestirme')) {
        return `
            <strong>🔗 Birleştirme Hizmeti</strong><br><br>
            Bitişik parsellerin tek parsel haline getirilmesidir.<br><br>
            <strong>Avantajları:</strong><br>
            • Tek tapu<br>
            • Proje kolaylığı<br>
            • Maliyet tasarrufu<br><br>
            Detaylar: <a href="/birlestirme">Birleştirme Sayfası</a>
        `;
    }
    
    if (lowerMessage.includes('irtifak')) {
        return `
            <strong>⚖️ İrtifak Hakkı Hizmetleri</strong><br><br>
            <strong>İrtifak Hakkı Tesisi:</strong> Taşınmaz üzerine elektrik/su/doğalgaz hattı geçişi<br>
            <strong>İrtifak Hakkı Terkini:</strong> Mevcut irtifak hakkının kaldırılması<br><br>
            • <a href="/irtifak-hakki-tesisi">İrtifak Tesisi</a><br>
            • <a href="/irtifak-hakki-terkini">İrtifak Terkini</a>
        `;
    }
    
    if (lowerMessage.includes('fiyat') || lowerMessage.includes('ücret') || lowerMessage.includes('tarife')) {
        return `
            <strong>💰 Hizmet Ücretleri</strong><br><br>
            Ücretlerimiz işlem tipine, parselin konumuna ve büyüklüğüne göre değişmektedir.<br><br>
            Güncel fiyat listesi: <a href="/islem-ucretleri">İşlem Ücretleri Sayfası</a><br><br>
            Özel fiyat teklifi için: <a href="/online-basvuru">Online Başvuru Yapın</a><br>
            veya bizi arayın: <a href="tel:+905403141401">0540 314 14 01</a>
        `;
    }
    
    if (lowerMessage.includes('randevu') || lowerMessage.includes('görüşme')) {
        return `
            <strong>📅 Randevu Al</strong><br><br>
            Randevu almak için:<br><br>
            1️⃣ <strong>Telefon:</strong> <a href="tel:+905403141401">0540 314 14 01</a><br>
            2️⃣ <strong>Online Form:</strong> <a href="/online-basvuru">Online Başvuru</a><br>
            3️⃣ <strong>E-posta:</strong> <a href="mailto:mail@bileciklihkab.com">mail@bileciklihkab.com</a><br><br>
            <strong>Çalışma Saatleri:</strong> Pazartesi-Cuma 09:00-18:00
        `;
    }
    
    if (lowerMessage.includes('hizmet') || lowerMessage.includes('neler yapıyorsunuz')) {
        return `
            <strong>📋 Hizmetlerimiz</strong><br><br>
            <strong>Ana Hizmetler:</strong><br>
            • Aplikasyon<br>
            • Cins Değişikliği<br>
            • Birleştirme<br>
            • İrtifak Hakkı Tesisi/Terkini<br>
            • Bağımsız Bölüm Yer Gösterme<br><br>
            <strong>Diğer Hizmetler:</strong><br>
            • Parselasyon<br>
            • Röperli Kroki<br>
            • Halihazır Harita<br>
            • İmar Planı Uygulamaları<br>
            • ve daha fazlası...<br><br>
            Tüm hizmetler: <a href="/#hizmetler">Hizmetler Bölümü</a>
        `;
    }
    
    if (lowerMessage.includes('neredesiniz') || lowerMessage.includes('adres') || lowerMessage.includes('konum')) {
        return `
            <strong>📍 Adres Bilgilerimiz</strong><br><br>
            <strong>Adres:</strong><br>
            Kasımpaşa Mh. Hükümet Cd.<br>
            Belediye İşhanı No:2/105<br>
            Bozüyük / BİLECİK<br><br>
            <strong>Telefon:</strong> <a href="tel:+905403141401">0540 314 14 01</a><br>
            <strong>E-posta:</strong> <a href="mailto:mail@bileciklihkab.com">mail@bileciklihkab.com</a><br><br>
            Detaylar: <a href="/iletisim">İletişim Sayfası</a>
        `;
    }
    
    if (lowerMessage.includes('bilecik') || lowerMessage.includes('osmaneli') || lowerMessage.includes('pazaryeri') || 
        lowerMessage.includes('gölpazarı') || lowerMessage.includes('söğüt') || lowerMessage.includes('bozüyük')) {
        return `
            <strong>🗺️ Hizmet Bölgelerimiz</strong><br><br>
            Bilecik il ve ilçelerinde hizmet veriyoruz:<br><br>
            ✅ Bilecik Merkez<br>
            ✅ Bozüyük<br>
            ✅ Gölpazarı<br>
            ✅ İnhisar<br>
            ✅ Osmaneli<br>
            ✅ Pazaryeri<br>
            ✅ Söğüt<br>
            ✅ Yenipazar<br><br>
            1998'den beri profesyonel hizmet!
        `;
    }
    
    if (lowerMessage.includes('teşekkür') || lowerMessage.includes('sağol') || lowerMessage.includes('thanks')) {
        return 'Rica ederim! Başka bir konuda yardımcı olabilir miyim? 😊';
    }
    
    // Varsayılan yanıt
    return `
        Anlayamadım, lütfen daha açık sorabilir misiniz?<br><br>
        Şunları sorabilirsiniz:<br>
        • "Aplikasyon nedir?"<br>
        • "Fiyatlar ne kadar?"<br>
        • "Randevu almak istiyorum"<br>
        • "Hangi hizmetleri veriyorsunuz?"<br><br>
        veya direkt <a href="tel:+905403141401">0540 314 14 01</a> numaralı telefonu arayabilirsiniz.
    `;
}

// Sayfa yüklendiğinde hoş geldin mesajı göster
window.addEventListener('load', function() {
    // İlk ziyarette chatbot'u otomatik aç (opsiyonel)
    // setTimeout(() => {
    //     if (!sessionStorage.getItem('chatbotShown')) {
    //         toggleChatbot();
    //         sessionStorage.setItem('chatbotShown', 'true');
    //     }
    // }, 3000);
});
