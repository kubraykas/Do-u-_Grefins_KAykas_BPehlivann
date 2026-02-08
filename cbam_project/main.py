"""
CBAM Calculation, Prediction & Reporting System
Main application module
"""

import os
import sys
from datetime import datetime
from google import genai

from src.cbam_calculator import CBAMCalculator
from src.ets_predictor import ETSPricePredictor
from src.cbam_cost_forecaster import CBAMCostForecaster
from src.report_generator import CBAMReportGenerator


class CBAMApplication:
    """
    Main CBAM application orchestrator
    """
    
    def __init__(self, gemini_api_key=None):
        """
        Initialize CBAM application
        
        Args:
            gemini_api_key (str): Gemini API key (optional, can use env variable)
        """
        # Setup Gemini API
        if gemini_api_key:
            os.environ["GOOGLE_API_KEY"] = gemini_api_key
        
        if "GOOGLE_API_KEY" not in os.environ:
            raise ValueError("GOOGLE_API_KEY must be set in environment or passed to constructor")
        
        self.gemini_client = genai.Client()
        
        # Initialize modules
        self.calculator = None
        self.ets_predictor = ETSPricePredictor(self.gemini_client)
        self.cost_forecaster = CBAMCostForecaster(self.gemini_client)
        self.report_generator = CBAMReportGenerator(self.gemini_client)
        
        self.cbam_summary = None
        self.ets_forecast = None
        self.ets_stats = None
        self.cbam_cost_forecast = None
        self.report_result = None
    
    def calculate_current_cbam(self, ets_price, quantity, cn_code):
        """
        Calculate current CBAM cost for a product
        
        Args:
            ets_price (float): Current EU ETS price (€/tCO2)
            quantity (float): Import quantity (tonnes)
            cn_code (str): Product CN code
            
        Returns:
            dict: CBAM calculation summary
        """
        print("\n" + "="*70)
        print("📊 CBAM HESAPLAMA BAŞLIYOR...")
        print("="*70 + "\n")
        
        self.calculator = CBAMCalculator(ets_price)
        
        # Get product data
        data = self.calculator.get_data_by_cn(cn_code)
        
        if data is None:
            print("❌ Bu CN Code veritabanında bulunamadı.")
            return None
        
        # Display product info
        print("--- ÜRÜN BİLGİLERİ ---")
        print(f"Açıklama: {data['description']}")
        print(f"Kategori: {data['category']}")
        print(f"Direkt EI: {data['direct_ei']} tCO2/t")
        print(f"İndirekt EI: {data['indirect_ei']} tCO2/t")
        print(f"Toplam EI: {data['total_ei']} tCO2/t")
        
        # Calculate CBAM
        result = self.calculator.calculate(quantity, data['direct_ei'], data['indirect_ei'])
        
        print("\n--- CBAM SONUÇLARI ---")
        print(f"Toplam Gömülü Emisyon: {result['total_emission']:.2f} tCO2e")
        print(f"Gerekli Sertifika: {result['certificates']:.2f}")
        print(f"CBAM Maliyeti: €{result['cbam_cost']:,.2f}")
        
        # Create summary
        self.cbam_summary = {
            "product": data["description"],
            "category": data["category"],
            "quantity_tonnes": quantity,
            "total_ei": result["total_ei"],
            "ets_price": ets_price,
            "cbam_cost": result["cbam_cost"]
        }
        
        print("\n✅ CBAM hesaplama tamamlandı\n")
        return self.cbam_summary
    
    def predict_ets_prices(self, csv_path):
        """
        Predict future ETS prices
        
        Args:
            csv_path (str): Path to historical ETS price data CSV
            
        Returns:
            pandas.DataFrame: ETS price forecast
        """
        print("\n" + "="*70)
        print("📈 ETS FİYAT TAHMİNİ BAŞLIYOR...")
        print("="*70 + "\n")
        
        self.ets_forecast, self.ets_stats = self.ets_predictor.predict(csv_path)
        
        print("--- ETS İSTATİSTİKLERİ ---")
        print(f"Son Değer: €{self.ets_stats['last_price']:.2f}")
        print(f"Ortalama: €{self.ets_stats['mean_price']:.2f}")
        print(f"Min: €{self.ets_stats['min_price']:.2f}")
        print(f"Max: €{self.ets_stats['max_price']:.2f}")
        print(f"Volatilite (Std): €{self.ets_stats['std_dev']:.2f}")
        
        print("\n--- ETS FİYAT TAHMİNLERİ ---")
        print(self.ets_forecast.to_string(index=False))
        
        print("\n✅ ETS fiyat tahmini tamamlandı\n")
        return self.ets_forecast
    
    def forecast_cbam_costs(self):
        """
        Forecast future CBAM costs based on ETS predictions
        
        Returns:
            str: CBAM cost forecast response
        """
        if self.cbam_summary is None:
            raise ValueError("CBAM hesaplaması yapılmamış. Önce calculate_current_cbam() çalıştırın.")
        
        if self.ets_forecast is None:
            raise ValueError("ETS tahmini yapılmamış. Önce predict_ets_prices() çalıştırın.")
        
        print("\n" + "="*70)
        print("💰 CBAM MALİYET TAHMİNİ BAŞLIYOR...")
        print("="*70 + "\n")
        
        self.cbam_cost_forecast = self.cost_forecaster.forecast(
            self.cbam_summary, 
            self.ets_forecast
        )
        
        print("--- CBAM MALİYET TAHMİNLERİ ---")
        print(self.cbam_cost_forecast)
        
        print("\n✅ CBAM maliyet tahmini tamamlandı\n")
        return self.cbam_cost_forecast
    
    def generate_executive_report(self, save_path=None):
        """
        Generate executive report
        
        Args:
            save_path (str): Optional path to save report
            
        Returns:
            dict: Report generation result
        """
        if self.cbam_summary is None or self.ets_forecast is None or self.cbam_cost_forecast is None:
            raise ValueError("Tüm analizler tamamlanmamış. Önce hesaplama ve tahmin adımlarını tamamlayın.")
        
        self.report_result = self.report_generator.generate_report(
            self.cbam_summary,
            self.ets_forecast,
            self.cbam_cost_forecast
        )
        
        if save_path:
            self.report_generator.save_report(self.report_result, save_path)
        
        return self.report_result
    
    def run_full_analysis(self, ets_price, quantity, cn_code, csv_path, save_report_path=None):
        """
        Run complete CBAM analysis pipeline
        
        Args:
            ets_price (float): Current EU ETS price (€/tCO2)
            quantity (float): Import quantity (tonnes)
            cn_code (str): Product CN code
            csv_path (str): Path to historical ETS price data CSV
            save_report_path (str): Optional path to save final report
            
        Returns:
            dict: Complete analysis results
        """
        print("\n" + "="*70)
        print("🚀 TAM CBAM ANALİZİ BAŞLIYOR...")
        print("="*70 + "\n")
        
        # Step 1: Calculate current CBAM
        cbam_summary = self.calculate_current_cbam(ets_price, quantity, cn_code)
        if cbam_summary is None:
            return None
        
        # Step 2: Predict ETS prices
        ets_forecast = self.predict_ets_prices(csv_path)
        
        # Step 3: Forecast CBAM costs
        cbam_cost_forecast = self.forecast_cbam_costs()
        
        # Step 4: Generate executive report
        report_result = self.generate_executive_report(save_report_path)
        
        print("\n" + "="*70)
        print("✅ TAM ANALİZ TAMAMLANDI!")
        print("="*70 + "\n")
        
        return {
            'cbam_summary': cbam_summary,
            'ets_forecast': ets_forecast,
            'cbam_cost_forecast': cbam_cost_forecast,
            'report': report_result
        }


