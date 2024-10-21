import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

logout_page = st.Page("logout_page.py", title="Logout", icon=":material/logout:")
data_page = st.Page("data_center.py", title="Data Center")
login_page = st.Page("login_page.py", title="Login", icon=":material/login:")

if st.session_state.logged_in: 
    pg = st.navigation(
        {
            "User": [logout_page],
            "Tools": [data_page]
        }
    )
else:
    pg = st.navigation(
        {"User": [login_page]})
pg.run()