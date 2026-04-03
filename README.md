# 📊 Electronic Campaigns Efficiency Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?logo=powerbi)
![SQL Server](https://img.shields.io/badge/SQL%20Server-Database-red?logo=microsoftsqlserver)
![Excel](https://img.shields.io/badge/Excel-Analytics-green?logo=microsoftexcel)

> A full-stack analytics solution for measuring and optimizing the performance of multi-channel electronic collection campaigns — covering **IVR, WhatsApp, Email, and SMS**.

---

## 🧩 Problem Statement

In a high-volume debt collection environment, campaigns run simultaneously across four channels — IVR auto-calls, WhatsApp, Email, and SMS. Without a unified view, the operations team had no way to answer critical questions:

- Which channel delivers the highest recovery rate per cost?
- At what time of day do customers respond most?
- Which customer segments convert better on which channel?
- How is campaign ROI trending over time?

Manual reporting was slow, inconsistent, and unable to catch performance drops in real time. The business needed a **single source of truth** that could drive fast, confident decisions.

---

## 🎯 Solution

Built an end-to-end analytics pipeline and interactive dashboard that consolidates campaign data across all four channels into a live, filterable Power BI report — powered by automated SQL pipelines and Python preprocessing.

### Architecture Overview

```
Raw Campaign Data (SQL Server)
        │
        ▼
Python ETL Pipeline (data cleaning, enrichment, KPI calculation)
        │
        ▼
SQL Server Data Warehouse (optimized views & stored procedures)
        │
        ▼
Power BI Dashboard (live connected, interactive filters)
        │
        ▼
Excel Export (for stakeholder reporting)
```

---

## 📈 Key KPIs Tracked

| KPI | Description |
|-----|-------------|
| **Response Rate** | % of contacted customers who responded per channel |
| **Recovery Rate** | % of debt successfully recovered from campaign targets |
| **Delivery Rate** | % of messages/calls successfully delivered |
| **Conversion Rate** | % of responses that resulted in a payment |
| **Cost per Contact** | Total campaign cost divided by number of contacts reached |
| **Campaign ROI** | Revenue recovered vs. campaign cost |

---

## 🔍 Key Findings

- 📞 **IVR** achieved the highest volume reach but lowest conversion — best used for early-stage reminders
- 💬 **WhatsApp** delivered the highest conversion rate, 2.3× higher than Email in the same segment
- 📧 **Email** had the lowest cost per contact, making it optimal for large low-priority segments
- ⏰ Campaigns sent between **10 AM – 12 PM** showed consistently higher response rates across all channels
- 🏆 Combining IVR (initial contact) → WhatsApp (follow-up) increased recovery rate by ~18% compared to single-channel campaigns

---

## 🛠️ Tools & Technologies

- **Python** — Data cleaning, ETL automation, KPI computation (Pandas, NumPy)
- **SQL Server** — Data warehouse, stored procedures, optimized views
- **Power BI** — Interactive dashboard with DAX measures and Power Query transformations
- **Excel** — Stakeholder reports and ad-hoc analysis

---

## 📁 Repository Structure

```
electronic-campaigns-dashboard/
│
├── README.md
│
├── data/
│   ├── sample_campaigns.csv        ← Synthetic dataset (mirrors real structure)
│   └── generate_synthetic_data.py  ← Script to regenerate sample data
│
├── sql/
│   ├── create_views.sql            ← SQL views used in Power BI
│   └── kpi_queries.sql             ← Core KPI calculation queries
│
├── notebooks/
│   └── campaign_analysis.ipynb     ← Full EDA and KPI analysis notebook
│
├── visuals/
│   └── dashboard_preview.png       ← Power BI dashboard screenshot
│
└── requirements.txt
```

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/abdelrahamannelmogyy/electronic-campaigns-dashboard.git
cd electronic-campaigns-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the synthetic dataset
```bash
python data/generate_synthetic_data.py
```

### 4. Run the analysis notebook
```bash
jupyter notebook notebooks/campaign_analysis.ipynb
```

### 5. Power BI
Open the `.pbix` file in Power BI Desktop and connect it to your local data source or the generated CSV files.

---

## 📊 Dashboard Preview

> *Screenshot of the Power BI dashboard goes here*

![Dashboard Preview](visuals/dashboard_preview.png)

---

## 💡 Business Impact

- Reduced manual reporting effort by **60%** through automated Python + SQL pipelines
- Enabled the operations team to identify underperforming campaigns **within hours** instead of days
- Directly contributed to optimizing campaign scheduling, improving overall recovery rates

---

## 👤 Author

**Abdelrahman Elmogy** — Data Analyst & Automation Engineer  
📍 Cairo, Egypt  
🔗 [LinkedIn](https://www.linkedin.com/in/abdelrahman-elmogy-5086b4245/) | 🌐 [Portfolio](https://abdelrahamannelmogyy.github.io)
