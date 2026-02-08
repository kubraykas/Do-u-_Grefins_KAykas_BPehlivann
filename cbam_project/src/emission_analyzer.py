"""
Emission Analyzer Module
Scope 1 and Scope 2 emissions calculation and analysis
"""

class EmissionAnalyzer:
    """Scope 1 ve Scope 2 emisyon analizi ve hesaplaması"""
    
    # Emisyon faktörleri (tCO2/birim)
    EMISSION_FACTORS = {
        'coking_coal': 1.6,          # tCO2/ton
        'natural_gas': 0.000494,     # tCO2/Nm³
        'fuel_oil': 3.1,             # tCO2/ton
        'limestone': 0.44,           # tCO2/ton (CaCO3 → CaO + CO2)
    }
    
    def __init__(self):
        self.scope1_emissions = {}
        self.scope2_emissions = {}
        self.total_emissions = 0
        
    def calculate_scope1(self, scope1_data):
        """
        Scope 1 (Doğrudan) emisyonları hesapla
        
        Args:
            scope1_data: dict with fuel, process, thermal_systems, steel_output_ton
        """
        if not scope1_data:
            return None
            
        fuel = scope1_data.get('fuel', {})
        process = scope1_data.get('process', {})
        thermal = scope1_data.get('thermal_systems', {})
        
        # Yakıt bazlı emisyonlar
        fuel_emissions = {
            'coking_coal': fuel.get('coking_coal_ton', 0) * self.EMISSION_FACTORS['coking_coal'],
            'natural_gas': fuel.get('natural_gas_nm3', 0) * self.EMISSION_FACTORS['natural_gas'],
            'fuel_oil': fuel.get('fuel_oil_ton', 0) * self.EMISSION_FACTORS['fuel_oil']
        }
        
        # Proses emisyonları
        process_emissions = {
            'limestone': process.get('limestone_ton', 0) * self.EMISSION_FACTORS['limestone']
        }
        
        # Termal sistem emisyonları
        thermal_emissions = {
            'reheating': thermal.get('reheating_fuel_nm3', 0) * self.EMISSION_FACTORS['natural_gas']
        }
        
        # Toplamlar
        total_fuel = sum(fuel_emissions.values())
        total_process = sum(process_emissions.values())
        total_thermal = sum(thermal_emissions.values())
        total_scope1 = total_fuel + total_process + total_thermal
        
        # Çelik üretimi bazında yoğunluk
        steel_output = scope1_data.get('steel_output_ton', 1)
        intensity = total_scope1 / steel_output if steel_output > 0 else 0
        
        self.scope1_emissions = {
            'fuel_emissions': fuel_emissions,
            'process_emissions': process_emissions,
            'thermal_emissions': thermal_emissions,
            'total_fuel': total_fuel,
            'total_process': total_process,
            'total_thermal': total_thermal,
            'total_scope1': total_scope1,
            'steel_output_ton': steel_output,
            'emission_intensity': intensity,
            'breakdown_percent': {
                'fuel': (total_fuel / total_scope1 * 100) if total_scope1 > 0 else 0,
                'process': (total_process / total_scope1 * 100) if total_scope1 > 0 else 0,
                'thermal': (total_thermal / total_scope1 * 100) if total_scope1 > 0 else 0
            }
        }
        
        return self.scope1_emissions
    
    def calculate_scope2(self, scope2_data):
        """
        Scope 2 (Dolaylı - Elektrik) emisyonları hesapla
        
        Args:
            scope2_data: dict with electricity consumption, grid factor, renewable share
        """
        if not scope2_data:
            return None
            
        electricity = scope2_data.get('electricity', {})
        
        consumption_mwh = electricity.get('electricity_consumption_mwh', 0)
        grid_factor = electricity.get('grid_emission_factor_kgco2_kwh', 0)
        renewable_percent = electricity.get('renewable_share_percent', 0)
        
        # Grid emisyonları (MWh → kWh → tCO2)
        grid_share = (100 - renewable_percent) / 100
        renewable_share = renewable_percent / 100
        
        grid_emissions = consumption_mwh * 1000 * grid_factor * grid_share / 1000  # tCO2
        renewable_emissions = 0  # Yenilenebilir kaynaklardan emisyon yok
        total_scope2 = grid_emissions + renewable_emissions
        
        self.scope2_emissions = {
            'consumption_mwh': consumption_mwh,
            'grid_emission_factor': grid_factor,
            'renewable_percent': renewable_percent,
            'grid_share_percent': grid_share * 100,
            'grid_emissions': grid_emissions,
            'renewable_emissions': renewable_emissions,
            'total_scope2': total_scope2,
            'breakdown': {
                'grid_kwh': consumption_mwh * 1000 * grid_share,
                'renewable_kwh': consumption_mwh * 1000 * renewable_share
            }
        }
        
        return self.scope2_emissions
    
    def get_optimization_scenarios(self, scope1_data, scope2_data, ets_price):
        """
        Optimizasyon senaryoları üret
        
        Returns:
            dict: Farklı optimizasyon senaryoları ve finansal etkileri
        """
        scenarios = {}
        
        # Scope 1 - Doğalgaz azaltma senaryosu
        if scope1_data and 'fuel' in scope1_data:
            natural_gas_nm3 = scope1_data['fuel'].get('natural_gas_nm3', 0)
            if natural_gas_nm3 > 0:
                reduction_20_percent = natural_gas_nm3 * 0.20
                emission_saving = reduction_20_percent * self.EMISSION_FACTORS['natural_gas']
                cost_saving = emission_saving * ets_price
                
                scenarios['natural_gas_reduction'] = {
                    'name': 'Doğalgaz Tüketimi %20 Azaltma',
                    'reduction_percent': 20,
                    'current_consumption': natural_gas_nm3,
                    'new_consumption': natural_gas_nm3 * 0.80,
                    'emission_saving_tco2': emission_saving,
                    'annual_cbam_saving_eur': cost_saving,
                    'investment_needed_eur': 50000,
                    'roi_years': 50000 / cost_saving if cost_saving > 0 else 0,
                    'measures': [
                        'Verimlilik iyileştirmeleri',
                        'Isı geri kazanım sistemleri',
                        'Prosess optimizasyonu'
                    ]
                }
        
        # Scope 2 - Yenilenebilir enerji artırma
        if scope2_data and 'electricity' in scope2_data:
            elec = scope2_data['electricity']
            current_renewable = elec.get('renewable_share_percent', 0)
            consumption_mwh = elec.get('electricity_consumption_mwh', 0)
            grid_factor = elec.get('grid_emission_factor_kgco2_kwh', 0)
            
            if current_renewable < 50 and consumption_mwh > 0:
                # %50'ye çıkarma senaryosu
                new_renewable = 50
                renewable_increase = (new_renewable - current_renewable) / 100
                emission_saving = consumption_mwh * 1000 * grid_factor * renewable_increase / 1000
                cost_saving = emission_saving * ets_price
                
                scenarios['renewable_energy_increase'] = {
                    'name': 'Yenilenebilir Enerji %50\'ye Çıkarma',
                    'current_renewable_percent': current_renewable,
                    'target_renewable_percent': new_renewable,
                    'emission_saving_tco2': emission_saving,
                    'annual_cbam_saving_eur': cost_saving,
                    'investment_needed_eur': 500000,
                    'roi_years': 500000 / cost_saving if cost_saving > 0 else 0,
                    'measures': [
                        'Çatı tipi güneş paneli kurulumu',
                        'Yeşil enerji tedarikçisi anlaşması',
                        'Rüzgar enerjisi yatırımı'
                    ]
                }
        
        # Kombine senaryo
        if len(scenarios) > 1:
            total_emission_saving = sum(s['emission_saving_tco2'] for s in scenarios.values())
            total_cost_saving = sum(s['annual_cbam_saving_eur'] for s in scenarios.values())
            total_investment = sum(s['investment_needed_eur'] for s in scenarios.values())
            
            scenarios['combined'] = {
                'name': 'Kombine Optimizasyon (Tüm Önlemler)',
                'included_scenarios': list(scenarios.keys()),
                'total_emission_saving_tco2': total_emission_saving,
                'total_annual_cbam_saving_eur': total_cost_saving,
                'total_investment_needed_eur': total_investment,
                'roi_years': total_investment / total_cost_saving if total_cost_saving > 0 else 0,
                'emission_reduction_percent': (total_emission_saving / (self.scope1_emissions.get('total_scope1', 1) + self.scope2_emissions.get('total_scope2', 1)) * 100) if (self.scope1_emissions and self.scope2_emissions) else 0
            }
        
        return scenarios
    
    def get_summary(self):
        """Özet istatistikler"""
        total = 0
        if self.scope1_emissions:
            total += self.scope1_emissions['total_scope1']
        if self.scope2_emissions:
            total += self.scope2_emissions['total_scope2']
            
        self.total_emissions = total
        
        return {
            'scope1': self.scope1_emissions,
            'scope2': self.scope2_emissions,
            'total_emissions': total,
            'breakdown_percent': {
                'scope1': (self.scope1_emissions['total_scope1'] / total * 100) if (self.scope1_emissions and total > 0) else 0,
                'scope2': (self.scope2_emissions['total_scope2'] / total * 100) if (self.scope2_emissions and total > 0) else 0
            }
        }
