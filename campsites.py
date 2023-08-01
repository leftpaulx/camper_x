from camply.search import SearchRecreationDotGov,\
                            SearchYellowstone,\
                            SearchGoingToCamp,\
                            SearchReserveCalifornia,\
                            SearchAlabamaStateParks,\
                            SearchArizonaStateParks,\
                            SearchFloridaStateParks,\
                            SearchMissouriStateParks,\
                            SearchOhioStateParks,\
                            SearchVirginiaStateParks,\
                            SearchFairfaxCountyParks,\
                            SearchMaricopaCountyParks,\
                            SearchOregonMetro,\
                            SearchMinnesotaStateParks

# List for supported provider

campsite_list={
    'reservecalifornia.com': SearchReserveCalifornia,
    'recreation.gov':SearchRecreationDotGov,
    'yellowstonenationalparklodges.com':SearchYellowstone,
    'goingtocamp.com':SearchGoingToCamp,
    'reservealapark.com':SearchAlabamaStateParks,
    'azstateparks.com':SearchArizonaStateParks,
    'floridastateparks.org':SearchFloridaStateParks,
    'icampmo1.usedirect.com':SearchMissouriStateParks,
    'reserveohio.com':SearchOhioStateParks,
    'reservevaparks.com':SearchVirginiaStateParks,
    'fairfax.usedirect.com':SearchFairfaxCountyParks,
    'maricopacountyparks.org':SearchMaricopaCountyParks,
    'oregonmetro.gov':SearchOregonMetro,
    'reservemn.usedirect.com':SearchMinnesotaStateParks
}