import streamlit as st

# Dummy user credentials for multiple users
USER_CREDENTIALS = {
    'admin@rpt.com': 'retail_123',
    'Walkeaze@rpt.com': 'Walkeaze@_123',
    'Urban_sole@rpt.com': '4',
    'HP@rpt.com': '8',
    'Bata@rpt.com': 'n',
    'OutFitter@rpt.com': 'OutFitter978',
    'DynastyApparel@rpt.com': '4',
    'Orient@rpt.com': 'orient@_321',
    
}

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
            background-image: url("https://images.unsplash.com/photo-1526666923127-b2970f64b422?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
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
.st-emotion-cache-187vdiz p {
    word-break: break-word;
    margin-bottom: 0px;
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
