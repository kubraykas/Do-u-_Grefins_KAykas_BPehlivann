"""
Hızlı test - Tam Analiz fonksiyonunu direkt çalıştır
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.cbam_calculator import CBAMCalculator
from src.ets_predictor import ETSPricePredictor
from src.cbam_cost_forecaster import CBAMCostForecaster
from src.report_generator import CBAMReportGenerator
from google import genai
from dotenv import load_dotenv

load_dotenv()

print("="*70)
print("🚀 HIZLI TAM ANALİZ TESTİ")
print("="*70)

# Gemini client
gemini_client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

# Test verileri
ets_price = 85.0
quantity = 1000
cn_code = '7201'
csv_path = r'C:\Users\LENOVO\Desktop\icap-graph-price-data-2014-01-01-2025-11-21.csv'

print(f"\n📊 Test Parametreleri:")
print(f"   ETS Fiyatı: €{ets_price}")
print(f"   Miktar: {quantity} ton")
print(f"   CN Code: {cn_code}")

# CBAM Hesaplama
print(f"\n1️⃣ CBAM Hesaplama...")
calc = CBAMCalculator(ets_price)
cbam_summary = calc.get_summary(cn_code, quantity)
print(f"   ✅ CBAM Maliyeti: €{cbam_summary['cbam_cost']:,.2f}")

# ETS Fiyat Tahmini
print(f"\n2️⃣ ETS Fiyat Tahmini (Gemini)...")
predictor = ETSPricePredictor(gemini_client)
ets_forecast, ets_stats = predictor.predict(csv_path)
print(f"   ✅ Tahmin tamamlandı - {len(ets_forecast)} çeyrek")

# CBAM Maliyet Projeksiyonu
print(f"\n3️⃣ CBAM Maliyet Projeksiyonu (Gemini)...")
forecaster = CBAMCostForecaster(gemini_client)
cbam_cost_forecast = forecaster.forecast(cbam_summary, ets_forecast)
print(f"   ✅ Projeksiyon tamamlandı")

# Yönetici Raporu
print(f"\n4️⃣ Yönetici Raporu Oluşturuluyor (Gemini)...")
generator = CBAMReportGenerator(gemini_client)
report = generator.generate_report(
    cbam_summary, 
    ets_forecast, 
    cbam_cost_forecast,
    emission_analysis=None,
    optimization_scenarios=None
)
print(f"   ✅ Rapor oluşturuldu - {len(report['report_text'])} karakter")

print("\n" + "="*70)
print("✅ TAM ANALİZ BAŞARILI!")
print("="*70)
print(f"\n📄 Rapor özeti (ilk 500 karakter):")
print(report['report_text'][:500])
