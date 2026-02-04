#!/usr/bin/env python3
"""
Filament Karar Motoru PRO++ (Endüstriyel Seviye - Genişletilmiş)
----------------------------------------------------------------
TR: FDM filamentleri 28+ kriter ile detaylı değerlendirme
EN: Detailed evaluation of FDM filaments with 28+ criteria

TR: Kullanıcı beklentilerini 0–5 arası ağırlıklandırır
EN: User expectations weighted from 0-5

TR: Donanım kısıtlarını hesaba katar (ceza sistemi)
EN: Takes hardware constraints into account (penalty system)

TR: Post-processing, optik, ileri baskı özellikleri dahil
EN: Includes post-processing, optical, advanced printing features

TR: En uygun filamentleri gerçekçi olarak sıralar
EN: Realistically ranks the most suitable filaments

Çalıştırma / Run:
./filament_karar_motoru.py
"""

import pandas as pd

# ============================================================================
# FİLAMENT VERİ TABANI / FILAMENT DATABASE
# ============================================================================
# TR: Her satır bir filament tipini temsil eder
# EN: Each row represents a filament type
#
# TR: Her sütun 0-100 arası bir mühendislik skorudur (100 = en iyi)
# EN: Each column is an engineering score from 0-100 (100 = best)
#
# TR: YENİ FİLAMENT EKLEMEK İÇİN:
# EN: TO ADD NEW FILAMENT:
#    1. Yeni bir liste ekleyin / Add a new list
#    2. İlk eleman filament adı / First element is filament name
#    3. Sonraki 30 eleman COLUMNS sırasına göre skorlar / Next 30 elements are scores in COLUMNS order
#    4. Örnek: ["PLA+", 45, 45, 72, 42, 50, 35, 35, ...]
# ============================================================================

