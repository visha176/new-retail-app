import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import tempfile

# Define functions (same as before)

def adjust_date(df, threshold_date):
    def adjust_single_date(date):
        threshold_timestamp = pd.Timestamp(threshold_date)
        if date <= threshold_timestamp:
            return threshold_timestamp
        else:
            return date

    df['1st Rcv Date'] = pd.to_datetime(df['1st Rcv Date'])
    df['Adjusted 1st Rcv Date'] = df['1st Rcv Date'].apply(adjust_single_date)
    return df

def calculate_sell_through(df):
    sell_through = (df['Sold Qty'] / (df['O.H QTY'] + df['Sold Qty']) * 100)
    sell_through = sell_through.replace([np.inf, -np.inf, np.nan], 0)
    df['shop Sell Through'] = sell_through.astype(int)
    return df

def calculate_days(df):
    current_date = datetime.now()
    df['Shop Days'] = (current_date - df['Adjusted 1st Rcv Date']).dt.days
    return df

def calculate_design_sell_through(df):
    df['Net Receiving'] = df['O.H QTY'] + df['Sold Qty']
    design_totals = df.groupby('UPC/SKU/Barcode').agg({
        'Sold Qty': 'sum',
        'Net Receiving': 'sum'
    }).reset_index()
    design_totals['design Sell Through'] = (design_totals['Sold Qty'] / design_totals['Net Receiving'] * 100)
    design_totals['design Sell Through'] = design_totals['design Sell Through'].replace([np.inf, -np.inf, np.nan], 0).astype(int)
    return design_totals

def apply_status_condition(df):
    df['Status'] = 'Low'
    df.loc[df['shop Sell Through'] >= df['design Sell Through'], 'Status'] = 'High'
    return df

def calculate_article_days(df):
    df = df.copy()  # Create a copy of the DataFrame to avoid SettingWithCopyWarning
    df['Adjusted 1st Rcv Date'] = pd.to_datetime(df['Adjusted 1st Rcv Date'], errors='coerce')
    df = df.dropna(subset=['Adjusted 1st Rcv Date'])
    today = pd.Timestamp.now().normalize()
    df['Max Design Days'] = (today - df['Adjusted 1st Rcv Date']).dt.days
    article_days = df.groupby('UPC/SKU/Barcode')['Max Design Days'].max().reset_index()
    return article_days

def process_and_calculate_cover(df, article_days):
    merged_df = pd.merge(df, article_days, on='UPC/SKU/Barcode', how='left', suffixes=('', '_max_days'))
    merged_df_grouped = merged_df.groupby('UPC/SKU/Barcode').agg({
        'O.H QTY': 'sum',
        'Sold Qty': 'sum',
        'Shop Days': 'max'
    }).reset_index()
    merged_df_grouped['Targeted Cover'] = merged_df_grouped['O.H QTY'] / (merged_df_grouped['Sold Qty'] / merged_df_grouped['Shop Days'])
    return merged_df_grouped[['UPC/SKU/Barcode', 'Targeted Cover']]

def calculate_required_cover(df):
    df['Sold Qty'] = df['Sold Qty'].fillna(0)
    df['Transfer in/out'] = df['Targeted Cover'] * (df['Sold Qty'] / df['Shop Days']) - df['O.H QTY']
    df['Transfer in/out'] = df['Transfer in/out'].fillna(0)
    return df

