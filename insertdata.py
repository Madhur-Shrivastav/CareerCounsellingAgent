import pandas as pd
import uuid
import random
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MySQL
engine = create_engine(f"mysql+pymysql://root:{os.getenv('MYSQL_PASSWORD')}@localhost:3306/customer_support")

# Load CSV files and limit to first 300 rows
customer_df = pd.read_csv("CustomerSupport.csv").head(300)
user_df = pd.read_csv("UsersDataset.csv").head(300)

# Rename customer_df columns
customer_df.columns = [
    "user_id", "age", "gender", "item_purchased", "category", "purchase_amount_usd",
    "location", "size", "color", "season", "review_rating", "subscription_status",
    "payment_method", "shipping_type", "discount_applied", "promo_code_used",
    "previous_purchases", "preferred_payment_method", "frequency_of_purchases"
]

# Rename user_df columns
user_df.columns = ["user_id", "name", "gender", "dob", "interests", "city", "country"]

# Generate and assign shared user_id UUIDs
uuids = [str(uuid.uuid4()) for _ in range(len(customer_df))]
customer_df["user_id"] = uuids
user_df["user_id"] = uuids


# Normalize fields in customer_df
customer_df["discount_applied"] = customer_df["discount_applied"].str.strip().str.lower().map({"yes": True, "no": False})
customer_df["promo_code_used"] = customer_df["promo_code_used"].str.strip().str.lower().map({"yes": True, "no": False})
customer_df["subscription_status"] = customer_df["subscription_status"].str.strip().str.lower().map({
    "yes": 1, "no": 0
})


# Fill missing values
customer_df = customer_df.fillna({
    "purchase_amount_usd": 0.0,
    "review_rating": 0.0,
    "subscription_status": "Not Subscribed",
    "discount_applied": False,
    "promo_code_used": False,
    "previous_purchases": 0,
    "frequency_of_purchases": "Rarely"
})

# Reorder customer columns
customer_df = customer_df[[
    "user_id", "age", "gender", "item_purchased", "category",
    "purchase_amount_usd", "location", "size", "color", "season",
    "review_rating", "subscription_status", "payment_method", "shipping_type",
    "discount_applied", "promo_code_used", "previous_purchases",
    "preferred_payment_method", "frequency_of_purchases"
]]

# Keep only needed fields for users table
user_df = user_df[["user_id", "name", "gender"]]
user_df["age"] = customer_df["age"]

# Generate email and contact
def generate_email(name):
    first_name = name.split()[0].lower()
    return f"{first_name}{random.randint(100, 999)}@gmail.com"

def generate_contact():
    return str(random.randint(6000000000, 9999999999))

user_df["email"] = user_df["name"].apply(generate_email)
user_df["contact"] = user_df["name"].apply(lambda _: generate_contact())
user_df["password"] = "123456789"

# Reorder user columns
user_df = user_df[["user_id", "name", "gender", "age", "email", "contact", "password"]]

# Insert into MySQL

# Step 1: Drop duplicates within the DataFrame itself
user_df.drop_duplicates(subset="email", inplace=True)

# Step 2: Optional — remove entries that already exist in the DB
from sqlalchemy import text

# Fetch existing emails from DB
with engine.connect() as conn:
    result = conn.execute(text("SELECT email FROM customer_support.users"))
    existing_emails = set([row[0] for row in result])

# Filter out rows already in DB
user_df = user_df[~user_df['email'].isin(existing_emails)]
customer_df = customer_df[customer_df["user_id"].isin(user_df["user_id"])]

user_df.to_sql("users", con=engine, schema="customer_support", if_exists="append", index=False)
customer_df.to_sql("customers", con=engine, schema="customer_support", if_exists="append", index=False)

print("✅ Inserted first 300 rows into `users` and `customers` tables successfully.")
