#!/usr/bin/env python3
"""
Filament Karar Motoru - Streamlit Web Uygulaması
------------------------------------------------
Web tarayıcısında çalışan interaktif filament seçim aracı

Çalıştırma:
streamlit run app_streamlit.py
"""

import streamlit as st
import pandas as pd
from filament_karar_motoru import FILAMENT_DATA, COLUMNS

# ============================================================================
# POPULER 3D YAZICI VERITABANI
# ============================================================================
YAZICI_VERITABANI = {
    # CREALITY YAZICILARI
    "Creality Ender 3": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Creality Ender 3 V2": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Creality Ender 3 V3": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    "Creality Ender 3 S1": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Creality Ender 3 S1 Pro": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Creality Ender 5": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Creality Ender 5 S1": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Creality Ender 5 Pro": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Creality CR-10": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Creality CR-10 S5": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Creality CR-X": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Creality Sermoon D1": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    
    # BAMBU LAB YAZICILARI
    "Bambu Lab X1": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 110,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Bambu Lab X1 Carbon": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 110,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Bambu Lab P1P": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 110,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Bambu Lab P1S": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 110,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Bambu Lab A1": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Bambu Lab A1 Mini": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    
    # ELEGOO YAZICILARI
    "Elegoo Neptune 3": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Elegoo Neptune 3 Pro": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Elegoo Neptune 3 Plus": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Elegoo Neptune 4": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    "Elegoo Neptune 4 Pro": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    "Elegoo Neptune 4 Plus": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    
    # PRUSA YAZICILARI
    "Prusa i3 MK3S+": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 280,
        "ekstruder_tipi": "Direct"
    },
    "Prusa i3 MK4": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Prusa XL": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    
    # ANYCUBIC YAZICILARI
    "Anycubic i3 Mega": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Anycubic i3 Mega S": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Anycubic Vyper": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Anycubic Vyper XL": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Anycubic 4Max Pro": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 80,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    
    # ARTILLERY YAZICILARI
    "Artillery Sidewinder X1": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Artillery Sidewinder X2": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Artillery Sidewinder X3": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    
    # ANET YAZICILARI
    "Anet A8": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Anet A6": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Anet ET4": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    
    # DIGER POPULER YAZICILAR
    "Ultimaker S5": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 280,
        "ekstruder_tipi": "Direct"
    },
    "Ultimaker S3": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 280,
        "ekstruder_tipi": "Direct"
    },
    "Flashforge Creator Pro": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Direct"
    },
    "Raise3D E2": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 110,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Raise3D Pro 2": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 110,
        "max_nozul_sicaklik": 300,
        "ekstruder_tipi": "Direct"
    },
    "Tronxy X5SA": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Geeetech A10": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Epax E180": {
        "kapali_kasa": False,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Longer LK4 Pro": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 60,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
    "Flashforge Hunter": {
        "kapali_kasa": True,
        "isitmali_yatak": True,
        "sert_nozul": False,
        "max_yatak_sicaklik": 100,
        "max_nozul_sicaklik": 260,
        "ekstruder_tipi": "Bowden"
    },
}

# Sayfa yapılandırması
st.set_page_config(
    page_title="Filament Karar Motoru",
    page_icon="🔧",
    layout="wide"
)

# Başlık
st.title("🔧 Filament Karar Motoru PRO++")
st.markdown("**FDM 3D yazıcınız için en uygun filamenti bulun**")
st.divider()

