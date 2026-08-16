AI-Based Sales Forecasting and Inventory Optimization System

An AI-powered Sales Forecasting and Inventory Optimization System designed to help businesses predict future product demand, analyze sales trends, and make better inventory management decisions.

🚀 Project Overview

This project combines Data Science, Machine Learning, Backend API development, Database Management, and React to create an intelligent sales and inventory management system.

The system analyzes historical sales data and uses Machine Learning models to forecast future product demand. Based on the forecast and current inventory levels, the system can provide inventory and reorder recommendations.

🎯 Objectives

- Predict future product demand using Machine Learning
- Analyze historical sales data
- Identify sales trends and patterns
- Monitor current inventory levels
- Provide inventory recommendations
- Reduce stockouts and overstocking
- Provide an interactive dashboard for business users

🧠 Machine Learning

The project currently experiments with:

- Random Forest
- XGBoost

Features

The forecasting model uses features such as:

- Day
- Month
- Day of Week
- Previous Day Quantity
- Previous Week Quantity
- Rolling Mean

Evaluation Metrics

Models are evaluated using:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score

The best-performing model is selected for forecasting.

📊 Exploratory Data Analysis

The project includes several visualizations:

- Monthly Sales
- Daily Sales
- Top 10 Products
- Category Sales
- Revenue Trend

These visualizations help identify important patterns and trends in the historical sales data.

🏗️ System Architecture

```text
React Frontend
       ↓
FastAPI Backend
       ↓
PostgreSQL Database
       ↓
Sales & Inventory Data
       ↓
Machine Learning Model
       ↓
Sales Forecast
       ↓
Inventory Recommendation
       ↓
React Dashboard
