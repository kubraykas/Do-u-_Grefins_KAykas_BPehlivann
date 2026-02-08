"""Test full analysis button"""
import requests

# Test data
data = {
    'action': 'full-analysis',
    'ets_price': '85.0',
    'quantity': '1000',
    'cn_code': '7201',
    'coking_coal_ton': '1200',
    'natural_gas_nm3': '850000',
    'fuel_oil_ton': '50',
    'limestone_ton': '300',
    'reheating_fuel_nm3': '12000',
    'steel_output_ton': '5000',
    'electricity_consumption_mwh': '4200',
    'grid_emission_factor': '0.62',
    'renewable_share_percent': '10'
}

url = 'http://localhost:5000/calculate'

print("🧪 Tam Analiz Butonu Testi")
print("="*50)
print(f"URL: {url}")
print(f"Action: {data['action']}")
print()

try:
    response = requests.post(url, data=data, timeout=60)
    
    if response.status_code == 200:
        print("✅ Başarılı! HTTP 200 OK")
        
        # Check if it's the full results page
        if 'Tam Analiz Raporu' in response.text:
            print("✅ Tam Analiz sayfası yüklendi!")
        elif 'Emisyon Profili' in response.text:
            print("✅ Emisyon analizi dahil edildi!")
        elif 'Optimizasyon' in response.text:
            print("✅ Optimizasyon senaryoları dahil edildi!")
        else:
            print("⚠️  Beklenmedik sayfa içeriği")
            
        # Check for errors
        if 'error' in response.text.lower() or 'hata' in response.text.lower():
            print("⚠️  Sayfada hata mesajı bulundu")
    else:
        print(f"❌ HTTP {response.status_code}")
        
except requests.exceptions.Timeout:
    print("❌ Timeout - Gemini API yanıt vermiyor olabilir")
except Exception as e:
    print(f"❌ Hata: {e}")

print()
print("="*50)
print("💡 Manuel Test:")
print("1. http://localhost:5000 adresine git")
print("2. ETS Fiyatı: 85.0, Miktar: 1000, CN Kod: 7201")
print("3. Detaylı Emisyon bölümünü aç ve verileri gir")
print("4. '📊 Tam Analiz (ETS + Rapor)' butonuna tıkla")
