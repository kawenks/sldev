import streamlit as st
import pandas as pd
import numpy as np
import pymongo
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import gridfs

STREAMLIT_AGGRID_URL = "https://github.com/PablocFonseca/streamlit-aggrid"

def aggrid_interactive_table(df: pd.DataFrame, HideCols=None):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    # hide columns if any
    if HideCols:
        for c in HideCols:
            options.configure_column(c,hide=True)

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="dark",
        pagination=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

@st.experimental_memo(ttl=300)
def get_tally(_db, view):
    df = pd.DataFrame(list(_db[view].find()))
    df = df.rename(columns={"_id":"Candidate","total_votes":"Votes"})
    return df

@st.experimental_memo(ttl=300)
def get_rawdata(_db, view, filter=None):
    df = pd.DataFrame(list(_db[view].find(filter)))
    return df

def get_photos(_fs, interview_key):
    images = []
    fn = []
    for i in _fs.find({'interview_key': interview_key}):
        if i.filename not in fn:
            images.append(i)
            fn.append(i.filename)

    return images

def get_one(_db, view, filter=None):
    df = _db[view].find_one(filter)
    return df

def set_field(_db, col, filter, set_cmd):
    _db[col].update_many(
        filter,
        set_cmd,
    )