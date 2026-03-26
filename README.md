# Customer Churn & RFM Segmentation Analytics (End-to-End)

## 📌 Overview

This project builds an **end-to-end customer analytics workflow** to identify high-value customer segments and customers at risk of churn.

Using transaction-level purchase data, the solution delivers:

* 📊 **RFM segmentation** (Recency, Frequency, Monetary)
* ⚠️ **Churn proxy analysis** using inactivity thresholds
* 🔁 **Cohort retention analysis**
* 💰 **Revenue impact & ROI simulation (Excel)**
* 📈 **Power BI dashboard** for stakeholder reporting

> 💡 Designed as a reusable framework for churn monitoring and retention strategy planning.

---

## 🎯 Business Objective

**Identify customers at risk of churn and high-value segments, and translate insights into actionable retention strategies.**

### Key Questions Answered

* Which segments contribute the most revenue?
* Which segments show the highest churn risk?
* How does retention behave across cohorts?
* What is the financial impact of improving churn?

---

## 📂 Dataset

**Online Retail II** dataset:

* Transaction-level purchase records
* Customer and product identifiers
* Quantity, price, invoice timestamps
* Customer geography

---

## 🛠️ Tech Stack

* **SQL Server (SSMS)** → RFM scoring, aggregations, window functions
* **Python (pandas, numpy, matplotlib, seaborn)** → cleaning, analysis, visualization
* **Excel** → revenue impact & ROI simulation
* **Power BI** → dashboarding & reporting

---

## ⚙️ Methodology

### 1️⃣ Data Cleaning (Python)

* Removed missing `customer_id`
* Removed cancelled invoices (`C` prefix)
* Removed non-positive quantities
* Created `total_amount = quantity × price`
* Parsed `invoicedate`

**Output:**
`data/processed/transactions_clean.csv`

---

### 2️⃣ RFM Feature Engineering

* Snapshot date = `max(invoicedate) + 1 day`

**Metrics:**

* Recency → days since last purchase
* Frequency → number of invoices
* Monetary → total spend

**Output:**
`data/processed/customer_rfm_segments.csv`

---

### 3️⃣ RFM Scoring (Quintiles)

* Scores: 1–5 (5 = best)
* Recency inverted
* Combined score:

```
rfm_score = R + F + M  (e.g., 555)
```

---

### 4️⃣ Customer Segmentation

* 🏆 Champions
* 🤝 Loyal Customers
* 🆕 New Customers
* ⚠️ At Risk
* 💤 Hibernating

---

### 5️⃣ Churn Proxy

```
Recency > 90 days → Churned
```

---

### 6️⃣ Cohort Retention

* Cohort = first purchase month
* Tracks retention over time

Used to identify:

* Early drop-offs
* Retention decay
* Cohort quality

---

### 7️⃣ Revenue Impact Model (Excel)

**Inputs:**

* Total Revenue
* Current churn rate
* Target churn reduction
* Campaign cost

**Outputs:**

* Revenue at risk
* Incremental revenue gain
* Net impact
* ROI

---

## 📊 Key Results

### 💰 Revenue Concentration

* **Champions → ~69% of revenue**

### ⚠️ Churn Risk

* Overall churn proxy: **50.9%**
* Highest risk: **At Risk** and **Hibernating**

### 📈 Business Impact

* Total revenue: **17.74M**
* Revenue at risk: **5.32M**
* 5% churn reduction → **~$266K incremental revenue**
* Campaign example:

  * Cost: $50K
  * ROI: **~432%**

---

## 📷 Visual Outputs

### Customer Segment Distribution

![Customer Segment Distribution](outputs/figures/01_segment_distribution.png)

### Revenue Contribution by Segment

![Revenue Contribution by Segment](outputs/figures/02_revenue_by_segment.png)

### Churn Rate by Segment (Proxy)

![Churn Rate by Segment](outputs/figures/03_churn_rate_by_segment.png)

### Cohort Retention Heatmap

![Cohort Retention Heatmap](outputs/figures/04_cohort_retention_heatmap.png)

---

## 📊 Power BI Dashboard

Interactive dashboard includes:

* Total customers, revenue, churn rate
* Segment distribution
* Revenue contribution
* Churn insights

**File:**
`dashboards/Customer_Churn_RFM_Dashboard.pbix`

---

## 🧠 SQL Implementation (SSMS)

* Built using:

  * CTEs
  * Aggregations
  * `NTILE` window functions

**Output:**
`data/processed/rfm_sql_export.xlsx`

---

## 📁 Project Structure

```
customer_churn_rfm_analytics/
├── dashboards/
│   └── Customer_Churn_RFM_Dashboard.pbix
├── data/
│   ├── raw/
│   └── processed/
│       ├── transactions_clean.csv
│       ├── customer_rfm_segments.csv
│       └── rfm_sql_export.xlsx
├── outputs/
│   ├── figures/
│   │   ├── 01_segment_distribution.png
│   │   ├── 02_revenue_by_segment.png
│   │   ├── 03_churn_rate_by_segment.png
│   │   └── 04_cohort_retention_heatmap.png
│   └── reports/
│       └── Revenue_Impact_Model.xlsx
├── src/
│   ├── data/
│   ├── features/
│   ├── analysis/
│   └── visualization/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How to Use

1. Clone the repository
2. Install dependencies (`requirements.txt`)
3. Run scripts from `src/`
4. Open Power BI dashboard
5. Explore Excel ROI model

---

## 💡 Key Takeaways

* Combines **analytics + business impact**
* Demonstrates **end-to-end workflow**
* Bridges **data analysis and decision-making**
