import streamlit as st
import numpy as np

def show_home():
    st.markdown("""
        <style>
                .stApp {
            background-image: url("https://emc2rrspvpp.exactdn.com/wp-content/themes/centricSoftware/img/correct-glow.jpg");
            background-size: cover;
            color:white;
        }
            .st-emotion-cache-ocqkz7 {
                display: flex;
                flex-wrap: wrap;
                -webkit-box-flex: 1;
                flex-grow: 1;
                -webkit-box-align: stretch;
                align-items: stretch;
                gap: 1rem;
                margin-left: -25rem;
                width: 1600px;
                padding:100px;
            }
                div.stButton > button:first-child {
background-color: #4040b7;color:white;font-size:20px;height:3em;width:10em;border-radius:10px 10px 10px 10px;
}

          
.st-emotion-cache-j5r0tf{
background-color: #5c5c6052;
    height: 300px}
.st-emotion-cache-bjh2tb {
    width: 1900px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    /* gap: 0rem; */
    background-color: black;
    height: 1900px;
    margin-left: -12rem;
}
                .st-emotion-cache-1gzyl8x {
    /* width: 200px; */
    position: relative;
    height: 362px;
    padding: 0 100px;
    /* margin-top: 10rem; */
    /* margin-bottom: 10rem; */
}
}

        
                
        </style>
    """, unsafe_allow_html=True)

    # Columns to divide the layout into three parts with larger gaps
    col1, col2, col3 = st.columns([2, 1, 1])  # Equal width columns

     # Content in the first column (left)
    with col1:
        st.markdown('<h1 style="color: white;">Choose Your Industry</h1>', unsafe_allow_html=True)
        st.write("Content specific to choosing industry goes here.")
        if st.button('Explore Industries'):
            st.session_state['current_page'] = 'Contact'  # Set session state to 'Contact'
            st.rerun()  # Rerun the app to switch pages

    # Adding larger gap between columns
    st.write("")  # Empty string for spacing

    # Content in the second column (middle)
    with col2:
        st.image('kl.png', use_column_width=True)
        

    # Adding larger gap between columns
    st.write("")  # Empty string for spacing

    # Content in the third column (right)
    with col3:
        st.write("- Increase efficiencies")
        st.write("- Drive sales")
        st.write("- Maximize margins")
        st.write("- Reduce inventories")
        st.write("- Enable sustainability")

    # Adding more space after the columns
    st.write("")  # Empty string for additional spacing

    # Second set of columns with images
    col4, col5, col6 = st.columns(3)

    with col4:
        st.image("https://emc2rrspvpp.exactdn.com/wp-content/uploads/2022/02/Resource-1.jpg?lossy=1&quality=92&webp=92&ssl=1", use_column_width=True)

    with col5:
        st.image("https://emc2rrspvpp.exactdn.com/wp-content/uploads/2022/03/Resource-2.jpg?lossy=1&quality=92&webp=92&ssl=1", use_column_width=True)

    with col6:
        st.image("https://emc2rrspvpp.exactdn.com/wp-content/uploads/2024/01/2023-CMI-in-review.jpg?lossy=1&quality=92&webp=92&ssl=1", use_column_width=True)

    # Adding space before final message
    st.write("")  # Empty string for spacing

    # Displaying the final message in two centered lines
    st.markdown('<h2 style="color: white;">Analyze market demand and competitors.</h2>', unsafe_allow_html=True)

    st.markdown("<p style='text-align: center;'>Streamline processes, reduce costs, maximize profitability and drive sustainability with a flexible and scalable digital foundation for growth.</p>", unsafe_allow_html=True)

   

    # Creating columns for each section
    col7, col8, col9, col10, col11 = st.columns(5)

    with col7:
        st.markdown('<h3 style="color: white; text-align: center;">Internal Store Transfers</h3>', unsafe_allow_html=True)
        st.write("""
    <div style="text-align: center;">
        Optimize internal transfers to ensure timely and efficient movement of stock between stores, improving availability and reducing overstock situations.
    </div>
    """, unsafe_allow_html=True)

    with col8:
        st.markdown('<h3 style="color: white;text-align: center;">Assortment Planning</h3>', unsafe_allow_html=True)
        st.write("""
    <div style="text-align: center;">
        Develop and execute strategic assortment plans to meet consumer demand, enhance product mix, and maximize sales opportunities.
    </div>
    """, unsafe_allow_html=True)


    with col9:
        st.markdown('<h3 style="color: white;text-align: center;">Replenishment Management</h3>', unsafe_allow_html=True)

        st.write("""
    <div style="text-align: center;">
        Automate replenishment processes to maintain optimal inventory levels, reduce stockouts, and ensure product availability across all locations.
    </div>
    """, unsafe_allow_html=True)

    with col10:
        st.markdown('<h3 style="color: white;text-align: center;">Inventory Optimization</h3>', unsafe_allow_html=True)
        st.write("""
    <div style="text-align: center;">
        Implement advanced inventory management techniques to balance stock levels, minimize holding costs, and increase overall efficiency.
    </div>
    """, unsafe_allow_html=True)


    with col11:
        st.markdown('<h3 style="color: white;text-align: center;">Inventory Management</h3>', unsafe_allow_html=True)
        st.write("""
    <div style="text-align: center;">
        Utilize comprehensive inventory management solutions to track, manage, and control stock levels, ensuring accurate and up-to-date inventory information.
    </div>
    """, unsafe_allow_html=True)
     
    col12, col13 = st.columns(2)

    with col12:
        st.markdown('<h3 style="color: white;text-align: center;">Inventory Management</h3>', unsafe_allow_html=True)
        st.write("Centric scalable, easy to use, AI-driven, best-of-breed solutions enable teams to plan, execute and price consumer-centric assortments that also meet sustainability and compliance goals.Collaboration is easy and innovation, possible. Leaving you to focus on what you do best: bringing the products to market that your customers want")
        
    with col13:
        st.image('pl.png', use_column_width=True)


   
if __name__ == "__main__":
    show_home()
