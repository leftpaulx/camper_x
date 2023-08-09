# Camper X :camping: Streamlit App

## Introduction

Welcome to **Camper X**, a Streamlit-based application that helps you find available campsites for your camping adventures. This application interacts with various campsite providers to search for camping opportunities based on your preferences.

## Getting Started

Simply access the app at https://camperx.streamlit.app/

## Usage

### Date Selection

- Use the date input widget to specify your camping date range. The search will be performed within the selected date range. Date range must be in the future, start date and end date are both needed.

### Provider Selection

- Choose a campsite provider from the dropdown list. Available providers are listed in the `campsites` module. 

### Day Preferences

- Use the "Only search for weekend availabilities?" checkbox to limit the search to weekends (Fridays and Saturdays). This option can be toggled on/off.
- The "Only search for certain days?" multiselect widget allows you to select specific weekdays for your camping search.

### Duration of Stay

- Specify the number of nights you would like to stay using the number input widget. Maximum 7 days

### Campsite Selection

- Enter the Recreation Area ID in the provided number input box. This ID can be found in the reservation website URL.
- If you're unable to find a campsite using the Recreation Area ID, you can try searching by Campground ID. Check the corresponding checkbox and enter the Campground ID.
- e.g., 
    -- https://www.reservecalifornia.com/Web/Default.aspx#!park/712/683, 712 is recreation area ID and 683 is campground ID. You can put 683 in the input box and check the checkbox to search this campsite only or just input
    712 in the input box to search all campgrounds in recreation area 712
    -- https://www.recreation.gov/camping/campgrounds/234330, you can find "campgrounds" is specified in the url, you can only input 234330 in the input box and check the checkbox to search this campsite 

### Continuous Search

- Enable the "Continuous Search" checkbox if you want the search to be performed continuously every 5 minutes.
- Provide your email address in the text input box if you want to receive alerts when a campsite is found.

### Search and Stop Buttons

- Click the "Search" button to initiate the campsite search. The app will display the search results in a DataFrame.
- Use the "Stop" button to halt the continuous search process.


## Run the app locally


Becuase some providers have blocked the IP address of the cloud server, it's better to run the app locally to have full functionality. To run this Streamlit app locally, follow these steps:

1. Make sure you have Python installed on your system.

2. Clone this repository to your local machine:
    git clone https://github.com/leftpaulx/camper_x.git
    cd camper_x

3. Install the required Python packages using pip:
    pip install -r requirements.txt

4. Set up environment variable for your own email alert (if you want to enable email alert)
    - create .env file under the camper_x directory
    - Input your email credentials:
        user="YourEmailAddress@abc.com"
        password="app secret key"
    You can find your app secret key for your gmail by referencing below link:
    https://support.google.com/mail/answer/185833?hl=en#:~:text=An%20app%20password%20is%20a,2%2DStep%20Verification%20turned%20on.

5. Run the Streamlit app:
    streamlit run main.py


## Acknowledgements

This Streamlit app was developed using Python and utilizes the Streamlit framework, with camply library. To know more about camply, or build your own search, please reference its repo at https://github.com/juftin/camply/tree/main

