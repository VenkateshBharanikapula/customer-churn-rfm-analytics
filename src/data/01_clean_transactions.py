import pandas as pd

INPUT_PATH = r"C:\Projects\customer_churn_rfm_analytics\data\raw\online_retail_II.csv"
OUTPUT_PATH = r"C:\Projects\customer_churn_rfm_analytics\data\processed\transactions_clean.csv"

df = pd.read_csv(INPUT_PATH, encoding="ISO-8859-1")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df = df.dropna(subset=["customer_id"])
df = df[~df["invoice"].astype(str).str.startswith("C")]
df = df[df["quantity"] > 0]

df["invoicedate"] = pd.to_datetime(df["invoicedate"])
df["total_amount"] = df["quantity"] * df["price"]

df.to_csv(OUTPUT_PATH, index=False)

print("Saved:", OUTPUT_PATH)
print("Shape:", df.shape)