def create_transfer_records(df):
    warehouse_df = df[df['STORE_NAME'] == 'Warehouse'].copy()
    store_df = df[(df['STORE_NAME'] != 'Warehouse') & (df['Transfer in/out'] > 0)].copy()
    transfer_records = []

    for warehouse_index, warehouse_row in warehouse_df.iterrows():
        excess_stock = warehouse_row['O.H QTY']
        
        if store_df.empty or excess_stock <= 0:
            continue
        
        relevant_store_df = store_df[store_df['UPC/SKU/Barcode'] == warehouse_row['UPC/SKU/Barcode']]
        
        for store_index, store_row in relevant_store_df.iterrows():
            if excess_stock <= 0:
                break
            
            store_need = store_row['Transfer in/out']
            store_sold_qty = store_row['Sold Qty']
            
            max_transfer_qty = min(store_need, store_sold_qty, excess_stock)
            
            if max_transfer_qty > 0:
                transfer_records.append({
                    'UPC/SKU/Barcode': warehouse_row['UPC/SKU/Barcode'],
                    'Sending Store': warehouse_row['STORE_NAME'],
                    'Receiving Store': store_row['STORE_NAME'],
                    'Transfer Qty': max_transfer_qty
                })
                
                excess_stock -= max_transfer_qty
                store_df.loc[store_index, 'Transfer in/out'] -= max_transfer_qty

                if store_df.loc[store_index, 'Transfer in/out'] <= 0:
                    store_df = store_df.drop(store_index)

        warehouse_df.loc[warehouse_index, 'O.H QTY'] = excess_stock
    
    transfer_df = pd.DataFrame(transfer_records)
    
    return transfer_df
def create_sample_files():
    # Sample data for the shop file
    shop_data = {
    'UPC/SKU/Barcode': ['12345', '67890'],
    'STORE_NAME': ['Shop1', 'Shop2'],
    'Shop Rcv Qty': [100, 150],
    'Disp. Qty': [10, 20],
    'O.H QTY': [50, 20],
    'Sold Qty': [20, 5],
    '1st Rcv Date': ['2024-01-01', '2024-02-01'],
    'Color':['Red','Blue'],
    'Size':['Small','Medium'],
    'Class':['Casual','Fancy'],
    'SubClass':['Lawn','Chiffon']
    }

    # Sample data for the warehouse file
    warehouse_data = {
        'UPC/SKU/Barcode': ['12345', '67890'],
        'STORE_NAME': ['Warehouse','Warehouse'],
        'O.H QTY': [100, 150]
    }

    # Create dataframes
    shop_df = pd.DataFrame(shop_data)
    warehouse_df = pd.DataFrame(warehouse_data)

    # Save the sample files to temporary paths
    shop_sample_file = tempfile.mktemp(suffix=".xlsx")
    warehouse_sample_file = tempfile.mktemp(suffix=".xlsx")

    shop_df.to_excel(shop_sample_file, index=False)
    warehouse_df.to_excel(warehouse_sample_file, index=False)

    return shop_sample_file, warehouse_sample_file

