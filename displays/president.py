import streamlit as st
import gridfs
import tools

client = tools.init_connection()
db = client.pollwatcher
fs = gridfs.GridFS(db)

def app():

    tally_df = tools.get_tally(db,'view_Tally_president')
    raw_df = tools.get_rawdata(db, 'view_rawdata_president')

    st.title('Presidential Candidates')
    st.markdown('Ctrl-Left Click to deselect a row.')

    selection = tools.aggrid_interactive_table(df=tally_df)

    # rawdata table columns to show
    raw_hidecolumns = ['_id','interview__key','Latitude', 'Longitude']
    if len(selection["selected_rows"])>0:
        candidate_filter = selection["selected_rows"][0]['Candidate']
        filtered_data = raw_df[raw_df['Candidate']==candidate_filter]
    else:
        candidate_filter = None
        filtered_data = raw_df

    rawtable = tools.aggrid_interactive_table(df=filtered_data,HideCols=raw_hidecolumns)

    if len(rawtable["selected_rows"])>0:
        interview_key = rawtable["selected_rows"][0]['interview__key']
        st.write(interview_key)

        # display the images
        for img in tools.get_photos(fs, interview_key):
            st.image(img.read())
