from turtle import width
import streamlit as st
import gridfs
import tools
import pandas as pd

client = tools.init_connection()
db = client.pollwatcher
fs = gridfs.GridFS(db)


def app():

    st.header('Overcounted Voters')
    
    results = tools.get_rawdata(db,'view_validation_overcount')

    pos_map = {'pw_president':'President', 'pw_vicepresident':'Vice-President'}
    rows = []
    for row in results.values:
        province, municipality, barangay, precinct, position, interview_key, votes_counted, votes_max, cluster, center, watcher, phone = row
        pos_title = pos_map[position]
        rows.append({'Province': province, 'Municipality': municipality, 
                    'Barangay': barangay, 'Precinct': precinct,
                    'Position': pos_title, 'Total Votes':votes_counted,
                    'Total Voters': votes_max,
                    'Key':interview_key, 'Cluster':cluster,
                    'Voting Center': center, 'Poll Watcher': watcher,
                    'Watcher Phone': phone})

    tbl = pd.DataFrame(rows)
    raw_hidecolumns = ['Key','Cluster','Voting Center', 'Poll Watcher', 'Watcher Phone']
    selection = tools.aggrid_interactive_table(df=tbl, HideCols=raw_hidecolumns)
    

    if len(selection["selected_rows"])>0:

        val = selection["selected_rows"][0]
        disp_dict = {'Key': val['Key'],
                    'Cluster': val['Cluster'],
                    'Voting Center': val['Voting Center'],
                    'Poll Watcher': val['Poll Watcher'],
                    'Watcher Phone': val['Watcher Phone']}

        c_op = '<tr><td align=right>' 
        c_md = '</td><td align=left>'
        c_cl = '</td></tr>'
        tbl_str = '<table>'
        for k, v in disp_dict.items():
            tbl_str += c_op + k +c_md + v +c_cl

        tbl_str += '</table>'
        
        st.markdown(tbl_str, unsafe_allow_html=True)

        if len(selection["selected_rows"])>0:
            key = selection["selected_rows"][0]["Key"]

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
    
        # display image
        for img in tools.get_photos(fs, key):
            st.image(img.read())

