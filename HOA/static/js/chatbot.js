
// Modern, öneri butonlu, localStorage destekli chatbot

const chatbotData = [
    {
        keywords: ["aplikasyon"],
        response: `<strong>📍 Aplikasyon Hizmeti</strong><br>Aplikasyon, taşınmazların kadastro müdürlüğüne gerçek yerlerinin gösterilmesidir.<br><strong>Gerekli Belgeler:</strong> Tapu fotokopisi, Kimlik fotokopisi<br><strong>Süre:</strong> 3-5 iş günü<br>Detaylı bilgi için: <a href='/aplikasyon'>Aplikasyon Sayfası</a> | <a href='/online-basvuru'>Online Başvuru</a>`
    },
    {
        keywords: ["cins değişikliği", "cins degisikligi"],
        response: `<strong>🏗️ Cins Değişikliği Hizmeti</strong><br>Taşınmaz cinsinin (arsa/arazi) değiştirilmesi işlemidir.<br>Ne Zaman Gerekir? Tarla/arazi üzerine bina yapıldığında, İmar planı değişikliğinde.<br>Detaylar: <a href='/cins-degisikligi'>Cins Değişikliği Sayfası</a>`
    },
    {
        keywords: ["birleştirme", "birlestirme"],
        response: `<strong>🔗 Birleştirme Hizmeti</strong><br>Bitişik parsellerin tek parsel haline getirilmesidir.<br>Avantajları: Tek tapu, Proje kolaylığı, Maliyet tasarrufu.<br>Detaylar: <a href='/birlestirme'>Birleştirme Sayfası</a>`
    },
    {
        keywords: ["irtifak"],
        response: `<strong>⚖️ İrtifak Hakkı Hizmetleri</strong><br>İrtifak Hakkı Tesisi: Taşınmaz üzerine elektrik/su/doğalgaz hattı geçişi<br>İrtifak Hakkı Terkini: Mevcut irtifak hakkının kaldırılması<br><a href='/irtifak-hakki-tesisi'>İrtifak Tesisi</a> | <a href='/irtifak-hakki-terkini'>İrtifak Terkini</a>`
    },
    {
        keywords: ["fiyat", "ücret", "tarife"],
        response: `<strong>💰 Hizmet Ücretleri</strong><br>Ücretlerimiz işlem tipine, parselin konumuna ve büyüklüğüne göre değişmektedir.<br>Güncel fiyat listesi: <a href='/islem-ucretleri'>İşlem Ücretleri</a> | <a href='/online-basvuru'>Online Başvuru</a> | <a href='tel:+905403141401'>0540 314 14 01</a>`
    },
    {
        keywords: ["randevu", "görüşme"],
        response: `<strong>📅 Randevu Al</strong><br>Randevu için: <a href='tel:+905403141401'>0540 314 14 01</a> | <a href='/online-basvuru'>Online Başvuru</a> | <a href='mailto:mail@bileciklihkab.com'>mail@bileciklihkab.com</a><br>Çalışma Saatleri: Pazartesi-Cuma 09:00-18:00` 
    },
    {
        keywords: ["hizmet", "neler yapıyorsunuz"],
        response: `<strong>📋 Hizmetlerimiz</strong><br>Ana Hizmetler: Aplikasyon, Cins Değişikliği, Birleştirme, İrtifak Hakkı Tesisi/Terkini, Bağımsız Bölüm Yer Gösterme<br>Diğer: Parselasyon, Röperli Kroki, Halihazır Harita, İmar Planı Uygulamaları...<br><a href='/#hizmetler'>Tüm Hizmetler</a>`
    },
    {
        keywords: ["neredesiniz", "adres", "konum"],
        response: `<strong>📍 Adres Bilgilerimiz</strong><br>Kasımpaşa Mh. Hükümet Cd.<br>Belediye İşhanı No:2/105<br>Bozüyük / BİLECİK<br><a href='/iletisim'>İletişim</a>`
    },
    {
        keywords: ["bilecik", "osmaneli", "pazaryeri", "gölpazarı", "söğüt", "bozüyük"],
        response: `<strong>🗺️ Hizmet Bölgelerimiz</strong><br>Bilecik il ve ilçelerinde hizmet veriyoruz: Bilecik Merkez, Bozüyük, Gölpazarı, İnhisar, Osmaneli, Pazaryeri, Söğüt, Yenipazar.`
    },
    {
        keywords: ["teşekkür", "sağol", "thanks"],
        response: `Rica ederim! Başka bir konuda yardımcı olabilir miyim? 😊`
    }
];

const chatbotSuggestions = [
    "Aplikasyon nedir?",
    "Fiyatlar ne kadar?",
    "Randevu almak istiyorum",
    "Adresiniz nerede?",
    "Hangi hizmetleri veriyorsunuz?"
];

function toggleChatbot() {
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    if (chatbotWindow.style.display === 'none') {
        chatbotWindow.style.display = 'flex';
        chatbotToggle.style.display = 'none';
        setTimeout(() => {
            document.getElementById('chatbot-input').focus();
        }, 200);
    } else {
        chatbotWindow.style.display = 'none';
        chatbotToggle.style.display = 'flex';
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

function sendQuickMessage(message) {
    document.getElementById('chatbot-input').value = message;
    sendChatMessage();
}

function sendChatMessage() {
    const input = document.getElementById('chatbot-input');
    const message = input.value.trim();
    if (!message) return;
    addMessage(message, 'user');
    input.value = '';
    addTypingIndicator();
    setTimeout(() => {
        removeTypingIndicator();
        const response = generateBotResponse(message);
        addMessage(response, 'bot');
        saveChatHistory();
        showSuggestions();
    }, 900);
    saveChatHistory();
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = text;
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

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

function generateBotResponse(message) {
    const lowerMessage = message.toLowerCase();
    for (const item of chatbotData) {
        if (item.keywords.some(k => lowerMessage.includes(k))) {
            return item.response;
        }
    }
    return `Anlayamadım, lütfen daha açık sorabilir misiniz?<br><br>Şunları sorabilirsiniz:<br>• "Aplikasyon nedir?"<br>• "Fiyatlar ne kadar?"<br>• "Randevu almak istiyorum"<br>• "Hangi hizmetleri veriyorsunuz?"<br><br>veya <a href='tel:+905403141401'>0540 314 14 01</a> numaralı telefonu arayabilirsiniz.`;
}

function showSuggestions() {
    const suggestionsDiv = document.getElementById('chatbot-suggestions');
    if (!suggestionsDiv) return;
    suggestionsDiv.innerHTML = '';
    chatbotSuggestions.forEach(s => {
        const btn = document.createElement('button');
        btn.className = 'chatbot-suggestion-btn';
        btn.innerText = s;
        btn.onclick = () => sendQuickMessage(s);
        suggestionsDiv.appendChild(btn);
    });
}

function saveChatHistory() {
    const messagesContainer = document.getElementById('chatbot-messages');
    localStorage.setItem('chatbotHistory', messagesContainer.innerHTML);
}

function loadChatHistory() {
    const messagesContainer = document.getElementById('chatbot-messages');
    const history = localStorage.getItem('chatbotHistory');
    if (history) {
        messagesContainer.innerHTML = history;
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

window.addEventListener('load', function() {
    loadChatHistory();
    showSuggestions();
});