# ============================================================================
# BASKL SORUNLARI VERITABANI - KAPSAMLI ÇÖZÜM REHBERI
# ============================================================================
BASKI_SORUNLARI = {
    "İlk Katman Yapışması": {
        "açıklama": "Baskının ilk katmanı tabla üzerine yapışmıyor veya kötü yapışıyor",
        "semptomlar": [
            "Filament tabla ile temas kurmuyor veya kayıyor",
            "Kıvrılmış veya dağınık katman",
            "Baskı sırasında tabla oynatma gerekliliği",
            "Nozzul açık havada kalıyor (filament çekilmiş)"
        ],
        "genel_çözümler": [
            "1️⃣ Tabla Hazırlığı: Tabla yüzeyini % isopropil alkol veya seramik temizleyici ile temizle",
            "2️⃣ Z-Offset Ayarı: Nozzul tabla ile hafif temas etmeli (kum kağıdı kalınlığında mesafe)",
            "3️⃣ Tabla Hızı: İlk katmanı 50-70% hızda bas (normal hızın %50'si)",
            "4️⃣ Tabla Sıcaklığı: Filament türüne göre +5-10°C arttır",
            "5️⃣ Yapışkan: Hairspray, glue stick veya PVA yapışkanı kullan",
            "6️⃣ Yüzey Aşındırması: Cam tabla veya PEI yüzeyini kum kağıdı (150-180 grit) ile hafifçe aşındır",
            "7️⃣ Nozzul Sıcaklığı: +5°C arttırdığında filament daha akışkan olur",
            "8️⃣ Yapısı (Raft): Brim ekle veya raft kullan - yapışma alanı artar"
        ],
        "filament_özellikleri": {
            "IlkKatmanYapisma": {
                "kritik": 60,
                "tavsiye_düşük": "Tabla yüzeyini özel kimyasallarla hazırlayın veya yapışkan kullanın",
                "tavsiye_yüksek": "Normal şartlarda iyi yapışacak, sadece temizlik yeterli"
            }
        }
    },
    
    "Underextrusion (Filament Yetersiz)": {
        "açıklama": "Nozzuldan çok az filament çıkıyor, baskı boşluklu ve zayıf görünüyor",
        "semptomlar": [
            "Boşluklu çevreler (perimeter)",
            "Zayıf detaylar ve kopuk çizgiler",
            "Baskı şeffaf veya transparan görünüyor",
            "Dış yüzeyde delikler var"
        ],
        "genel_çözümler": [
            "1️⃣ Flow Ayarı: Slicer'da flow rate'i %100'den %105-110'a çıkar",
            "2️⃣ E-Steps Kalibrasyonu: Ekstruder motor adımlarını kalibre et (100mm test)",
            "3️⃣ Filament Kalınlığı: Filament kalınlığını micrometer ile ölç (1.75 veya 2.85mm)",
            "4️⃣ Nozzul Sıcaklığı: +5-10°C arttır (filament akışlı olsun)",
            "5️⃣ Baskı Hızı: Hızı azalt (%20-30 düşür)",
            "6️⃣ Filament Basıncı: Ekstruder feederin filamenti sıkıştırıp sıkıştırmadığını kontrol et",
            "7️⃣ Nozzul Tıkanması: Nozzulun tıkanık olmadığını kontrol et",
            "8️⃣ Retract Ayarları: Retract mesafesi çok fazla ise azalt"
        ],
        "filament_özellikleri": {}
    },
    
    "Overextrusion (Fazla Filament)": {
        "açıklama": "Nozzuldan çok fazla filament çıkıyor, baskı puflaştırılmış görünüyor",
        "semptomlar": [
            "Baskı şişmiş ve puflaştırılmış",
            "Yapışkan ve temas eden parçalar",
            "Çevre kalınlığı hedeften fazla",
            "Detay kaybı (ince bölümler birleşiyor)"
        ],
        "genel_çözümler": [
            "1️⃣ Flow Rate: Slicer'da flow rate'i %100'den %95-90'a düşür",
            "2️⃣ E-Steps: Ekstruder motor adımlarını tekrar kalibre et",
            "3️⃣ Nozzul Kalınlığı: 0.4mm nozzul kullanıyorsan kontrol et (1/3 çapı değişirse etki büyük)",
            "4️⃣ Line Width: Slicer'da line width'i nozzul çapıyla eşleştir (0.4mm nozzul = 0.4mm width)",
            "5️⃣ Nozzul Sıcaklığı: -5°C düşür (daha az akışkan)",
            "6️⃣ Baskı Hızı: Hızı arttır",
            "7️⃣ Yatak Sıcaklığı: Filament yatak sıcaklığında çok yumuşaksa - sıcaklık azalt",
            "8️⃣ Nozzul Temizliği: Nozzulun alt kısmında kalıntı varsa temizle"
        ],
        "filament_özellikleri": {}
    },
    
    "Banding / Layer Ghosting": {
        "açıklama": "Baskı yüzeyinde periyodik tabaka izleri veya dalgalar görülüyor",
        "semptomlar": [
            "Düzenli aralıklarla yatay çizgiler",
            "Dalgalı veya pütürlü yüzey",
            "Görüntü tekrar eden desen şeklinde",
            "STL dosyada olmayan kalıplar görülüyor"
        ],
        "genel_çözümler": [
            "1️⃣ Tabla Tutarlılığı: Tabla yüzeyinin düz olup olmadığını kontrol et (level alma)",
            "2️⃣ Mekanik: Z-aks ilerlemesini kontrol et (Z-rod'u temizle ve yağla)",
            "3️⃣ Baskı Hızı: Hızı azalt ve tutarlı tut (değişken hız banding yaratabilir)",
            "4️⃣ Jerk Ayarları: Firmware'de jerk değerlerini azalt (güvenli hızlanma)",
            "5️⃣ Nozzul Sıcaklığı: Sabit tut (dalgalanmayan sıcaklık)",
            "6️⃣ Fan Hızı: Sabit tutmalı (değişken soğutma banding yaratır)",
            "7️⃣ İçinde Boş Alan: Banding kalıbı 3D modelinin içindeki boşluklardan kaynaklanabilir",
            "8️⃣ Firmware Update: Son firmware sürümüne güncelle (Z banding iyileştirmeleri olabilir)"
        ],
        "filament_özellikleri": {}
    },
    
    "İpliklenme (Stringing)": {
        "açıklama": "Baskının farklı bölümleri arasında ince iplikler kalıyor",
        "semptomlar": [
            "Web benzeri ince filament iplikler",
            "Raf kenarlarında dangıl filamentler",
            "Detaylı bölümlerde iplik oluşumu"
        ],
        "genel_çözümler": [
            "Retract mesafesini arttırın (2-6 mm arasında test edin)",
            "Retract hızını arttırın (40-60 mm/s)",
            "Nozzle sıcaklığını 5-10°C azaltın",
            "Baskı hızını azaltın (10-20% düşürün)",
            "Travel hızını arttırın",
            "Stringing test modelini slicing programından baskılaştırın",
            "Slicing programında 'Combing' veya 'Avoid crossing perimeters' etkinleştirin"
        ],
        "filament_özellikleri": {
            "StringOlusumu": {
                "kritik": 40,
                "tavsiye_düşük": "Retract ayarlarını iyileştirmek gerekebilir, daha bilinçli ayarlar lazım",
                "tavsiye_yüksek": "Bu filament az ipliklenme yapıyor, temel ayarlar yeterli"
            }
        }
    },
    
    "Warping (Raf Bükülmesi)": {
        "açıklama": "Baskının köşeleri veya kenarları yukarı kalkıyor ve büküyor",
        "semptomlar": [
            "Raf köşeleri yukarı doğru kıvrılıyor",
            "Baskı başlangıcında raf dışa çıkıyor",
            "Soğuma sırasında şekil değişimi"
        ],
        "genel_çözümler": [
            "Yatak sıcaklığını 5-10°C arttırın",
            "Kapalı kasa kullanın (ortam sıcaklığını 30-40°C tut)",
            "Baskı alanını kaplayın (Enclosure, tent veya kapalı kutu)",
            "Rafın çevresine raf köprüsü (brim veya skirt) ekleyin",
            "Soğutma fanını azaltın veya kapatın",
            "Baskı hızını azaltın",
            "İlk katman sıcaklığını daha yüksek tutun (ilk 5-10 katman)",
            "Tabla yapışkanlı mat kullanın (daha iyi yapışma)"
        ],
        "filament_özellikleri": {
            "WarpingDirenci": {
                "kritik": 70,
                "tavsiye_düşük": "Warping eğilimi yüksek - yatak sıcaklığını max çıkar ve kasa kapa",
                "tavsiye_yüksek": "Bu filament warping konusunda dirençli, standart ayarlar yeterli"
            }
        }
    },
    
    "Kötü Yüzey Kalitesi": {
        "açıklama": "Baskının yüzeyi pürüzlü, mat veya düzensiz görünüyor",
        "semptomlar": [
            "Tabaka izi (banding) görülüyor",
            "Pürüzlü, zımparalanmış görüntü",
            "Mat veya cansız görünüş",
            "Detay kaybı"
        ],
        "genel_çözümler": [
            "Baskı hızını azaltın (25-50% düşürün)",
            "Nozzle sıcaklığını optimize edin (5°C aralıklarında test et)",
            "Soğutma fanını %100'e çıkarın (PLA için)",
            "Layer height'ı azaltın (0.2mm yerine 0.12-0.16mm)",
            "Filament kalitesinin iyi olduğundan emin ol",
            "Ekstruder ilerlemesini kontrol et (filament sıkışmış olabilir)",
            "Tabla leveling'i iyileştir",
            "Baskı kafasını temizle (nozzul ve hotend temiz tutulmalı)"
        ],
        "filament_özellikleri": {
            "BaskiKolayligi": {
                "kritik": 60,
                "tavsiye_düşük": "Baskı hassas - ayarlar kritik, sabır gerekli",
                "tavsiye_yüksek": "Bu filament sağlam, temel optimizasyon yeterli"
            }
        }
    },
    
    "Bridges Başarısız Olması": {
        "açıklama": "Boş alanlara köprü atılan filament düşüyor veya koparılıyor",
        "semptomlar": [
            "Köprü alanları eksik veya çökmüş",
            "Sarkan filament yapısı",
            "Tulostin detay bölümlerinde problemler"
        ],
        "genel_çözümler": [
            "Bridge akışını azaltın (%90'a ayarlayın)",
            "Köprü fanını max yapın (cooling fan %100)",
            "Köprü hızını azaltın (25-40 mm/s)",
            "Nozzle sıcaklığını azaltın (daha hızlı katılaşma)",
            "Retract ayarlarını iyileştir (köprüden çıkışta sorun)",
            "Slicing programında köprü ayarlarını optimize et"
        ],
        "filament_özellikleri": {
            "KoprulemeYeteneği": {
                "kritik": 60,
                "tavsiye_düşük": "Köprüleme zayıf - daha yavaş ve soğutmalı baskı gerekli",
                "tavsiye_yüksek": "Bu filament köprüye uygun, standart ayarlar yeterli"
            }
        }
    },
    
    "Çıkıntı (Overhang) Başarısız": {
        "açıklama": "Destek olmadan çıkan geometriler başarısız oluyor",
        "semptomlar": [
            "Çıkıntı kısımları çöküyor veya sarkan",
            "Angled geometry'ler kötü çıkıyor",
            "Ince kenarlar başarısız"
        ],
        "genel_çözümler": [
            "Çıkıntı açısını sınırlayın (<45° için destek)",
            "Soğutma fanını %100'e çıkarın",
            "Baskı hızını azaltın",
            "Nozzle sıcaklığını azaltın",
            "Filament akışını azaltın (%85-95%)",
            "Model tasarımını düzeltin (çıkıntı açılarını azalt)",
            "Destek ekle (malzeme israfı fakat kalite artar)"
        ],
        "filament_özellikleri": {
            "CikintiPerformansi": {
                "kritik": 60,
                "tavsiye_düşük": "Çıkıntı yeteneği zayıf - destek eklemeyi düşün",
                "tavsiye_yüksek": "Bu filament çıkıntılara uygun, minimal destek yeterli"
            }
        }
    },
    
    "Nozzle Tıkanması": {
        "açıklama": "Hotend veya nozzle filament akışını engellediği için baskı duruyor",
        "semptomlar": [
            "Aniden filament akışı durması",
            "Nozzul filament dışarı çıkarmıyor",
            "Fan hızında değişiklik durumuyla ilgili",
            "Baskının ortasında filament çıkmıyor"
        ],
        "genel_çözümler": [
            "Nozzulu temizle (1.5-2mm drill ile veya nozzle temizleme seti)",
            "Hotend'i soğut ve filamenti geri çekmeye çalış",
            "Filamentı kaldır ve yenisini yükle",
            "Hotend sıcaklığını optimal yapı (filament tipine göre +5°C)",
            "Nozzl/hotend kalibrasyonunu kontrol et",
            "E-steps kalibrasyonunu yap (ekstruder motor basamakları)",
            "Filament kalitesini kontrol et (toz/nem olabilir)",
            "Pressure advance/linear advance ayarını optimize et"
        ],
        "filament_özellikleri": {}
    },
    
    "Excessive Cooling (Fazla Soğutma)": {
        "açıklama": "Filament fazla soğunca, katmanlar birbirine yapışmıyor",
        "semptomlar": [
            "Katmanlar arasında boşluk (delamination)",
            "Baskı kırılgan ve çabuk kırılıyor",
            "Katman aderansı zayıf"
        ],
        "genel_çözümler": [
            "Fan hızını azaltın (%30-50'ye düşür)",
            "İlk 2-3 katmanı fan kapalı başlat",
            "Nozzle sıcaklığını arttır (tutuşabilir filament için)",
            "Print hızını azalt (filament daha iyi yapışsın)",
            "Yatak sıcaklığını optimize et",
            "Filament tipine uygun soğutma seviyesi bul (ABS=%0-20, PLA=%100)"
        ],
        "filament_özellikleri": {}
    },
    
    "Insufficient Adhesion Between Layers": {
        "açıklama": "Katmanlar arasında yeterli tutunma yok, baskı zayıf",
        "semptomlar": [
            "Katman aderansı düşük",
            "Baskı kolayca kırılabiliyor",
            "Detaylar koparılabiliyor"
        ],
        "genel_çözümler": [
            "1️⃣ Nozzul Sıcaklığı: +5-10°C arttır (filament daha akışkan olur)",
            "2️⃣ Soğutma Fanı: %10-30'a düşür (katmanlar daha iyi yapışsın)",
            "3️⃣ Baskı Hızı: 20-30% azalt",
            "4️⃣ Line Width: Arttır (daha kalın katmanlar = daha iyi yapışma)",
            "5️⃣ Pressure Advance: İyileştir (filament basıncı optimize)",
            "6️⃣ İlk Katman Sıcaklığı: Daha yüksek tutun",
            "7️⃣ Yatak Sıcaklığı: +5°C arttır",
            "8️⃣ Ekstruder Basıncı: Feeder dişlisini kontrol et"
        ],
        "filament_özellikleri": {
            "KatmanAderans": {
                "kritik": 60,
                "tavsiye_düşük": "Katman yapışması zayıf - sıcaklık ve hız ayarı kritik",
                "tavsiye_yüksek": "Bu filament katman yapışmasında iyi, standart ayarlar yeterli"
            }
        }
    },
    
    "Elephant Foot (Tabanda Çıkıntı)": {
        "açıklama": "Baskının taban katmanları yanlarında şişiyor, fil ayağı gibi görünüyor",
        "semptomlar": [
            "Taban çıkıntılı ve kalın görünüyor",
            "Yukarı doğru baskı kısmının kapıya sıkışması",
            "Taban dış kenarlarında kabarıklık"
        ],
        "genel_çözümler": [
            "1️⃣ Z Offset: Nozzulu tabla'dan daha yüksek tutun (0.1-0.2mm)",
            "2️⃣ İlk Katman Hızı: Çok azalt (%50 veya daha az)",
            "3️⃣ Yatak Sıcaklığı: İlk 1-2 katmandan sonra azalt",
            "4️⃣ İlk Katman Sıcaklığı: Azalt (5-10°C düşür)",
            "5️⃣ Brim Genişliği: Azalt (fazla yapışan brim sorun yaratır)",
            "6️⃣ Print Hızı: İlk katman 30mm/s'den fazla olmasın",
            "7️⃣ Flow Rate (İlk Katman): %90-95'e azalt",
            "8️⃣ Tabla Leveling: Z'yi 0.05mm temas mesafesini koru"
        ],
        "filament_özellikleri": {}
    },
    
    "Ringing / Ghosting (Titreşim İzleri)": {
        "açıklama": "Baskı yüzeyinde çan sesi etkisi, dalgalar ve titreşim izleri",
        "semptomlar": [
            "Köşelerde ve keskin dönüşlerde dalgalar",
            "Tahmin edilemeyen hareket izleri",
            "Titreşim sesi yazıcıdan geliyor"
        ],
        "genel_çözümler": [
            "1️⃣ Baskı Hızı: Azalt (akselerasyon azalacak)",
            "2️⃣ Jerk Ayarları: Firmware'de jerk değerini düşür (10-20mm/s)",
            "3️⃣ Dönüş Hızı: Sharp corners hızını azalt",
            "4️⃣ Mekanik Sıkılığı: Aks bağlantılarını sıkılaştır",
            "5️⃣ Kama Kemerleri: Paylaşan kama yerleşimini kontrol et",
            "6️⃣ Yazıcı Stablitesi: Yazıcı düz ve sabit zeminde olmalı",
            "7️⃣ Vibration Damping: Yazıcıya ek dampening ekle",
            "8️⃣ Nozzle Cooler: Ağır cooler'ı hafifler ile değiştir"
        ],
        "filament_özellikleri": {}
    },
    
    "Nozzle Dragging (Nozzul Sürüyor)": {
        "açıklama": "Nozzul baskıyı rasgelere sürüyor, raf veya filamentle temas ediyor",
        "semptomlar": [
            "Nozzulda baskı kalıntıları",
            "Baskı kısımları hareket ediyor",
            "Kötü yüzey ve bozuk detaylar"
        ],
        "genel_çözümler": [
            "1️⃣ Z-Hop: Travel sırasında nozzul 0.2-0.4mm kaldır",
            "2️⃣ Retraction: Retract mesafesini arttır (filament boşaltılsın)",
            "3️⃣ Travel Speed: Yükselt (hızlı geçiş)",
            "4️⃣ Mesh Leveling: Tabla yüksekliğini optimize et",
            "5️⃣ Nozzule Cleaner: Nozzulun altını temizle",
            "6️⃣ Model Pozisyonu: Modeli optimum konuma koy",
            "7️⃣ Travel Paths: Slicerda Avoid Crossing Perimeter etkinleştir",
            "8️⃣ Cooling Fan: Azalt (daha sağlam baskı)"
        ],
        "filament_özellikleri": {}
    },
    
    "Gaps Between Perimeters (Çevre Boşlukları)": {
        "açıklama": "Dış çevre ve iç dolgu arasında boşluklar var",
        "semptomlar": [
            "Dış kenarlar içe doğru çekik",
            "İç ve dış çevreler arasında aralık",
            "Su geçişine açık baskılar"
        ],
        "genel_çözümler": [
            "1️⃣ Flow Rate: %100-105'e çıkar",
            "2️⃣ Wall Line Width: Nozzul çapı kadar ayarla (0.4mm=0.4mm)",
            "3️⃣ Nozzul Sıcaklığı: +5°C arttır",
            "4️⃣ Print Speed: Azalt",
            "5️⃣ Z-Seam Alignment: Dış köşeyi Hide opsiyonuyla ayarla",
            "6️⃣ Perimeter First: Önce çevre, sonra dolgu bas",
            "7️⃣ Combing Mode: 'Within Infill' seçeneğini aç",
            "8️⃣ Infill Density: Arttır (%15 yerine %20'ye çıkar)"
        ],
        "filament_özellikleri": {}
    },
    
    "Top Layers Holes (Üst Katmanında Delikler)": {
        "açıklama": "Baskının üst yüzeyinde küçük delikler veya boşluklar",
        "semptomlar": [
            "Üst dolgu katmanlarında delikler",
            "Kalın model içi boş kalmış",
            "Dış yüzey tam kapanmamış"
        ],
        "genel_çözümler": [
            "1️⃣ Top Layer Thickness: Arttır (3 katman yerine 4-5 katman)",
            "2️⃣ Infill Density: Arttır (%20'ye çıkar)",
            "3️⃣ Flow Rate: %105-110'a çıkar",
            "4️⃣ Top Layer Speed: Azalt (yavaş bas)",
            "5️⃣ Nozzul Sıcaklığı: +5°C arttır",
            "6️⃣ Nozzul Size: Daha büyük nozzul kullan (0.6mm)",
            "7️⃣ Infill Pattern: Linear yerine Grid veya Gyroid seç",
            "8️⃣ Z-Seam Position: Top layer seam'ini optimize et"
        ],
        "filament_özellikleri": {}
    },
    
    "Blob/Zits (Lekeleri ve Noktaları)": {
        "açıklama": "Baskıda rastgele noktalar, tınak damlası gibi lekeleri",
        "semptomlar": [
            "Beklenmedik küçük toplar veya damla lekeleri",
            "Baskı yüzeyinde çıkıntılar",
            "Kötü estetik görünüş"
        ],
        "genel_çözümler": [
            "1️⃣ Retraction: Retract mesafesini arttır (çok az = sızıntı)",
            "2️⃣ Z-Raise: Retract sırasında Z'yi kaldır",
            "3️⃣ Nozzul Sıcaklığı: Azalt (filament çabuk katılaşsın)",
            "4️⃣ Combing: 'Within Infill' seçeneğini aç",
            "5️⃣ Print Speed: Azalt",
            "6️⃣ Pressure Advance: Arttır (filament basıncını kontrol et)",
            "7️⃣ Z-Seam Alignment: Hidden seç",
            "8️⃣ Blob Detection: Slicer'da 'Avoid Blobs' aktif et"
        ],
        "filament_özellikleri": {}
    },
    
    "Model Shifting / Desynchronization": {
        "açıklama": "Baskı ortasında model yaşayan ve katlı hale geliyor",
        "semptomlar": [
            "Model birseyinden sonra sağa/sola kaymış",
            "Katmanlar yer değiştirmiş gibi",
            "Baskı ve dosya eşleşmiyor"
        ],
        "genel_çözümler": [
            "1️⃣ USB Hızı: Serial iletişim hızını azalt (115200'den başla)",
            "2️⃣ Printer Placement: Yazıcıyı elektromanyetik gürültüden uzak koy",
            "3️⃣ Kablolar: Tüm kablolar güvence altında olmalı",
            "4️⃣ Firmware: Son sürüme güncelle",
            "5️⃣ Thermal Runaway: Sicaklık sensörünü kontrol et",
            "6️⃣ Motor Çıkışı: Stepper motor hatalarını izle",
            "7️⃣ SD Kart: Direkt SD karttan bas (USB yerine)",
            "8️⃣ Firmware Buffer: G-code buffer boyutunu arttır"
        ],
        "filament_özellikleri": {}
    },
    
    "Horizontal Lines at Layer Changes": {
        "açıklama": "Her katman değişiminde yatay çizgiler veya kalınlık değişimi",
        "semptomlar": [
            "Z ekseninde düzenli çizgiler",
            "Baskı yüzeyinde yukarı inme izleri",
            "Periyodik kalınlık varyasyonu"
        ],
        "genel_çözümler": [
            "1️⃣ Z-Offset Ayarı: Tekrar leveling yap",
            "2️⃣ Layer Height: Değiştir (0.2mm yerine 0.16mm)",
            "3️⃣ Z-Seam Position: Random seç",
            "4️⃣ Print Speed: Azalt",
            "5️⃣ Z Motor Oyunu: Kepçe varsa sıkılaştır",
            "6️⃣ Bed Leveling Method: Manual leveling yerine probe kullan",
            "7️⃣ Firmware Tuning: Z feed rate'i optimize et",
            "8️⃣ Layer-to-Layer: Model dosyasında düzeyde çizgiler varsa - yeniden tasarımla"
        ],
        "filament_özellikleri": {}
    },
    
    "Pitting (Çukur Oluşumu)": {
        "açıklama": "Yüzey pürüzlü, çukurlu ve çatlamış gibi görünüyor",
        "semptomlar": [
            "Derin çukurlar ve boşluklar",
            "Pütürlü, zımparalanmış görüntü",
            "Yüzey parçalanmış gibi"
        ],
        "genel_çözümler": [
            "1️⃣ Nozzul Sıcaklığı: Optimize et ±10°C test et",
            "2️⃣ Fan Speed: Arttır (%100'e çıkar)",
            "3️⃣ Print Speed: Azalt (30-50mm/s)",
            "4️⃣ Wall Line Count: Arttır (2 yerine 3-4 kat)",
            "5️⃣ Infill Density: Arttır",
            "6️⃣ Filament Quality: İyi kaliteli filament kullan",
            "7️⃣ Layer Height: Azalt (0.1mm olarak dene)",
            "8️⃣ Cooling: Daha iyi soğutma sistemi kur"
        ],
        "filament_özellikleri": {}
    },
    
    "Sagging (Sarkan Bölümler)": {
        "açıklama": "Geniş yatay bölümler ortasında sarkıyor, destek olmamasına rağmen",
        "semptomlar": [
            "Düz yüzeyin ortası aşağı çökmüş",
            "Çatı bölümleri eksik",
            "Taşkın yapısı kötü"
        ],
        "genel_çözümler": [
            "1️⃣ Infill Density: Arttır (%20+ yap)",
            "2️⃣ Infill Pattern: Gyroid veya Grid seç (linear yerine)",
            "3️⃣ Top Layer Count: Arttır (3 yerine 5-6)",
            "4️⃣ Support Add: Destek ekle (gerekirse)",
            "5️⃣ Nozzul Sıcaklığı: Azalt",
            "6️⃣ Print Speed: Azalt",
            "7️⃣ Orientation: Modeli rotasyon ver (daha kısa açıklık)",
            "8️⃣ Veri Kalınlığı: Kalınlaştır"
        ],
        "filament_özellikleri": {}
    },
    
    "Split/Crack (Çatlak)": {
        "açıklama": "Baskıda çatlaklar oluşuyor, parçalanmış görünüyor",
        "semptomlar": [
            "Keskin çatlaklar",
            "Baskı kırılgan ve kolay parçalara ayrılıyor",
            "Soğuma sırasında kütük şekli değişiyor"
        ],
        "genel_çözümler": [
            "1️⃣ Baskı Sıcaklığı: Optimize et (çok sıcak olabilir)",
            "2️⃣ Yatak Sıcaklığı: Arttır (daha iyi tutunma)",
            "3️⃣ Soğutma: Azalt (hızlı soğuma çatlak yaratır)",
            "4️⃣ Kapalı Kasa: Ortam sıcaklığı uniform tutun",
            "5️⃣ Nozzul Sıcaklığı: Filament türüne en uygun değer bul",
            "6️⃣ Print Speed: Azalt",
            "7️⃣ Wall Thickness: Arttır",
            "8️⃣ Filament Storage: Filamenti nem ve ısıdan koru (nemli filament çatlak yaratır)"
        ],
        "filament_özellikleri": {}
    },
    
    "Perimeter Bulges (Kenar Çıkıntıları)": {
        "açıklama": "Baskının kenarları dışa doğru şişiyor, balonlaştırıyor",
        "semptomlar": [
            "Dış kenarlar puf gibi genişlemiş",
            "Şekil hedeflenen boyuttan büyük",
            "Asimetrik şişme"
        ],
        "genel_çözümler": [
            "1️⃣ Outer Wall Flow: %95'e düşür",
            "2️⃣ Wall Line Width: Azalt (0.35mm veya daha az)",
            "3️⃣ Print Speed: Azalt",
            "4️⃣ Nozzul Sıcaklığı: Azalt",
            "5️⃣ Pressure Advance: İyileştir",
            "6️⃣ Z-Offset: Kontrol et",
            "7️⃣ Outer Wall Order: Last seç",
            "8️⃣ Cooler Power: Arttır"
        ],
        "filament_özellikleri": {}
    },
    
    "Fishy/Squiggly Lines": {
        "açıklama": "Baskı çizgileri düzensiz, dalgalı veya sakatlanmış görünüyor",
        "semptomlar": [
            "Çizgiler sabit değil, dalgalı",
            "Çevre eksik veya bozuk",
            "Rastgele başarısızlık bölgeleri"
        ],
        "genel_çözümler": [
            "1️⃣ Belt Tension: Kama kemerlerin gerginliğini kontrol et",
            "2️⃣ Eccentric Nut Tightness: Eksantrik somunları sıkılaştır",
            "3️⃣ Stepper Motors: Çalışıp çalışmadığını kontrol et",
            "4️⃣ Smooth Rod: Temizle ve yağla",
            "5️⃣ Nozzle Quality: Nozzulu değiştir (tıkanık olabilir)",
            "6️⃣ Print Speed: Azalt",
            "7️⃣ Motor Currents: Firmware'de motor akımını optimize et",
            "8️⃣ USB Cable: Kablo kötü olabilir, değiştir"
        ],
        "filament_özellikleri": {}
    },
    
    "Curling (Kıvrılma - Özellikle Kenarlar)": {
        "açıklama": "Baskının sadece kenarları kıvrılıyor, ortası iyi",
        "semptomlar": [
            "Sadece kenar bölümleri yukarı kalkıyor",
            "Raf köpekleri benzeri görünüş",
            "Merkezde iyi, çevrede kötü"
        ],
        "genel_çözümler": [
            "1️⃣ Kenar Soğutması: Kenarları hedef sıcaklıkta tut",
            "2️⃣ Brim Genişliği: Arttır (daha fazla yapışma yüzeyi)",
            "3️⃣ Yatak Sıcaklığı: Arttır",
            "4️⃣ Kapalı Kasa: Ortam sıcaklığını uniform tut",
            "5️⃣ Print Speed (İlk Katman): Azalt",
            "6️⃣ Raft Yazma: Raft kullan brim yerine",
            "7️⃣ Tabla Leveling: Kenarları kontrol et",
            "8️⃣ Ortam Akımı: Açık kapı/pencere kapa"
        ],
        "filament_özellikleri": {}
    },
    
    "Filament Skipping / Grinding": {
        "açıklama": "Ekstruder motorunun dişleri filamenti ezmesi, basması",
        "semptomlar": [
            "Ekstruder dişlerinden çatırtı sesi",
            "Filament esnetilemez",
            "Baskı sırasında beklenmedik durma"
        ],
        "genel_çözümler": [
            "1️⃣ Feeder Basıncı: Ayarla (çok sıkı = ezme, çok gevşek = kayma)",
            "2️⃣ Nozzul Sıcaklığı: Arttır (filament akışlı olsun)",
            "3️⃣ Baskı Hızı: Azalt (az basınç)",
            "4️⃣ Nozzul Kontrol: Tıkanık nozzulu temizle veya değiştir",
            "5️⃣ Filament Kalitesi: Kaliteli filament kullan",
            "6️⃣ Feeder Dişler: Temizle ve ezilmiş filament kalıntılarını sil",
            "7️⃣ Filament Çekme: Retract ayarlarını kontrol et",
            "8️⃣ Smooth Rod Friction: Tüm eksenleri kontrol et (tıkanlı olabilir)"
        ],
        "filament_özellikleri": {}
    },
    
    "Moisture Marks (Nem Izleri)": {
        "açıklama": "Baskıda beyaz çizgiler, baloncuk veya foam gibi görünüş",
        "semptomlar": [
            "Beyaz veya opak çizgiler",
            "Baloncuk benzeri yapılar",
            "Baskı gözenekli ve spongeli"
        ],
        "genel_çözümler": [
            "1️⃣ Filament Kurutma: 4-8 saat 50-70°C'de kuru",
            "2️⃣ Filament Saklama: Kuru ortamda saklı tut (desiccant ile)",
            "3️⃣ Baskı Hızı: Azalt (filament nem kaybı)",
            "4️⃣ Nozzul Sıcaklığı: Arttır (+10°C)",
            "5️⃣ Filament Dryer: Drying box kullan",
            "6️⃣ Ortam Nem: Yazıcı alanında nem kontrol et",
            "7️⃣ Storage Container: Klip kapaklı kutu + desiccant kullan",
            "8️⃣ Vakum Paketleme: İyi filamenti vakum pak'te saklı tut"
        ],
        "filament_özellikleri": {}
    }
}


