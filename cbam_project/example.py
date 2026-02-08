"""
Example usage script demonstrating how to use the CBAM system
"""

from main import CBAMApplication


def example_full_analysis():
    """
    Complete analysis example
    """
    print("=== ÖRNEK: TAM ANALİZ ===\n")
    
    # Initialize application (API key from environment)
    app = CBAMApplication()
    
    # Run full analysis
    result = app.run_full_analysis(
        ets_price=85.0,
        quantity=1000,
        cn_code="7201",  # Pig iron
        csv_path=r"C:\Users\LENOVO\Desktop\icap-graph-price-data-2014-01-01-2025-11-21.csv",
        save_report_path="reports/example_report.txt"
    )
    
    if result:
        print("\n✅ Analiz başarıyla tamamlandı!")
        print(f"Toplam CBAM Maliyeti: €{result['cbam_summary']['cbam_cost']:,.2f}")


def example_step_by_step():
    """
    Step-by-step analysis example
    """
    print("\n=== ÖRNEK: ADIM ADIM ANALİZ ===\n")
    
    app = CBAMApplication()
    
    # Step 1: Calculate current CBAM
    print("1️⃣ CBAM Hesaplama...")
    cbam = app.calculate_current_cbam(
        ets_price=85.0,
        quantity=500,
        cn_code="7601"  # Aluminium
    )
    
    if cbam is None:
        return
    
    # Step 2: Predict ETS prices
    print("\n2️⃣ ETS Fiyat Tahmini...")
    ets_forecast = app.predict_ets_prices(
        r"C:\Users\LENOVO\Desktop\icap-graph-price-data-2014-01-01-2025-11-21.csv"
    )
    
    # Step 3: Forecast CBAM costs
    print("\n3️⃣ CBAM Maliyet Tahmini...")
    cbam_costs = app.forecast_cbam_costs()
    
    # Step 4: Generate report
    print("\n4️⃣ Rapor Oluşturma...")
    report = app.generate_executive_report()
    
    print("\n✅ Tüm adımlar tamamlandı!")


def example_calculator_only():
    """
    Using calculator module only
    """
    print("\n=== ÖRNEK: SADECE HESAPLAYICI ===\n")
    
    from src.cbam_calculator import CBAMCalculator
    
    # Create calculator
    calc = CBAMCalculator(ets_price=90.0)
    
    # Get product data
    data = calc.get_data_by_cn("2523 21 00")  # White Portland cement
    
    if data:
        print(f"Ürün: {data['description']}")
        print(f"Kategori: {data['category']}")
        
        # Calculate CBAM
        result = calc.calculate(
            quantity=2000,
            direct_ei=data['direct_ei'],
            indirect_ei=data['indirect_ei']
        )
        
        print(f"\nToplam Emisyon: {result['total_emission']:.2f} tCO2e")
        print(f"CBAM Maliyeti: €{result['cbam_cost']:,.2f}")


def example_search_products():
    """
    Search for products in database
    """
    print("\n=== ÖRNEK: ÜRÜN ARAMA ===\n")
    
    from src.cn_code_database import search_by_description, get_categories
    
    # Search for steel products
    steel_products = search_by_description("steel")
    print(f"Bulunan çelik ürünleri: {len(steel_products)}")
    for product in steel_products[:5]:
        print(f"  - {product['cn_code']}: {product['description']}")
    
    # Get all categories
    print("\n\nTüm kategoriler:")
    categories = get_categories()
    for cat in sorted(categories):
        print(f"  - {cat}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌍 CBAM SİSTEMİ KULLANIM ÖRNEKLERİ")
    print("="*70)
    
    # Choose which example to run
    print("\n1. Tam Analiz Örneği")
    print("2. Adım Adım Analiz Örneği")
    print("3. Sadece Hesaplama Örneği")
    print("4. Ürün Arama Örneği")
    
    choice = input("\nSeçiminiz (1-4): ").strip()
    
    if choice == "1":
        example_full_analysis()
    elif choice == "2":
        example_step_by_step()
    elif choice == "3":
        example_calculator_only()
    elif choice == "4":
        example_search_products()
    else:
        print("Geçersiz seçim!")
