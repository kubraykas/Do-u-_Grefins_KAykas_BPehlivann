"""
ETS Price Prediction Module
Uses Gemini LLM to predict future ETS carbon prices
"""

import pandas as pd
import numpy as np
from google import genai


class ETSPricePredictor:
    """
    Predicts future ETS prices using historical data and LLM
    """
    
    def __init__(self, gemini_client):
        """
        Initialize predictor with Gemini client
        
        Args:
            gemini_client: Gemini API client instance
        """
        self.client = gemini_client
    
    def load_data(self, csv_path):
        """
        Load and preprocess historical ETS price data with robust handling
        """
        # Load CSV efficiently
        try:
            # BOM ve farklı kodlamaları da yönetmek için 'utf-8-sig' kullanıyoruz
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
            
            # Tüm sütun isimlerini temizle (boşluklar ve tırnaklar)
            df.columns = df.columns.astype(str).str.replace('"', '').str.strip()
            
            # Sütun isimlerini küçük harfe çevirerek daha kolay eşleşme sağla
            col_map = {c.lower(): c for c in df.columns}
            
            # 'Date' sütununu bul (büyük-küçük harf duyarsız)
            date_col = next((col_map[k] for k in ['date', 'tarih'] if k in col_map), None)
            # 'Primary Market' veya 'Price' sütununu bul
            price_col = next((col_map[k] for k in ['primary market', 'ets price', 'price', 'fiyat'] if k in col_map), None)
            
            if not date_col or not price_col:
                raise ValueError(f"Gerekli sütunlar bulunamadı. Mevcut sütunlar: {list(df.columns)}")

            # Sütunları standart isimlere çevir
            df = df.rename(columns={date_col: 'date', price_col: 'ETS Price'})
            
            # Tarih dönüşümü
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Fiyat dönüşümü (Sayısal olmayan değerleri temizle)
            df['ETS Price'] = pd.to_numeric(
                df['ETS Price'].astype(str).str.replace(',', '').str.replace('€', '').str.strip(), 
                errors='coerce'
            )
            
            # Temizlik ve indexleme
            df = df.dropna(subset=['date', 'ETS Price'])
            df = df.set_index('date')
            df = df[['ETS Price']]
            df = df.sort_index()
            
            # MEMORY OPTIMIZATION: Sadece son 200 kaydı tut (Tahmin için yeterli)
            # Bu, Render'ın 512MB RAM sınırına takılmamızı önler.
            if len(df) > 200:
                df = df.tail(200)
            
            return df
            
        except Exception as e:
            print(f"❌ Veri Yükleme Hatası: {e}")
            raise e
        
        return df
    
    def calculate_statistics(self, df):
        """
        Calculate statistical metrics from time series
        
        Args:
            df (pandas.DataFrame): Time series data
            
        Returns:
            dict: Statistical metrics
        """
        stats = {
            'last_price': df['ETS Price'].iloc[-1],
            'mean_price': df['ETS Price'].mean(),
            'std_dev': df['ETS Price'].std(),
            'min_price': df['ETS Price'].min(),
            'max_price': df['ETS Price'].max(),
            'avg_change': df['ETS Price'].diff().dropna().mean()
        }
        
        # Last 20 data points
        last_20 = "\n".join([
            f"{date.date()} | {price:.2f}" 
            for date, price in df['ETS Price'].tail(20).items()
        ])
        stats['last_20_points'] = last_20
        
        return stats
    
    def build_prediction_prompt(self, stats):
        """
        Build LLM prompt for price prediction
        
        Args:
            stats (dict): Statistical metrics
            
        Returns:
            str: Formatted prompt for Gemini
        """
        prompt = f"""
Sen yalnızca sayısal zaman serileri üzerinde çalışan bir yapay zeka ajanısın.

Finans bilmezsin.
ETS nedir bilmezsin.
Gerçek dünya hakkında hiçbir bilgin yoktur.

Sadece verilen sayısal verideki matematiksel örüntüleri analiz edebilirsin.
Bu veri çeyreklik fiyatlardan oluşan bir zaman serisidir.

SERİNİN İSTATİSTİKSEL ÖZETİ

Son değer: {stats['last_price']:.2f}
Ortalama değer: {stats['mean_price']:.2f}
Zaman adımı başına ortalama değişim (drift): {stats['avg_change']:.4f}
Standart sapma (volatilite): {stats['std_dev']:.4f}
Minimum gözlenen değer: {stats['min_price']:.2f}
Maksimum gözlenen değer: {stats['max_price']:.2f}

GERÇEK GEÇMİŞ VERİ ÖRNEKLERİ
(Bunlar seriden alınmış gerçek değerlerdir)

{stats['last_20_points']}

YAPMAN GEREKEN ANALİZLER

1. Serinin davranış tipini belirle:
- Trend var mı?
- Ortalama etrafında dalgalanma mı?
- Volatilite sabit mi değişken mi?

2. Çeyreklik fiyat değişim hızını analiz et.
3. Volatiliteyi tahminlere yansıt.

4. Tahmin modeli şu davranışı izlemelidir:
x(t+1) = x(t) + drift ± volatilite

5. Tahminler:
- Düz çizgi OLMAMALI
- Aşırı pürüzsüz OLMAMALI
- Gerçek zaman serisi gibi küçük dalgalanmalar içermeli

6. Aşırı sıçramalar yapma. Tahminler geçmiş aralıkla tutarlı olmalı.
7. GELECEK hakkında dış bilgi kullanamazsın.

GÖREV 1 — GELECEK TAHMİNİ
Q1 2025 – Q4 2030 arasındaki ÇEYREKLİK değerleri tahmin et.

---  FORECAST ---
Quarter | Forecasted Value
"""
        return prompt
    
    def predict(self, csv_path, model="gemini-2.0-flash"):
        """
        Generate ETS price forecast
        
        Args:
            csv_path (str): Path to historical data CSV
            model (str): Gemini model to use
            
        Returns:
            pandas.DataFrame: Forecast table with quarters and prices
        """
        # Load and process data
        df = self.load_data(csv_path)
        
        # Calculate statistics
        stats = self.calculate_statistics(df)
        
        # Build prompt
        prompt = self.build_prediction_prompt(stats)
        
        # Call Gemini with retry logic for rate limits
        import time
        max_retries = 3
        response = None
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                break
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"⚠️ Gemini Rate Limit (429) hit. Retrying in {attempt + 2} seconds...")
                    time.sleep(attempt + 2)
                else:
                    raise e
        
        # Parse response into DataFrame
        forecast_df = self._parse_forecast_response(response.text)
        
        return forecast_df, stats
    
    def _parse_forecast_response(self, response_text):
        """
        Parse LLM response into structured DataFrame
        
        Args:
            response_text (str): Raw LLM response
            
        Returns:
            pandas.DataFrame: Parsed forecast data
        """
        lines = response_text.split('\n')
        data = []
        
        for line in lines:
            if '|' in line and 'Quarter' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 2:
                    try:
                        quarter = parts[0]
                        value = float(parts[1].replace('€', '').replace(',', '').strip())
                        data.append({'Quarter': quarter, 'Forecasted Value': value})
                    except:
                        continue
        
        return pd.DataFrame(data)
