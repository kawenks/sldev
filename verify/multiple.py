from turtle import width
import streamlit as st
import gridfs
import tools
import pandas as pd

client = tools.init_connection()
db = client.pollwatcher
fs = gridfs.GridFS(db)


def app():

    st.header('Duplicate Precinct Postings')

    col1, col2 = st.columns(2)

    filter = {'NumberOfSubmits': {'$gt': 1}}
    results = tools.get_rawdata(db,'view_validation_duplicates', filter)

    rows = []
    for row in results.values:
        id_obj, keys, submits = row
        province, municipality, barangay, precinct = id_obj.values()
        rows.append({'Province': province, 'Municipality': municipality, 'Barangay': barangay, 'Precinct': precinct, 'Submissions': submits, 'IDs': keys})

    tbl = pd.DataFrame(rows)

    with col1.container():
        selection = tools.aggrid_interactive_table(df=tbl)

    if len(selection["selected_rows"])>0:
        # from array of elements to list
        IDs = eval(selection["selected_rows"][0]['IDs'])

        with col2.container():
            # top level list of interviews
            d0_rows = []
            for key in IDs:
                drilldown_filter = {'Key': key}
                df0 = tools.get_one(db,'view_validation_rawdata', drilldown_filter)
                interviewer = df0['Interviewer']
                cellphone = df0['Cellphone']
                timestamp = df0['Timestamp']
                d0_rows.append({'Key': key, 'Interviewer':interviewer, 'Cellphone': cellphone, 'Date/Time': timestamp})

            d0_df = pd.DataFrame(d0_rows)
            dd1 = tools.aggrid_interactive_table(df=d0_df)

            if len(dd1["selected_rows"])>0:
                key = dd1["selected_rows"][0]["Key"]

                discard = st.checkbox('Discard {}?'.format(key))
                if discard:
                    update_qry = {"interview__key":key}
                    set_cmd = {"$set": {"rejected": True}}
                    tools.set_field(db, "staging", update_qry, set_cmd)
                    st.write('Discarded. Refresh the page to view the updated duplicate list.')
                # CSS to inject contained in a string
                hide_dataframe_row_index = """
                            <style>
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                            </style>
                            """
                st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

                positions = {"President": "pw_president", "Vice-President": "pw_vicepresident", "Senator": "pw_senators"}
                with col1.container():
                    for pos, label in positions.items():
                        dd2_filter = {"Key": key,"Position": label}
                        dd2 = tools.get_rawdata(db,'view_validation_rawdata',dd2_filter)
                        dd2_tbl = dd2[["Candidate", "Votes"]]
                        dd2_tbl.set_index("Candidate")
                        st.write(pos)
                        st.dataframe(dd2_tbl)
        
                with col2.container():
                    if len(dd1["selected_rows"])>0:
                        key = dd1["selected_rows"][0]["Key"]

                    # display the images
                    for img in tools.get_photos(fs, key):
                        st.image(img.read())

