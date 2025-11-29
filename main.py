import streamlit as st

def streamlit_app():
  pages = st.navigation([
    st.Page("home.py", title="Home"),
    st.Page("about.py", title="About"),
    st.Page("help.py", title="Help")
  ])

  pages.run()

if __name__ == "__main__":
  streamlit_app()
