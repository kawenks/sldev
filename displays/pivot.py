import streamlit as st
import pandas as pd
import numpy as np
import pymongo
import gridfs
import tools
import numpy
   
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()
db = client.pollwatcher
fs = gridfs.GridFS(db)

def app():

    st.subheader('Presidential Tally by Province')
    raw_df = tools.get_rawdata(db,'view_rawdata_president')
    pres_pv = pd.pivot_table(raw_df, values='Votes', index=['Province'], columns='Candidate', aggfunc=np.sum)
    st.table(pres_pv)

    with st.expander('Presidential Tally by Municipality'):
        pres_muni = pd.pivot_table(raw_df, values='Votes', index=['Province','Municipality'], columns='Candidate', aggfunc=np.sum )
        st.table(pres_muni)

    with st.expander('Presidential Tally by Barangay'):
        pres_bgy = pd.pivot_table(raw_df, values='Votes', index=['Province','Municipality', 'Barangay'], columns='Candidate', aggfunc=np.sum )
        st.table(pres_bgy)

    st.subheader('Presidential Tally by Province')
    raw_df_vp  = tools.get_rawdata(db,'view_rawdata_vicepresident')
    vpres_pv = pd.pivot_table(raw_df_vp, values='Votes', index=['Province'], columns='Candidate', aggfunc=np.sum)
    st.table(vpres_pv)

    with st.expander('Vice-Presidential Tally by Municipality'):
        vpres_muni = pd.pivot_table(raw_df_vp, values='Votes', index=['Province','Municipality'], columns='Candidate', aggfunc=np.sum )
        st.table(vpres_muni)

    with st.expander('Vice-Presidential Tally by Barangay'):
        vpres_bgy = pd.pivot_table(raw_df_vp, values='Votes', index=['Province','Municipality', 'Barangay'], columns='Candidate', aggfunc=np.sum )
        st.table(vpres_bgy)
