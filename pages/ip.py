# pages/home.py
import streamlit as st

def show_ip():
    st.markdown("""
        <style>
                .stApp {
            background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1129");
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
                }

        
                
        </style>
    """, unsafe_allow_html=True)
    st.title("IP⌛")
    st.write("Coming Soon")
