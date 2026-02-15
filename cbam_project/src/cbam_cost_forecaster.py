"""
CBAM Cost Forecast Module
Predicts future CBAM costs based on ETS price forecasts
"""

import pandas as pd


class CBAMCostForecaster:
    """
    Forecasts CBAM costs using predicted ETS prices
    """
    
    def __init__(self, gemini_client):
        """
        Initialize forecaster with Gemini client
        
        Args:
            gemini_client: Gemini API client instance
        """
        self.client = gemini_client
    
    def build_forecast_prompt(self, cbam_summary, ets_forecast_table):
        """
        Build LLM prompt for CBAM cost forecasting
        
        Args:
            cbam_summary (dict): Current CBAM calculation summary
            ets_forecast_table (pandas.DataFrame): ETS price forecasts
            
        Returns:
            str: Formatted prompt for Gemini
        """
        # Convert forecast table to string
        if hasattr(ets_forecast_table, 'to_string'):
            ets_table_str = ets_forecast_table.to_string(index=False)
        else:
            ets_table_str = str(ets_forecast_table)
        
        prompt = f"""
You are an EU CBAM financial forecasting AI.
Current import data:
Product: {cbam_summary['product']}
Sector: {cbam_summary['category']}
Import volume: {cbam_summary['quantity_tonnes']} tonnes
Total emission intensity: {cbam_summary['total_ei']} tCO2/t
Current CBAM cost: €{cbam_summary['cbam_cost']}

**USE THESE EXACT FORECASTED ETS PRICES (from previous carbon price prediction):**
{ets_table_str}

Task:
Calculate CBAM cost for each quarter from Q1 2025 to Q4 2030 using the ETS prices provided above.

Formula: CBAM Cost = (Import Volume × Total EI × Forecasted Value)

Where:
- Import Volume = {cbam_summary['quantity_tonnes']} tonnes
- Total EI = {cbam_summary['total_ei']} tCO2/t
- Forecasted Value = from the "Forecasted Value" column in the table above

Provide output as a TABLE:
Quarter | Forecasted ETS Price (EUR) | Estimated CBAM Cost (EUR) 

Be realistic, policy-aware, and analytical.
IMPORTANT: Use the EXACT values from the "Forecasted Value" column in the forecast table above. DO NOT generate your own ETS price estimates.
"""
        return prompt
    
    def forecast(self, cbam_summary, ets_forecast_table, model="gemini-2.0-flash"):
        """
        Generate CBAM cost forecast
        
        Args:
            cbam_summary (dict): Current CBAM calculation summary
            ets_forecast_table (pandas.DataFrame): ETS price forecasts
            model (str): Gemini model to use
            
        Returns:
            str: Raw LLM response with forecast table
        """
        prompt = self.build_forecast_prompt(cbam_summary, ets_forecast_table)
        
        response = self.client.models.generate_content(
            model=model,
            contents=prompt
        )
        
        return response.text
    
    def parse_forecast_response(self, llm_text):
        """
        Parse LLM CBAM cost forecast into DataFrame
        
        Args:
            llm_text (str): Raw LLM response
            
        Returns:
            pandas.DataFrame: Parsed CBAM cost forecast
        """
        cols = ['Quarter', 'ETS_Price', 'CBAM_Cost']

        if not isinstance(llm_text, str) or '|' not in llm_text:
            return pd.DataFrame(columns=cols)

        lines = [l.strip() for l in llm_text.split('\n') if '|' in l]
        parsed = []

        for line in lines:
            if 'quarter' in line.lower() or '---' in line:
                continue

            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 3:
                continue

            try:
                parsed.append({
                    'Quarter': parts[0],
                    'ETS_Price': float(parts[1].replace('€','').replace(',','').replace('EUR','').strip()),
                    'CBAM_Cost': float(parts[2].replace('€','').replace(',','').replace('EUR','').strip())
                })
            except:
                continue

        return pd.DataFrame(parsed, columns=cols)
