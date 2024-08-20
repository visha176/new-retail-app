import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO

def create_sample_file():
    # Creating a sample DataFrame with the required headers
    sample_data = {
        'Zone': ['Zone1', 'Zone2'],
        'DESIGN': ['Design1', 'Design2'],
        'STORE_NAME': ['Store1', 'Store2'],
        '1st Rcv Date': [datetime(2023, 1, 1), datetime(2023, 2, 1)],
        'UPC/Barcode/SKU':[1223456,345678],
        'Shop Rcv Qty': [100, 150],
        'Disp. Qty': [10, 20],
        'O.H Qty': [90, 130],
        'Sold Qty': [50, 80],
        'Color':['Red','Blue'],
        'Size':['Small','Medium'],
        'Class':['Casual','Fancy'],
        'SubClass':['Lawn','Chiffon']
    }
    sample_df = pd.DataFrame(sample_data)

    # Converting DataFrame to an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        sample_df.to_excel(writer, index=False, sheet_name='Sample Data')
    processed_data = output.getvalue()
    return processed_data

def load_data(file):
    return pd.read_excel(file)

def adjust_date(df, threshold_date):
    threshold_timestamp = pd.Timestamp(threshold_date)
    
    # 1. Explicitly create a copy of the DataFrame to avoid SettingWithCopyWarning
    df = df.copy()

    df['1st Rcv Date'] = pd.to_datetime(df['1st Rcv Date'], errors='coerce')
    df = df.dropna(subset=['1st Rcv Date'])  # Remove rows where date conversion failed
    
    # 2. Use .loc to ensure you're modifying the DataFrame in place
    df.loc[:, 'Adjusted 1st Rcv Date'] = np.where(df['1st Rcv Date'] <= threshold_timestamp, 
                                                  threshold_timestamp, 
                                                  df['1st Rcv Date'])
    df.loc[:, 'Adjusted 1st Rcv Date'] = pd.to_datetime(df['Adjusted 1st Rcv Date'], errors='coerce')
    
    return df

def aggregate_data(df, threshold_date):
    df = adjust_date(df, threshold_date)
    return df.groupby(['UPC/Barcode/SKU','Zone','STORE_NAME','DESIGN','Adjusted 1st Rcv Date','Class','SubClass','Size','Color']).agg({
        'Shop Rcv Qty': 'sum',
        'Disp. Qty': 'sum',
        'O.H Qty': 'sum',
        'Sold Qty': 'sum'
    }).reset_index()

def calculate_sell_through(desired_df):
    sell_through = (desired_df['Sold Qty'] / (desired_df['Shop Rcv Qty'] - desired_df['Disp. Qty']) * 100)
    sell_through = sell_through.replace([np.inf, -np.inf, np.nan], 0)
    desired_df['shop Sell Through'] = sell_through.astype(int)
    return desired_df

def calculate_days(df):
    current_date = datetime.now()
    df['Days'] = (current_date - df['Adjusted 1st Rcv Date']).dt.days
    return df

def calculate_design_sell_through(df):
    df['Net Receiving'] = df['Shop Rcv Qty'] - df['Disp. Qty']
    design_totals = df.groupby('DESIGN').agg({'Sold Qty': 'sum', 'Net Receiving': 'sum'}).reset_index()
    design_totals['design Sell Through'] = (design_totals['Sold Qty'] / design_totals['Net Receiving'] * 100)
    design_totals['design Sell Through'] = design_totals['design Sell Through'].replace([np.inf, -np.inf, np.nan], 0).astype(int)
    return design_totals

def merge_data(desired_df, design_totals):
    return pd.merge(desired_df, design_totals[['DESIGN', 'design Sell Through']], on='DESIGN', how='left')

def apply_status_condition(desired_df):
    desired_df['Status'] = 'Low'
    desired_df.loc[desired_df['shop Sell Through'] > desired_df['design Sell Through'], 'Status'] = 'High'
    return desired_df

