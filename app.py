import streamlit as st
from streamlit_navigation_bar import st_navbar

import pages.assortment as assortment
import pages.home as home
import pages.ip as ip
import pages.Network as network
import pages.regional as regional
import pages.city as city
import pages.contact as contact
import pages.login as login  # Import the updated login module

# Define the available pages with icons
all_pages = {
    "Home 🏠": home.show_home,
    "Contact 📞": contact.show_contact,
    "Assortment 🛒": assortment.show_assortment,
    "Internal Store Transfer📦": {
        "Network 🌐": network.show_Network,
        "City 🏙️": city.show_city,
        "Regional 🌍": regional.show_regional,
    },
    "IP 🔐": ip.show_ip,
    "Logout 🚪": None,  # Placeholder for logout option
}

initial_pages = {
    "Home 🏠": home.show_home,
    "Contact 📞": contact.show_contact,
    "Login 🔑": login.show_login,
}


# Custom styles for the navigation bar
styles = {
    "nav": {
        "background-color": "#000000",
        "font-family": "Arial, sans-serif",
        "font-size": "15px",
        "height": "90px",
        "display": "flex",
        "align-items": "center",
        "justify-content": "flex-end",
        "padding": "0 20px",
        "overflow": "hidden", 
    },
    "span": {
        "color": "#FFFFFF",
        "margin-left": "10px",  # Adjusted to make icons closer to text
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
    },
    "active": {
        "background-color": "#000000",
    },
    "hover": {
        "background-color": "#000000",
    },
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home 🏠"

# Function to handle login
def handle_login():
    st.session_state.logged_in = True

# Function to handle logout
def handle_logout():
    st.session_state.logged_in = False
    st.session_state.selected_page = "Home 🏠"
    st.rerun()

# Custom login function
def custom_login():
    login.show_login()  # Use the login page function from login.py

# Navigation bar logic
if st.session_state.logged_in:
    selected_page = st_navbar(list(all_pages.keys()), styles=styles, key="navbar_logged_in")
else:
    selected_page = st_navbar(list(initial_pages.keys()), styles=styles, key="navbar_initial")

# Handling Logout
if selected_page == "Logout 🚪":
    handle_logout()
elif st.session_state.logged_in:
    if selected_page == "Internal Store Transfer📦":
        # Show dropdown for IST pages
        selected_ist_sidebar = st.selectbox("Select a sub-page", list(all_pages["Internal Store Transfer📦"].keys()), key="ist_selectbox")
        if selected_ist_sidebar in all_pages["Internal Store Transfer📦"]:
            # Call the selected page function
            all_pages["Internal Store Transfer📦"][selected_ist_sidebar]()
        else:
            st.write("Page content not found.")
    else:
        if selected_page in all_pages:
            all_pages[selected_page]()
        else:
            st.write("Page content not found.")
else:
    if selected_page == "Login 🔑":
        custom_login()
    elif selected_page in initial_pages:
        initial_pages[selected_page]()
    else:
        st.write("Page content not found.")

# Apply custom styles and JavaScript to hide the sidebar and arrow
st.markdown("""
<style>
.st-emotion-cache-144mis {
    display: none;
}
div[data-testid="collapsedControl"] {
    left: 0.3125rem;
    top: calc((90px - 2rem) / 2);
    display: none;
}
           
</style>
""", unsafe_allow_html=True)
