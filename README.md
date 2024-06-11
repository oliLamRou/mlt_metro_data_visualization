# mlt_metro_data_visualization

# Project Structure
## Data
### Web Scrapping
- I'm using another [repo](https://github.com/oliLamRou/WebScrapper) to download all tweets from STM and REM Twitter handles.  
- Twitter has a limit of hundreds of tweets every hour or so. In a few tries, this Web Scrapper is adding data from where it stopped last time.
- Each line has its own CSV file with `raw_date` and `raw_text`, capturing everything without filtering.  

## Categorization Class
### Tweets
1. Combining all CSV files and creating a clean column to help further processing. The columns will be:  
	* `line`
	* `tweet`
	* `preprocessed`
	* `date`

2. Create the `preprocessed` column with a simplified version of `tweet`.
	* Removing short words
	* Changing line names(i.e. 'stm_orange') to 'Line'
	* Removing tweets from users
	* Removing many English tweets since they are just duplicates of French ones

### OneHotEncoding
1. Creating one-hot encoding for:
	* `stop`
	* `normal`
	* `slow`
	* `restart`
	* `elevator`
	* `elevator_closed`
	* `station`
	* `event`

I'm trying to get the difference between tweets when the service restarts after an interruption and specifically a part of the line is down using REGEX and other Python string operations with Pandas functionality.

## Dashboard Class
### Time Interval
* I didn't want to graph intraday data, so I'm combining every `int` with a `max()` function and all `float` with a `sum()` function. This way, I have each day that has at least 
one event but combine the duration of all interruptions throughout the day.
* I can then sum events or durations if I go for higher time frames like month or year.

### Dashboard Section
* I tried to have some reusability, so creating sections and graphs will be easier once set up.

## Dashboard
* Run `mtl_metro_data_visualization/dashboard.py` to start the server. (http://127.0.0.1:8050/)