FILAMENT_DATA = [
    # Filament Adı / Filament Name
    # -------------------------------------------------------------------------
    # DAYANIM (7 kriter) / DURABILITY (7 criteria):
    #   Isi: Isı dayanımı / Heat resistance
    #   UV: UV dayanımı / UV resistance
    #   Nem: Nem dayanımı / Moisture resistance
    #   Kim: Kimyasal dayanım / Chemical resistance
    #   Dar: Darbe dayanımı / Impact resistance
    #   Yuk: Yük taşıma / Load bearing
    #   Asn: Aşınma direnci / Wear resistance
    # -------------------------------------------------------------------------
    # MEKANİK (7 kriter) / MECHANICAL (7 criteria):
    #   Kat: Katman aderansı / Layer adhesion
    #   Sta: Boyutsal stabilite / Dimensional stability
    #   Esn: Esneklik / Flexibility
    #   Tit: Titreşim sönümleme / Vibration damping
    #   Sur: Sürünme direnci / Creep resistance
    #   Yor: Yorulma dayanımı / Fatigue resistance
    #   Cek: Çekme mukavemeti / Tensile strength
    # -------------------------------------------------------------------------
    # BASKI (7 kriter) / PRINTING (7 criteria):
    #   War: Warping direnci / Warping resistance
    #   Kol: Baskı kolaylığı / Print ease
    #   Str: String oluşmaması / No stringing (higher = less string)
    #   IlkK: İlk katman yapışma / First layer adhesion
    #   Kop: Köprüleme / Bridging capability
    #   Cik: Çıkıntı performansı / Overhang performance
    #   BskH: Baskı hızı / Print speed capability
    # -------------------------------------------------------------------------
    # POST-PROCESSING (3 kriter) / POST-PROCESSING (3 criteria):
    #   Zim: Zımparalanabilirlik / Sandability
    #   Boy: Boyanabilirlik / Paintability
    #   Yap: Yapıştırılabilirlik / Gluability
    # -------------------------------------------------------------------------
    # OPTİK (2 kriter) / OPTICAL (2 criteria):
    #   Sef: Şeffaflık / Transparency
    #   YuzP: Yüzey parlaklığı / Surface gloss
    # -------------------------------------------------------------------------
    # RİSKLER (5 kriter - YÜKSEK = KÖTÜ) / RISKS (5 criteria - HIGH = BAD):
    #   Kap: Kapalı kasa ihtiyacı / Enclosed chamber need
    #   NemH: Nem hassasiyeti / Moisture sensitivity
    #   Noz: Nozul aşındırıcılık / Nozzle abrasiveness
    #   Kok: Koku / Odor
    #   DesI: Destek ihtiyacı / Support requirement
    #   YatakI: Isıtmalı yatak ihtiyacı / Heated bed requirement (0-100, higher = more need)
    #   MinNoz: Minimum nozul sıcaklığı / Minimum nozzle temp (°C)
    #   BowZor: Bowden zorluğu / Bowden difficulty (0-100, higher = harder with Bowden)
    # -------------------------------------------------------------------------
    # TABLA UYUMLULUK (6 kriter) / BED SURFACE COMPATIBILITY (6 criteria):
    #   Cam: Cam tabla / Glass bed (0-100, higher = better adhesion)
    #   PEI_S: PEI Smooth / PEI Smooth (0-100)
    #   PEI_T: PEI Textured / PEI Textured (0-100)
    #   Build: BuildTak/PEX (0-100)
    #   Garo: Garolite (FR4) (0-100)
    #   PP: PP Sheet (0-100)
    # -------------------------------------------------------------------------
    # NOZZLE (1 kriter) / NOZZLE (1 criterion):
    #   MinNozzle: Minimum önerilen nozzle (mm) / Minimum recommended nozzle (mm)
    # -------------------------------------------------------------------------

    # ========== PLA AİLESİ / PLA FAMILY ==========
    
    ["PLA",
     40, 40, 70, 40, 45, 30, 30,
     60, 80, 0, 20, 30, 35, 40,
     80, 90, 10, 75, 70, 65, 85,
     90, 90, 85,
     60, 70,
     0, 20, 0, 5, 10,
     10, 190, 5,
     95, 90, 75, 85, 30, 40,
     0.2],

    ["PLA+",
     45, 45, 75, 45, 55, 40, 35,
     70, 85, 0, 25, 40, 45, 50,
     85, 90, 15, 80, 75, 70, 85,
     95, 95, 90,
     50, 75,
     0, 15, 0, 5, 10,
     10, 200, 5,
     92, 88, 78, 88, 32, 42,
     0.2],

    ["Silk PLA",
     38, 35, 68, 38, 40, 25, 25,
     55, 75, 0, 15, 25, 30, 35,
     75, 85, 5, 70, 65, 60, 80,
     75, 80, 70,
     40, 95,
     0, 20, 0, 5, 15,
     10, 200, 10,
     90, 85, 70, 82, 28, 38,
     0.4],

    ["Wood PLA",
     35, 30, 60, 35, 35, 20, 40,
     50, 70, 0, 15, 20, 25, 30,
     70, 80, 15, 65, 60, 55, 75,
     95, 70, 60,
     10, 40,
     0, 25, 15, 10, 20,
     10, 200, 10,
     88, 82, 68, 80, 25, 35,
     0.6],

    ["Metal Fill PLA",
     42, 38, 65, 42, 40, 35, 50,
     55, 78, 0, 20, 35, 38, 42,
     75, 75, 20, 68, 62, 58, 70,
     85, 65, 75,
     5, 85,
     0, 22, 30, 8, 25,
     15, 205, 15,
     85, 78, 65, 75, 23, 33,
     0.6],

    ["Matte PLA",
     40, 40, 72, 40, 48, 32, 32,
     62, 82, 0, 22, 32, 37, 42,
     82, 88, 12, 75, 72, 67, 83,
     88, 88, 83,
     45, 25,
     0, 18, 0, 5, 12,
     10, 195, 5,
     93, 87, 72, 83, 29, 39,
     0.2],

    # ========== PETG AİLESİ / PETG FAMILY ==========

    ["PETG",
     60, 60, 75, 60, 65, 60, 50,
     70, 70, 0, 30, 50, 55, 55,
     70, 80, 25, 80, 65, 60, 75,
     65, 75, 70,
     80, 75,
     0, 30, 0, 10, 20,
     30, 230, 15,
     75, 95, 92, 80, 35, 45,
     0.2],

    ["PETG-CF",
     75, 70, 70, 70, 70, 75, 80,
     75, 80, 0, 35, 70, 75, 75,
     75, 65, 30, 75, 60, 55, 70,
     55, 70, 65,
     50, 65,
     10, 35, 70, 15, 25,
     40, 250, 20,
     70, 92, 95, 75, 40, 50,
     0.4],

    ["PETG-GF",
     72, 68, 68, 68, 72, 80, 75,
     72, 82, 0, 32, 68, 72, 72,
     72, 68, 28, 72, 62, 58, 72,
     58, 72, 68,
     55, 68,
     5, 32, 50, 12, 22,
     35, 245, 18,
     72, 90, 93, 77, 38, 48,
     0.4],

    # ========== ABS/ASA AİLESİ / ABS/ASA FAMILY ==========

    ["ABS",
     85, 40, 65, 60, 75, 70, 60,
     65, 60, 0, 25, 65, 70, 75,
     40, 50, 40, 70, 55, 50, 80,
     85, 95, 80,
     30, 50,
     80, 30, 0, 70, 35,
     85, 240, 20,
     60, 88, 92, 70, 50, 35,
     0.2],

    ["ASA",
     90, 85, 80, 65, 75, 70, 60,
     65, 65, 0, 25, 70, 75, 75,
     50, 50, 35, 75, 60, 55, 80,
     85, 95, 80,
     20, 55,
     70, 30, 0, 65, 30,
     90, 250, 20,
     62, 90, 95, 72, 52, 37,
     0.2],

    ["PC-ABS",
     88, 50, 72, 68, 82, 78, 68,
     72, 68, 0, 28, 72, 78, 82,
     45, 45, 42, 72, 58, 52, 78,
     82, 92, 78,
     25, 52,
     85, 35, 0, 68, 38,
     92, 260, 22,
     58, 85, 90, 68, 51, 36,
     0.2],

    # ========== TPU AİLESİ / TPU FAMILY ==========

    ["TPU 95A",
     50, 60, 85, 70, 95, 0, 80,
     90, 85, 100, 90, 95, 90, 30,
     90, 40, 5, 60, 85, 90, 45,
     40, 50, 60,
     50, 40,
     0, 40, 0, 20, 45,
     20, 220, 90,
     85, 95, 90, 88, 25, 55,
     0.4],

    ["TPU 85A",
     48, 58, 88, 72, 98, 0, 85,
     92, 88, 95, 95, 98, 95, 28,
     92, 35, 3, 58, 88, 92, 40,
     35, 45, 55,
     45, 38,
     0, 45, 0, 22, 50,
     18, 215, 95,
     88, 97, 93, 90, 23, 58,
     0.4],

    ["TPU 60D",
     45, 55, 90, 75, 100, 0, 88,
     95, 90, 90, 98, 100, 98, 25,
     95, 30, 2, 55, 90, 95, 35,
     30, 40, 50,
     40, 35,
     0, 50, 0, 25, 55,
     15, 210, 98,
     90, 98, 95, 92, 28, 60,
     0.6],

    # ========== NYLON (PA) AİLESİ / NYLON (PA) FAMILY ==========

    ["PA6 (Nylon 6)",
     95, 60, 40, 80, 90, 90, 85,
     80, 75, 0, 30, 85, 85, 90,
     60, 30, 30, 65, 50, 45, 70,
     70, 80, 75,
     10, 45,
     60, 90, 0, 25, 50,
     70, 250, 30,
     55, 80, 95, 65, 95, 40,
     0.4],

    ["PA12 (Nylon 12)",
     92, 62, 45, 82, 88, 88, 82,
     82, 78, 0, 32, 82, 82, 88,
     65, 35, 32, 68, 52, 48, 72,
     72, 82, 78,
     12, 48,
     55, 85, 0, 22, 48,
     65, 245, 28,
     58, 82, 93, 68, 94, 41,
     0.4],

    ["PA612",
     94, 61, 42, 81, 89, 89, 84,
     81, 76, 0, 31, 84, 84, 89,
     62, 32, 31, 66, 51, 46, 71,
     71, 81, 76,
     11, 46,
     58, 88, 0, 24, 49,
     68, 255, 29,
     56, 81, 94, 66, 95, 40,
     0.4],

    ["PA6-GF",
     98, 65, 38, 85, 85, 95, 90,
     75, 82, 0, 28, 88, 88, 92,
     68, 25, 28, 62, 48, 42, 68,
     68, 78, 72,
     8, 42,
     65, 85, 60, 28, 55,
     75, 265, 32,
     52, 78, 92, 62, 96, 38,
     0.6],

    ["PA-CF",
     100, 65, 55, 85, 85, 95, 95,
     70, 85, 0, 20, 90, 90, 95,
     70, 20, 25, 60, 45, 40, 65,
     50, 75, 60,
     5, 40,
     80, 70, 90, 30, 60,
     75, 280, 35,
     50, 75, 90, 60, 98, 42,
     0.6],

    ["PA12-CF",
     98, 66, 58, 86, 86, 93, 93,
     72, 86, 0, 22, 88, 88, 93,
     72, 25, 27, 62, 47, 42, 67,
     52, 77, 62,
     7, 42,
     75, 68, 85, 28, 58,
     72, 275, 33,
     52, 77, 88, 62, 97, 41,
     0.6],

    # ========== PC AİLESİ / PC FAMILY ==========

    ["PC",
     95, 60, 70, 75, 90, 85, 70,
     75, 65, 0, 25, 75, 80, 85,
     30, 30, 45, 65, 45, 40, 70,
     60, 85, 70,
     85, 80,
     90, 40, 0, 50, 40,
     95, 290, 25,
     55, 85, 95, 65, 45, 38,
     0.4],

    ["PC-CF",
     100, 65, 68, 80, 88, 92, 85,
     78, 75, 0, 22, 82, 88, 92,
     40, 25, 48, 62, 42, 38, 68,
     55, 82, 68,
     50, 75,
     95, 38, 75, 52, 45,
     98, 300, 28,
     50, 82, 92, 60, 48, 36,
     0.6],

    # ========== DESTEK MALZEMELERİ / SUPPORT MATERIALS ==========

    ["PVA",
     35, 30, 0, 50, 25, 15, 20,
     40, 55, 5, 10, 15, 20, 20,
     60, 70, 5, 60, 50, 45, 65,
     20, 30, 95,
     30, 40,
     0, 100, 0, 5, 0,
     10, 190, 15,
     92, 88, 75, 85, 28, 35,
     0.2],

    ["HIPS",
     75, 35, 60, 55, 60, 50, 45,
     55, 58, 0, 20, 50, 55, 60,
     45, 60, 30, 65, 52, 48, 70,
     80, 85, 90,
     25, 45,
     70, 25, 0, 65, 0,
     75, 230, 18,
     62, 86, 90, 72, 48, 33,
     0.2],

    ["Breakaway",
     42, 38, 68, 42, 48, 28, 32,
     52, 72, 2, 18, 32, 38, 42,
     72, 75, 12, 72, 68, 62, 78,
     75, 78, 92,
     52, 58,
     0, 22, 0, 8, 0,
     12, 205, 12,
     90, 87, 78, 83, 29, 39,
     0.2],

    # ========== ÖZEL MALZEMELER / SPECIAL MATERIALS ==========

    ["PEEK",
     100, 80, 85, 95, 95, 100, 100,
     85, 90, 0, 15, 95, 95, 100,
     50, 10, 50, 55, 35, 30, 50,
     40, 70, 55,
     5, 50,
     100, 80, 100, 80, 80,
     100, 400, 50,
     40, 70, 98, 50, 48, 35,
     0.4],

    ["PEI (Ultem)",
     100, 75, 80, 90, 92, 98, 98,
     82, 88, 0, 18, 92, 92, 98,
     45, 15, 48, 58, 38, 32, 55,
     45, 75, 60,
     8, 55,
     100, 75, 95, 75, 75,
     100, 380, 45,
     45, 75, 98, 55, 50, 37,
     0.4],

    ["PP (Polypropylene)",
     70, 65, 95, 85, 80, 60, 75,
     50, 60, 10, 35, 70, 75, 70,
     85, 55, 60, 40, 65, 70, 65,
     55, 65, 60,
     20, 50,
     40, 60, 0, 35, 45,
     55, 220, 35,
     30, 55, 75, 40, 30, 98,
     0.4],
]

