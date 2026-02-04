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

# Sidebar - Donanım bilgileri
st.sidebar.header("⚙️ Yazıcı Donanımı")

donanim = {}
donanim['kapali_kasa'] = st.sidebar.checkbox("Kapalı kasa var", value=False)
donanim['kurutma'] = st.sidebar.checkbox("Filament kurutucu var", value=False)
donanim['sert_nozul'] = st.sidebar.checkbox("Sertleştirilmiş nozzle var", value=False)

donanim['isitmali_yatak'] = st.sidebar.checkbox("Isıtmalı yatak var", value=True)
if donanim['isitmali_yatak']:
    donanim['max_yatak_sicaklik'] = st.sidebar.number_input(
        "Yatak max sıcaklık (°C)", 
        min_value=0, 
        max_value=200, 
        value=60
    )
else:
    donanim['max_yatak_sicaklik'] = 0

donanim['max_nozul_sicaklik'] = st.sidebar.number_input(
    "Nozzle max sıcaklık (°C)", 
    min_value=150, 
    max_value=500, 
    value=260
)

donanim['bowden'] = st.sidebar.selectbox(
    "Ekstruder tipi",
    ["Direct", "Bowden"]
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
    default=["0.4 mm (standart)"]
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
    "Tabla yüzeyleri",
    options=list(tabla_secenekleri.keys()),
    default=["PEI Smooth"]
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
    w_uv = st.slider("UV dayanımı", 0, 5, 0)
    w_nem = st.slider("Nem dayanımı", 0, 5, 0)
    w_kimyasal = st.slider("Kimyasal dayanım", 0, 5, 0)
    w_darbe = st.slider("Darbe dayanımı", 0, 5, 0)
    w_yuk = st.slider("Yük taşıma", 0, 5, 0)
    w_asinma = st.slider("Aşınma direnci", 0, 5, 0)

with col2:
    st.subheader("⚙️ Mekanik Özellikler")
    w_katman = st.slider("Katman aderansı", 0, 5, 0)
    w_boyutsal = st.slider("Boyutsal stabilite", 0, 5, 0)
    w_esneklik = st.slider("Esneklik", 0, 5, 0)
    w_titresim = st.slider("Titreşim sönümleme", 0, 5, 0)
    w_surunme = st.slider("Sürünme direnci", 0, 5, 0)
    w_yorulma = st.slider("Yorulma dayanımı", 0, 5, 0)
    w_cekme = st.slider("Çekme mukavemeti", 0, 5, 0)

with col3:
    st.subheader("🖨️ Baskı & İşleme")
    w_warping = st.slider("Warping direnci", 0, 5, 0)
    w_kolaylik = st.slider("Baskı kolaylığı", 0, 5, 0)
    w_string = st.slider("String oluşmaması", 0, 5, 0)
    w_ilk_katman = st.slider("İlk katman yapışma", 0, 5, 0)
    w_kopruleme = st.slider("Köprüleme", 0, 5, 0)
    w_cikinti = st.slider("Çıkıntı performansı", 0, 5, 0)
    w_hiz = st.slider("Hızlı baskı", 0, 5, 0)
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
