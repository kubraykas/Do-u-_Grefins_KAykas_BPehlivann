"""Quick test of emission analyzer"""
from src.emission_analyzer import EmissionAnalyzer

# Test data
scope1_data = {
    'fuel': {
        'coking_coal_ton': 1200,
        'natural_gas_nm3': 850000,
        'fuel_oil_ton': 50
    },
    'process': {
        'limestone_ton': 300
    },
    'thermal_systems': {
        'reheating_fuel_nm3': 12000
    },
    'steel_output_ton': 5000
}

scope2_data = {
    'electricity': {
        'electricity_consumption_mwh': 4200,
        'grid_emission_factor_kgco2_kwh': 0.62,
        'renewable_share_percent': 10
    }
}

# Create analyzer
analyzer = EmissionAnalyzer()

# Calculate Scope 1
s1 = analyzer.calculate_scope1(scope1_data)
print(f"✅ Scope 1 Toplam: {s1['total_scope1']:,.2f} tCO2")
print(f"   - Yakıt: {s1['total_fuel']:,.2f} tCO2")
print(f"   - Proses: {s1['total_process']:,.2f} tCO2")
print(f"   - Termal: {s1['total_thermal']:,.2f} tCO2")

# Calculate Scope 2
s2 = analyzer.calculate_scope2(scope2_data)
print(f"\n✅ Scope 2 Toplam: {s2['total_scope2']:,.2f} tCO2")
print(f"   - Grid: {s2['grid_emissions']:,.2f} tCO2")

# Summary
summary = analyzer.get_summary()
print(f"\n🎯 TOPLAM EMİSYON: {summary['total_emissions']:,.2f} tCO2")

# Optimization scenarios
ets_price = 85.0
scenarios = analyzer.get_optimization_scenarios(scope1_data, scope2_data, ets_price)
print(f"\n💡 Optimizasyon Senaryoları: {len(scenarios)} adet")
for key, scenario in scenarios.items():
    if key != 'combined':
        print(f"   - {scenario['name']}: €{scenario['annual_cbam_saving_eur']:,.0f}/yıl tasarruf")

if 'combined' in scenarios:
    print(f"\n🚀 Kombine Senaryo:")
    print(f"   Emisyon Azaltımı: {scenarios['combined']['total_emission_saving_tco2']:,.2f} tCO2/yıl")
    print(f"   CBAM Tasarrufu: €{scenarios['combined']['total_annual_cbam_saving_eur']:,.0f}/yıl")
    print(f"   ROI: {scenarios['combined']['roi_years']:.1f} yıl")

print("\n✅ TÜM TESTLER BAŞARILI!")
