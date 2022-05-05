import streamlit as st
st.set_page_config(
    page_title="Validate Submissions",
    layout="wide",
    initial_sidebar_state="expanded"
)

from tally_selector import MultiApp
from verify import multiple, overage

app = MultiApp()

st.markdown("""
# Election 2022 
# Verify Watcher Submissions
""")

# Add all your application here
app.add_app("Multiple Submissions", multiple.app)
app.add_app("Over-counting", overage.app)

# The main app
app.run()
