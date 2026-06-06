import warnings
warnings.filterwarnings("ignore")


import pandas as pd
import mysql.connector

# CSV Read
import pandas as pd

df = pd.read_csv("sales_data_500_records_2025.csv")

print(df.head())

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt

# ==========================
# MYSQL CONNECTION
# ==========================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="product_db"
)

# Read Data from MySQL
df = pd.read_sql("SELECT * FROM sales", conn)

# ==========================
# DATA PREPARATION
# ==========================

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.strftime('%b')

df['quantity'] = pd.to_numeric(df['quantity'])
df['price'] = pd.to_numeric(df['price'])

df['total_sales'] = df['quantity'] * df['price']

# ==========================
# SALES REPORT
# ==========================

total_revenue = np.sum(df['total_sales'])
avg_sales = np.mean(df['total_sales'])
max_sale = np.max(df['total_sales'])

print("\n===== SALES REPORT =====")
print("Total Revenue :", total_revenue)
print("Average Sale  :", avg_sales)
print("Highest Sale  :", max_sale)

# ==========================
# PRODUCT SALES
# ==========================

product_sales = df.groupby('product')['total_sales'].sum()

# ==========================
# MONTH WISE PRODUCT SALES
# ==========================

monthly_product_sales = df.pivot_table(
    values='total_sales',
    index='month',
    columns='product',
    aggfunc='sum',
    fill_value=0
)

months_order = [
    'Jan','Feb','Mar','Apr','May','Jun',
    'Jul','Aug','Sep','Oct','Nov','Dec'
]

monthly_product_sales = monthly_product_sales.reindex(months_order)

# ==========================
# DASHBOARD
# ==========================

fig, axs = plt.subplots(2, 2, figsize=(18, 10))

# --------------------------------
# Chart 1 - Product Wise Sales
# --------------------------------

colors = [
    'red','blue','green',
    'orange','purple',
    'brown','pink'
]

axs[0,0].bar(
    product_sales.index,
    product_sales.values,
    color=colors
)

axs[0,0].set_title("Product Wise Sales")
axs[0,0].set_xlabel("Product")
axs[0,0].set_ylabel("Revenue")
axs[0,0].tick_params(axis='x', rotation=45)

# --------------------------------
# Chart 2 - Month Wise Product Sales
# --------------------------------

monthly_product_sales.plot(
    kind='bar',
    ax=axs[0,1],
    colormap='tab10'
)

axs[0,1].set_title("Month Wise Product Sales")
axs[0,1].set_xlabel("Month")
axs[0,1].set_ylabel("Revenue")

# --------------------------------
# Chart 3 - Top 4 Highest Products
# --------------------------------

top4_products = product_sales.nlargest(4)

for product in top4_products.index:

    pdata = df[df['product'] == product]

    monthly_sales = pdata.groupby('month')['total_sales'].sum()

    axs[1,0].plot(
        monthly_sales.index,
        monthly_sales.values,
        marker='o',
        linewidth=2,
        label=product
    )

axs[1,0].set_title("Top 4 Highest Sales Products")
axs[1,0].set_xlabel("Month")
axs[1,0].set_ylabel("Revenue")
axs[1,0].legend()
axs[1,0].grid(True)

# --------------------------------
# Chart 4 - Lowest 5 Products
# --------------------------------

lowest_products = product_sales.nsmallest(5)

axs[1,1].plot(
    lowest_products.index,
    lowest_products.values,
    marker='o',
    color='red',
    linewidth=3
)

for x, y in zip(
    lowest_products.index,
    lowest_products.values
):
    axs[1,1].text(x, y, f'₹{int(y)}')

axs[1,1].set_title("Lowest 5 Sales Products")
axs[1,1].set_xlabel("Product")
axs[1,1].set_ylabel("Revenue")
axs[1,1].grid(True)

# ==========================
# DASHBOARD TITLE
# ==========================

fig.suptitle(
    "SALES ANALYSIS DASHBOARD",
    fontsize=20,
    fontweight='bold'
)

plt.tight_layout()
plt.show()

conn.close()