# ============================================================================
# SÜTUN TANIMLARI / COLUMN DEFINITIONS
# ============================================================================
# TR: Bu liste FILAMENT_DATA'daki her sütunun ne anlama geldiğini tanımlar
# EN: This list defines what each column in FILAMENT_DATA means
#
# TR: YENİ KRİTER EKLEMEK İÇİN:
# EN: TO ADD NEW CRITERIA:
#    1. COLUMNS listesine yeni sütun adını ekleyin / Add new column name to COLUMNS list
#    2. FILAMENT_DATA'daki TÜM filamentlere o sütun için skor ekleyin / Add score for that column to ALL filaments in FILAMENT_DATA
#    3. main() fonksiyonundaki 'kriterler' dictionary'sine ekleyin / Add to 'kriterler' dictionary in main() function
# ============================================================================

COLUMNS = [
    "Filament",
    # Dayanım / Durability
    "IsiDayanim",
    "UVDayanim",
    "NemDayanim",
    "KimyasalDayanim",
    "DarbeDayanim",
    "YukTasima",
    "AsinmaDirenci",
    # Mekanik davranış / Mechanical behavior
    "KatmanAderans",
    "BoyutsalStabilite",
    "Esneklik",
    "TitreisimSondumleme",
    "SurunmeDirenci",
    "YorulmaDayanimi",
    "CekmeMukavemeti",
    # Baskı davranışı / Printing behavior
    "WarpingDirenci",
    "BaskiKolayligi",
    "StringOlusumu",  # düşük = kötü (az string = iyi) / low = bad (less string = good)
    "IlkKatmanYapisma",
    "KoprulemeYeteneği",
    "CikintiPerformansi",
    "BaskiHizi",
    # Post-processing
    "Zimparalanabilirlik",
    "Boyanabilirlik",
    "Yapistirilabilirlik",
    # Optik / Optical
    "Seffaflik",
    "YuzeyParlaklik",
    # Operasyonel riskler (yüksek = kötü) / Operational risks (high = bad)
    "KapaliKasaIhtiyaci",
    "NemHassasiyeti",
    "NozulAsindiricilik",
    "Koku",  # yüksek = kötü / high = bad
    "DestekIhtiyaci",  # yüksek = kötü / high = bad
    "IsitmalıYatakIhtiyaci",  # yüksek = kötü (yatak yoksa) / high = bad (if no heated bed)
    "MinNozulSicaklik",  # °C - minimum gerekli sıcaklık / °C - minimum required temp
    "BowdenZorlugu",  # yüksek = kötü (Bowden'da) / high = bad (with Bowden)
    # Tabla uyumluluk / Bed surface compatibility
    "CamTabla",  # Cam tabla uyumluluk / Glass bed compatibility
    "PEI_Smooth",  # PEI Smooth uyumluluk / PEI Smooth compatibility
    "PEI_Textured",  # PEI Textured uyumluluk / PEI Textured compatibility
    "BuildTak",  # BuildTak/PEX uyumluluk / BuildTak/PEX compatibility
    "Garolite",  # Garolite (FR4) uyumluluk - Nylon için ideal / Garolite (FR4) compatibility - Ideal for Nylon
    "PPSheet",  # PP Sheet uyumluluk - PP filament için / PP Sheet compatibility - For PP filament
    # Nozzle
    "MinNozzle"  # Minimum önerilen nozzle (mm) / Minimum recommended nozzle (mm)
]


