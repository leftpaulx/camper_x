import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from campsite_search import camper_x
from campsites import campsite_list
from camply.exceptions import SearchError
from requests import HTTPError

#Streamlit page setup

## title
st.title("Camper X :camping:")

## date input widget
dates=st.date_input("When do you want to go camping? 🌎",
              value=(dt.date.today(),dt.date.today()+dt.timedelta(days=7)),
              min_value=dt.date.today(),
              help='Search will be performed in the daterange you select')

## provider input widget
provider=st.selectbox('Do you know where to reserve your campsite? 	',
                        options=list(campsite_list.keys()))

## function to check no conflicts between weekday requirements and weekend requirements
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

## Only search for weekend input widget
st.checkbox('Only search for weekend availabilities?',
                  key='weekends',
                  help='Search will be performed among Fridays and Saturdays if selected',
                  on_change=weekday_check)

## Weekday search widget
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

## consecutive nights input widget 
nights=st.number_input('How many nights would you like to stay?',
                       min_value=1,
                       max_value=7,
                       step=1)

## campsite id input widget 
col1, col2 = st.columns(2)
with col1:
    rec_area=st.number_input('Please enter the recreation area ID',
                       min_value=1,
                       step=1,
                       help='Recreation area ID can be found in the reservation website url')
    
with col2:
    if st.checkbox('Search by Campground id?',help="Try checking this box if you see string 'campground' in the url or recreation area ID does not work."):
        campground_id=rec_area
        rec_area=1
    else:
        campground_id=None   

## if continuous search input widget                 
continuous=  st.checkbox('Continuous Search',help='Search will be performed every 5 minutes') 

## email input widget if continuous is selected
if continuous:
    email = st.text_input('Please enter your email', help='Optional. If valid email is provided, alert will be sent to the email when the campsite is found') 
else:
    email = None

def stop():
    if 'recording' not in st.session_state:
        st.session_state['recording']=False
    if st.session_state['recording'] == True:
        st.session_state['recording'] = False
        st.info('Searching stopped ☔, please refresh the page to restart')
        st.cache_data.clear()
        st.stop()

## start and stop button
col3, col4 = st.columns(2)
with col3:
    run_code=st.button('Search')
with col4:
    stop_code=st.button('Stop',on_click=stop)


def main():  
    if run_code:    
        # initiate camper_x 
        cx=camper_x(dates[0],dates[1],provider=provider,weekends_only=st.session_state['weekends'],days_of_the_week=st.session_state['weekdays'],nights=nights) 
        # set starting session state
        st.session_state['recording'] = True
        while st.session_state['recording']== True:
            try:
                with st.spinner('Searching...'):                 
                    df=cx.ult_search(continuous=continuous,rec_area=rec_area,campground_id=campground_id,email=email,session_state=st.session_state['recording'])
                if len(df)>0:
                    st.success("Let's go camping!!! 🌄")
                    st.dataframe(df)
                else:
                    st.warning('No available campsite found! ❌')
            except (SystemExit,IndexError):
                st.warning('Invalid entry, please check your input! ⚠️')
            except SearchError:
                st.warning('Invalid Recreation or Campground ID, please check your input! ⚠️')
            except HTTPError:
                st.warning('Oops, the IP seems to be blocked by the provider. Please try running the search on local ⚠️')
            st.session_state['recording']=False


if __name__=='__main__':
    main()
  
        
    
      
    


    