
# FLYR Data Science Challenge


### Part 1: Build a model that predicts an offered airfare
In EDA, there was definitive variance.  Some of the sites really offered quite a few mixed carrier flights (with usually cheaper but longer routes), while others focused on direct flights. I also found a pretty large variance depending on the search input. For the most part, I was searching for flights out of San Fran to Asia. I also wondered how travel time compared to price. I assumed this comparison would be a linear negative correlation, with price decreasing as travel duration increased, which is not always the case. However for the same miles (trip distance between origin and destination excluding the layover miles) the shorter of the trip time duration, the more expensive it gets (yeah makes sense!)
![part1](images/fare_by_trip_distance_and_time.jpg)

I looked at mean prices across different time of day. Late night and afternoon flights are definitely more costly.

As for the model, I first converted all fare to USD to be used as the target. Then feature engineer to get to
* Travel time spent outbound, inbound
* Miles based on longtitude and latitude
* Number of layovers (for direct flight, 0)
* Main airline for outbound and inbound (the dominating airline)
* Time of day for departure (early am, morning, afternoon, evening,  late evening)
* Roundtrip or not
* Seasonality
In addition to the original features such as partner site(encoded), airlines, cabin class(encoded), number of passengers etc

 With max min scaler to normalize the feature matrix, I tried to fit into a linear regression and later ensemble approaches. The accuracy score on test dataset is close to ~30% for linear regression and 55% for random forest regression


The most important features are:
* miles per hour
* airlines
* cabin class
* travel site
* seasonality
* num of layovers

It's obvious that distance, cabin class, airline, number of layovers and seasonality dictate the price. What's interesting is the variability in travel site in price. For the same itinerary, the price can be vastly different depending on the travel site, ID 294 tend to offer on the higher end.

### Part 2: Predict which airfares are ultimately booked
For this exercise, I used booking dataset combined with search. Note booking is a subset of search. With booked '1', not booked '0' which will be the target variable we are trying to predict.

First note is ~1.4% search gets booked, which is small percentage (but that's the reality of this business), so very unbalanced dataset. Hence we might have to position the problem as either anomaly detection or use SMOTE or other method to oversample/undersample


Model:
Used simple logistic regression leading to ~80% accuracy, f1 score, precision, and recall in test dataset.

Key features are:
* fare
* travel site
* season, time of the day
* number of requests

As expected, fare is number one factor for booking.(that's why FLYR!)
Also day of the time and season are keys as there is a spike in summer and holiday.
Again, booking rate per travel site varies a lot, some site offers better prices for the mile, hours per trip hence are getting more itineraries booked.
![part2](images/booking_per_website.png)

Moreover, number of requests and 'bookedness' are negatively correlated, more demand leads to more competitions and harder to book it(?)
With more time I would definitely like to spend more time in understanding feature and how they are inter correlated and engineer them better.  


## Next Steps:
There are plenty of questions which can be answered by this dataset and other datasets if we get,  but for now we can  find a solid way to compare across a few aggregators and some new airline price search tools going forward. Even better if we can get market data, competitors' and more travel website search history and consumers' data we can create a recommendation pipeline based on demand supply and price elasticity per consumer in close to real time. This will expand to last minute deals for each travel site and optimize the occupancy rate and ROI of flights for Airlines at the  same time.
Also YOY trend might be an interesting thing to look into as the current dataset only contains 2017 data.
