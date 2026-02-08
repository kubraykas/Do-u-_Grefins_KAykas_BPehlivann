"""
CBAM Calculator Module
Core calculation logic for CBAM costs and emissions
"""

from .cn_code_database import CN_CODE_DATABASE


class CBAMCalculator:
    """
    CBAM Calculator for calculating carbon costs and emissions
    """
    
    def __init__(self, ets_price):
        """
        Initialize calculator with ETS price
        
        Args:
            ets_price (float): Current EU ETS price in €/tCO2
        """
        self.ets_price = ets_price

    def normalize_code(self, code):
        """
        Normalize CN code format
        
        Args:
            code (str): CN code to normalize
            
        Returns:
            str: Normalized CN code
        """
        return code.strip()

    def get_data_by_cn(self, cn_code):
        """
        Retrieve emission data for a specific CN code
        
        Args:
            cn_code (str): CN code to lookup
            
        Returns:
            dict or None: Product emission data or None if not found
        """
        cn_code = self.normalize_code(cn_code)
        data = CN_CODE_DATABASE.get(cn_code)

        if data:
            return {
                "description": data["description"],
                "category": data["category"],
                "direct_ei": data["direct"],
                "indirect_ei": data["indirect"],
                "total_ei": data["total"]
            }
        else:
            return None

    def calculate(self, quantity, direct_ei, indirect_ei, foreign_carbon_price=0):
        """
        Calculate CBAM costs and emissions
        
        Args:
            quantity (float): Import quantity in tonnes
            direct_ei (float): Direct emission intensity (tCO2/t)
            indirect_ei (float): Indirect emission intensity (tCO2/t)
            foreign_carbon_price (float): Foreign carbon price (€/tCO2)
            
        Returns:
            dict: Calculation results including emissions and costs
        """
        total_ei = direct_ei + indirect_ei
        total_emission = quantity * total_ei
        certificates = total_emission

        cost = total_emission * self.ets_price
        adjusted_cost = cost - (total_emission * foreign_carbon_price)

        return {
            "total_ei": total_ei,
            "total_emission": total_emission,
            "certificates": certificates,
            "cbam_cost": cost,
            "cbam_cost_adjusted": adjusted_cost
        }
    
    def get_summary(self, cn_code, quantity):
        """
        Get complete CBAM summary for a product
        
        Args:
            cn_code (str): Product CN code
            quantity (float): Import quantity in tonnes
            
        Returns:
            dict or None: Complete CBAM summary or None if CN code not found
        """
        data = self.get_data_by_cn(cn_code)
        
        if data is None:
            return None
        
        result = self.calculate(quantity, data["direct_ei"], data["indirect_ei"])
        
        return {
            "product": data["description"],
            "category": data["category"],
            "quantity_tonnes": quantity,
            "direct_ei": data["direct_ei"],
            "indirect_ei": data["indirect_ei"],
            "total_ei": result["total_ei"],
            "total_emission": result["total_emission"],
            "certificates": result["certificates"],
            "ets_price": self.ets_price,
            "cbam_cost": result["cbam_cost"],
            "cbam_cost_adjusted": result["cbam_cost_adjusted"]
        }
