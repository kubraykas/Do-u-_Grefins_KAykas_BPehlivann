#  CBAM Calculation, Prediction & Reporting System

Profesyonel modüler AB CBAM (Carbon Border Adjustment Mechanism) hesaplama, ETS fiyat tahmini ve yönetici raporlama sistemi.

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Private-red)

**AB Sınırda Karbon Düzenleme Mekanizması için kapsamlı çözüm**

</div>

---

#

Mevcut sisteme ek olarak, aşağıdaki profesyonel özellikler entegre edilmiştir:

### 1. 💎 Premium Arayüz ve İnteraktif Grafikler
- **Dark Mode UI**: Göz yormayan, modern ve kurumsal "Dark Mode" tasarımı.
- **Chart.js Entegrasyonu**: Emisyon dağılımı ve maliyet projeksiyonları için canlı, interaktif grafikler.
- **Dashboard**: "Banka Hazır" ve "Düşük Risk" indikatörleri ile anlık durum takibi.

### 2. ☁️ AWS DynamoDB Entegrasyonu
- **Bulut Kayıt**: Tüm analiz raporları artık AWS DynamoDB üzerinde güvenle saklanıyor.
- **UUID Takibi**: Her rapor için benzersiz kimlik (UUID) oluşturuluyor.

### 3. 🤖 Gelişmiş AI Strateji Raporları
- **Stratejik Odak**: "Maliyet" yerine "Sermaye Kazanımı" odaklı yönetici raporları.
- **Markdown Rendering**: Yapay zeka çıktıları artık temiz, okunabilir formatta (kalın başlıklar, listeler) sunuluyor.

### 4. 📄 Profesyonel PDF Çıktısı
- **Markalı Tasarım**: Enerji yeşili konseptine uygun, logolu ve grafikli PDF raporu.
- **Table of Contents**: Otomatik içindekiler tablosu ve yönetici özeti.

### 5. 🔬 Kapsamlı Emisyon Analizi (Scope 1 & 2)
- **Detaylı Girdi**: Doğalgaz, elektrik, kömür gibi kaynak bazlı emisyon hesaplama.
- **Optimizasyon**: ROI (Yatırım Getirisi) hesaplamalı iyileştirme senaryoları.

---

##  İçindekiler

