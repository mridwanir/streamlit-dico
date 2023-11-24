import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)

    return daily_orders_df
def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_bycity_df(df):
    bystate_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df
orders_df = pd.read_csv("/workspaces/streamlit-dico/Data/orders_dataset.csv")
customers_df = pd.read_csv("/workspaces/streamlit-dico/Data/customers_dataset.csv")
product_df = pd.read_csv("/workspaces/streamlit-dico/top_product.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
orders_df.sort_values(by="order_purchase_timestamp", inplace=True)
orders_df.reset_index(inplace=True)
 
for column in datetime_columns:
    orders_df[column] = pd.to_datetime(orders_df[column])

min_date = orders_df["order_purchase_timestamp"].min()
max_date = orders_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = orders_df[(orders_df["order_purchase_timestamp"] >= str(start_date)) & 
                (orders_df["order_purchase_timestamp"] <= str(end_date))]
daily_orders_df = create_daily_orders_df(main_df)

sum_top_product = product_df.groupby("product_category_name").order_id.nunique().sort_values(ascending=False).reset_index()
sum_top_product.head(15)
by_city = customers_df.groupby(by="customer_city").customer_id.nunique().reset_index()
by_city.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)

# bystate_df = create_bystate_df(main_df)
st.header('E Commerce Dashboard :sparkles:')
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
# with col2:
    # total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    # st.metric("Total Revenue RP. .............")
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.subheader("Best & Worst Performing Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order_id", y="product_category_name", data=sum_top_product.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_id", y="product_category_name", data=sum_top_product.sort_values(by="order_id", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)
st.subheader("Customer Demographics") 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="customer_city",
    data=by_city.sort_values(by="customer_count", ascending=False).head(10),
    palette=colors,
    ax=ax
)
ax.set_title("Top 10 City by Customer", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)