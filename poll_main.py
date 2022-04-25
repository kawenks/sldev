import streamlit as st
from tally_selector import MultiApp
from displays import president, vicepresident, senators # import your app modules here

app = MultiApp()

st.markdown("""
# Election 2022 
# Unofficial Quick-Count

This site displays aggregated results of ***independently recorded (i.e. unofficial) precinct tallies***.

""")

# Add all your application here
app.add_app("President", president.app)
app.add_app("Vice President", vicepresident.app)
app.add_app("Senators", senators.app)

# The main app
app.run()
