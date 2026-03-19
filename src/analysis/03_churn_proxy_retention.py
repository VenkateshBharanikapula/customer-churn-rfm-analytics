import pandas as pd

RFM_PATH = r"C:\Projects\customer_churn_rfm_analytics\data\processed\customer_rfm_segments.csv"

rfm = pd.read_csv(RFM_PATH)

CHURN_THRESHOLD_DAYS = 90
rfm["is_churned"] = (rfm["recency"] > CHURN_THRESHOLD_DAYS).astype(int)

summary = rfm.groupby("segment").agg(
    customers=("customer_id", "count"),
    churned=("is_churned", "sum"),
    churn_rate=("is_churned", "mean"),
    revenue=("monetary", "sum")
).reset_index()

summary["churn_rate"] = (summary["churn_rate"] * 100).round(2)

print("Churn Threshold (days):", CHURN_THRESHOLD_DAYS)
print("\nChurn by Segment:")
print(summary.sort_values("churn_rate", ascending=False))