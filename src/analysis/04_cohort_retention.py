import pandas as pd

INPUT_PATH = r"C:\Projects\customer_churn_rfm_analytics\data\processed\transactions_clean.csv"

df = pd.read_csv(INPUT_PATH)
df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# Create invoice month
df["invoice_month"] = df["invoicedate"].dt.to_period("M")

# Get first purchase month per customer
df["cohort_month"] = df.groupby("customer_id")["invoice_month"].transform("min")

# Calculate months since first purchase
df["cohort_index"] = (
    (df["invoice_month"].dt.year - df["cohort_month"].dt.year) * 12 +
    (df["invoice_month"].dt.month - df["cohort_month"].dt.month)
)

# Create retention table
cohort_data = df.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()

cohort_pivot = cohort_data.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="customer_id"
)

# Convert to retention %
cohort_size = cohort_pivot.iloc[:, 0]
retention = cohort_pivot.divide(cohort_size, axis=0)

retention = retention.round(3)

print("Retention Matrix (first 10 rows):")
print(retention.head(10))