def show_assortment():
    st.markdown("""
        <style>
                .stApp {
            background-image: url("https://emc2rrspvpp.exactdn.com/wp-content/themes/centricSoftware/img/correct-glow.jpg");
            background-size: cover;
            color:white;
        }
                .st-emotion-cache-1vt4y43 {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    font-weight: 400;
    padding: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    min-height: 2.5rem;
    margin: 0px;
    line-height: 1.6;
    color: white;
    width: auto;
    user-select: none;
    background-color: rgb(70 87 169);
    border: 1px solid rgba(49, 51, 63, 0.2);
}
                h3 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(255 255 255);
    letter-spacing: -0.005em;
    padding: 0.5rem 0px 1rem;
    margin: 0px;
    line-height: 1.2;
}
                h1 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 700;
    color: rgb(252 252 255);
    padding: 1.25rem 0px 1rem;
    margin: 0px;
    line-height: 1.2;
}
                .st-emotion-cache-1whx7iy p {
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 14px;
    color: white;
}
                }

        
                
        </style>
    """, unsafe_allow_html=True)
    st.title('Replenishment✍')
     # Sample files download section
    shop_sample_file, warehouse_sample_file = create_sample_files()

    st.markdown("### Download Sample Files")
    with open(shop_sample_file, "rb") as shop_file:
        st.download_button(
            label="Download Sample Shop File",
            data=shop_file.read(),
            file_name="sample_shop_file.xlsx"
        )
    with open(warehouse_sample_file, "rb") as warehouse_file:
        st.download_button(
            label="Download Sample Warehouse File",
            data=warehouse_file.read(),
            file_name="sample_warehouse_file.xlsx"
        )
    uploaded_warehouse_file = st.file_uploader("Upload Warehouse File", type=["xlsx"])
    uploaded_shop_file = st.file_uploader("Upload Shop File", type=["xlsx"])

    threshold_date = st.date_input("Season Launch Date", value=datetime(2024, 2, 17))
    sell_through_threshold = st.number_input("Enter Sell-Through Threshold (%)", min_value=0, max_value=100, value=60)
    days_threshold = st.number_input("Enter Minimum Age", min_value=0, max_value=100, value=30)

    if 'combined_file_path' not in st.session_state:
        st.session_state.combined_file_path = None
    if 'transfer_file_path' not in st.session_state:
        st.session_state.transfer_file_path = None

    if uploaded_warehouse_file and uploaded_shop_file:
        if st.button('Start Processing'):
            with st.spinner('Processing data...'):
                warehouse_df = pd.read_excel(uploaded_warehouse_file)
                shop_df = pd.read_excel(uploaded_shop_file)

                # Adjust dates
                shop_df = adjust_date(shop_df, threshold_date)

                # Process and combine data
                warehouse_subset = warehouse_df[['UPC/SKU/Barcode', 'STORE_NAME', 'O.H QTY']]
                combined_df = pd.concat([shop_df, warehouse_subset], ignore_index=True)
                combined_df['Adjusted 1st Rcv Date'] = pd.to_datetime(combined_df['Adjusted 1st Rcv Date'], errors='coerce')
                shop_data = combined_df[combined_df['STORE_NAME'] != 'Warehouse']
                highest_dates = shop_data.groupby('UPC/SKU/Barcode')['Adjusted 1st Rcv Date'].max()
                default_date = pd.to_datetime('2024-02-17')
                combined_df.loc[
                    (combined_df['STORE_NAME'] == 'Warehouse') & (combined_df['Adjusted 1st Rcv Date'].isna()), 
                    'Adjusted 1st Rcv Date'
                ] = combined_df.loc[
                    (combined_df['STORE_NAME'] == 'Warehouse'), 
                    'UPC/SKU/Barcode'
                ].map(highest_dates).fillna(default_date)
                
                combined_df = calculate_sell_through(combined_df)
                combined_df = calculate_days(combined_df)
                design_sell_through = calculate_design_sell_through(combined_df)
                combined_df = pd.merge(combined_df, design_sell_through[['UPC/SKU/Barcode', 'design Sell Through']], on='UPC/SKU/Barcode', how='left')
                combined_df = apply_status_condition(combined_df)
                article_days = calculate_article_days(combined_df)
                targeted_cover_df = process_and_calculate_cover(combined_df, article_days)
                combined_df = pd.merge(combined_df, targeted_cover_df, on='UPC/SKU/Barcode', how='left')
                combined_df = calculate_required_cover(combined_df)
                transfer_df = create_transfer_records(combined_df)

                # Save files to temporary files
                st.session_state.combined_file_path = tempfile.mktemp(suffix=".xlsx")
                st.session_state.transfer_file_path = tempfile.mktemp(suffix=".xlsx")

                combined_df.drop(columns=['Net Receiving', '1st Rcv Date']).to_excel(st.session_state.combined_file_path, index=False)
                transfer_df.to_excel(st.session_state.transfer_file_path, index=False)

                st.success("Processing complete. You can now download the files.")

    if st.session_state.combined_file_path and st.session_state.transfer_file_path:
        with open(st.session_state.combined_file_path, "rb") as combined_file:
            st.download_button(
                label="Download Combined Data",
                data=combined_file.read(),
                file_name="combined_data.xlsx"
            )
        with open(st.session_state.transfer_file_path, "rb") as transfer_file:
            st.download_button(
                label="Download Transfer Details",
                data=transfer_file.read(),
                file_name="TRANSFER_data.xlsx"
            )

if __name__ == "__main__":
    show_assortment()
