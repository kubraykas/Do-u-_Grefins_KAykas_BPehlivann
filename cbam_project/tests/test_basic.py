"""
Test Dosyaları
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.cbam_calculator import CBAMCalculator
from src.cn_code_database import CN_CODE_DATABASE


def test_database():
    """CN Code veritabanı testi"""
    print("1️⃣ Veritabanı Testi...")
    assert len(CN_CODE_DATABASE) > 0, "Veritabanı boş!"
    print(f"   ✅ {len(CN_CODE_DATABASE)} ürün kayıtlı\n")


def test_calculator():
    """CBAM hesaplama testi"""
    print("2️⃣ Hesaplama Testi...")
    calc = CBAMCalculator(ets_price=85.0)
    summary = calc.get_summary("7201", 1000)
    
    assert summary is not None, "Hesaplama başarısız!"
    assert summary['cbam_cost'] > 0, "Maliyet hesaplanamadı!"
    print(f"   ✅ 1000 ton Pig iron: €{summary['cbam_cost']:,.2f}\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 CBAM TESTLER")
    print("="*60 + "\n")
    
    test_database()
    test_calculator()
    
    print("="*60)
    print("✅ Tüm testler başarılı!")
    print("="*60 + "\n")