# TAB SEÇIMI - Mod seçimi
tab1, tab2, tab3 = st.tabs(["🎯 Projeye Uygun Filament Seçimi", "⚡ Filamente Uygun Proje Seçimi", "🔧 Baskı Sorunları Çözümü"])

# ============================================================================
# TAB 2: FILAMENTE UYGUN PROJE SEÇİMİ - Elinde Var Olan İçin %100 Verim
# ============================================================================
with tab2:
    st.header("⚡ Filamente Uygun Proje Seçimi")
    st.markdown("Elindeki filamentten **%100 verim** almak için optimal ayarları öğren!")
    st.divider()
    
    # Filament seçimi
    filament_isimleri = [f[0] for f in FILAMENT_DATA]
    secili_filament = st.selectbox(
        "🧵 Hangi filamenti kullanıyorsun?",
        options=filament_isimleri,
        index=0
    )
    
    # Seçilen filamenti bul
    secili_row = None
    for f in FILAMENT_DATA:
        if f[0] == secili_filament:
            secili_row = f
            break
    
    if secili_row:
        # Filament verilerini aç
        filament_dict = dict(zip(COLUMNS, secili_row))
        
        st.success(f"✅ **{secili_filament}** seçildi")
        st.divider()
        
        # Optimal Ayarlar
        st.header("🎛️ Optimal Baskı Ayarları")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sıcaklık Ayarları")
            min_noz = int(filament_dict["MinNozulSicaklik"])
            max_noz = min_noz + 30
            
            st.info(f"🌡️ **Nozzle Sıcaklığı**: {min_noz}°C - {max_noz}°C")
            st.caption(f"Optimal: {min_noz + 10}°C (düşük = detay, yüksek = yapışma)")
            
            # Yatak sıcaklığı tahmini
            filament_adi = secili_filament.upper()
            
            yatak_sicaklik_tahmin = {
                'ABS': "95-105°C", 'ASA': "95-105°C", 'PC': "100-120°C", 'PC-ABS': "100-110°C",
                'NYLON': "60-80°C", 'PA6': "70-80°C", 'PA12': "60-70°C",
                'PEEK': "120-140°C", 'PEI': "100-120°C",
                'PLA': "0-60°C", 'PETG': "60-80°C", 'TPU': "30-50°C", 'ABS-ESD': "95-105°C"
            }
            
            yatak_str = "Soğuk tabla veya 30-50°C"
            for key, value in yatak_sicaklik_tahmin.items():
                if key in filament_adi:
                    yatak_str = value
                    break
            
            st.info(f"🛏️ **Yatak Sıcaklığı**: {yatak_str}")
        
        with col2:
            st.subheader("Hız Ayarları")
            
            # Baskı hızı önerisi
            bask_kolayligi = filament_dict["BaskiKolayligi"]
            
            if bask_kolayligi >= 80:
                hiz_str = "70-100 mm/s"
                hiz_tavsi = "Hızlı baskıya uygun"
            elif bask_kolayligi >= 60:
                hiz_str = "50-70 mm/s"
                hiz_tavsi = "Orta hızda iyi sonuç"
            else:
                hiz_str = "20-50 mm/s"
                hiz_tavsi = "Yavaş, kontrollü baskı önerilir"
            
            st.info(f"⚡ **Baskı Hızı**: {hiz_str}\n{hiz_tavsi}")
            
            # Soğutma önerisi
            if secili_filament in ["PLA", "Silk PLA", "Wood PLA"]:
                st.info(f"❄️ **Fan Hızı**: %100\nPLA soğutma gerektirir")
            else:
                st.info(f"❄️ **Fan Hızı**: %0-30%\nSoğutma sınırlı olmalı")
        
        st.divider()
        
        # Gelişmiş Özellikler
        st.header("🏆 Filament Özellikleri & Tavsiyeler")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Dayanıklılık", f"{filament_dict['IsiDayanim']}/100")
            st.metric("Baskı Kolaylığı", f"{filament_dict['BaskiKolayligi']}/100")
            st.metric("Üzey Kalitesi", f"{(filament_dict['Seffaflik'] + filament_dict['YuzeyParlaklik'])//2}/100")
        
        with col2:
            st.metric("String Riski", f"{100 - filament_dict['StringOlusumu']}/100", delta="Düşük iyi")
            st.metric("Warping Riski", f"{100 - filament_dict['WarpingDirenci']}/100", delta="Düşük iyi")
            st.metric("Destek Kolaylığı", f"{100 - filament_dict['DestekIhtiyaci']}/100", delta="Yüksek iyi")
        
        with col3:
            st.metric("Nozul Min.", f"{filament_dict['MinNozzle']}mm")
            st.metric("Nem Hassasiyeti", f"{filament_dict['NemHassasiyeti']}/100", delta="Düşük iyi")
            st.metric("Nozul Aşındırıcılığı", f"{filament_dict['NozulAsindiricilik']}/100", delta="Düşük iyi")
        
        st.divider()
        
        # Tabla Uyumluluk Tablosu
        st.header("📋 Tabla Yüzeyi Uyumluluğu")
        
        tabla_map = {
            "Cam": "CamTabla",
            "PEI Smooth": "PEI_Smooth",
            "PEI Textured": "PEI_Textured",
            "BuildTak/PEX": "BuildTak",
            "Garolite (FR4)": "Garolite",
            "PP Sheet": "PPSheet"
        }
        
        tabla_data = []
        for nama, kolon in tabla_map.items():
            score = filament_dict[kolon]
            tabla_data.append({
                "Tabla Yüzeyi": nama,
                "Uyumluluk": score,
                "Durum": "✅ Mükemmel" if score >= 80 else "👍 İyi" if score >= 60 else "⚠️ Uygun" if score >= 40 else "❌ Zayıf"
            })
        
        tabla_df = pd.DataFrame(tabla_data)
        st.dataframe(tabla_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Pratik İpuçları
        st.header("💡 Pratik İpuçları")
        
        tips = []
        
        # İpucu 1: Nem kontrolü
        if filament_dict["NemHassasiyeti"] >= 80:
            tips.append("🌡️ **Nem Kontrolü**: Bu filament çok nem hassasıdır. Baskıdan hemen önce 4-6 saat kurutun ve kurutulmuş şekilde saklayın.")
        
        # İpucu 2: İlk Katman
        if filament_dict["IlkKatmanYapisma"] >= 80:
            tips.append("📌 **İlk Katman**: Tabla yüzeyini temiz tutun ve ilk katman yavaşça yazın.")
        else:
            tips.append("📌 **İlk Katman**: İlk katmanda yapışma sorunları yaşayabilirsiniz. Tabla yüzeyini aşındırın veya yapışkan kullanın.")
        
        # İpucu 3: Warping
        if filament_dict["WarpingDirenci"] < 70:
            tips.append("📐 **Warping**: Raf bükülmesine eğilimli. Isıtmalı yatak kullanın ve kapalı kasa önerilir.")
        
        # İpucu 4: Post-processing
        if filament_dict["Zimparalanabilirlik"] >= 70:
            tips.append("✨ **Sonrası**: Bu filament zımpara ve boyaya çok uygun. Baskı sonrası güzelleştirme yapılabilir.")
        elif filament_dict["Boyanabilirlik"] >= 70:
            tips.append("✨ **Sonrası**: Boyanmaya uygundur. Baskı sonrası renklendirebilirsiniz.")
        
        # İpucu 5: Hız
        if filament_dict["BaskiHizi"] >= 80:
            tips.append("⚡ **Hız**: Bu filament hızlı baskıya uygundur. 80-100 mm/s hızlarla düzgün sonuçlar alabilirsiniz.")
        elif filament_dict["BaskiHizi"] < 50:
            tips.append("🐢 **Hız**: Yavaş ve kontrollü baskı en iyi sonuçları verir. 30-50 mm/s ile başlayın.")
        
        # İpucu 6: Soğutma
        if secili_filament in ["PLA", "Silk PLA", "Wood PLA"]:
            tips.append("❄️ **Soğutma**: Fan hızını %100'e çıkarın. Soğutma detaylı ve temiz baskı için kritik önemde.")
        
        # İpucu 7: Destek
        if filament_dict["DestekIhtiyaci"] >= 70:
            tips.append("🏗️ **Destek**: Destek yapısı gerekli. Tulostin kalite ayarlarını optimize edin.")
        
        if tips:
            for i, tip in enumerate(tips, 1):
                st.info(tip)
        
        st.divider()
        
        # Olası Sorunlar ve Çözümler
        st.header("🔧 Yaşayabileceğiniz Sorunlar")
        
        sorunlar = []
        
        if filament_dict["NozulAsindiricilik"] >= 70:
            sorunlar.append({
                "Sorun": "Nozzle Hızlı Aşınması",
                "Çözüm": "Sertleştirilmiş nozzle (hardened steel) kullanın veya aşındıramayan malzeme tercih edin"
            })
        
        if filament_dict["StringOlusumu"] < 40:
            sorunlar.append({
                "Sorun": "Fazla İplik (Stringing)",
                "Çözüm": "Nozzle sıcaklığını azaltın (5-10°C düşürün) veya retract ayarlarını iyileştirin"
            })
        
        if filament_dict["WarpingDirenci"] < 60:
            sorunlar.append({
                "Sorun": "Raf Bükülmesi (Warping)",
                "Çözüm": "Yatak sıcaklığını 5-10°C arttırın veya baskı alanını kapla"
            })
        
        if filament_dict["IlkKatmanYapisma"] < 60:
            sorunlar.append({
                "Sorun": "İlk Katman Yapışması",
                "Çözüm": "Tabla yüzeyini tertemiz yapın, tabla aralığını iyileştirin veya yapışkan (glue stick) kullanın"
            })
        
        if sorunlar:
            for sorun in sorunlar:
                st.warning(f"**{sorun['Sorun']}**\n{sorun['Çözüm']}")

# ============================================================================
# TAB 1: PROJEYE UYGUN FILAMENT SEÇİMİ - Orijinal Mode
# ============================================================================
with tab1:
    st.header("🎯 Projeye Uygun Filament Seçimi")
    st.markdown("Proje gereksinimlerinize göre en ideal filamenti bulun")
    st.divider()

    # Sidebar - Donanım bilgileri
    st.sidebar.header("⚙️ Yazıcı Donanımı")
    
    # Yazıcı Seçimi
    st.sidebar.subheader("📋 Yazıcı Modeli")
    yazici_secim = st.sidebar.selectbox(
        "Yazıcı marka ve modeli",
        ["Bilmiyorum / Manuel Gir"] + sorted(list(YAZICI_VERITABANI.keys())),
        index=0,
        help="Bildiğiniz yazıcı modelini seçin, otomatik olarak özellikler doldurulacak"
    )
    
    donanim = {}
    
    # Eğer yazıcı seçildiyse, otomatik olarak doldur
    if yazici_secim != "Bilmiyorum / Manuel Gir":
        yazici_ozellikleri = YAZICI_VERITABANI[yazici_secim]
        
        st.sidebar.success(f"✅ {yazici_secim} özellikleri otomatik yüklendi!")
        
        donanim['kapali_kasa'] = st.sidebar.checkbox(
            "Kapalı kasa var", 
            value=yazici_ozellikleri['kapali_kasa'],
            disabled=True
        )
        donanim['kurutma'] = st.sidebar.checkbox("Filament kurutucu var", value=False)
        donanim['sert_nozul'] = st.sidebar.checkbox("Sertleştirilmiş nozzle var", value=False)
        
        donanim['isitmali_yatak'] = st.sidebar.checkbox(
            "Isıtmalı yatak var", 
            value=yazici_ozellikleri['isitmali_yatak'],
            disabled=True
        )
        if donanim['isitmali_yatak']:
            donanim['max_yatak_sicaklik'] = st.sidebar.number_input(
                "Yatak max sıcaklık (°C)", 
                min_value=0, 
                max_value=200, 
                value=yazici_ozellikleri['max_yatak_sicaklik'],
                disabled=True
            )
        else:
            donanim['max_yatak_sicaklik'] = 0
        
        donanim['max_nozul_sicaklik'] = st.sidebar.number_input(
            "Nozzle max sıcaklık (°C)", 
            min_value=0, 
            max_value=500, 
            value=yazici_ozellikleri['max_nozul_sicaklik'],
            disabled=True
        )
        
        donanim['bowden'] = st.sidebar.selectbox(
            "Ekstruder tipi",
            ["Seçiniz", "Direct", "Bowden"],
            index=1 if yazici_ozellikleri['ekstruder_tipi'] == "Direct" else 2,
            disabled=True
        ) == "Bowden"
    else:
        # Manuel giriş modu
        st.sidebar.info("ℹ️ Yazıcı özelliklerini manuel olarak girebilirsiniz")
        
        donanim['kapali_kasa'] = st.sidebar.checkbox("Kapalı kasa var", value=False)
        donanim['kurutma'] = st.sidebar.checkbox("Filament kurutucu var", value=False)
        donanim['sert_nozul'] = st.sidebar.checkbox("Sertleştirilmiş nozzle var", value=False)

        donanim['isitmali_yatak'] = st.sidebar.checkbox("Isıtmalı yatak var", value=False)
        if donanim['isitmali_yatak']:
            donanim['max_yatak_sicaklik'] = st.sidebar.number_input(
                "Yatak max sıcaklık (°C)", 
                min_value=0, 
                max_value=200, 
                value=0
            )
        else:
            donanim['max_yatak_sicaklik'] = 0

        donanim['max_nozul_sicaklik'] = st.sidebar.number_input(
            "Nozzle max sıcaklık (°C)", 
            min_value=0, 
            max_value=500, 
            value=0
        )

        donanim['bowden'] = st.sidebar.selectbox(
            "Ekstruder tipi",
            ["Seçiniz", "Direct", "Bowden"],
            index=0
        ) == "Bowden"

    # Nozzle ölçüleri - çoklu seçim
    nozzle_secenekleri = {
        "0.2 mm": 0.2,
        "0.4 mm (standart)": 0.4,
        "0.6 mm": 0.6,
        "0.8 mm": 0.8
    }
    secili_nozzles = st.sidebar.multiselect(
        "Nozzle ölçüleri (birden fazla seçebilirsiniz)",
        options=list(nozzle_secenekleri.keys()),
        default=[]
    )
    donanim['nozzle_olculeri'] = [nozzle_secenekleri[n] for n in secili_nozzles]

    # Tabla tipleri - çoklu seçim
    tabla_secenekleri = {
        "Cam (Glass)": ("CamTabla", "Cam"),
        "PEI Smooth": ("PEI_Smooth", "PEI Smooth"),
        "PEI Textured": ("PEI_Textured", "PEI Textured"),
        "BuildTak/PEX": ("BuildTak", "BuildTak/PEX"),
        "Garolite (FR4)": ("Garolite", "Garolite (FR4)"),
        "PP Sheet": ("PPSheet", "PP Sheet")
    }
    secili_tablalar = st.sidebar.multiselect(
        "Tabla yüzeyleri (birden fazla seçebilirsiniz)",
        options=list(tabla_secenekleri.keys()),
        default=[]
    )
    donanim['tablalar'] = [
        {'kolon': tabla_secenekleri[t][0], 'isim': tabla_secenekleri[t][1]} 
        for t in secili_tablalar
    ]

    st.sidebar.divider()

    # Ana alan - Kriter ağırlıkları
    st.header("📊 Kullanım Gereksinimleri")
    st.markdown("Her kriter için 0-5 arası önem derecesi belirleyin (0=önemsiz, 5=kritik)")

    # Kriterler kategorilere ayrılmış
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🛡️ Dayanıklılık")
        w_isi = st.slider("Isı dayanımı", 0, 5, 0)
        w_uv = st.slider("Ultraviyole dayanımı", 0, 5, 0)
        w_nem = st.slider("Nem dayanımı", 0, 5, 0)
        w_kimyasal = st.slider("Kimyasal dayanım", 0, 5, 0)
        w_darbe = st.slider("Darbe dayanımı", 0, 5, 0)
        w_yuk = st.slider("Yük taşıma kapasitesi", 0, 5, 0)
        w_asinma = st.slider("Aşınma direnci", 0, 5, 0)

    with col2:
        st.subheader("⚙️ Mekanik Özellikler")
        w_katman = st.slider("Katman aderansı (yapışması)", 0, 5, 0)
        w_boyutsal = st.slider("Boyutsal stabilite", 0, 5, 0)
        w_esneklik = st.slider("Esneklik", 0, 5, 0)
        w_titresim = st.slider("Titreşim sönümleme", 0, 5, 0)
        w_surunme = st.slider("Sürünme direnci", 0, 5, 0)
        w_yorulma = st.slider("Yorulma dayanımı", 0, 5, 0)
        w_cekme = st.slider("Çekme mukavemeti", 0, 5, 0)

    with col3:
        st.subheader("🖨️ Baskı & İşleme")
        w_warping = st.slider("Bükülme (warping) direnci", 0, 5, 0)
        w_kolaylik = st.slider("Baskı kolaylığı", 0, 5, 0)
        w_string = st.slider("İplik oluşmaması (stringing)", 0, 5, 0)
        w_ilk_katman = st.slider("İlk katman yapışması", 0, 5, 0)
        w_kopruleme = st.slider("Köprüleme yeteneği", 0, 5, 0)
        w_cikinti = st.slider("Çıkıntı performansı", 0, 5, 0)
        w_hiz = st.slider("Hızlı baskı desteği", 0, 5, 0)
        w_zimpara = st.slider("Zımparalanabilirlik", 0, 5, 0)
        w_boya = st.slider("Boyanabilirlik", 0, 5, 0)
        w_yapistir = st.slider("Yapıştırılabilirlik", 0, 5, 0)
        w_seffaflik = st.slider("Şeffaflık", 0, 5, 0)
        w_parlaklik = st.slider("Yüzey parlaklığı", 0, 5, 0)

    st.divider()

    # HESAPLA butonu
    if st.button("🚀 FİLAMENTLERİ DEĞERLENDIR", type="primary", use_container_width=True):
        
        # Ağırlıkları topla
        USER_WEIGHTS = {
            "IsiDayanim": w_isi, "UVDayanim": w_uv, "NemDayanim": w_nem,
            "KimyasalDayanim": w_kimyasal, "DarbeDayanim": w_darbe,
            "YukTasima": w_yuk, "AsinmaDirenci": w_asinma,
            "KatmanAderans": w_katman, "BoyutsalStabilite": w_boyutsal,
            "Esneklik": w_esneklik, "TitreisimSondumleme": w_titresim,
            "SurunmeDirenci": w_surunme, "YorulmaDayanimi": w_yorulma,
            "CekmeMukavemeti": w_cekme, "WarpingDirenci": w_warping,
            "BaskiKolayligi": w_kolaylik, "StringOlusumu": w_string,
            "IlkKatmanYapisma": w_ilk_katman, "KoprulemeYeteneği": w_kopruleme,
            "CikintiPerformansi": w_cikinti, "BaskiHizi": w_hiz,
            "Zimparalanabilirlik": w_zimpara, "Boyanabilirlik": w_boya,
            "Yapistirilabilirlik": w_yapistir, "Seffaflik": w_seffaflik,
            "YuzeyParlaklik": w_parlaklik
        }
        
        # DataFrame oluştur
        df = pd.DataFrame(FILAMENT_DATA, columns=COLUMNS)
        
        # Skor hesapla
        df["Skor"] = 0
        for kriter, agirlik in USER_WEIGHTS.items():
            df["Skor"] += df[kriter] * agirlik
        
        # Ceza sistemi - Orijinal dosyadaki tam sistem
        # 1. Kapalı kasa cezası
        if not donanim['kapali_kasa']:
            df["Skor"] -= df["KapaliKasaIhtiyaci"] * 2
        
        # 2. Kurutma cezası
        if not donanim['kurutma']:
            df["Skor"] -= df["NemHassasiyeti"] * 2
        
        # 3. Sertleştirilmiş nozul cezası
        if not donanim['sert_nozul']:
            df["Skor"] -= df["NozulAsindiricilik"] * 3
        
        # 4. Isıtmalı yatak cezası
        if not donanim['isitmali_yatak']:
            df["Skor"] -= df["IsitmalıYatakIhtiyaci"] * 2.5
        elif donanim['max_yatak_sicaklik'] < 90:
            df["Skor"] -= df["IsitmalıYatakIhtiyaci"] * 1.5
        
        # 5. Nozul sıcaklığı cezası
        for idx, row in df.iterrows():
            min_sicaklik = row["MinNozulSicaklik"]
            if donanim['max_nozul_sicaklik'] < min_sicaklik:
                ceza = 500 * (min_sicaklik - donanim['max_nozul_sicaklik'])
                df.loc[idx, "Skor"] -= ceza
            elif donanim['max_nozul_sicaklik'] < min_sicaklik + 20:
                df.loc[idx, "Skor"] -= 100
        
        # 6. Bowden ekstruder cezası
        if donanim['bowden']:
            df["Skor"] -= df["BowdenZorlugu"] * 2
        
        # 7. Nozzle ölçüsü cezası
        max_kullanici_nozzle = max(donanim['nozzle_olculeri']) if donanim['nozzle_olculeri'] else 0
        for idx, row in df.iterrows():
            min_nozzle = row["MinNozzle"]
            if max_kullanici_nozzle < min_nozzle:
                ceza = 100 * (min_nozzle - max_kullanici_nozzle) * 5
                df.loc[idx, "Skor"] -= ceza
        
        # 8. Küçük sabit cezalar
        df["Skor"] -= df["Koku"] * 0.5
        df["Skor"] -= df["DestekIhtiyaci"] * 0.5
        
        # 8.5. Tabla sıcaklık kontrolü cezası
        tabla_sicaklik_gereksinimleri = {
            'ABS': 100, 'ASA': 100, 'PC': 110, 'PC-ABS': 105, 'PC-CF': 115,
            'Nylon': 70, 'PA6': 70, 'PA12': 70, 'PA612': 70, 'PA6-GF': 80, 'PA-CF': 80, 'PA12-CF': 80,
            'PEEK': 140, 'PEI': 130, 'PEKK': 140, 'PPS': 120
        }
        
        if donanim['isitmali_yatak']:
            for idx, row in df.iterrows():
                filament_adi = row['Filament']
                for key, min_temp in tabla_sicaklik_gereksinimleri.items():
                    if key in filament_adi:
                        if donanim['max_yatak_sicaklik'] < min_temp:
                            ceza = 200 * (min_temp - donanim['max_yatak_sicaklik'])
                            df.loc[idx, "Skor"] -= ceza
                        break
        
        # 9. Tabla uyumluluk bonusu - En iyi tabla skorunu bul
        df["EnIyiTabla"] = 0
        df["EnIyiTablaIsim"] = ""
        
        max_kullanici_nozzle = max(donanim['nozzle_olculeri']) if donanim['nozzle_olculeri'] else 0
        
        for idx, row in df.iterrows():
            en_iyi_skor = 0
            en_iyi_tabla = ""
            
            for tabla in donanim['tablalar']:
                tabla_skor = row[tabla['kolon']]
                if tabla_skor > en_iyi_skor:
                    en_iyi_skor = tabla_skor
                    en_iyi_tabla = tabla['isim']
            
            df.loc[idx, "EnIyiTabla"] = en_iyi_skor
            df.loc[idx, "EnIyiTablaIsim"] = en_iyi_tabla
            df.loc[idx, "Skor"] += en_iyi_skor * 0.5
        
        # Uyarı Sistemi - Orijinal Dosyadaki ile Aynı
        def olustur_uyari(row, donanim, max_kullanici_nozzle):
            uyari_listesi = []
            filament_adi = row['Filament']
            
            # UYARI 1: Kapalı kasa gereksinimi
            if row['KapaliKasaIhtiyaci'] >= 80 and not donanim['kapali_kasa']:
                uyari_listesi.append("⚠️ KAPALIBÖLME ŞART")
            
            # UYARI 2: Filament kurutucu gereksinimi
            if row['NemHassasiyeti'] >= 80 and not donanim['kurutma']:
                uyari_listesi.append("⚠️ KURUTUCU ŞİDDETLE ÖNERİLİR")
            
            # UYARI 3: Sertleştirilmiş nozzle gereksinimi
            if row['NozulAsindiricilik'] >= 80 and not donanim['sert_nozul']:
                uyari_listesi.append("⚠️ SERTLEŞTİRİLMİŞ NOZZLE ZORUNLU")
            
            # UYARI 4: Nozzle sıcaklık yetersizliği
            if donanim['max_nozul_sicaklik'] < row['MinNozulSicaklik']:
                uyari_listesi.append(f"❌ BASILAMAZ (Min {int(row['MinNozulSicaklik'])}°C gerekli)")
            
            # UYARI 5: Tabla sıcaklık yetersizliği
            tabla_sicaklik_gereksinimleri = {
                'ABS': 100, 'ASA': 100, 'PC': 110, 'PC-ABS': 105, 'PC-CF': 115,
                'PA6': 70, 'PA12': 70, 'PA612': 70, 'PA6-GF': 80, 'PA-CF': 80, 'PA12-CF': 80,
                'PEEK': 140, 'PEI': 130, 'PEKK': 140, 'PPS': 120
            }
            for key, min_temp in tabla_sicaklik_gereksinimleri.items():
                if key in filament_adi and donanim['isitmali_yatak']:
                    if donanim['max_yatak_sicaklik'] < min_temp:
                        uyari_listesi.append(f"⚠️ TABLA {min_temp}°C+ GEREKLİ (Mevcut: {donanim['max_yatak_sicaklik']}°C)")
                    break
            
            # UYARI 6: Bowden ile zorlanma
            if row['BowdenZorlugu'] >= 80 and donanim['bowden']:
                uyari_listesi.append("⚠️ BOWDEN İLE ZOR")
            
            # UYARI 7: Nozzle ölçüsü yetersizliği
            if max_kullanici_nozzle < row['MinNozzle']:
                uyari_listesi.append(f"⚠️ MIN {row['MinNozzle']}mm NOZZLE GEREKLİ")
            
            # UYARI 8: Tabla uyumsuzluğu
            en_iyi_tabla_skor = 0
            for tabla in donanim['tablalar']:
                tabla_skor = row[tabla['kolon']]
                if tabla_skor > en_iyi_tabla_skor:
                    en_iyi_tabla_skor = tabla_skor
            if en_iyi_tabla_skor < 60:
                uyari_listesi.append("⚠️ TABLA UYUMLULUĞU DÜŞÜK")
            
            return " | ".join(uyari_listesi) if uyari_listesi else "✅ Sorunsuz"
        
        # Uyarıları hesapla
        df["Uyarilar"] = df.apply(lambda row: olustur_uyari(row, donanim, max_kullanici_nozzle), axis=1)
        
        # Normalizasyon
        skor_min = df["Skor"].min()
        skor_max = df["Skor"].max()
        
        if skor_max != skor_min:
            df["Skor_Normalize"] = ((df["Skor"] - skor_min) / (skor_max - skor_min) * 100).round(1)
        else:
            df["Skor_Normalize"] = 100.0
        
        # Sırala
        df = df.sort_values("Skor", ascending=False)
        
        # SONUÇLAR
        st.success("✅ Değerlendirme tamamlandı!")
        
        # Top 10 - Uyarılar ile birlikte
        st.header("🏆 En Uygun 10 Filament")
        
        top10 = df.head(10)[["Filament", "Skor_Normalize", "EnIyiTablaIsim", "Uyarilar"]].copy()
        top10.columns = ["Filament", "Uyumluluk (%)", "En İyi Tabla", "Uyarılar"]
        
        st.dataframe(
            top10,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Uyarılar": st.column_config.TextColumn(width="large")
            }
        )
        
        # Detaylı tablo - Uyarılar ile birlikte
        st.header("📋 Tüm Filamentler")
        
        detay_kolonlar = ["Filament", "Skor_Normalize", "IsiDayanim", "YukTasima", 
                          "BaskiKolayligi", "StringOlusumu", "EnIyiTablaIsim", "Uyarilar"]
        detay_df = df[detay_kolonlar].copy()
        detay_df.columns = ["Filament", "Uyumluluk (%)", "Isı", "Yük", "Kolay", "String", "Tabla", "Uyarılar"]
        
        st.dataframe(
            detay_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Uyarılar": st.column_config.TextColumn(width="large")
            }
        )
        
        # CSV indirme - Uyarılar dahil
        csv_df = df[["Filament", "Skor_Normalize", "Uyarilar", "EnIyiTablaIsim"]].copy()
        csv_df.columns = ["Filament", "Uyumluluk (%)", "Uyarılar", "En İyi Tabla"]
        csv = csv_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 CSV Olarak İndir",
            data=csv,
            file_name="filament_sonuclari.csv",
            mime="text/csv"
        )
        
        # Tabla bazlı öneriler
        if donanim['tablalar']:
            st.header("📋 Tabla Bazlı Öneriler")
            
            tabs = st.tabs([tabla['isim'] for tabla in donanim['tablalar']])
            
            for i, tabla in enumerate(donanim['tablalar']):
                with tabs[i]:
                    tabla_df = df.copy()
                    tabla_df["TablaUyumluluk"] = tabla_df[tabla['kolon']]
                    tabla_df = tabla_df.sort_values("TablaUyumluluk", ascending=False)
                    
                    tabla_top = tabla_df.head(10)[["Filament", "TablaUyumluluk"]].copy()
                    tabla_top.columns = ["Filament", "Uyumluluk"]
                    
                    st.dataframe(tabla_top, use_container_width=True, hide_index=True)

    else:
        st.info("👆 Yan menüden donanım bilgilerinizi girin ve yukarıdaki sliderlardan kriterlerinizi ayarlayın, sonra 'Değerlendir' butonuna basın.")