def process_data(desired_df):
    article_days = desired_df.groupby('DESIGN')['Days'].max().reset_index()
    merged_df = pd.merge(desired_df, article_days, on='DESIGN', how='left', suffixes=('', '_max_days'))
    merged_df_grouped = merged_df.groupby('DESIGN').agg({
        'O.H Qty': 'sum',
        'Sold Qty': 'sum',
        'Days': 'max'
    }).reset_index()
    result_df = merged_df_grouped[['DESIGN', 'Days']].rename(columns={'Days': 'Date Difference'})
    return result_df

def process_and_calculate_cover(df, article_days):
    merged_df = pd.merge(df, article_days, on='DESIGN', how='left', suffixes=('', '_max_days'))
    merged_df_grouped = merged_df.groupby('DESIGN').agg({
        'O.H Qty': 'sum',
        'Sold Qty': 'sum',
        'Days': 'max'
    }).reset_index()
    result_df = merged_df_grouped[['DESIGN', 'Days']].rename(columns={'Days': 'Date Difference'})
    merged_df_grouped = pd.merge(merged_df_grouped, result_df, on='DESIGN', how='left')
    merged_df_grouped['desired_cover'] = merged_df_grouped['O.H Qty'] / (merged_df_grouped['Sold Qty'] / merged_df_grouped['Date Difference'])
    return merged_df_grouped

def merge_with_desired_cover(desired_df, merged_df_grouped):
    desired_df = pd.merge(desired_df, merged_df_grouped[['DESIGN', 'desired_cover']], on='DESIGN', how='left')
    desired_df['desired_cover'] = desired_df['desired_cover'].fillna(0).replace([np.inf, -np.inf], 0).astype(int)
    return desired_df

def calculate_article_days(df):
    df['Adjusted 1st Rcv Date'] = pd.to_datetime(df['Adjusted 1st Rcv Date'], errors='coerce')
    df = df.dropna(subset=['Adjusted 1st Rcv Date'])
    today = pd.Timestamp.now().normalize()
    df['Design_Days'] = (today - df['Adjusted 1st Rcv Date']).dt.days
    article_days = df.groupby('DESIGN')['Design_Days'].max().reset_index()
    return article_days

def calculate_required_cover(desired_df):
    desired_df['Transfer in/out'] = desired_df['desired_cover'] * (desired_df['Sold Qty'] / desired_df['Days']) - desired_df['O.H Qty']
    desired_df['Transfer in/out'] = desired_df['Transfer in/out'].replace([np.inf, -np.inf, np.nan], 0).astype(int)
    return desired_df

def merge_desired_with_article_days(desired_df, article_days):
    desired_df = pd.merge(desired_df, article_days, on='DESIGN', how='left')
    return desired_df

def filter_data(desired_df, sell_through_threshold, days_threshold):
    filtered_df = desired_df[(desired_df['design Sell Through'] > sell_through_threshold) & (desired_df['Design_Days'] > days_threshold)]
    return filtered_df

