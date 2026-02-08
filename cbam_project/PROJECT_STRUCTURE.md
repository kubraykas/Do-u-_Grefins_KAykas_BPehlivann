# CBAM Project - Düzenli Klasör Yapısı

Profesyonel CBAM (Carbon Border Adjustment Mechanism) hesaplama ve raporlama sistemi.

## 📁 Klasör Yapısı

```
cbam_project/
│
├── src/                          # Ana kaynak kodlar
│   ├── __init__.py
│   ├── cn_code_database.py       # CN kod veritabanı (48 ürün)
│   ├── cbam_calculator.py        # CBAM hesaplama motoru
│   ├── emission_analyzer.py      # Scope 1&2 emisyon analizi (YENİ!)
│   ├── ets_predictor.py          # ETS fiyat tahmini (Gemini AI)
│   ├── cbam_cost_forecaster.py   # Maliyet projeksiyonu
│   ├── report_generator.py       # AI rapor üretimi (geliştirildi)
│   └── pdf_generator.py          # PDF rapor oluşturma (YENİ!)
│
├── web/                          # Web Uygulaması
│   ├── app.py                    # Flask uygulaması (rapor kaydetme eklendi)
│   ├── templates/                # HTML şablonları
│   │   ├── index.html            # Ana form (Scope 1&2 girişli)
│   │   ├── results.html          # Hızlı sonuç
│   │   ├── full_results.html     # Detaylı analiz (YENİ!)
│   │   ├── cn_codes.html         # CN kod listesi
│   │   └── error.html            # Hata sayfası
│   └── static/                   # CSS, JS, resimler
│       └── style.css             # Minimal beyaz/gri tasarım
│
├── cli/                          # Komut Satırı Araçları
│   └── cbam_cli.py              # CLI uygulaması
│
├── tests/                        # Test dosyaları
│   └── test_basic.py
│
├── data/                         # Veri dosyaları
│   └── (CSV dosyaları buraya)
│
├── config/                       # Konfigürasyon
│   └── (ayar dosyaları)
│
├── reports/                      # Oluşturulan raporlar
│   ├── celik_raporu.txt          # Örnek rapor
│   └── (otomatik kaydedilen raporlar)
│
├── docs/                         # Dokümantasyon
│   └── (kullanım kılavuzları)
│
├── main.py                       # Ana Python API
├── example.py                    # Kullanım örnekleri
├── requirements.txt              # Bağımlılıklar
├── README.md                     # Proje açıklaması
├── .env.example                  # Çevre değişkeni şablonu
└── .gitignore                    # Git ignore

```

## 🚀 Hızlı Başlangıç

### 1. Web Arayüzü (Önerilen)
```bash
cd web
python app.py
# Tarayıcıda: http://localhost:5000
```

### 2. Komut Satırı
```bash
cd cli
python cbam_cli.py
```

### 3. Python API
```python
from src.cbam_calculator import CBAMCalculator

calc = CBAMCalculator(ets_price=85.0)
summary = calc.get_summary("7201", 1000)
print(f"CBAM: €{summary['cbam_cost']:,.2f}")
```

## 📦 Kurulum

```bash
pip install -r requirements.txt
```

## 🧪 Test

```bash
cd tests
python test_basic.py
```

## 📖 Kullanım Kılavuzları

Her modül için detaylı kullanım:

- **Web Uygulaması**: `web/README.md`
- **CLI Kullanımı**: `cli/README.md`
- **API Referansı**: `docs/API.md`

## 🎯 Özellikler

✅ CBAM maliyet hesaplama  
✅ 48+ ürün CN kodu desteği  
✅ Scope 1&2 emisyon analizi (YENİ!)  
✅ Optimizasyon senaryoları (3 senaryo, ROI analizi)  
✅ Otomatik rapor kaydetme (YENİ!)  
✅ PDF indirme özelliği (YENİ!)  
✅ Gemini AI entegrasyonu (sayısal öneriler)  
✅ Minimal web arayüzü (beyaz/gri profesyonel tasarım)  
✅ Komut satırı arayüzü  
✅ Python API  
✅ Modüler yapı  
✅ Session management (cookie limit fix)  

---

**Versiyon**: 1.0.0  
**Lisans**: Özel Kullanım
