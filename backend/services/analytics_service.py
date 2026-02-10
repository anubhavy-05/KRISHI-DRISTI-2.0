"""
Advanced Analytics Service - Price Analysis & Market Intelligence
Krishi Drishti 2.0 - Advanced Analytics Module
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os


class AnalyticsService:
    """Service class for advanced crop price analytics"""
    
    def __init__(self, data_file: str = None):
        """Initialize analytics service with data file"""
        if data_file is None:
            # Get project root directory
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            project_root = os.path.dirname(backend_dir)
            data_file = os.path.join(project_root, "all_crop_data.csv")
        
        self.data_file = data_file
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Load and preprocess data"""
        try:
            self.df = pd.read_csv(self.data_file)
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df = self.df.sort_values('Date')
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()
    
    def _filter_data(self, crop: str, state: str, days: int = None) -> pd.DataFrame:
        """Filter data by crop and state"""
        filtered_df = self.df[
            (self.df['Crop'].str.lower() == crop.lower()) &
            (self.df['State'].str.lower() == state.lower())
        ].copy()
        
        if days and len(filtered_df) > 0:
            cutoff_date = filtered_df['Date'].max() - timedelta(days=days)
            filtered_df = filtered_df[filtered_df['Date'] >= cutoff_date]
        
        return filtered_df
    
    # ==================== PRICE VOLATILITY ANALYSIS ====================
    
    def calculate_price_volatility(self, crop: str, state: str, period_days: int = 30) -> Dict:
        """
        Calculate price volatility and risk assessment
        
        Returns:
            - volatility_percentage: Standard deviation as percentage
            - risk_level: Low/Medium/High
            - price_range: [min, max]
            - average_price: Mean price
            - coefficient_variation: CV for relative volatility
        """
        df = self._filter_data(crop, state, days=period_days)
        
        if len(df) < 5:
            return {
                "error": "Insufficient data for volatility analysis",
                "data_points": len(df)
            }
        
        prices = df['Price'].values
        
        # Calculate statistics
        mean_price = np.mean(prices)
        std_dev = np.std(prices)
        volatility_pct = (std_dev / mean_price) * 100
        
        # Calculate daily returns for better volatility measure
        if len(prices) > 1:
            returns = np.diff(prices) / prices[:-1]
            daily_volatility = np.std(returns) * 100
        else:
            daily_volatility = 0
        
        # Determine risk level
        if volatility_pct < 5:
            risk_level = "Low"
            risk_color = "🟢"
            risk_score = 1
        elif volatility_pct < 10:
            risk_level = "Medium"
            risk_color = "🟡"
            risk_score = 2
        else:
            risk_level = "High"
            risk_color = "🔴"
            risk_score = 3
        
        # Coefficient of variation
        cv = (std_dev / mean_price) * 100
        
        return {
            "crop": crop,
            "state": state,
            "period_days": period_days,
            "volatility_percentage": round(volatility_pct, 2),
            "daily_volatility": round(daily_volatility, 2),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "risk_score": risk_score,
            "standard_deviation": round(std_dev, 2),
            "average_price": round(mean_price, 2),
            "price_range": {
                "min": round(float(np.min(prices)), 2),
                "max": round(float(np.max(prices)), 2)
            },
            "coefficient_variation": round(cv, 2),
            "data_points": len(df),
            "latest_price": round(float(prices[-1]), 2) if len(prices) > 0 else None
        }
    
    # ==================== SEASONAL PATTERN DETECTION ====================
    
    def detect_seasonal_patterns(self, crop: str, state: str) -> Dict:
        """
        Identify seasonal price patterns and optimal selling periods
        
        Returns:
            - best_month: Month with highest average price
            - worst_month: Month with lowest average price
            - monthly_averages: Dict of month-wise prices
            - price_difference: Difference between best and worst
            - peak_season: Season classification
        """
        df = self._filter_data(crop, state)
        
        if len(df) < 12:
            return {
                "error": "Insufficient data for seasonal analysis (need at least 12 months)",
                "data_points": len(df)
            }
        
        # Extract month and calculate monthly averages
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%B')
        
        monthly_stats = df.groupby(['Month', 'Month_Name'])['Price'].agg([
            'mean', 'median', 'std', 'count'
        ]).reset_index()
        
        monthly_stats = monthly_stats.sort_values('Month')
        
        # Find best and worst months
        best_month_idx = monthly_stats['mean'].idxmax()
        worst_month_idx = monthly_stats['mean'].idxmin()
        
        best_month = monthly_stats.loc[best_month_idx]
        worst_month = monthly_stats.loc[worst_month_idx]
        
        # Calculate price difference
        price_diff = best_month['mean'] - worst_month['mean']
        price_diff_pct = (price_diff / worst_month['mean']) * 100
        
        # Determine peak season (Kharif: June-Oct, Rabi: Nov-March)
        kharif_months = [6, 7, 8, 9, 10]
        rabi_months = [11, 12, 1, 2, 3]
        
        if int(best_month['Month']) in kharif_months:
            peak_season = "Kharif (Monsoon Season)"
        elif int(best_month['Month']) in rabi_months:
            peak_season = "Rabi (Winter Season)"
        else:
            peak_season = "Zaid (Summer Season)"
        
        # Create monthly averages dict
        monthly_data = []
        for _, row in monthly_stats.iterrows():
            monthly_data.append({
                "month": int(row['Month']),
                "month_name": row['Month_Name'],
                "average_price": round(float(row['mean']), 2),
                "median_price": round(float(row['median']), 2),
                "price_std": round(float(row['std']), 2),
                "sample_size": int(row['count'])
            })
        
        return {
            "crop": crop,
            "state": state,
            "best_month": {
                "month": int(best_month['Month']),
                "name": best_month['Month_Name'],
                "average_price": round(float(best_month['mean']), 2),
                "icon": "📈"
            },
            "worst_month": {
                "month": int(worst_month['Month']),
                "name": worst_month['Month_Name'],
                "average_price": round(float(worst_month['mean']), 2),
                "icon": "📉"
            },
            "price_difference": {
                "absolute": round(float(price_diff), 2),
                "percentage": round(float(price_diff_pct), 2)
            },
            "peak_season": peak_season,
            "monthly_data": monthly_data,
            "recommendation": f"Best time to sell: {best_month['Month_Name']} (₹{best_month['mean']:.2f}/quintal)"
        }
    
    # ==================== YEAR-OVER-YEAR COMPARISON ====================
    
    def calculate_year_over_year_trends(self, crop: str, state: str, years: int = 3) -> Dict:
        """
        Compare prices across multiple years
        
        Returns:
            - yearly_averages: Average prices by year
            - growth_rates: YoY growth percentages
            - cagr: Compound Annual Growth Rate
            - trend_direction: Increasing/Decreasing/Stable
        """
        df = self._filter_data(crop, state)
        
        if len(df) < 30:
            return {
                "error": "Insufficient data for year-over-year analysis",
                "data_points": len(df)
            }
        
        # Extract year
        df['Year'] = df['Date'].dt.year
        
        # Get yearly statistics
        yearly_stats = df.groupby('Year')['Price'].agg([
            'mean', 'median', 'min', 'max', 'count'
        ]).reset_index()
        
        yearly_stats = yearly_stats.sort_values('Year')
        
        # Limit to recent years
        yearly_stats = yearly_stats.tail(years)
        
        if len(yearly_stats) < 2:
            return {
                "error": "Need at least 2 years of data for comparison",
                "available_years": len(yearly_stats)
            }
        
        # Calculate growth rates
        growth_rates = []
        for i in range(1, len(yearly_stats)):
            prev_price = yearly_stats.iloc[i-1]['mean']
            curr_price = yearly_stats.iloc[i]['mean']
            growth_pct = ((curr_price - prev_price) / prev_price) * 100
            
            growth_rates.append({
                "from_year": int(yearly_stats.iloc[i-1]['Year']),
                "to_year": int(yearly_stats.iloc[i]['Year']),
                "growth_percentage": round(float(growth_pct), 2),
                "absolute_change": round(float(curr_price - prev_price), 2)
            })
        
        # Calculate CAGR
        first_year_price = yearly_stats.iloc[0]['mean']
        last_year_price = yearly_stats.iloc[-1]['mean']
        num_years = len(yearly_stats) - 1
        
        if num_years > 0:
            cagr = (((last_year_price / first_year_price) ** (1/num_years)) - 1) * 100
        else:
            cagr = 0
        
        # Determine trend direction
        avg_growth = np.mean([g['growth_percentage'] for g in growth_rates])
        
        if avg_growth > 5:
            trend = "Increasing ↗️"
            trend_color = "🟢"
        elif avg_growth < -5:
            trend = "Decreasing ↘️"
            trend_color = "🔴"
        else:
            trend = "Stable ➡️"
            trend_color = "🟡"
        
        # Prepare yearly data
        yearly_data = []
        for _, row in yearly_stats.iterrows():
            yearly_data.append({
                "year": int(row['Year']),
                "average_price": round(float(row['mean']), 2),
                "median_price": round(float(row['median']), 2),
                "min_price": round(float(row['min']), 2),
                "max_price": round(float(row['max']), 2),
                "data_points": int(row['count'])
            })
        
        return {
            "crop": crop,
            "state": state,
            "years_analyzed": len(yearly_stats),
            "yearly_data": yearly_data,
            "growth_rates": growth_rates,
            "cagr": round(float(cagr), 2),
            "trend_direction": trend,
            "trend_color": trend_color,
            "average_yearly_growth": round(float(avg_growth), 2),
            "price_range": {
                "lowest_year": int(yearly_stats.loc[yearly_stats['mean'].idxmin(), 'Year']),
                "lowest_price": round(float(yearly_stats['mean'].min()), 2),
                "highest_year": int(yearly_stats.loc[yearly_stats['mean'].idxmax(), 'Year']),
                "highest_price": round(float(yearly_stats['mean'].max()), 2)
            }
        }
    
    # ==================== MARKET SENTIMENT INDICATOR ====================
    
    def calculate_market_sentiment(self, crop: str, state: str, 
                                   predicted_price: float = None) -> Dict:
        """
        Calculate market sentiment based on price trends
        
        Returns:
            - sentiment: Bullish/Bearish/Neutral
            - confidence: Confidence score (0-100)
            - price_momentum: Recent price momentum
            - rsi: Relative Strength Index
            - recommendation: BUY/SELL/HOLD
        """
        df = self._filter_data(crop, state, days=90)
        
        if len(df) < 14:
            return {
                "error": "Insufficient data for sentiment analysis (need 14+ data points)",
                "data_points": len(df)
            }
        
        prices = df['Price'].values
        current_price = prices[-1]
        
        # Calculate price changes
        price_1w_ago = prices[-7] if len(prices) >= 7 else prices[0]
        price_1m_ago = prices[-30] if len(prices) >= 30 else prices[0]
        
        change_1w = ((current_price - price_1w_ago) / price_1w_ago) * 100
        change_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100
        
        # Calculate RSI (Relative Strength Index)
        rsi = self._calculate_rsi(prices, period=14)
        
        # Calculate momentum (rate of change)
        if len(prices) >= 10:
            momentum = ((prices[-1] - prices[-10]) / prices[-10]) * 100
        else:
            momentum = 0
        
        # Determine sentiment
        sentiment_score = 0
        
        # RSI contribution
        if rsi > 70:
            sentiment_score -= 2  # Overbought - bearish
        elif rsi < 30:
            sentiment_score += 2  # Oversold - bullish
        elif 40 <= rsi <= 60:
            sentiment_score += 0  # Neutral
        
        # Momentum contribution
        if momentum > 5:
            sentiment_score += 2
        elif momentum < -5:
            sentiment_score -= 2
        
        # Recent trends contribution
        if change_1w > 3 and change_1m > 5:
            sentiment_score += 1
        elif change_1w < -3 and change_1m < -5:
            sentiment_score -= 1
        
        # Prediction contribution (if provided)
        if predicted_price:
            pred_change = ((predicted_price - current_price) / current_price) * 100
            if pred_change > 10:
                sentiment_score += 2
            elif pred_change < -10:
                sentiment_score -= 2
        
        # Determine sentiment label
        if sentiment_score >= 3:
            sentiment = "Bullish"
            sentiment_emoji = "🐂"
            sentiment_color = "🟢"
            recommendation = "BUY"
        elif sentiment_score <= -3:
            sentiment = "Bearish"
            sentiment_emoji = "🐻"
            sentiment_color = "🔴"
            recommendation = "SELL"
        else:
            sentiment = "Neutral"
            sentiment_emoji = "➡️"
            sentiment_color = "🟡"
            recommendation = "HOLD"
        
        # Calculate confidence (0-100)
        confidence = min(abs(sentiment_score) * 15, 100)
        
        return {
            "crop": crop,
            "state": state,
            "sentiment": sentiment,
            "sentiment_emoji": sentiment_emoji,
            "sentiment_color": sentiment_color,
            "sentiment_score": sentiment_score,
            "confidence": round(float(confidence), 1),
            "recommendation": recommendation,
            "current_price": round(float(current_price), 2),
            "rsi": round(float(rsi), 2),
            "momentum": round(float(momentum), 2),
            "price_changes": {
                "1_week": round(float(change_1w), 2),
                "1_month": round(float(change_1m), 2)
            },
            "indicators": {
                "rsi_status": "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Normal",
                "momentum_status": "Strong Up" if momentum > 5 else "Strong Down" if momentum < -5 else "Moderate"
            }
        }
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI
        
        # Calculate price changes
        deltas = np.diff(prices)
        
        # Separate gains and losses
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        # Calculate average gains and losses
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    # ==================== PROFIT OPPORTUNITY ALERTS ====================
    
    def find_profit_opportunities(self, crop: str, state: str, 
                                  predicted_price: float,
                                  threshold_percent: float = 15) -> Dict:
        """
        Identify profit opportunities based on price predictions
        
        Returns:
            - opportunity_found: Boolean
            - potential_profit: Profit amount per quintal
            - action_recommendation: HOLD/SELL NOW
            - confidence_level: LOW/MEDIUM/HIGH
        """
        df = self._filter_data(crop, state, days=30)
        
        if len(df) == 0:
            return {
                "error": "No data available for this crop-state combination"
            }
        
        current_price = df['Price'].iloc[-1]
        
        # Calculate potential profit
        price_diff = predicted_price - current_price
        profit_percent = (price_diff / current_price) * 100
        
        # Determine opportunity
        opportunity_found = profit_percent >= threshold_percent
        
        # Calculate historical volatility for confidence
        volatility_data = self.calculate_price_volatility(crop, state, period_days=30)
        risk_level = volatility_data.get('risk_level', 'Medium')
        
        # Determine confidence level
        if risk_level == 'Low' and abs(profit_percent) > 20:
            confidence = "HIGH"
            confidence_color = "🟢"
        elif risk_level == 'Medium' or (10 <= abs(profit_percent) <= 20):
            confidence = "MEDIUM"
            confidence_color = "🟡"
        else:
            confidence = "LOW"
            confidence_color = "🔴"
        
        # Action recommendation
        if profit_percent >= threshold_percent:
            action = "HOLD"
            action_emoji = "⏳"
            message = f"Wait for price to reach ₹{predicted_price:.2f} for {profit_percent:.1f}% profit"
        elif profit_percent <= -10:
            action = "SELL NOW"
            action_emoji = "⚠️"
            message = f"Price may drop by {abs(profit_percent):.1f}%. Consider selling now"
        else:
            action = "MONITOR"
            action_emoji = "👁️"
            message = "Price expected to remain stable. Monitor market conditions"
        
        # Calculate potential profit for different quantities
        profit_scenarios = [
            {"quantity_quintal": 10, "profit": round(price_diff * 10, 2)},
            {"quantity_quintal": 50, "profit": round(price_diff * 50, 2)},
            {"quantity_quintal": 100, "profit": round(price_diff * 100, 2)}
        ]
        
        return {
            "crop": crop,
            "state": state,
            "opportunity_found": opportunity_found,
            "current_price": round(float(current_price), 2),
            "predicted_price": round(float(predicted_price), 2),
            "price_difference": {
                "absolute": round(float(price_diff), 2),
                "percentage": round(float(profit_percent), 2)
            },
            "action": action,
            "action_emoji": action_emoji,
            "message": message,
            "confidence_level": confidence,
            "confidence_color": confidence_color,
            "risk_assessment": risk_level,
            "profit_scenarios": profit_scenarios,
            "recommendation_details": {
                "should_hold": profit_percent >= threshold_percent,
                "should_sell_now": profit_percent <= -10,
                "estimated_days_to_target": 30,  # Can be refined with more data
                "stop_loss_price": round(float(current_price * 0.9), 2)
            }
        }
    
    # ==================== COMPREHENSIVE DASHBOARD DATA ====================
    
    def get_comprehensive_analytics(self, crop: str, state: str, 
                                    predicted_price: float = None) -> Dict:
        """
        Get all analytics in one call for dashboard
        """
        try:
            result = {
                "crop": crop,
                "state": state,
                "timestamp": datetime.now().isoformat(),
                "volatility": self.calculate_price_volatility(crop, state),
                "seasonal_patterns": self.detect_seasonal_patterns(crop, state),
                "trends": self.calculate_year_over_year_trends(crop, state),
                "sentiment": self.calculate_market_sentiment(crop, state, predicted_price)
            }
            
            if predicted_price:
                result["profit_opportunities"] = self.find_profit_opportunities(
                    crop, state, predicted_price
                )
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "crop": crop,
                "state": state
            }