- [Özellikler](#-özellikler)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Proje Yapısı](#-proje-yapısı)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Modüller](#-modüller)
- [CN Kodları](#-cn-kodları)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Örnekler](#-örnekler)
- [Konfigürasyon](#-konfigürasyon)
- [Sorun Giderme](#-sorun-giderme)

---

##  Özellikler

###  CBAM Hesaplama
-  **48+ ürün desteği** - Çelik, alüminyum, çimento, gübre, hidrojen
-  **Direkt ve indirekt emisyon** hesaplama
-  **Sertifika sayısı** otomatik hesaplama
-  **Maliyet analizi** - ETS fiyatına göre anlık hesaplama
-  **CN kod doğrulama** - Otomatik kod kontrolü

###  Emisyon Analizi (Yeni!)
-  **Scope 1 Emisyonlar** - Doğrudan emisyonlar (yakıt yanması, proses, termal enerji)
-  **Scope 2 Emisyonlar** - Dolaylı emisyonlar (elektrik tüketimi, yenilenebilir enerji payı)
-  **15+ veri girişi** - Kok kömürü, doğalgaz, elektrik tüketimi, proses emisyonları vb.
-  **Otomatik hesaplama** - Emisyon faktörleri ile otomatik CO2 hesabı
-  **Optimizasyon senaryoları** - 3 senaryo ile maliyet azaltım önerileri
-  **ROI analizi** - Yatırım geri ödeme ve karlılık hesaplamaları

###  ETS Fiyat Tahmini
-  **Gemini LLM entegrasyonu** - Yapay zeka tabanlı tahmin
-  **Çeyreklik projeksiyonlar** - Q1 2025 - Q4 2030
-  **İstatistiksel analiz** - Trend, volatilite, drift hesaplama
-  **Geçmiş veri analizi** - 2014'ten günümüze ETS fiyatları

###  CBAM Maliyet Projeksiyonu
-  **6 yıllık tahmin** - 2025-2030 arası detaylı analiz
-  **Risk seviyeleri** - Yüksek, orta, düşük risk dönemleri
-  **Yıllık toplam maliyetler** - Finansal planlama için
-  **Kritik dönem tespiti** - En yüksek maliyet dönemleri

###  Yönetici Raporları
-  **Profesyonel formatlar** - Türkçe yönetici raporu
-  **Otomatik üretim** - Gemini AI ile akıllı rapor (emisyon verileri dahil)
-  **Stratejik öneriler** - Kısa, orta, uzun vadeli aksiyonlar (sayısal hedeflerle)
-  **Risk analizi** - Detaylı risk değerlendirmesi
-  **Finansal etki** - Bütçe ve nakit akışı analizi
-  **Otomatik kaydetme** - Her rapor otomatik dosya sisteminize kaydedilir
-  **PDF indirme** - Tek tıkla profesyonel PDF raporu

###  Kullanıcı Arayüzleri
-  **Web Arayüzü** - Flask tabanlı minimal ve profesyonel tasarım
-  **Responsive Tasarım** - Mobil ve masaüstü uyumlu
-  **Minimal UI** - Beyaz/gri temiz tasarım (kurumsal görünüm)
-  **4 Adımlı Analiz** - CBAM → ETS → Maliyet → Emisyon Analizi → Rapor
-  **Komut Satırı** - CLI ile hızlı hesaplama
-  **Python API** - Programatik kullanım için

###  Teknik Özellikler
-  **Modüler yapı** - Her bileşen bağımsız
-  **Test edilmiş** - Kapsamlı test senaryoları
-  **Dokümante** - Detaylı kullanım kılavuzları
-  **Ölçeklenebilir** - Kolay genişletilebilir
-  **Bakımı kolay** - Temiz kod yapısı

---

## Proje Yapısı

```
cbam_project/
│
├──  src/                              # Ana Kaynak Kodlar
│   ├── __init__.py                      # Paket başlatıcı
│   ├── cn_code_database.py              # CN kod veritabanı (48 ürün)
│   ├── cbam_calculator.py               # CBAM hesaplama motoru
│   ├── emission_analyzer.py             # Scope 1&2 emisyon analizi (YENİ!)
│   ├── ets_predictor.py                 # ETS fiyat tahmin modülü (LLM)
│   ├── cbam_cost_forecaster.py          # CBAM maliyet tahmin modülü
│   ├── report_generator.py              # Yönetici raporu oluşturma (AI geliştirildi)
│   └── pdf_generator.py                 # PDF rapor oluşturma (YENİ!)
│
├──  web/                              # Web Uygulaması (Flask)
│   ├── app.py                           # Flask sunucu (rapor kaydetme eklendi)
│   ├── templates/                       # HTML şablonları
│   │   ├── index.html                   # Ana form sayfası (Scope 1&2 girişli)
│   │   ├── results.html                 # Hızlı sonuç sayfası
│   │   ├── full_results.html            # Detaylı analiz sayfası (YENİ!)
│   │   ├── cn_codes.html                # CN kod listesi
│   │   └── error.html                   # Hata sayfası
│   └── static/                          # Statik dosyalar
│       └── style.css                    # Minimal UI tasarımı (güncellendi)
│
├──  cli/                              # Komut Satırı Arayüzü
│   └── cbam_cli.py                      # CLI uygulaması
│
├──  tests/                            # Test Dosyaları
│   └── test_basic.py                    # Temel testler
│
├──  data/                             # Veri Dosyaları
│   └── (ETS geçmiş fiyat CSV dosyaları)
│
├──  config/                           # Konfigürasyon
│   └── (Ayar dosyaları)
│
├──  reports/                          # Oluşturulan Raporlar
│   └── (Otomatik üretilen raporlar)
│
├──  docs/                             # Dokümantasyon
│   └── (Kullanım kılavuzları)
│
├── Uygulamalar
│   ├── main.py                          # Ana Python API
│   ├── example.py                       # Kullanım örnekleri
│   └── RUN.py                           # Başlatma kılavuzu
│
├── Dokümantasyon
│   ├── README.md                        # Ana dokümantasyon
│   ├── PROJECT_STRUCTURE.md             # Proje yapısı
│   ├── requirements.txt                 # Python bağımlılıkları
│   ├── .env.example                     # Çevre değişkeni şablonu
│   └── .gitignore                       # Git ignore kuralları
│
└── Güvenlik
    └── .env                             # API anahtarları (gizli)
```

---

##  Hızlı Başlangıç

###  Web Arayüzü (Önerilen - En Kolay)

```bash
# 1. Proje dizinine git
cd cbam_project/web

# 2. Web uygulamasını başlat
python app.py

# 3. Tarayıcıda aç
# http://localhost:5000
```

**Avantajlar:**
-  Görsel arayüz
-  Form ile kolay girdi
-  Anında sonuçlar
-  CN kod listesi
-  API gerekmez

###  Komut Satırı (Hızlı Hesaplama)

```bash
# CLI'ya git
cd cbam_project/cli

# Çalıştır
python cbam_cli.py

# Ekranda adım adım ilerle
```

###  Python API (Gelişmiş Kullanım)

```python
from src.cbam_calculator import CBAMCalculator

# Hesaplayıcı oluştur
calc = CBAMCalculator(ets_price=85.0)

# Hesapla
summary = calc.get_summary(cn_code="7201", quantity=1000)

# Sonuçları göster
print(f"CBAM Maliyeti: €{summary['cbam_cost']:,.2f}")
print(f"Toplam Emisyon: {summary['total_emission']:,.2f} tCO2e")
print(f"Gerekli Sertifika: {summary['certificates']:,.2f}")
```

---

## Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- İnternet bağlantısı (LLM özellikleri için)

### Adım Adım Kurulum

```bash
# 1. Proje dizinine git
cd cbam_project

# 2. Sanal ortam oluştur (önerilen)
python -m venv venv

# 3. Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Bağımlılıkları yükle
pip install -r requirements.txt

# 5. Çevre değişkenlerini ayarla
# .env.example dosyasını .env olarak kopyala
copy .env.example .env

# 6. .env dosyasını düzenle ve API anahtarını ekle
# GOOGLE_API_KEY=your_api_key_here
```

### Bağımlılıklar

```txt
pandas>=2.0.0          # Veri işleme
numpy>=1.24.0          # Numerik hesaplamalar
google-genai>=0.2.0    # Gemini LLM entegrasyonu
flask>=2.3.0           # Web uygulaması (opsiyonel)
```

---

##  Kullanım

### 1 Web Arayüzü ile Kullanım

**Başlatma:**
```bash
cd web
python app.py
```

**Tarayıcıda:** `http://localhost:5000`

**Adımlar:**
1. ETS fiyatını girin (örn: 85.0 €/tCO2)
2. İthalat miktarını girin (örn: 1000 ton)
3. CN kodunu seçin veya yazın (örn: 7201)
4. "Hesapla" butonuna basın
5. Sonuçları görün

**Ne görürsünüz:**
- Toplam emisyon (tCO2e)
- Gerekli sertifika sayısı
- CBAM maliyeti (€)
- Ürün detayları
- Emisyon yoğunluğu

### 2 Komut Satırı ile Kullanım

```bash
cd cli
python cbam_cli.py
```

**Etkileşimli Girdi:**
```
ETS Fiyatı (€/tCO2): 85.0
Miktar (ton): 1000
CN Code: 7201
```

**Çıktı:**
```
 SONUÇLAR
Ürün: Pig iron
Kategori: Iron and Steel
Miktar: 1,000 ton

Direkt EI: 1.9 tCO2/ton
İndirekt EI: 0.17 tCO2/ton
Toplam EI: 2.07 tCO2/ton

Toplam Emisyon: 2,070.00 tCO2e
Gerekli Sertifika: 2,070.00

 CBAM Maliyeti: €175,950.00
```

### 3 Python Script ile Kullanım

**Basit Hesaplama:**
```python
from src.cbam_calculator import CBAMCalculator

# Hesaplayıcı oluştur
calc = CBAMCalculator(ets_price=85.0)

# Tek satırda sonuç
result = calc.get_summary("7201", 1000)
print(f"CBAM: €{result['cbam_cost']:,.2f}")
```

**Detaylı Hesaplama:**
```python
from src.cbam_calculator import CBAMCalculator

calc = CBAMCalculator(ets_price=85.0)

# Ürün verilerini al
data = calc.get_data_by_cn("7201")
if data:
    print(f"Ürün: {data['description']}")
    print(f"Toplam EI: {data['total_ei']} tCO2/ton")
    
    # Hesaplama yap
    result = calc.calculate(
        quantity=1000,
        direct_ei=data['direct_ei'],
        indirect_ei=data['indirect_ei']
    )
    
    print(f"Emisyon: {result['total_emission']} tCO2e")
    print(f"Sertifika: {result['certificates']}")
    print(f"Maliyet: €{result['cbam_cost']:,.2f}")
```

**Tam Analiz (LLM ile):**
```python
from main import CBAMApplication

# Uygulama oluştur (API key environment'dan)
app = CBAMApplication()

# Tam analiz çalıştır (hesaplama + tahmin + rapor)
result = app.run_full_analysis(
    ets_price=85.0,
    quantity=1000,
    cn_code="7201",
    csv_path="data/ets_prices.csv",
    save_report_path="reports/my_report.txt"
)

# Sonuçlar
print(f"Mevcut CBAM: €{result['cbam_summary']['cbam_cost']:,.2f}")
print(f"2025-2030 Toplam: €{result['report']['metrics']['total_cbam_cost']:,.2f}")
```

---

## Modüller

### 1. CN Code Database (`src/cn_code_database.py`)

**Amaç:** CBAM kapsamındaki ürünlerin emisyon yoğunluğu veritabanı

**İçerik:**
- 48+ ürün kaydı
- 9 farklı kategori
- Direkt, indirekt ve toplam emisyon değerleri

**Kategoriler:**
-  Iron and Steel (Demir ve Çelik)
-  Crude Steel (Ham Çelik)
-  Steel Products (Çelik Ürünleri)
-  Stainless Steel (Paslanmaz Çelik)
-  Cement (Çimento)
-  Aluminium (Alüminyum)
-  Aluminium Products (Alüminyum Ürünleri)
-  Fertilizers (Gübreler)
-  Hydrogen (Hidrojen)

**Kullanım:**
```python
from src.cn_code_database import CN_CODE_DATABASE, get_categories, search_by_description

# Tüm kategoriler
categories = get_categories()
print(categories)  # ['Iron and Steel', 'Cement', ...]

# Ürün arama
steel_products = search_by_description("steel")
print(f"{len(steel_products)} çelik ürünü bulundu")

# Direkt erişim
product = CN_CODE_DATABASE["7201"]
print(product["description"])  # "Pig iron"
print(product["total"])         # 2.07 tCO2/ton
```

---

### 2. CBAM Calculator (`src/cbam_calculator.py`)

**Amaç:** Temel CBAM hesaplama motoru

**Özellikler:**
- CN koda göre ürün verisi
- Emisyon hesaplama
- Sertifika sayısı
- Maliyet hesaplama
- Yabancı karbon fiyat düzeltmesi

**Sınıf:** `CBAMCalculator`

**Metodlar:**
```python
# 1. Constructor
CBAMCalculator(ets_price: float)

# 2. CN koda göre veri al
get_data_by_cn(cn_code: str) -> dict

# 3. Hesaplama yap
calculate(quantity: float, direct_ei: float, indirect_ei: float, 
          foreign_carbon_price: float = 0) -> dict

# 4. Tam özet
get_summary(cn_code: str, quantity: float) -> dict
```

**Örnek:**
```python
from src.cbam_calculator import CBAMCalculator

# Oluştur
calc = CBAMCalculator(ets_price=85.0)

# Ürün bilgisi
data = calc.get_data_by_cn("7201")
print(data)
# {
#     "description": "Pig iron",
#     "category": "Iron and Steel",
#     "direct_ei": 1.9,
#     "indirect_ei": 0.17,
#     "total_ei": 2.07
# }

# Hesapla
result = calc.calculate(
    quantity=1000,
    direct_ei=1.9,
    indirect_ei=0.17
)
print(result)
# {
#     "total_ei": 2.07,
#     "total_emission": 2070.0,
#     "certificates": 2070.0,
#     "cbam_cost": 175950.0,
#     "cbam_cost_adjusted": 175950.0
# }

# Tam özet (tek çağrı)
summary = calc.get_summary("7201", 1000)
print(summary.keys())
# ['product', 'category', 'quantity_tonnes', 'direct_ei', 
#  'indirect_ei', 'total_ei', 'total_emission', 'certificates', 
#  'ets_price', 'cbam_cost', 'cbam_cost_adjusted']
```

---

### 3. ETS Predictor (`src/ets_predictor.py`)

**Amaç:** Gemini LLM ile ETS fiyat tahmini

**Özellikler:**
- Geçmiş veri analizi
- İstatistiksel metrikler
- Çeyreklik tahminler (Q1 2025 - Q4 2030)
- Trend ve volatilite analizi

**Sınıf:** `ETSPricePredictor`

**Metodlar:**
```python
# 1. Constructor
ETSPricePredictor(gemini_client)

# 2. CSV yükle
load_data(csv_path: str) -> DataFrame

# 3. İstatistik hesapla
calculate_statistics(df: DataFrame) -> dict

# 4. Tahmin yap
predict(csv_path: str, model: str = "gemini-2.5-flash") -> (DataFrame, dict)
```

**Örnek:**
```python
from src.ets_predictor import ETSPricePredictor
from google import genai

# Gemini client
client = genai.Client()

# Predictor oluştur
predictor = ETSPricePredictor(client)

# Tahmin yap
forecast, stats = predictor.predict("data/ets_prices.csv")

# İstatistikler
print(f"Son fiyat: €{stats['last_price']:.2f}")
print(f"Ortalama: €{stats['mean_price']:.2f}")
print(f"Volatilite: €{stats['std_dev']:.2f}")

# Tahminler
print(forecast.head())
#     Quarter  Forecasted Value
# 0  Q1 2025             88.50
# 1  Q2 2025             92.30
# 2  Q3 2025             95.80
```

---

### 4. CBAM Cost Forecaster (`src/cbam_cost_forecaster.py`)

**Amaç:** ETS tahminlerine göre CBAM maliyet projeksiyonu

**Özellikler:**
- 6 yıllık maliyet tahmini
- ETS fiyat entegrasyonu
- Çeyreklik detay

**Sınıf:** `CBAMCostForecaster`

**Metodlar:**
```python
# 1. Constructor
CBAMCostForecaster(gemini_client)

# 2. Tahmin yap
forecast(cbam_summary: dict, ets_forecast_table: DataFrame, 
         model: str = "gemini-2.5-flash") -> str

# 3. Sonuçları parse et
parse_forecast_response(llm_text: str) -> DataFrame
```

**Örnek:**
```python
from src.cbam_cost_forecaster import CBAMCostForecaster

forecaster = CBAMCostForecaster(client)

# Tahmin
cost_forecast_text = forecaster.forecast(cbam_summary, ets_forecast)

# Parse et
cost_df = forecaster.parse_forecast_response(cost_forecast_text)

print(cost_df.head())
#     Quarter  ETS_Price  CBAM_Cost
# 0  Q1 2025      88.50   183195.0
# 1  Q2 2025      92.30   191040.0
```

---

### 5. Report Generator (`src/report_generator.py`)

**Amaç:** Profesyonel yönetici raporu oluşturma

**Özellikler:**
- Risk analizi
- Metrik hesaplama
- Stratejik öneriler
- Finansal etki analizi
- Türkçe rapor

**Sınıf:** `CBAMReportGenerator`

**Metodlar:**
```python
# 1. Constructor
CBAMReportGenerator(gemini_client)

# 2. Risk ekle
add_risk_analysis(cbam_df: DataFrame) -> DataFrame

# 3. Metrik hesapla
calculate_metrics(cbam_summary: dict, ets_forecast_table: DataFrame, 
                  cbam_df: DataFrame) -> dict

# 4. Rapor oluştur
generate_report(cbam_summary: dict, ets_forecast_table: DataFrame,
                cbam_cost_response: str, model: str = "gemini-2.5-flash") -> dict

# 5. Rapor kaydet
save_report(report_result: dict, output_path: str)
```

**Örnek:**
```python
from src.report_generator import CBAMReportGenerator

generator = CBAMReportGenerator(client)

# Rapor oluştur
report = generator.generate_report(
    cbam_summary,
    ets_forecast,
    cbam_cost_response
)

# Kaydet
generator.save_report(report, "reports/executive_report.txt")

# İçerik
print(report.keys())
# ['metrics', 'cbam_df', 'report_text', 'timestamp']
```

---

##  Desteklenen CN Kodları

Sisteme kayıtlı 50+ ürün kategorisi:
- **Demir ve Çelik**: 2601 12 00, 7201, 7208, vb.
- **Çimento**: 2523 10 00, 2523 21 00, vb.
- **Alüminyum**: 7601, 7604, 7606, vb.
- **Gübre**: 2814, 3102 10, 3102 30, vb.
- **Hidrojen**: 2804 10 00

Tam liste için `src/cn_code_database.py` dosyasına bakın.

##  Veri Formatı

ETS fiyat CSV dosyası formatı:

```csv
Date,Primary Market
2014-01-01,5.23
2014-02-01,5.45
...
```

##  Örnek Çıktı

```
--- CBAM SONUÇLARI ---
Toplam Gömülü Emisyon: 2070.00 tCO2e
Gerekli Sertifika: 2070.00
CBAM Maliyeti: €175,950.00

--- ETS FİYAT TAHMİNLERİ ---
Quarter | Forecasted Value
Q1 2025 | 88.50
Q2 2025 | 92.30
...

--- CBAM MALİYET PROJEKSİYONLARI ---
Quarter | Forecasted ETS Price (EUR) | Estimated CBAM Cost (EUR)
Q1 2025 | 88.50 | 183,195.00
...
```

##  Konfigürasyon

`config/` klasöründe özel ayarlar yapabilirsiniz:
- API ayarları
- Model parametreleri
- Rapor formatları
- Varsayılan değerler

##  Notlar

- Tüm hesaplamalar AB CBAM regülasyonlarına göre yapılır
- ETS fiyat tahminleri geçmiş verilere dayalıdır
- Raporlar Türkçe olarak üretilir
- API anahtarınızı güvenli tutun

##  Güvenlik

- API anahtarlarını kod içine yazmayın
- `.env` dosyasını `.gitignore`'a ekleyin
- Üretim ortamında çevre değişkeni kullanın

##  Katkıda Bulunma

Projeyi geliştirmek için:
1. Fork yapın
2. Feature branch oluşturun
3. Değişiklikleri commit edin
4. Pull request açın

## � CN Kod Referansı

###  Demir ve Çelik (Iron and Steel)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 7201 | Pig iron | 1.90 | 0.17 | 2.07 |
| 7202 | Ferro-alloys | 1.76 | 0.64 | 2.40 |
| 7203 | Ferrous products obtained by direct reduction | 0.75 | 0.13 | 0.88 |
| 7204 | Ferrous waste and scrap | 0.10 | 0.01 | 0.11 |
| 7205 | Granules and powders, of pig iron | 1.30 | 0.20 | 1.50 |
| 7206 | Iron and non-alloy steel in ingots | 1.92 | 0.18 | 2.10 |

### Ham Çelik (Crude Steel)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 7207 | Semi-finished products of iron or non-alloy steel | 1.28 | 0.27 | 1.55 |
| 7208 | Flat-rolled products | 1.34 | 0.29 | 1.63 |
| 7209 | Flat-rolled products of iron or non-alloy steel | 1.35 | 0.28 | 1.63 |
| 7210 | Flat-rolled products plated or coated | 1.40 | 0.30 | 1.70 |
| 7211 | Flat-rolled products not further worked | 1.38 | 0.31 | 1.69 |
| 7212 | Flat-rolled products clad, plated or coated | 1.42 | 0.32 | 1.74 |

### Çelik Ürünleri (Steel Products)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 7213 | Bars and rods, hot-rolled | 1.45 | 0.25 | 1.70 |
| 7214 | Bars and rods | 1.46 | 0.26 | 1.72 |
| 7215 | Other bars and rods of iron or non-alloy steel | 1.43 | 0.24 | 1.67 |
| 7216 | Angles, shapes and sections | 1.50 | 0.28 | 1.78 |
| 7217 | Wire of iron or non-alloy steel | 1.55 | 0.30 | 1.85 |
| 7218 | Stainless steel in ingots | 2.50 | 0.40 | 2.90 |

### Paslanmaz Çelik (Stainless Steel)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 7219 | Flat-rolled products of stainless steel | 2.55 | 0.42 | 2.97 |
| 7220 | Flat-rolled products of stainless steel | 2.58 | 0.43 | 3.01 |
| 7221 | Bars and rods, hot-rolled, stainless steel | 2.45 | 0.38 | 2.83 |
| 7222 | Other bars and rods of stainless steel | 2.48 | 0.39 | 2.87 |
| 7223 | Wire of stainless steel | 2.60 | 0.45 | 3.05 |

### Çimento (Cement)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 2507 | Kaolin and other kaolinic clays | 0.15 | 0.05 | 0.20 |
| 2523 | Portland cement, aluminous cement | 0.766 | 0.045 | 0.811 |
| 2527 | Natural barium sulphate (barytes) | 0.10 | 0.03 | 0.13 |

### Alüminyum (Aluminium)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 7601 | Unwrought aluminium | 1.75 | 8.25 | 10.00 |
| 7603 | Aluminium powders and flakes | 1.80 | 8.50 | 10.30 |
| 7604 | Aluminium bars, rods and profiles | 0.45 | 2.30 | 2.75 |
| 7605 | Aluminium wire | 0.48 | 2.35 | 2.83 |
| 7606 | Aluminium plates, sheets and strip | 0.50 | 2.40 | 2.90 |

### Alüminyum Ürünleri (Aluminium Products)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 7607 | Aluminium foil | 0.52 | 2.45 | 2.97 |
| 7608 | Aluminium tubes and pipes | 0.55 | 2.50 | 3.05 |
| 7609 | Aluminium tube or pipe fittings | 0.58 | 2.55 | 3.13 |
| 7610 | Aluminium structures | 0.60 | 2.60 | 3.20 |
| 7611 | Aluminium reservoirs, tanks, vats | 0.62 | 2.65 | 3.27 |
| 7612 | Aluminium casks, drums, cans, boxes | 0.65 | 2.70 | 3.35 |

### Gübreler (Fertilizers)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 2808 | Nitric acid | 0.50 | 0.10 | 0.60 |
| 2814 | Ammonia | 1.80 | 0.20 | 2.00 |
| 2834 | Nitrites and nitrates | 0.40 | 0.08 | 0.48 |
| 3102 | Mineral or chemical fertilisers, nitrogenous | 1.50 | 0.25 | 1.75 |
| 3105 | Mineral or chemical fertilisers containing NPK | 1.60 | 0.30 | 1.90 |

### Hidrojen (Hydrogen)

| CN Kodu | Ürün Açıklaması | Direkt | İndirekt | Toplam |
|---------|----------------|--------|----------|--------|
| 2804 | Hydrogen | 10.00 | 1.50 | 11.50 |

**Not:** Tüm emisyon değerleri tCO2/ton cinsinden verilmiştir.

---

## Yapılandırma

### .env Dosyası

```bash
# Gemini API Anahtarı
GOOGLE_API_KEY=your_gemini_api_key_here

# Varsayılan ETS Fiyatı (€/tCO2)
DEFAULT_ETS_PRICE=85.0

# ETS Fiyat Verisi (ICAP 2019-2025)
ETS_CSV_PATH=data/icap-graph-price-data-2014-01-01-2025-11-21.csv

# Rapor Klasörü
REPORT_DIR=reports

# Log Seviyesi
LOG_LEVEL=INFO
```

---

## Sorun Giderme

### API Hataları

**Problem:** `429 RESOURCE_EXHAUSTED`
```
Gemini API quota aşıldı
```

**Çözüm:**
- Ücretsiz tier sınırı doldu, 24 saat bekleyin
- Ücretli plana geçin
- Web arayüzünü kullanarak basit hesaplamalar yapın (API gerektirmez)

---

**Problem:** `INVALID_ARGUMENT: Invalid API key`

**Çözüm:**
1. [Google AI Studio](https://aistudio.google.com/app/apikey) adresinden yeni API key alın
2. `.env` dosyasını güncelleyin
3. Virtual environment'ı yeniden başlatın

---

### Veri Hataları

**Problem:** `FileNotFoundError: CSV file not found`

**Çözüm:**
```bash
# CSV dosyasını data/ klasörüne kopyalayın
mkdir data
copy C:\Users\LENOVO\Desktop\icap-graph-price-data-2014-01-01-2025-11-21.csv data\

# .env dosyasını kontrol edin
ETS_CSV_PATH=data/icap-graph-price-data-2014-01-01-2025-11-21.csv
```

---

**Problem:** `KeyError: CN code '7201' not found`

**Çözüm:**
```python
from src.cn_code_database import CN_CODE_DATABASE

# Mevcut CN kodlarını listele
print("Mevcut CN Kodları:")
for code in sorted(CN_CODE_DATABASE.keys()):
    print(f"  {code}: {CN_CODE_DATABASE[code]['description']}")
```

---

### Web App Hataları

**Problem:** `Port 5000 already in use`

**Çözüm:**
```python
# app.py içinde portu değiştirin
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## Hesaplama Formülleri

### 1. Toplam Emisyon Yoğunluğu
```
Toplam EI = Direkt EI + İndirekt EI
```

### 2. Toplam Emisyon
```
Toplam Emisyon = Miktar (ton) × Toplam EI
```

### 3. CBAM Sertifika Sayısı
```
Sertifika = Toplam Emisyon
```

### 4. CBAM Maliyeti
```
CBAM Maliyeti = Toplam Emisyon × ETS Fiyatı
```

### 5. Düzeltilmiş CBAM Maliyeti
```
Düzeltilmiş Maliyet = CBAM Maliyeti - (Toplam Emisyon × Yabancı Karbon Fiyatı)
```

---

## Örnek Senaryo

### Pig Iron İthalatı Analizi

```python
from src.cbam_calculator import CBAMCalculator

# Parametreler
ets_price = 85.0  # €/tCO2
cn_code = "7201"  # Pig iron
quantity = 1000   # ton

# Hesaplama
calc = CBAMCalculator(ets_price)
summary = calc.get_summary(cn_code, quantity)

# Sonuçlar
print(f"Ürün: {summary['product']}")
print(f"Toplam Emisyon: {summary['total_emission']:,.2f} tCO2")
print(f"CBAM Sertifika: {summary['certificates']:,.0f}")
print(f"CBAM Maliyeti: €{summary['cbam_cost']:,.2f}")
```

**Çıktı:**
```
Ürün: Pig iron
Toplam Emisyon: 2,070.00 tCO2
CBAM Sertifika: 2,070
CBAM Maliyeti: €175,950.00
```

---

## Veri Kaynakları

### ETS Fiyat Verileri

**Kaynak:** ICAP ETS Price Data (2019-2025)  
**Dosya:** `data/icap-graph-price-data-2014-01-01-2025-11-21.csv`  
**İçerik:** Günlük ETS karbon fiyat verileri

**Not:** ETS fiyat tahminleri, 2019-2025 yılları arasındaki ICAP (International Carbon Action Partnership) verileri kullanılarak Gemini LLM tarafından yapılmaktadır.

### Emisyon Yoğunluğu Verileri

**Kaynak:** EU Commission CBAM Default Values  
**Standart:** EU Regulation 2023/956  
**Güncelleme:** 2025 Q4

---

## Lisans

Bu proje özel kullanım içindir.

## Destek

Sorular veya sorunlar için issue açın.

---

**Geliştirici**: Grefins  
**Versiyon**: 1.0.0  
**Son Güncelleme**: Ocak 2026
