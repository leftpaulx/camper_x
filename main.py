import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from go_camping import go_camping
from console_streamlit_redirect import st_stderr
from campsites import campsite_list


st.title("Camper Helper X :camping:")
dates=st.date_input("When do you want to go camping? 🌎",
              value=(dt.date.today(),dt.date.today()+dt.timedelta(days=7)),
              min_value=dt.date.today(),
              help='Search will be performed in the daterange you select')

provider=st.selectbox('Do you know where to reserve your campsite? 	',
                        options=list(campsite_list.keys()))

def weekend_check():
    week_days=[0,1,2,3,6]
    for day in week_days:
        if day in st.session_state['weekdays']:
            st.session_state['weekends']=False
def weekday_check():
    if st.session_state['weekends']==True:
        st.session_state['weekdays']=[]

if 'weekends' not in st.session_state:
    st.session_state['weekends']=True
if 'weekdays' not in st.session_state:
    st.session_state['weekdays']=[]

st.checkbox('Only search for weekend availabilities?',
                  key='weekends',
                  help='Search will be performed among Fridays and Saturdays if selected',
                  on_change=weekday_check)
weekday_map={0:'Monday',
             1:'Tuesday',
             2:'Wednesday',
             3:'Thursday',
             4:'Friday',
             5:'Saturday',
             6:'Sunday'}
st.multiselect('Only search for certain days?',
                      options=np.arange(0,7),
                      key='weekdays',
                      format_func=lambda x: weekday_map[x],
                      on_change=weekend_check )



nights=st.number_input('How many nights would you like to stay?',
                       min_value=1,
                       max_value=7,
                       step=1)

col1, col2 = st.columns(2)

with col1:
    rec_area=st.number_input('Please enter the recreation area id',
                       min_value=1,
                       step=1,
                       help='Recreation area id can be found in the reservation website url')
    
with col2:
    if st.checkbox('Is there a campground id',help='Campground id can be found in the reservation website url after recreation area id (optional)'):
        campground_id=st.number_input('Please enter the campground id',
                        min_value=0,
                        step=1)
    else:
        campground_id=None                    
continuous=  st.checkbox('Continuous Search',help='Search will be performed every 5 minutes') 
if continuous:
    email = st.text_input('Please enter your email', help='Alert will be sent to you email if the campsite is available') 
col3, col4 = st.columns(2)
with col3:
    run_code=st.button('Search')
with col4:
    stop_code=st.button('Stop')


def camp_run():
    ## search initiate
    camps=go_camping(dates[0],dates[1],provider=provider,weekends_only=st.session_state['weekends'],days_of_the_week=st.session_state['weekdays'],nights=nights)
    if continuous:
        df=camps.continuous_search_campsite(rec_area=rec_area,email=email,session_state=st.session_state,campground_id=campground_id)
        st.dataframe(df)
    else:
        df=camps.find_campsite(rec_area=rec_area,campground_id=campground_id)
    return df


if __name__=='__main__':
    if run_code:     
        st.session_state['recording'] = True
        st.write(st.session_state['recording'])
        while st.session_state['recording']== True:
            try:
                with st.spinner('Searching...'):
                    with st_stderr("code"):
                        df=camp_run()
                if len(df)>0:
                    st.success("Let's go camping!!! 🌄")
                    st.dataframe(df)
                else:
                    st.warning('No available campsite found! ❌')
            except SystemExit:
                st.warning('Invalid entry, please check your input! ⚠️')
            st.session_state['recording']=False
    if stop_code:
        st.session_state['recording'] = False
        st.write(st.session_state['recording'])
        st.info('Searching stopped ☔')
        st.stop()
        
    
      
    


    