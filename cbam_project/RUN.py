"""
🚀 CBAM Projesini Çalıştırma Kılavuzu
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║           🌍 CBAM PROJESİNİ ÇALIŞTIRMA                      ║
╚══════════════════════════════════════════════════════════════╝

📁 PROJE YAPISI:

cbam_project/
├── web/          → Web uygulaması (Flask)
├── cli/          → Komut satırı uygulaması
├── src/          → Ana kaynak kodlar
├── tests/        → Test dosyaları
└── data/         → Veri dosyaları

═══════════════════════════════════════════════════════════════

🎯 ÇALIŞTIRMA SEÇENEKLERİ:

1️⃣  WEB ARAYÜZÜ (ÖNERİLEN)
   cd web
   python app.py
   → http://localhost:5000

2️⃣  KOMUT SATIRI
   cd cli
   python cbam_cli.py

3️⃣  PYTHON API
   python example.py

4️⃣  TESTLER
   cd tests
   python test_basic.py

═══════════════════════════════════════════════════════════════

💡 HIZLI TEST:

   python -c "from src.cbam_calculator import CBAMCalculator; 
   c = CBAMCalculator(85); 
   s = c.get_summary('7201', 1000); 
   print(f'CBAM: €{s[\"cbam_cost\"]:,.2f}')"

═══════════════════════════════════════════════════════════════

📚 DAHA FAZLA BİLGİ:
   - README.md
   - PROJECT_STRUCTURE.md
   - docs/

╚══════════════════════════════════════════════════════════════╝
""")