def process_transfer_details(filtered_df):
    transfer_details = []

    # Sending stores: Transfer out (negative values)
    sending_stores = filtered_df[filtered_df['Transfer in/out'] < 0]
    # Receiving stores: Transfer in (positive values)
    receiving_stores = filtered_df[filtered_df['Transfer in/out'] > 0]

    # Iterate over sending stores
    for sending_index, sending_row in sending_stores.iterrows():
        excess_quantity = abs(sending_row['Transfer in/out'])
        upc = sending_row['UPC/Barcode/SKU']
        from_store = sending_row['STORE_NAME']
        from_zone = sending_row['Zone']  # Zone of the sending store
        design = sending_row['DESIGN']
        
        # Find matching receiving stores based on UPC, DESIGN, Zone, and excluding the same store
        matches = receiving_stores[
            (receiving_stores['UPC/Barcode/SKU'] == upc) &
            (receiving_stores['DESIGN'] == design) &
            (receiving_stores['STORE_NAME'] != from_store) &
            (receiving_stores['Zone'] == from_zone) &  # Ensure same Zone
            (receiving_stores['Transfer in/out'] > 0)
        ]

        for receiving_index, receiving_row in matches.iterrows():
            if excess_quantity <= 0:
                break

            # Calculate the amount to transfer
            transfer_qty = min(excess_quantity, receiving_row['Transfer in/out'])
            
            # Record the transfer details
            transfer_details.append({
                'UPC/Barcode/SKU': upc,
                'From Store': from_store,
                'To Store': receiving_row['STORE_NAME'],
                'Zone': from_zone,  # Added Zone
                'DESIGN': design,
                'Size': sending_row['Size'],
                'Color': sending_row['Color'],
                'Class': sending_row['Class'],
                'SubClass': sending_row['SubClass'],
                'Quantity Transferred': transfer_qty
            })

            # Update the quantities
            excess_quantity -= transfer_qty
            receiving_stores.at[receiving_index, 'Transfer in/out'] -= transfer_qty
            sending_stores.at[sending_index, 'Transfer in/out'] += transfer_qty

        # Update filtered_df after processing all receiving stores for the current sending store
        filtered_df.update(sending_stores)
        filtered_df.update(receiving_stores)

    # Convert transfer details into a DataFrame
    transfer_df = pd.DataFrame(transfer_details)
    return transfer_df



def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

def show_regional():
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
    color: inherit;
    width: auto;
    user-select: none;
    background-color: rgb(70 87 169);
    border: 1px solid rgba(49, 51, 63, 0.2);
}
                .st-emotion-cache-144mis {
  
    display: none;
}
                }

        
                
        </style>
    """, unsafe_allow_html=True)
    st.title('Network🌐')

    # Download sample file
   
    # Download sample file
    sample_file = create_sample_file()
    st.download_button(
        label="Download Sample Excel File",
        data=sample_file,
        file_name='sample_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])

    if uploaded_file is not None:
        threshold_date = st.date_input("Season Launch Date", min_value=datetime(2020, 1, 1), value=datetime.now())
        sell_through_threshold = st.number_input("Enter Sell-Through Threshold (%)", min_value=0, max_value=100, value=60)
        days_threshold = st.number_input("Enter Minimum Age", min_value=0, max_value=100, value=30)

        if st.button("Process Data"):
            with st.spinner('Processing data, please wait...'):
                data = load_data(uploaded_file)
                adjusted_data = adjust_date(data, threshold_date)
                aggregated_data = aggregate_data(adjusted_data, threshold_date)
                sell_through_data = calculate_sell_through(aggregated_data)
                days_data = calculate_days(sell_through_data)
                design_sell_through_data = calculate_design_sell_through(days_data)
                merged_data = merge_data(days_data, design_sell_through_data)
                status_data = apply_status_condition(merged_data)
                processed_data = process_data(status_data)
                cover_data = process_and_calculate_cover(status_data, processed_data)
                cover_merged_data = merge_with_desired_cover(status_data, cover_data)
                article_days = calculate_article_days(cover_merged_data)
                required_cover_data = calculate_required_cover(cover_merged_data)
                final_data = merge_desired_with_article_days(required_cover_data, article_days)
                filtered_data = filter_data(final_data, sell_through_threshold, days_threshold)
                transfer_details = process_transfer_details(filtered_data)

                st.session_state.filtered_data = filtered_data
                st.session_state.transfer_details = transfer_details

                st.dataframe(filtered_data)

    if 'filtered_data' in st.session_state and 'transfer_details' in st.session_state:
        processed_data_excel = to_excel(st.session_state.filtered_data)
        transfer_data_excel = to_excel(st.session_state.transfer_details)

        st.download_button(
            label="Download Processed Data",
            data=processed_data_excel,
            file_name="processed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.download_button(
            label="Download Transfer Details",
            data=transfer_data_excel,
            file_name="transfer_details.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
if __name__ == "__main__":
    show_regional()
