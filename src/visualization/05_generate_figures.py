import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = r"C:\Projects\customer_churn_rfm_analytics"
RFM_PATH = os.path.join(BASE, "data", "processed", "customer_rfm_segments.csv")
TXN_PATH = os.path.join(BASE, "data", "processed", "transactions_clean.csv")
OUT_DIR = os.path.join(BASE, "outputs", "figures")

os.makedirs(OUT_DIR, exist_ok=True)

# ----------------------------
# Load data
# ----------------------------
rfm = pd.read_csv(RFM_PATH)
tx = pd.read_csv(TXN_PATH)

# ----------------------------
# Figure 1: Segment distribution
# ----------------------------
seg_counts = rfm["segment"].value_counts().sort_values(ascending=False)

plt.figure()
seg_counts.plot(kind="bar")
plt.title("Customer Segment Distribution")
plt.xlabel("Segment")
plt.ylabel("Customers")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "01_segment_distribution.png"), dpi=200)
plt.close()

# ----------------------------
# Figure 2: Revenue by segment
# ----------------------------
seg_revenue = rfm.groupby("segment")["monetary"].sum().sort_values(ascending=False)

plt.figure()
seg_revenue.plot(kind="bar")
plt.title("Revenue Contribution by Segment")
plt.xlabel("Segment")
plt.ylabel("Total Revenue")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "02_revenue_by_segment.png"), dpi=200)
plt.close()

# ----------------------------
# Figure 3: Churn rate by segment (proxy: recency > 90)
# ----------------------------
CHURN_THRESHOLD_DAYS = 90
rfm["is_churned"] = (rfm["recency"] > CHURN_THRESHOLD_DAYS).astype(int)

seg_churn_rate = rfm.groupby("segment")["is_churned"].mean().sort_values(ascending=False) * 100

plt.figure()
seg_churn_rate.plot(kind="bar")
plt.title(f"Churn Rate by Segment (Recency > {CHURN_THRESHOLD_DAYS} days)")
plt.xlabel("Segment")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "03_churn_rate_by_segment.png"), dpi=200)
plt.close()

# ----------------------------
# Figure 4: Cohort retention heatmap (monthly)
# ----------------------------
tx["invoicedate"] = pd.to_datetime(tx["invoicedate"])
tx["invoice_month"] = tx["invoicedate"].dt.to_period("M")
tx["cohort_month"] = tx.groupby("customer_id")["invoice_month"].transform("min")

tx["cohort_index"] = (
    (tx["invoice_month"].dt.year - tx["cohort_month"].dt.year) * 12 +
    (tx["invoice_month"].dt.month - tx["cohort_month"].dt.month)
)

cohort_data = tx.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")

cohort_size = cohort_pivot.iloc[:, 0]
retention = cohort_pivot.divide(cohort_size, axis=0)

plt.figure(figsize=(12, 6))
sns.heatmap(retention, annot=False)
plt.title("Cohort Retention Heatmap (Monthly)")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_cohort_retention_heatmap.png"), dpi=200)
plt.close()

print("Saved figures to:", OUT_DIR)