import streamlit as st
import pandas as pd
import numpy as np
import io

def create_sample_file(file_type):
    if file_type == "shop":
        sample_data = {
            'STORE_NAME': ['Store1', 'Store2'],
            'UPC': ['1234567890', '0987654321'],
            'Shop Rcv Qty': [100, 200],
            'Disp. Qty': [10, 20],
            'Sold Qty': [50, 150],
            'DESIGN': ['Design1', 'Design2'],
            'Color':['Red','Blue'],
            'Size':['Small','Medium'],
            'Class':['Casual','Fancy'],
            'SubClass':['Lawn','Chiffon']
        }
    elif file_type == "warehouse":
        sample_data = {
            'UPC': ['1234567890', '0987654321'],
            'QTY': [300, 400]
        }

    sample_df = pd.DataFrame(sample_data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        sample_df.to_excel(writer, index=False, sheet_name='Sample Data')
        writer.close()  # Close the writer
    output.seek(0)

    return output

def process_data(file1, file2, threshold):
    df = pd.read_excel(file1)
    new_df = pd.read_excel(file2)

    df['Shop Rcv Qty'] = pd.to_numeric(df['Shop Rcv Qty'], errors='coerce')
    df['Disp. Qty'] = pd.to_numeric(df['Disp. Qty'], errors='coerce')
    df['Net Rcv'] = df['Shop Rcv Qty'] - df['Disp. Qty']
    df['Sold Qty'] = pd.to_numeric(df['Sold Qty'], errors='coerce')

    df['Sell Through Rate (%)'] = ((df['Sold Qty'] / df['Net Rcv']) * 100).round(0)
    df['Sell Through Rate (%)'].replace([float('inf'), float('-inf'), np.nan], 0, inplace=True)

    df['UPC Sell Through Rate (%)'] = df.groupby('UPC')['Sold Qty'].transform('sum') / df.groupby('UPC')['Net Rcv'].transform('sum') * 100
    df['UPC Sell Through Rate (%)'].replace([float('inf'), float('-inf'), np.nan], 0, inplace=True)
    df['UPC Sell Through Rate (%)'] = df['UPC Sell Through Rate (%)'].round(0)

    df['Status'] = np.where(df['Sell Through Rate (%)'] > threshold, 'High', 'Low')

    pivot_table = df.pivot_table(values=['Net Rcv', 'Sold Qty', 'Sell Through Rate (%)', 'UPC Sell Through Rate (%)', 'Status'], 
                                 index=['STORE_NAME', 'UPC'], 
                                 aggfunc={'Net Rcv': 'sum', 'Sold Qty': 'sum', 'Sell Through Rate (%)': 'first', 
                                          'UPC Sell Through Rate (%)': 'first', 'Status': 'first'})

    pivot_table['Transfer Qty'] = 0

    high_priority_stores = pivot_table[pivot_table['Status'] == 'High'].copy()
    high_priority_stores.sort_values(['Sell Through Rate (%)', 'UPC Sell Through Rate (%)'], ascending=[False, False], inplace=True)

    for index, row in new_df.iterrows():
        upc = row['UPC']
        qty_to_distribute = row['QTY']

        eligible_stores = high_priority_stores.loc[high_priority_stores.index.get_level_values('UPC') == upc]

        for store_index, store_row in eligible_stores.iterrows():
            if qty_to_distribute <= 0:
                break

            if store_row['Sold Qty'] < 0:
                additional_transfer = 0
            else:
                max_transferable = min(store_row['Sold Qty'], qty_to_distribute)
                current_transfer = pivot_table.loc[store_index, 'Transfer Qty']
                additional_transfer = min(max_transferable, store_row['Sold Qty'] - current_transfer)

            pivot_table.loc[store_index, 'Transfer Qty'] += additional_transfer
            qty_to_distribute -= additional_transfer

    return pivot_table.reset_index()

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
    color: inherit;
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
                }

        
                
        </style>
    """, unsafe_allow_html=True)
    st.title('Assortment✍')
    
    # Provide the sample files for download
    shop_sample_file = create_sample_file("shop")
    warehouse_sample_file = create_sample_file("warehouse")
    
    st.download_button(label="Download Shop Sample File", data=shop_sample_file, file_name='shop_sample_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.download_button(label="Download Warehouse Sample File", data=warehouse_sample_file, file_name='warehouse_sample_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    
    # File upload and processing section
    st.markdown("### Upload Files for Processing")
    file1 = st.file_uploader("Upload the shop Excel file", type=["xlsx"])
    file2 = st.file_uploader("Upload the warehouse Excel file", type=["xlsx"])
    threshold = st.number_input("Set Sell-Through Threshold (%)", min_value=0, max_value=100, value=50, step=1)
    
    if file1 is not None and file2 is not None and st.button("Process Data"):
        result = process_data(file1, file2, threshold)
        st.success("Data processed successfully!")
        st.dataframe(result)
        st.download_button(label="Download Result", data=result.to_csv(index=False), file_name='result.csv', mime='text/csv')
    elif st.button("Process Data"):
        st.error("Please upload both files to proceed.")

if __name__ == "__main__":
    show_assortment()
