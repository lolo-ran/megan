

import streamlit as st

st.title("Megan Project App")

def logout():
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

logout()