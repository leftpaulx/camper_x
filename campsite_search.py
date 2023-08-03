from datetime import datetime as dt
import logging
from typing import Any, Dict, Generator, Iterable, List, Optional, Sequence, Set, Union
from campsites import campsite_list
from camply.containers import SearchWindow
import pandas as pd
from alert_setup import email_alert
import time
import streamlit as st
from console_streamlit_redirect import st_stderr,st_stdout

class camper_x:
    def __init__(
    self,
    start_date,
    end_date,
    provider,
    weekends_only: bool=True,
    days_of_the_week: Optional[Sequence[int]] = None,
    nights: int=1
    ):
        """
        Initialize with search parameters
        
        parameters
        ----------
        start_date: in format m/d/yyyy
        
        end_date: in format m/d/yyyy
        
        provider: select between "reserve california" and "recreation.gov"
        
        weekends_only: bool
        
        days_of_the_week: Optional[Sequence[int]] Days of the week (by weekday integer) to search for.
        
        nights: minimum number of consecutive nights to search per campsite,defaults to 1
        """
        self.start_date=start_date
        self.end_date=end_date
        self.provider=provider
        self.weekends_only=weekends_only
        self.days_of_the_week=days_of_the_week
        self.nights=nights
        

    def find_campsite(self,rec_area,log=True,verbose=True,campground_id=None):
        """
        find campsites
        
        parameters
        ----------
        rec_area: rec_area id which can be found in campsite url
        campground_id: optional
        log: optional, default True. If showing the searching log
        verbose: optional, default True. If getting verbose log
        
        """
        logging.basicConfig(format="[%(asctime)s] : %(message)s",level=logging.INFO)
        startdate=self.start_date
        enddate=self.end_date
        window=SearchWindow(start_date=startdate,end_date=enddate)
        finder=campsite_list[self.provider](search_window=window,recreation_area=rec_area,campgrounds=campground_id,weekends_only=self.weekends_only,nights=self.nights,days_of_the_week=self.days_of_the_week)
        camp_list=finder.get_matching_campsites(log=log, 
                                             verbose=verbose)
        return pd.DataFrame([dict(camp) for camp in camp_list])
    
    
    @st.cache(max_entries=50,suppress_st_warning=True)   #cache setup to avoid too large cache
    def continuous_search_campsite(self,rec_area,session_state=True,email=None,campground_id=None):
        """
        continuous_search_campsite
        
        parameters
        ----------
        rec_area: rec_area id which can be found in campsite url
        campground_id: optional
        seesion_state: connect to the streamlit session state to control this function
        email: optional. Email that notification is sent to
        
        """
        notification=email_alert()
        #set up welcome email
        if len(email)>0:
            try:
                notification.welcome(email)
                valid_email=1
            except:
                st.warning('Email entry is not valid, no notification will be sent out.')
                valid_email=0
        while True:
            print(f'{dt.now()}    🌎🌎🌎🌎Searching Started...')
            df=self.find_campsite(rec_area,log=False,verbose=False,campground_id=campground_id)
            if session_state==False:
                break
            if len(df)>0:
                #email alert setup
                if len(email)>0 and valid_email:     
                    notification.alert(email,df[['booking_date','booking_end_date','campsite_use_type','recreation_area','facility_name','booking_url']])
                break
            else:
                print(f'{dt.now()}    ❌ ❌ ❌ ❌ 0 Reservable Campsites Matching Search Preference.')
                #sleep 4 min after each search
            for i in range(240):
                if session_state==False:
                    break
                time.sleep(1)
                placeholder=st.empty()
                #call streamlit to make streamlit active while time.sleep
                with placeholder:
                    st.write(".")
                placeholder.empty()        
        return df
    

    def ult_search(self,continuous,rec_area,session_state=True,campground_id=None,email=None):
        """
        ult_search
        
        parameters
        ----------
        continuous: boolen. If conducting continuous search
        rec_area: rec_area id which can be found in campsite url
        campground_id: optional
        seesion_state: connect to the streamlit session state to control this function
        email: optional. Email that notification is sent to
        
        """
        if continuous:
            ## direct continuous search stdout to streamlit
            with st_stdout("code"):
                df=self.continuous_search_campsite(rec_area=rec_area,email=email,session_state=session_state,campground_id=campground_id)
        else:   
            ## direct regular search stderr to streamlit
            with st_stderr("code"):
                df=self.find_campsite(rec_area=rec_area,campground_id=campground_id)
        if len(df)>0:
            df=df[['booking_date','booking_end_date','campsite_use_type','recreation_area','facility_name','booking_url']]
        return df


