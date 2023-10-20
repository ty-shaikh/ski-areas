import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome to the Ski Area Dashboard!")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This dashboard allows you to find ski areas either by different
    mountain characteristics like vertical descent and annual snowfall or
    distance from your current location.

    **👈 Select a page from the sidebar** to find your ideal ski area!
"""
)