# ============================================================================
# ANA PROGRAM / MAIN PROGRAM
# ============================================================================

def main():
    # TR: Filament verilerini pandas DataFrame'e yükle
    # EN: Load filament data into pandas DataFrame
    df = pd.DataFrame(FILAMENT_DATA, columns=COLUMNS)

    # ========================================================================
    # DONANIM DURUMU SORGULAMA / HARDWARE STATUS INQUIRY
    # ========================================================================
    # TR: Kullanıcının sahip olduğu donanım yeteneklerini öğren
    # EN: Learn about user's hardware capabilities
    #
    # TR: Bu bilgiler ceza sisteminde kullanılır
    # EN: This information is used in the penalty system
    # ========================================================================
    
    print("\n=== DONANIM VE ORTAM BİLGİLERİ ===")
    print("Aşağıdaki sorulara yanıt verin:\n")
    
    donanim = {}
    
    # 1. Kapalı kasa
    donanim['kapali_kasa'] = input("Kapalı kasa var mı? (e/h): ").lower() == 'e'
    
    # 2. Filament kurutma
    donanim['kurutma'] = input("Filament kurutma yapabilir misin? (e/h): ").lower() == 'e'
    
    # 3. Sertleştirilmiş nozul
    donanim['sert_nozul'] = input("Sertleştirilmiş nozul var mı? (e/h): ").lower() == 'e'
    
    # 4. Isıtmalı yatak
    donanim['isitmali_yatak'] = input("Isıtmalı yatak var mı? (e/h): ").lower() == 'e'
    if donanim['isitmali_yatak']:
        while True:
            try:
                donanim['max_yatak_sicaklik'] = int(input("Yatak max kaç °C çıkabilir? (örn: 60, 100, 120): "))
                if donanim['max_yatak_sicaklik'] > 0:
                    break
                print("Lütfen pozitif bir değer girin.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")
    else:
        donanim['max_yatak_sicaklik'] = 0
    
    # 5. Maksimum nozul sıcaklığı
    while True:
        try:
            donanim['max_nozul_sicaklik'] = int(input("Nozul max kaç °C çıkabilir? (örn: 260, 300, 350): "))
            if donanim['max_nozul_sicaklik'] > 0:
                break
            print("Lütfen pozitif bir değer girin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
    
    # 6. Ekstruder tipi
    print("\nEkstruder tipi:")
    print("  1 - Direkt ekstruder (TPU için ideal)")
    print("  2 - Bowden ekstruder")
    while True:
        try:
            ekstruder = int(input("Seçiminiz (1/2): "))
            if ekstruder in [1, 2]:
                donanim['bowden'] = (ekstruder == 2)
                break
            print("Lütfen 1 veya 2 girin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
    
    # 7. Nozzle ölçüleri - BİRDEN FAZLA OLABİLİR
    print("\nSahip olduğunuz TÜMÜ nozzle ölçülerini seçin (virgülle ayırın):")
    print("  1 - 0.2 mm")
    print("  2 - 0.4 mm (standart)")
    print("  3 - 0.6 mm")
    print("  4 - 0.8 mm")
    print("Örnek: 1,2,3 veya sadece 2")
    nozzle_map = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8}
    while True:
        try:
            nozzle_input = input("Seçimleriniz: ").replace(" ", "")
            nozzle_secimler = [int(x) for x in nozzle_input.split(',')]
            if all(n in nozzle_map for n in nozzle_secimler):
                donanim['nozzle_olculeri'] = [nozzle_map[n] for n in nozzle_secimler]
                break
            print("Lütfen 1, 2, 3 veya 4 değerlerini virgülle ayırarak girin.")
        except ValueError:
            print("Lütfen geçerli sayılar girin (örn: 1,2,3).")
    
    # 8. Tabla sayısı ve tipleri - GÜNCELLEME: 6 TİP
    tabla_tipleri_map = {
        1: ("Cam", "CamTabla"),
        2: ("PEI Smooth", "PEI_Smooth"),
        3: ("PEI Textured", "PEI_Textured"),
        4: ("BuildTak/PEX", "BuildTak"),
        5: ("Garolite (FR4)", "Garolite"),
        6: ("PP Sheet", "PPSheet")
    }
    
    print("\nKaç adet tabla yüzeyiniz var?")
    while True:
        try:
            tabla_sayisi = int(input("Tabla sayısı (1-6): "))
            if 1 <= tabla_sayisi <= 6:
                break
            print("Lütfen 1-6 arasında bir değer girin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
    
    donanim['tablalar'] = []
    print("\nTabla tiplerini seçin:")
    print("  1 - Cam (Glass)")
    print("  2 - PEI Smooth")
    print("  3 - PEI Textured / Powder Coated")
    print("  4 - BuildTak / PEX")
    print("  5 - Garolite (FR4) - Nylon için mükemmel!")
    print("  6 - PP Sheet - PP filament için ideal!")
    
    for i in range(tabla_sayisi):
        while True:
            try:
                tabla_tip = int(input(f"{i+1}. tabla tipi (1/2/3/4/5/6): "))
                if tabla_tip in tabla_tipleri_map:
                    donanim['tablalar'].append({
                        'tip': tabla_tip,
                        'isim': tabla_tipleri_map[tabla_tip][0],
                        'kolon': tabla_tipleri_map[tabla_tip][1]
                    })
                    break
                print("Lütfen 1, 2, 3, 4, 5 veya 6 girin.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")

    # ========================================================================
    # KULLANICI BEKLENTİLERİ (AĞIRLIKLANDIRMA) / USER EXPECTATIONS (WEIGHTING)
    # ========================================================================
    # TR: Her kriter için kullanıcıdan 0-5 arası önem derecesi al
    # EN: Get importance level from 0-5 for each criterion from user
    #
    # TR: 0 = Hiç önemli değil, 5 = Kritik öneme sahip
    # EN: 0 = Not important at all, 5 = Critically important
    #
    # TR: YENİ KRİTER EKLEMEK İÇİN:
    # EN: TO ADD NEW CRITERIA:
    #    1. 'kriterler' dictionary'sine yeni satır ekle / Add new line to 'kriterler' dictionary
    #    2. Anahtar: COLUMNS'daki isim / Key: name in COLUMNS
    #    3. Değer: Kullanıcıya gösterilecek açıklama / Value: description to show user
    #    4. Örnek: "YeniKriter": "Yeni kriterin açıklaması"
    # ========================================================================
    
    print("\n=== UYGULAMA GEREKSİNİMLERİNİ BELİRLEYİN ===")
    print("Her bir kriter için 0-5 arası puan verin:")
    print("(0 = önemsiz, 5 = kritik)\n")
    
    USER_WEIGHTS = {}
    kriterler = {
        # Dayanım / Durability
        "IsiDayanim": "Isı dayanımı",
        "UVDayanim": "UV dayanımı",
        "NemDayanim": "Nem dayanımı",
        "KimyasalDayanim": "Kimyasal dayanım",
        "DarbeDayanim": "Darbe dayanımı",
        "YukTasima": "Yük taşıma kapasitesi",
        "AsinmaDirenci": "Aşınma direnci",
        # Mekanik / Mechanical
        "KatmanAderans": "Katman aderansı",
        "BoyutsalStabilite": "Boyutsal stabilite / ölçü toleransı",
        "Esneklik": "Esneklik / yumuşaklık",
        "TitreisimSondumleme": "Titreşim / gürültü sönümleme",
        "SurunmeDirenci": "Sürünme direnci (uzun süreli yük)",
        "YorulmaDayanimi": "Yorulma dayanımı (tekrarlı yük)",
        "CekmeMukavemeti": "Çekme mukavemeti",
        # Baskı / Printing
        "WarpingDirenci": "Warping / eğilme direnci",
        "BaskiKolayligi": "Baskı kolaylığı",
        "StringOlusumu": "String oluşmaması (temiz baskı)",
        "IlkKatmanYapisma": "İlk katman yapışması",
        "KoprulemeYeteneği": "Köprüleme (bridging) yeteneği",
        "CikintiPerformansi": "Çıkıntı (overhang) performansı",
        "BaskiHizi": "Hızlı baskı yapabilme",
        # Post-processing
        "Zimparalanabilirlik": "Zımparalanabilirlik",
        "Boyanabilirlik": "Boyanabilirlik",
        "Yapistirilabilirlik": "Yapıştırılabilirlik",
        # Optik / Optical
        "Seffaflik": "Şeffaflık / ışık geçirgenliği",
        "YuzeyParlaklik": "Yüzey parlaklığı"
    }
    
    # TR: Her kriter için kullanıcıdan puan al (0-5 arası doğrulama ile)
    # EN: Get score from user for each criterion (with 0-5 validation)
    for key, label in kriterler.items():
        while True:
            try:
                puan = int(input(f"{label}: "))
                if 0 <= puan <= 5:
                    USER_WEIGHTS[key] = puan
                    break
                else:
                    print("Lütfen 0-5 arasında bir değer girin.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")

    # ========================================================================
    # POZİTİF SKOR HESAPLAMA / POSITIVE SCORE CALCULATION
    # ========================================================================
    # TR: Her filament için temel skoru hesapla
    # EN: Calculate base score for each filament
    #
    # TR: Formül: Skor = Σ(özellik_değeri × kullanıcı_ağırlığı)
    # EN: Formula: Score = Σ(property_value × user_weight)
    #
    # TR: Örnek: Kullanıcı "Isı dayanımı = 5" verdi
    #            PLA'nın Isı skoru = 40
    #            PLA'ya bu kriterden: 40 × 5 = 200 puan gelir
    # EN: Example: User gave "Heat resistance = 5"
    #              PLA's Heat score = 40
    #              PLA gets from this criterion: 40 × 5 = 200 points
    # ========================================================================
    
    df["Skor"] = 0
    for kriter, agirlik in USER_WEIGHTS.items():
        df["Skor"] += df[kriter] * agirlik

    # ========================================================================
    # CEZA SİSTEMİ / PENALTY SYSTEM
    # ========================================================================
    # TR: Kullanıcının donanımına uygun olmayan filamentlere ceza ver
    # EN: Penalize filaments not suitable for user's hardware
    #
    # TR: CEZA MANTĞI:
    # EN: PENALTY LOGIC:
    #    - Kapalı kasa yoksa → Yüksek sıcaklık filamentleri ceza yer (×2)
    #      No enclosure → High-temp filaments get penalty (×2)
    #    - Kurutma yoksa → Nem hassas filamentler ceza yer (×2)
    #      No dryer → Moisture-sensitive filaments get penalty (×2)
    #    - Sert nozul yoksa → Aşındırıcı filamentler AĞIR ceza yer (×3)
    #      No hardened nozzle → Abrasive filaments get HEAVY penalty (×3)
    #    - Isıtmalı yatak yoksa/yetersizse → High-temp filamentler ceza yer (×2.5)
    #      No/insufficient heated bed → High-temp filaments get penalty (×2.5)
    #    - Nozul sıcaklığı yetersizse → Bazı filamentler KULLANILMAZ (×5)
    #      Insufficient nozzle temp → Some filaments UNUSABLE (×5)
    #    - Bowden ekstruder → Esnek filamentler ceza yer (×2)
    #      Bowden extruder → Flexible filaments get penalty (×2)
    #
    # TR: YENİ CEZA EKLEMEK İÇİN:
    # EN: TO ADD NEW PENALTY:
    #    1. Yeni donanım sorusu ekle (yukarıda donanim dictionary'ye)
    #    2. Burada if kontrolü ekle
    #    3. İlgili risk sütununu ceza olarak çıkar
    # ========================================================================
    
    print("\n⚙️  Ceza sistemi devreye giriyor...")
    
    # 1. Kapalı kasa cezası
    if not donanim['kapali_kasa']:
        ceza = df["KapaliKasaIhtiyaci"] * 2
        df["Skor"] -= ceza
        print("   → Kapalı kasa yok: Yüksek sıcaklık filamentlerine ceza")
    
    # 2. Kurutma cezası
    if not donanim['kurutma']:
        ceza = df["NemHassasiyeti"] * 2
        df["Skor"] -= ceza
        print("   → Kurutma yok: Nem hassas filamentlere ceza")
    
    # 3. Sertleştirilmiş nozul cezası
    if not donanim['sert_nozul']:
        ceza = df["NozulAsindiricilik"] * 3
        df["Skor"] -= ceza
        print("   → Sertleştirilmiş nozul yok: Aşındırıcı filamentlere ağır ceza")
    
    # 4. Isıtmalı yatak cezası
    if not donanim['isitmali_yatak']:
        ceza = df["IsitmalıYatakIhtiyaci"] * 2.5
        df["Skor"] -= ceza
        print("   → Isıtmalı yatak yok: High-temp filamentlere ağır ceza")
    elif donanim['max_yatak_sicaklik'] < 90:
        # Yatak var ama düşük sıcaklık (ABS/ASA için 100°C+ gerekir)
        ceza = df["IsitmalıYatakIhtiyaci"] * 1.5
        df["Skor"] -= ceza
        print(f"   → Yatak sıcaklığı düşük ({donanim['max_yatak_sicaklik']}°C): High-temp filamentlere kısmi ceza")
    
    # 5. Nozul sıcaklığı cezası
    for idx, row in df.iterrows():
        min_sicaklik = row["MinNozulSicaklik"]
        if donanim['max_nozul_sicaklik'] < min_sicaklik:
            # Filament basılamaz
            ceza = 500 * (min_sicaklik - donanim['max_nozul_sicaklik'])
            df.loc[idx, "Skor"] -= ceza
            if idx == df.index[0]:  # İlk uyarıda genel mesaj
                print(f"   → Nozul max {donanim['max_nozul_sicaklik']}°C: Bazı filamentler basılamaz")
        elif donanim['max_nozul_sicaklik'] < min_sicaklik + 20:
            # Sınırda, riskli
            ceza = 100
            df.loc[idx, "Skor"] -= ceza
    
    # 6. Bowden ekstruder cezası
    if donanim['bowden']:
        ceza = df["BowdenZorlugu"] * 2
        df["Skor"] -= ceza
        print("   → Bowden ekstruder: Esnek filamentlere ceza")
    
    # 7. Nozzle ölçüsü cezası - ÇOKLU NOZZLE DESTEĞİ (YUMUŞATıLDı)
    max_kullanici_nozzle = max(donanim['nozzle_olculeri'])  # En büyük nozzle'ı kullan
    for idx, row in df.iterrows():
        min_nozzle = row["MinNozzle"]
        if max_kullanici_nozzle < min_nozzle:
            # Kullanıcının en büyük nozzle'ı bile çok küçük, filament basılamaz veya zorlanır
            ceza = 100 * (min_nozzle - max_kullanici_nozzle) * 5  # DAHA DENGELI: Her 0.1mm fark için ceza
            df.loc[idx, "Skor"] -= ceza
            if idx == df.index[0]:  # İlk uyarıda genel mesaj
                print(f"   → Nozzle {max_kullanici_nozzle} mm (max): Bazı dolgulu filamentler zorlanabilir")
    
    # 8. Küçük sabit cezalar (her zaman aktif)
    df["Skor"] -= df["Koku"] * 0.5  # Koku cezası / Odor penalty
    df["Skor"] -= df["DestekIhtiyaci"] * 0.5  # Destek cezası / Support penalty
    
    # 8.5. Tabla sıcaklık kontrolü (YENİ)
    # Bazı filamentler minimum tabla sıcaklığı gerektirir
    tabla_sicaklik_gereksinimleri = {
        'ABS': 100, 'ASA': 100, 'PC': 110, 'PC-ABS': 105, 'PC-CF': 115,
        'Nylon': 70, 'PA6': 70, 'PA12': 70, 'PA612': 70, 'PA6-GF': 80, 'PA-CF': 80, 'PA12-CF': 80,
        'PEEK': 140, 'PEI': 130, 'PEKK': 140, 'PPS': 120
    }
    
    if donanim['isitmali_yatak']:
        for idx, row in df.iterrows():
            filament_adi = row['Filament']
            # Kısmi eşleşme için kontrol (örn: "PA6 (Nylon 6)" için "PA6" gereksinimini bul)
            for key, min_temp in tabla_sicaklik_gereksinimleri.items():
                if key in filament_adi:
                    if donanim['max_yatak_sicaklik'] < min_temp:
                        # Tabla sıcaklığı yetersiz
                        ceza = 200 * (min_temp - donanim['max_yatak_sicaklik'])
                        df.loc[idx, "Skor"] -= ceza
                    break
    
    # 9. Tabla uyumluluk bonusu (sahip olunan tablalar için bonus ver) - 6 TİP
    tabla_kolonlari = {
        1: "CamTabla",
        2: "PEI_Smooth",
        3: "PEI_Textured",
        4: "BuildTak",
        5: "Garolite",
        6: "PPSheet"
    }
    
    # Her filament için en iyi tabla skorunu hesapla ve UYARI LİSTESİ oluştur
    df["EnIyiTabla"] = 0
    df["EnIyiTablaIsim"] = ""
    df["Uyarilar"] = ""  # Yeni kolon: Uyarı mesajları
    
    for idx, row in df.iterrows():
        uyari_listesi = []
        
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
        filament_adi = row['Filament']
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
        
        # UYARI 8: Tabla uyumsuzluğu (en iyi tabla bile düşükse)
        en_iyi_tabla_skor = 0
        for tabla in donanim['tablalar']:
            tabla_skor = row[tabla['kolon']]
            if tabla_skor > en_iyi_tabla_skor:
                en_iyi_tabla_skor = tabla_skor
        if en_iyi_tabla_skor < 60:
            uyari_listesi.append("⚠️ TABLA UYUMLULUĞU DÜŞÜK")
        
        # Uyarıları birleştir
        df.loc[idx, "Uyarilar"] = " | ".join(uyari_listesi) if uyari_listesi else "✅ Sorunsuz"

        en_iyi_skor = 0
        en_iyi_tabla = ""
        
        for tabla in donanim['tablalar']:
            tabla_kolon = tabla['kolon']  # Artık kolon adı direkt olarak tabla dict'inde
            tabla_skor = row[tabla_kolon]
            
            if tabla_skor > en_iyi_skor:
                en_iyi_skor = tabla_skor
                en_iyi_tabla = tabla['isim']
        
        df.loc[idx, "EnIyiTabla"] = en_iyi_skor
        df.loc[idx, "EnIyiTablaIsim"] = en_iyi_tabla
        
        # Bonus ekle (en iyi tabla skoru * 0.5 bonus)
        df.loc[idx, "Skor"] += en_iyi_skor * 0.5

    # ========================================================================
    # NORMALİZASYON / NORMALIZATION
    # ========================================================================
    # TR: Skorları 0-100 arasına normalize et (en yüksek skor = 100, en düşük = 0)
    # EN: Normalize scores to 0-100 range (highest score = 100, lowest = 0)
    #
    # TR: Min-Max normalizasyon kullanılır
    # EN: Min-Max normalization is used
    # ========================================================================
    
    # Min-Max normalizasyon: (Skor - Min) / (Max - Min) * 100
    skor_min = df["Skor"].min()
    skor_max = df["Skor"].max()
    
    if skor_max != skor_min:  # Sıfıra bölme hatası önleme
        df["Skor_Normalize"] = ((df["Skor"] - skor_min) / (skor_max - skor_min) * 100).round(1)
    else:
        df["Skor_Normalize"] = 100.0  # Tüm skorlar eşitse hepsi 100

    # ========================================================================
    # SONUÇLARI SIRALAMA VE GÖRÜNTÜLEME / SORT AND DISPLAY RESULTS
    # ========================================================================
    # TR: Filamentleri skora göre azalan sırada sırala
    # EN: Sort filaments by score in descending order
    # ========================================================================
    
    df = df.sort_values("Skor", ascending=False)

    print("\n" + "="*60)
    print("=== FILAMENT KARAR MOTORU SONUCU (PRO) ===")
    print("="*60 + "\n")
    print(df[["Filament", "Skor_Normalize"]].to_string(index=False))

    # TR: Detaylı analiz tablosu (seçili özellikler)
    # EN: Detailed analysis table (selected properties)
    print("\n📊 Detaylı analiz:\n")
    print(df[["Filament", "Skor", "IsiDayanim", "YukTasima", "BaskiKolayligi", 
              "SurunmeDirenci", "YorulmaDayanimi", "StringOlusumu", "BaskiHizi",
              "Zimparalanabilirlik", "Seffaflik"]].to_string(index=False))
    
    # TR: Tüm filamentlerin yüzdelik skorları
    # EN: Percentage scores of all filaments
    print("\n✅ Tüm filamentler (sıralı):")
    for i, row in df.iterrows():
        tabla_bilgi = f" [{row['EnIyiTablaIsim']}]" if row['EnIyiTablaIsim'] else ""
        uyari_kisa = "" if row['Uyarilar'] == "✅ Sorunsuz" else f" {row['Uyarilar'].split('|')[0].strip()}"
        print(f"   {row['Filament']}: %{row['Skor_Normalize']:.1f}{tabla_bilgi}{uyari_kisa}")
    
    # ========================================================================
    # CSV EXPORT - SONUÇLARI DOSYAYA KAYDET
    # ========================================================================
    csv_dosya = "filament_secim_sonucu.csv"
    
    # Seçili kolonları CSV'ye kaydet
    csv_kolonlar = [
        'Filament', 'Skor_Normalize', 'Skor', 
        'EnIyiTablaIsim', 'EnIyiTabla',
        'IsiDayanim', 'YukTasima', 'BaskiKolayligi', 
        'StringOlusumu', 'IlkKatmanYapisma',
        'Zimparalanabilirlik', 'MinNozulSicaklik',
        'Uyarilar'
    ]
    
    df_export = df[csv_kolonlar].copy()
    df_export.columns = [
        'Filament', 'Uyumluluk (%)', 'Ham Skor',
        'En İyi Tabla', 'Tabla Skoru',
        'Isı Dayanımı', 'Yük Taşıma', 'Baskı Kolaylığı',
        'String Yok', 'İlk Katman Yapışma',
        'Zımparalanabilirlik', 'Min Nozzle Sıcaklık',
        'Uyarılar'
    ]
    
    df_export.to_csv(csv_dosya, index=False, encoding='utf-8-sig')
    print(f"\n💾 Sonuçlar kaydedildi: {csv_dosya}")
    
    # TR: Tabla bazlı öneriler - 6 TİP DESTEĞİ
    # EN: Bed-specific recommendations - 6 TYPES SUPPORTED
    print("\n" + "="*60)
    print("📋 TABLA BAZLI ÖNERİLER / BED-SPECIFIC RECOMMENDATIONS")
    print("="*60)
    
    for tabla in donanim['tablalar']:
        tabla_kolon = tabla['kolon']
        tabla_isim = tabla['isim']
        
        print(f"\n🔹 {tabla_isim} için en uygun filamentler:")
        
        # Bu tabla için skorları sırala
        tabla_uyumlu = df.copy()
        tabla_uyumlu["TablaUyumluluk"] = tabla_uyumlu[tabla_kolon]
        tabla_uyumlu = tabla_uyumlu.sort_values("TablaUyumluluk", ascending=False)
        
        # En iyi 10 filament göster
        for idx, row in tabla_uyumlu.head(10).iterrows():
            uyumluluk = row["TablaUyumluluk"]
            if uyumluluk >= 80:
                emoji = "✅"
            elif uyumluluk >= 60:
                emoji = "⚠️"
            else:
                emoji = "❌"
            print(f"   {emoji} {row['Filament']}: %{uyumluluk:.0f} uyumluluk")


# ============================================================================
# PROGRAM BAŞLATMA / PROGRAM STARTUP
# ============================================================================
if __name__ == "__main__":
    main()
