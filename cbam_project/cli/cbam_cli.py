"""
CLI - Command Line Interface
Komut satırından CBAM hesaplama
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.cbam_calculator import CBAMCalculator
from src.cn_code_database import CN_CODE_DATABASE


def main():
    print("\n" + "="*60)
    print("🌍 CBAM HESAPLAMA - CLI")
    print("="*60 + "\n")
    
    # Girdiler
    try:
        ets_price = float(input("ETS Fiyatı (€/tCO2): "))
        quantity = float(input("Miktar (ton): "))
        cn_code = input("CN Code: ")
        
        # Hesapla
        calc = CBAMCalculator(ets_price)
        summary = calc.get_summary(cn_code, quantity)
        
        if summary is None:
            print("\n❌ CN Code bulunamadı!")
            return
        
        # Sonuçlar
        print("\n" + "="*60)
        print("📊 SONUÇLAR")
        print("="*60)
        print(f"\nÜrün: {summary['product']}")
        print(f"Kategori: {summary['category']}")
        print(f"Miktar: {summary['quantity_tonnes']:,.0f} ton")
        print(f"\nDirekt EI: {summary['direct_ei']} tCO2/ton")
        print(f"İndirekt EI: {summary['indirect_ei']} tCO2/ton")
        print(f"Toplam EI: {summary['total_ei']} tCO2/ton")
        print(f"\nToplam Emisyon: {summary['total_emission']:,.2f} tCO2e")
        print(f"Gerekli Sertifika: {summary['certificates']:,.2f}")
        print(f"\n💰 CBAM Maliyeti: €{summary['cbam_cost']:,.2f}")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nİptal edildi.")
    except Exception as e:
        print(f"\n❌ Hata: {e}")


if __name__ == "__main__":
    main()
