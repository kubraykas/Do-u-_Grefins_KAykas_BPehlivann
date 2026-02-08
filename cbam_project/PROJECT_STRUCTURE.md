# CBAM Project - Düzenli Klasör Yapısı

Profesyonel CBAM (Carbon Border Adjustment Mechanism) hesaplama ve raporlama sistemi.

## 📁 Klasör Yapısı

```
cbam_project/
│
├── src/                          # Ana kaynak kodlar
│   ├── __init__.py
│   ├── cn_code_database.py       # CN kod veritabanı
│   ├── cbam_calculator.py        # Hesaplama motoru
│   ├── ets_predictor.py          # ETS fiyat tahmini
│   ├── cbam_cost_forecaster.py   # Maliyet projeksiyonu
│   └── report_generator.py       # Rapor üretimi
│
├── web/                          # Web Uygulaması
│   ├── app.py                    # Flask uygulaması
│   ├── templates/                # HTML şablonları
│   │   ├── index.html
│   │   ├── results.html
│   │   ├── cn_codes.html
│   │   └── error.html
│   └── static/                   # CSS, JS, resimler
│       └── style.css
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
│   └── (rapor çıktıları)
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
✅ Web arayüzü  
✅ Komut satırı arayüzü  
✅ Python API  
✅ Modüler yapı  

---

**Versiyon**: 1.0.0  
**Lisans**: Özel Kullanım
