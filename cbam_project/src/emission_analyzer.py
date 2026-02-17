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
        'diesel': 0.0027,            # tCO2/Litre
        'limestone': 0.44,           # tCO2/ton (CaCO3 -> CaO + CO2)
        'electrode': 2.8,            # tCO2/ton (Graphite Elektrot)
        'anode': 3.6,                # tCO2/ton (Karbon Anot)
        'coke_injection': 3.1,       # tCO2/ton (Reductants)
        'pfc_emissions': 1.0,        # tCO2e (tCO2e/ton Alüminyum * Al_ton)
        'purchased_heat': 0.18,      # tCO2/MWh (Standard Steam/Heat factor)
        'ammonia': 2.1,              # tCO2/ton (Amonyak Üretimi)
        'nitric_acid': 0.3,          # tCO2/ton (Nitrik Asit - N2O emisyonu dahil)
        'magnesium': 12.0,           # tCO2/ton (Aluminum Alloy Precursor)
        'silicon': 5.0,              # tCO2/ton (Aluminum Alloy Precursor)
    }
    
    def __init__(self):
        self.scope1_emissions = {}
        self.scope2_emissions = {}
        self.total_emissions = 0
        
    def calculate_scope1(self, scope1_data):
        """
        Scope 1 (Doğrudan) emisyonları hesapla
        
        Args:
            scope1_data: dict with fuel, process, mobile, thermal_systems, steel_output_ton
        """
        if not scope1_data:
            return None
            
        fuel = scope1_data.get('fuel', {})
        process = scope1_data.get('process', {})
        mobile = scope1_data.get('mobile', {})
        thermal = scope1_data.get('thermal_systems', {})
        
        # Yakıt bazlı emisyonlar
        fuel_emissions = {
            'coking_coal': fuel.get('coking_coal_ton', 0) * self.EMISSION_FACTORS['coking_coal'],
            'natural_gas': fuel.get('natural_gas_nm3', 0) * self.EMISSION_FACTORS['natural_gas'],
            'fuel_oil': fuel.get('fuel_oil_ton', 0) * self.EMISSION_FACTORS['fuel_oil']
        }
        
        # Mobil Yanma (Forklift, Araçlar vb.)
        mobile_emissions = {
            'diesel': mobile.get('diesel_liter', 0) * self.EMISSION_FACTORS['diesel']
        }
        
        # Proses emisyonları (Sektörel Girdiler)
        process_emissions = {
            'limestone': process.get('limestone_ton', 0) * self.EMISSION_FACTORS['limestone'],
            'electrode': process.get('electrode_ton', 0) * self.EMISSION_FACTORS['electrode'], # EAF Çelik
            'anode': process.get('anode_ton', 0) * self.EMISSION_FACTORS['anode'],             # Alüminyum
            'reductants': process.get('reductants_ton', 0) * self.EMISSION_FACTORS['coke_injection'], # Steel
            'pfc': process.get('pfc_emissions_ton', 0) * self.EMISSION_FACTORS['pfc_emissions'],      # Aluminum
            'ammonia': process.get('ammonia_ton', 0) * self.EMISSION_FACTORS['ammonia'],             # Fertilizer
            'nitric_acid': process.get('nitric_acid_ton', 0) * self.EMISSION_FACTORS['nitric_acid'], # Fertilizer
            'alloy_elements': process.get('alloy_elements_ton', 0) * 8.0                            # Aluminum Precursors
        }
        
        # Termal sistem emisyonları (Dışarıdan satın alınan ısı dahil)
        thermal_emissions = {
            'reheating': thermal.get('reheating_fuel_nm3', 0) * self.EMISSION_FACTORS['natural_gas'],
            'purchased_heat': thermal.get('purchased_heat_mwh', 0) * self.EMISSION_FACTORS['purchased_heat']
        }
        
        # Toplamlar
        total_fuel = sum(fuel_emissions.values())
        total_mobile = sum(mobile_emissions.values())
        total_process = sum(process_emissions.values())
        total_thermal = sum(thermal_emissions.values())
        
        total_scope1 = total_fuel + total_mobile + total_process + total_thermal
        
        # Çelik üretimi bazında yoğunluk (Varsayılan 1 ton hatayı önlemek için)
        steel_output = scope1_data.get('steel_output_ton', 1)
        intensity = total_scope1 / steel_output if steel_output > 0 else 0
        
        self.scope1_emissions = {
            'fuel_emissions': fuel_emissions,
            'mobile_emissions': mobile_emissions,
            'process_emissions': process_emissions,
            'thermal_emissions': thermal_emissions,
            'total_fuel': total_fuel,
            'total_mobile': total_mobile,
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
            scope2_data: dict with electricity consumption, grid factor, source_type
        """
        if not scope2_data:
            return None
            
        electricity = scope2_data.get('electricity', {})
        
        consumption_mwh = electricity.get('electricity_consumption_mwh', 0)
        grid_factor = electricity.get('grid_emission_factor_kgco2_kwh', 0)
        source_type = electricity.get('source_type', 'grid').lower() # grid, irec, ppa, solar
        
        # Yenilenebilir Kontrolü (Yeşil Enerji)
        is_green = source_type in ['irec', 'ppa', 'solar']
        
        if is_green:
            # Yeşil enerji -> 0 Emisyon (Market-based yaklaşım)
            grid_emissions = 0
            description = f"Green Energy Verified ({source_type.upper()})"
        else:
            # Standart Şebeke
            grid_emissions = consumption_mwh * 1000 * grid_factor / 1000  # tCO2
            description = "Standard Grid Mix"
        
        renewable_emissions = 0 # Sıfır kabul edilir
        total_scope2 = grid_emissions
        
        self.scope2_emissions = {
            'consumption_mwh': consumption_mwh,
            'grid_emission_factor': grid_factor,
            'source_type': source_type,
            'is_green_energy': is_green,
            'description': description,
            'total_grid_emissions': grid_emissions,
            'total_scope2': total_scope2,
            'breakdown': {
                'grid_kwh': consumption_mwh * 1000, # All consumption
                'emissions_tco2': total_scope2
            }
        }
        
        return self.scope2_emissions
    
    def get_optimization_scenarios(self, scope1_data, scope2_data, ets_price):
        """
        Optimizasyon senaryoları üret
        """
        scenarios = {}
        
        # 1. Doğalgaz Azaltma Senaryosu
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
                    'target_consumption': natural_gas_nm3 * 0.80,
                    'emission_saving_tco2': emission_saving,
                    'annual_cbam_saving_eur': cost_saving,
                    'investment_needed_eur': 50000,
                    'roi_years': 50000 / cost_saving if cost_saving > 0 else 0,
                    'measures': [
                        'Atık ısı geri kazanım sistemleri',
                        'Yüksek verimli brülör teknolojileri',
                        'Proses optimizasyonu'
                    ]
                }
        
        # 2. Yeşil Enerji Dönüşümü Senaryosu
        if scope2_data and 'electricity' in scope2_data:
            elec = scope2_data['electricity']
            source_type = elec.get('source_type', 'grid')
            consumption_mwh = elec.get('electricity_consumption_mwh', 0)
            grid_factor = elec.get('grid_emission_factor_kgco2_kwh', 0)
            
            # Eğer halihazırda yeşil değilse (grid ise)
            if source_type == 'grid' and consumption_mwh > 0:
                # Mevcut emisyonun tamamını sıfırlama potansiyeli
                current_emission = consumption_mwh * 1000 * grid_factor / 1000
                cost_saving = current_emission * ets_price
                
                scenarios['green_energy_transition'] = {
                    'name': 'Yeşil Enerjiye Geçiş (I-REC / PPA / GES)',
                    'current_source': 'Şebeke',
                    'target_source': 'Yenilenebilir (%)',
                    'emission_saving_tco2': current_emission,
                    'annual_cbam_saving_eur': cost_saving,
                    'investment_needed_eur': 100000, # Tahmini I-REC + Danışmanlık
                    'roi_years': 100000 / cost_saving if cost_saving > 0 else 0,
                    'measures': [
                        'I-REC sertifikası satın alımı',
                        'PPA (Power Purchase Agreement) anlaşması',
                        'Fabrika çatısı güneş enerjisi (GES) yatırımı'
                    ]
                }
        
        # 3. Hurda Kullanımı Artırma (Çelik İçin) - Mockup Logic
        # Eğer process inputlarında hurda/rate bilgisi varsa buraya eklenebilir
        
        # Kombine senaryo
        if len(scenarios) > 1:
            total_emission_saving = sum(s['emission_saving_tco2'] for s in scenarios.values())
            total_cost_saving = sum(s['annual_cbam_saving_eur'] for s in scenarios.values())
            total_investment = sum(s['investment_needed_eur'] for s in scenarios.values())
            
            scenarios['combined'] = {
                'name': 'Kombine Dönüşüm Stratejisi',
                'included_scenarios': list(scenarios.keys()),
                'total_emission_saving_tco2': total_emission_saving,
                'total_annual_cbam_saving_eur': total_cost_saving,
                'total_investment_needed_eur': total_investment,
                'roi_years': total_investment / total_cost_saving if total_cost_saving > 0 else 0,
                'emission_reduction_percent': (total_emission_saving / self.total_emissions * 100) if self.total_emissions > 0 else 0
            }
        
        return scenarios
    
    def get_summary(self):
        """Özet istatistikler"""
        total = 0
        scope1_val = self.scope1_emissions.get('total_scope1', 0) if self.scope1_emissions else 0
        scope2_val = self.scope2_emissions.get('total_scope2', 0) if self.scope2_emissions else 0
        
        total = scope1_val + scope2_val
        self.total_emissions = total
        
        return {
            'scope1': self.scope1_emissions,
            'scope2': self.scope2_emissions,
            'total_emissions': total,
            'breakdown_percent': {
                'scope1': (scope1_val / total * 100) if total > 0 else 0,
                'scope2': (scope2_val / total * 100) if total > 0 else 0
            }
        }
