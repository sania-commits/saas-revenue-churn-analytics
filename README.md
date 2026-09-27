# SaaS Revenue & Churn Analytics Platform

An end-to-end Power BI analytics project designed to analyze SaaS recurring revenue, customer churn, retention, and revenue movement.

## Project Overview

This project transforms subscription and monthly revenue data into an interactive SaaS analytics solution for monitoring business growth and customer retention.

The report contains two analytical views:

### Executive Overview
Provides a high-level view of SaaS business performance using:

- Current MRR
- ARR
- Active Customers
- Churn Rate
- Retention Rate
- MRR Growth
- Monthly Recurring Revenue Trend
- MRR Movement
- MRR by Plan
- Churn Rate by Plan
- MRR by Region
- Interactive Year filtering

### Monthly Revenue & Churn Analysis
Provides detailed month-level analysis including:

- Total MRR
- New MRR
- Expansion MRR
- Contraction MRR
- Churned MRR
- Net New MRR
- MRR Growth %
- Churn Rate %
- Retention Rate %
- Acquisition vs Churn trends
- Dynamic MRR performance insight
- Conditional formatting for positive/negative growth

## Data Model

The Power BI model includes:

- Customers
- Subscriptions
- Monthly Revenue
- Plans
- Regions
- Date dimension

Relationships were designed to support customer, subscription, plan, regional, and time-based analysis.

## DAX Measures

Key measures developed include:

- Total MRR
- Current MRR
- ARR
- Active Customers
- New MRR
- Expansion MRR
- Contraction MRR
- Churned MRR
- Net New MRR
- MRR Growth %
- Churn Rate %
- Retention Rate %
- ARPU
- Dynamic MRR Insight

## Tools & Technologies

- Power BI Desktop
- Power Query
- DAX
- Data Modeling
- Star Schema concepts
- Time Intelligence
- Conditional Formatting
- Interactive Slicers
- Git & GitHub

## Dashboard Pages

### 1. Executive Overview
Executive-level dashboard for monitoring revenue, growth, customer activity, churn, retention, plan performance, and regional performance.

### 2. Monthly Analysis
Detailed operational view for analyzing monthly recurring revenue movement, acquisition, churn, and retention trends.

## Key Business Insights

The dashboard enables stakeholders to:

- Monitor recurring revenue growth
- Track customer acquisition and churn
- Compare performance across subscription plans
- Analyze geographic revenue contribution
- Measure expansion and contraction revenue
- Identify monthly revenue growth or decline
- Monitor customer retention performance

## Project Structure

```text
saas-revenue-churn-analytics/
├── data/
├── docs/
├── exports/
├── scripts/
├── saas-revenue-churn-analytics.pbix
└── README.md
