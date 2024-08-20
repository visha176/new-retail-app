import streamlit as st

# Dummy user credentials
USER_CREDENTIALS = {'admin': 'password'}

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    remember_me = st.checkbox("Remember me")
    
    if st.button("Login"):
        if USER_CREDENTIALS.get(username) == password:
            st.session_state['logged_in'] = True
            st.rerun()  # Rerun to switch to the main content page
        else:
            st.error("Invalid username or password")

def show_login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Apply custom CSS for layout and spacing
    st.markdown("""
        <style>
                .stApp {
            background-image: url("https://img.freepik.com/free-vector/geometric-gradient-futuristic-background_23-2149116406.jpg?t=st=1723646938~exp=1723650538~hmac=e0f0a12b66db401ec6a336cc207a282f9641e218d274591c71dba1910c5c6769&w=996");
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
                h1 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 700;
    color: rgb(255 255 255);
    padding: 1.25rem 0px 1rem;
    margin: 0px;
    line-height: 1.2;
}
                h2 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(255 255 255);
    letter-spacing: -0.005em;
    padding: 1rem 0px;
    margin: 0px;
    line-height: 1.2;
}
                .st-emotion-cache-1whx7iy p {
    margin-bottom: auto;
    font-size: 19px;
    font-family: 'Source Sans Pro';
    color: 'white';
}
                .st-emotion-cache-1vt4y43 {
                background-color: rgb(31 55 154);
    border: 1px solid rgba(49, 51, 63, 0.2);
}
                
        </style>
    """, unsafe_allow_html=True)

    # Create a layout with three columns
    col1, col2, col3 = st.columns([1, 0.5, 1])  # Adjust column widths as needed

    with col1:
        if not st.session_state['logged_in']:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            login_page()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("You are already logged in.")

    with col2:
        # This column is left empty to create a gap
        st.markdown('<div class="gap"></div>', unsafe_allow_html=True)

    with col3:
        # Display the welcome message
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
        st.header("Welcome")
        st.write("Welcome to the Internal Store Transfer and Assortment Management App!")
        st.write("Upload your Excel file to manage assortments and streamline internal store transfers.")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_login()