# ============================================================================
# TAB 3: BASKI SORUNLARI ÇÖZÜMÜ
# ============================================================================
with tab3:
    st.header("🔧 Baskı Sorunları Çözümü")
    st.markdown("Yaşadığınız baskı sorununa göre filament önerileri ve çözüm adımlarını öğrenin")
    st.divider()
    
    # Sorunu seç
    secili_sorun = st.selectbox(
        "📌 Hangi sorunla karşılaşıyorsun?",
        options=list(BASKI_SORUNLARI.keys()),
        index=0
    )
    
    if secili_sorun in BASKI_SORUNLARI:
        sorun_bilgi = BASKI_SORUNLARI[secili_sorun]
        
        # Sorun başlığı ve açıklaması
        st.subheader(f"❓ {secili_sorun}")
        st.markdown(f"**{sorun_bilgi['açıklama']}**")
        st.divider()
        
        # Semptomlar
        st.subheader("🔍 Semptomlar")
        for semptom in sorun_bilgi['semptomlar']:
            st.write(f"• {semptom}")
        st.divider()
        
        # Genel Çözümler
        st.subheader("✅ Çözüm Adımları")
        for i, çözüm in enumerate(sorun_bilgi['genel_çözümler'], 1):
            st.write(f"{i}. {çözüm}")
        st.divider()
        
        # Filament Önerileri
        st.subheader("🧵 Filament Seçimi Önerileri")
        
        # Filament verilerini al
        df = pd.DataFrame(FILAMENT_DATA, columns=COLUMNS)
        
        # Sorunla ilgili filament özelliklerini analiz et
        if sorun_bilgi['filament_özellikleri']:
            # Öznitelik-tabanlı tavsiye
            for ozellik, bilgi in sorun_bilgi['filament_özellikleri'].items():
                kritik_deger = bilgi['kritik']
                
                # İyi olanlar (kritik değerin üzerinde)
                iyi_filamentler = df[df[ozellik] >= kritik_deger].sort_values(ozellik, ascending=False).head(5)
                
                # Kötü olanlar (kritik değerin altında)
                kotu_filamentler = df[df[ozellik] < kritik_deger].sort_values(ozellik).head(5)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success(f"✅ **ÖNERILEN FİLAMENTLER** ({ozellik})")
                    st.markdown(f"*{bilgi['tavsiye_yüksek']}*")
                    for _, row in iyi_filamentler.iterrows():
                        st.write(f"• **{row['Filament']}** - Skor: {int(row[ozellik])}/100")
                
                with col2:
                    st.error(f"❌ **KAÇINILMASI GEREKEN** ({ozellik})")
                    st.markdown(f"*{bilgi['tavsiye_düşük']}*")
                    for _, row in kotu_filamentler.iterrows():
                        st.write(f"• **{row['Filament']}** - Skor: {int(row[ozellik])}/100")
        
        st.divider()
        
        # İlk Katman Sorunu İçin Özel Tablo
        if secili_sorun == "İlk Katman Yapışması":
            st.subheader("📊 Filamentlerin İlk Katman Yapışma Sıralaması")
            
            ilk_katman_df = df[['Filament', 'IlkKatmanYapisma', 'WarpingDirenci', 'NemHassasiyeti']].copy()
            ilk_katman_df.columns = ['Filament', 'İlk Katman', 'Warping', 'Nem Hassas.']
            ilk_katman_df = ilk_katman_df.sort_values('İlk Katman', ascending=False)
            
            st.dataframe(ilk_katman_df.head(15), use_container_width=True, hide_index=True)
        
        # İpliklenme Sorunu İçin Özel Tablo
        elif secili_sorun == "İpliklenme (Stringing)":
            st.subheader("📊 Filamentlerin String Çıkarmama Sıralaması")
            
            string_df = df[['Filament', 'StringOlusumu', 'BaskiKolayligi']].copy()
            string_df.columns = ['Filament', 'String Direnci', 'Baskı Kolaylığı']
            string_df = string_df.sort_values('String Direnci', ascending=False)
            
            st.dataframe(string_df.head(15), use_container_width=True, hide_index=True)
        
        # Warping Sorunu İçin Özel Tablo
        elif secili_sorun == "Warping (Raf Bükülmesi)":
            st.subheader("📊 Filamentlerin Warping Direnci Sıralaması")
            
            warping_df = df[['Filament', 'WarpingDirenci', 'IsitmalıYatakIhtiyaci', 'KapaliKasaIhtiyaci']].copy()
            warping_df.columns = ['Filament', 'Warping Direnci', 'Yatak Gerekli', 'Kasa Gerekli']
            warping_df = warping_df.sort_values('Warping Direnci', ascending=False)
            
            st.dataframe(warping_df.head(15), use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Pratik İpuçları - Filament Bazlı
        st.subheader("💡 Filament Tipine Göre Özel İpuçları")
        
        sorun_filament_tips = {
            "İlk Katman Yapışması": {
                "PLA": "🟢 PLA: Hairspray/glue stick en etkili. Tabla 50-60°C, nozzul 200-210°C. İlk katman yavaş (30mm/s)",
                "ABS": "🔴 ABS: Ísıtmalı tabla zorunlu (100°C+), kapalı kasa önerilir. Yapışkan (hairspray) kullan.",
                "PETG": "🟡 PETG: PEI yüzeyde mükemmel. Tabla 70-80°C. Cam tablada sorun yaşayabilir.",
                "TPU": "🟣 TPU: Esnek filament yapışma zor. Brim zorunlu. Tabla 40-50°C, yavaş bas.",
                "Nylon": "🔵 Nylon: Kapalı kasa + yüksek tabla (60-70°C). Nem kontrolü kritik.",
                "ASA": "🔴 ASA: ABS gibi davran. 100-110°C tabla, kapalı kasa zorunlu."
            },
            "İpliklenme (Stringing)": {
                "PLA": "🟢 PLA: Retract 2-3mm, 40mm/s. Stringing az olur. Z-Hop 0.2mm ekle.",
                "ABS": "🔴 ABS: Retract 4-6mm (Bowden), 60mm/s gerekir. Sıcaklığı 5°C düşür.",
                "PETG": "🟡 PETG: Retract 3-4mm, 50mm/s. Nozzul 235-240°C optimize et.",
                "TPU": "🟣 TPU: Retract çok dikkatli (1-2mm). Hızı azalt.",
                "PC": "🔵 PC: Yüksek temp = string. Retract 4-5mm, sıcaklık optimize et."
            },
            "Warping (Raf Bükülmesi)": {
                "PLA": "🟢 PLA: Az warping. 50°C tabla yeterli, kapalı kasa opsiyonel.",
                "ABS": "🔴 ABS: Çok warping! 100°C+ tabla, kapalı kasa ZORUNLU, brim ekle.",
                "PETG": "🟡 PETG: Orta warping. 70-80°C tabla, brim ekle, fan 50% azalt.",
                "PC": "🔵 PC: Çok warping! 110°C+ tabla, kapalı kasa zorunlu, soğutma min.",
                "TPU": "🟣 TPU: Az warping fakat yapışma zor. 40-50°C tabla."
            },
            "Underextrusion (Filament Yetersiz)": {
                "PLA": "🟢 PLA: Flow %105-110, hızı azalt. Feeder basıncını kontrol et.",
                "ABS": "🔴 ABS: Flow %110 deneme. Nozzul 245°C optimize et.",
                "PETG": "🟡 PETG: Flow %105, nozzul 250°C+ gerekebilir.",
                "Nylon": "🔵 Nylon: Çok düşük akış = problem. Flow %115 deneme."
            },
            "Banding / Layer Ghosting": {
                "PLA": "🟢 PLA: Hızı 40mm/s'e azalt. Z-motor oyunu kontrol et.",
                "ABS": "🔴 ABS: Sıcaklık dalgalanmaya duyarlı. Fan sabit tutmalı.",
                "PETG": "🟡 PETG: Hızı 50mm/s'e azalt, table level kontrol et."
            },
            "Nozzule Tıkanması": {
                "PLA": "🟢 PLA: 1.5-2mm drill ile nozzulu temizle. Minimum sıcaklık 195°C.",
                "ABS": "🔴 ABS: 240°C'de temizle, akaryağında beklet.",
                "PETG": "🟡 PETG: 245°C optimize et. Karbon karbonizasyon gözle."
            },
            "Filament Skipping": {
                "Nylon": "🔵 Nylon: Feeder basıncı dikkat et (çok sıkı = ezme).",
                "PC": "🔵 PC: Yüksek sıcaklık + yüksek akış = sıkışma. Nozzul 260°C+ kontrol.",
                "ABS-CF": "🔴 ABS-CF: Carbon fill = aşındırıcı. Hardened nozzul kullan."
            },
            "Moisture Marks": {
                "Nylon": "🔵 Nylon: ÇOK NEM HASSASı. 6-8 saat 60°C kurutma zorunlu!",
                "ASA": "🔴 ASA: 4-6 saat 70°C kurutma önerilir.",
                "PC": "🔵 PC: 4-6 saat 70°C kurutma.",
                "PETG": "🟡 PETG: Az nem hassas fakat yine kurut (2-3 saat)."
            },
            "Curling (Kenar Kıvrılması)": {
                "ABS": "🔴 ABS: 100°C+ tabla, kapalı kasa ZORUNLU. Brim uzun tutun.",
                "PC": "🔵 PC: 110°C+ tabla, kapalı kasa, raft kullan.",
                "ASA": "🔴 ASA: 105°C tabla, kapalı kasa önerilir."
            },
            "Üst Katmanında Delikler": {
                "PLA": "🟢 PLA: Top layer 4-5 katman, infill %20+ yap.",
                "PETG": "🟡 PETG: Flow %105 üst katmanda, hızı azalt.",
                "ABS": "🔴 ABS: İnfill %25+, top layer kalınlaştır."
            }
        }
        
        for filament_tipi, ipucu in sorun_filament_tips.get(secili_sorun, {}).items():
            st.info(ipucu)
        
        st.divider()
        
        # Video ve kaynak önerileri
        st.subheader("📚 Ek Kaynaklar & İpuçları")
        st.markdown("""
        ### 🧪 Deneme Modellleri (Thingiverse'te Ara):
        - **Stringing Test**: İplik kontrolü
        - **Warping Test / Torture Test**: Warping & mekanikal özellikler
        - **First Layer Test**: İlk katman iyileştirmeleri
        - **Overhang Test**: Çıkıntı performansı
        - **Bridging Test**: Köprü yeteneği
        - **Adhesion Test**: Tabla yapışması
        
        ### 💡 Pratik İpuçları:
        - **Her filament benzersizdir**: Farklı üreticiler = farklı ayarlar. Test et!
        - **5°C Önemlidir**: Sıcaklıkta 5°C değişim = büyük fark
        - **Bir şeyi değiştir**: Aynı anda çok sayıda ayar değiştirme (karıştırır)
        - **Notlar Al**: Hangi ayarlar çalıştı, hangisi çalışmadı - kaydet
        - **Filament Kalitesi**: Ucuz filament = ucuz sonuç. Kaliteli marka seç
        - **Nem = Düşman**: Filamenti kuru tut. Kurtucu hatta böyle yatır
        - **Kalibrasyonlar**:
          - E-Steps: 100mm test ile kalibre et
          - PID Tuning: Sıcaklık sabitliği için
          - Pressure Advance: Filament basıncı
        - **Z-Offset**: Tabla leveling'in 80% sorunu çözer
        
        ### 🔧 Yazıcı Bakımı:
        - Aylık: Tüm eksenleri temizle/yağla
        - Kama kemerleri: Düzgün gerginlik tut
        - Nozzul: Her filament değişiminde temizle
        - Hotend: Karbon temizliği yap
        
        ### 📊 Ayar Cheat Sheet:
        | Sorun | Çözüm |
        |-------|--------|
        | Kötü yapışma | Tabla leveling, +sıcaklık, yavaş hız |
        | Stringing | Retract +, sıcaklık -, travel hızı + |
        | Warping | Tabla sıcaklık +, kapalı kasa, brim |
        | Underextrusion | Flow +, hız -, nozzul sıcak |
        | Zayıf detay | Hız -, soğutma +, nozzul optimize |
        """)
