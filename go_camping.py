from datetime import datetime
import logging
from typing import Any, Dict, Generator, Iterable, List, Optional, Sequence, Set, Union
from campsites import campsite_list
from camply.containers import AvailableCampsite, SearchWindow
import pandas as pd
from alert_setup import email_alert
import time
from threading import Thread
import streamlit as st

class go_camping:
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
        

    def find_campsite(self,rec_area,campground_id=None):
        """
        find campsites
        
        parameters
        ----------
        rec_area: rec_area id which can be found in campsite url
        campground_id: optional
        
        """
        logging.basicConfig(format="[%(asctime)s] : %(message)s",level=logging.INFO)
        startdate=self.start_date
        enddate=self.end_date
        window=SearchWindow(start_date=startdate,end_date=enddate)
        finder=campsite_list[self.provider](search_window=window,recreation_area=rec_area,campgrounds=campground_id,weekends_only=self.weekends_only,nights=self.nights,days_of_the_week=self.days_of_the_week)
        camp_list=finder.get_matching_campsites(log=True, 
                                             verbose=True)
        return pd.DataFrame([dict(camp) for camp in camp_list])
    
    def search_pause(self):
        time.sleep(60)


    def continuous_search_campsite(self,rec_area,session_state=True,email=None,campground_id=None):
        while True:
            df=self.find_campsite(rec_area,campground_id)
            if len(df)>0:
                if email!=None:
                    email_msg=f"{ len(df) } campsites available:\n\n info: \n\n {df[['booking_date','booking_end_date','campsite_use_type','recreation_area','facility_name','booking_url']]}"
                    email_alert('Your Campsite Available !!!', email_msg,email)
                break
            for i in range(240):
                if session_state==False:
                    break
                time.sleep(1)

        return df