def interactive_mode():
    """
    Interactive command-line interface
    """
    print("\n" + "="*70)
    print("🌍 CBAM HESAPLAMA, TAHMİN VE RAPORLAMA SİSTEMİ")
    print("="*70 + "\n")
    
    # API Key
    api_key = input("Gemini API Key (veya ENTER - çevre değişkeninden alınacak): ").strip()
    if not api_key:
        api_key = None
    
    try:
        app = CBAMApplication(gemini_api_key=api_key)
    except ValueError as e:
        print(f"❌ Hata: {e}")
        return
    
    # User inputs
    print("\n--- ÜRÜN BİLGİLERİNİ GİRİN ---")
    ets_price = float(input("EU ETS Fiyatı (€/tCO2): "))
    quantity = float(input("İthalat Miktarı (ton): "))
    cn_code = input("CN Code: ")
    
    print("\n--- VERİ DOSYASI ---")
    csv_path = input("ETS geçmiş veri CSV dosya yolu: ")
    
    print("\n--- RAPOR KAYIT ---")
    save_report = input("Raporu kaydetmek ister misiniz? (e/h): ").lower()
    save_path = None
    if save_report == 'e':
        save_path = input("Rapor dosya yolu (örn: reports/cbam_report.txt): ")
        if not save_path:
            save_path = f"reports/cbam_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Run analysis
    result = app.run_full_analysis(ets_price, quantity, cn_code, csv_path, save_path)
    
    if result:
        print("\n🎉 Analiz başarıyla tamamlandı!")
    else:
        print("\n❌ Analiz tamamlanamadı.")


def main():
    """
    Main entry point
    """
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        print("CBAM Calculation, Prediction & Reporting System")
        print("Kullanım:")
        print("  python main.py --interactive  # İnteraktif mod")
        print("\nVeya Python scriptinde import ederek kullanın:")
        print("  from main import CBAMApplication")


if __name__ == "__main__":
    main()
