import pandas as pd

FILE_PATH = "C:/Projects/customer_churn_rfm_analytics/data/raw/online_retail_II.csv"

df = pd.read_csv(FILE_PATH, encoding="ISO-8859-1")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Initial Shape:", df.shape)

# 1️⃣ Remove missing customer_id
df = df.dropna(subset=["customer_id"])

# 2️⃣ Remove cancelled invoices
df = df[~df["invoice"].astype(str).str.startswith("C")]

# 3️⃣ Remove negative or zero quantity
df = df[df["quantity"] > 0]

# 4️⃣ Create total amount
df["total_amount"] = df["quantity"] * df["price"]

print("Cleaned Shape:", df.shape)
print("\nMissing values after cleaning:")
print(df.isna().sum())

print("\nSample:")
print(df.head())

# Convert invoice date to datetime
df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# Snapshot date (1 day after last transaction)
snapshot_date = df["invoicedate"].max() + pd.Timedelta(days=1)

# Aggregate RFM metrics
rfm = df.groupby("customer_id").agg({
    "invoicedate": lambda x: (snapshot_date - x.max()).days,  # Recency
    "invoice": "nunique",  # Frequency
    "total_amount": "sum"  # Monetary
}).reset_index()

rfm.columns = ["customer_id", "recency", "frequency", "monetary"]

print("\nRFM Shape:", rfm.shape)
print("\nRFM Sample:")
print(rfm.head())

# Create R, F, M scores using quintiles

rfm["r_score"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1])
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm["m_score"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5])

# Convert to int
rfm["r_score"] = rfm["r_score"].astype(int)
rfm["f_score"] = rfm["f_score"].astype(int)
rfm["m_score"] = rfm["m_score"].astype(int)

# Create combined RFM score
rfm["rfm_score"] = (
    rfm["r_score"].astype(str) +
    rfm["f_score"].astype(str) +
    rfm["m_score"].astype(str)
)

print("\nRFM Scored Sample:")
print(rfm.head())

print("\nTop RFM combinations:")
print(rfm["rfm_score"].value_counts().head())

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

print("\nSegment Distribution:")
print(rfm["segment"].value_counts())

# Revenue by segment
segment_revenue = rfm.groupby("segment").agg({
    "customer_id": "count",
    "monetary": "sum"
}).reset_index()

segment_revenue.columns = ["segment", "customer_count", "total_revenue"]

segment_revenue["revenue_share_%"] = (
    segment_revenue["total_revenue"] /
    segment_revenue["total_revenue"].sum() * 100
).round(2)

print("\nRevenue Contribution by Segment:")
print(segment_revenue.sort_values("total_revenue", ascending=False))