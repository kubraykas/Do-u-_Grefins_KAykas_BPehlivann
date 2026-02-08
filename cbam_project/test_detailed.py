"""Test full analysis with better error handling"""
import requests
import time

data = {
    'action': 'full-analysis',
    'ets_price': '85.0',
    'quantity': '1000',
    'cn_code': '7201'
}

url = 'http://localhost:5000/calculate'

print("🔍 Detaylı Test - Tam Analiz")
print("="*70)

try:
    print("📤 POST isteği gönderiliyor...")
    start = time.time()
    response = requests.post(url, data=data, timeout=120)
    elapsed = time.time() - start
    
    print(f"⏱️  Süre: {elapsed:.1f} saniye")
    print(f"📊 HTTP Status: {response.status_code}")
    print()
    
    # Save response to file for inspection
    with open('test_response.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print("💾 Yanıt 'test_response.html' dosyasına kaydedildi")
    print()
    
    # Check content
    content_checks = {
        'CBAM Tam Analiz': 'Tam Analiz Raporu' in response.text or 'Tam Analiz' in response.text,
        'Emisyon Analizi': 'Emisyon Profili' in response.text or 'Scope 1' in response.text,
        'Optimizasyon': 'Optimizasyon' in response.text,
        'ETS Tahmin': 'ETS Fiyat' in response.text or 'Forecasted' in response.text,
        'Gemini Rapor': 'Yönetici' in response.text or 'Executive' in response.text,
        'Hata': 'error' in response.text.lower() or 'Error' in response.text
    }
    
    print("📋 İçerik Kontrolleri:")
    for check, result in content_checks.items():
        icon = "✅" if result else "❌"
        print(f"   {icon} {check}")
    
    # If error, try to extract it
    if content_checks['Hata']:
        lines = response.text.split('\n')
        for i, line in enumerate(lines):
            if 'error' in line.lower() or 'hata' in line.lower():
                print(f"\n⚠️  Hata Satırı {i}: {line.strip()[:200]}")
                
except Exception as e:
    print(f"❌ İstek Hatası: {e}")

print()
print("="*70)
