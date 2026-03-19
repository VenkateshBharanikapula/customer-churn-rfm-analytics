import pandas as pd

INPUT_PATH = r"C:\Projects\customer_churn_rfm_analytics\data\processed\transactions_clean.csv"
OUTPUT_PATH = r"C:\Projects\customer_churn_rfm_analytics\data\processed\customer_rfm_segments.csv"

df = pd.read_csv(INPUT_PATH)
df["invoicedate"] = pd.to_datetime(df["invoicedate"])

snapshot_date = df["invoicedate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg({
    "invoicedate": lambda x: (snapshot_date - x.max()).days,
    "invoice": "nunique",
    "total_amount": "sum"
}).reset_index()

rfm.columns = ["customer_id", "recency", "frequency", "monetary"]

rfm["r_score"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1]).astype(int)
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["m_score"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5]).astype(int)

rfm["rfm_score"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)

def segment_customer(row):
    if row["r_score"] >= 4 and row["f_score"] >= 4:
        return "Champions"
    elif row["r_score"] >= 3 and row["f_score"] >= 3:
        return "Loyal Customers"
    elif row["r_score"] >= 4 and row["f_score"] <= 2:
        return "New Customers"
    elif row["r_score"] <= 2 and row["f_score"] >= 3:
        return "At Risk"
    else:
        return "Hibernating"

rfm["segment"] = rfm.apply(segment_customer, axis=1)

rfm.to_csv(OUTPUT_PATH, index=False)

print("Saved:", OUTPUT_PATH)
print("Customers:", rfm.shape[0])
print(rfm["segment"].value_counts())