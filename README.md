# mlt_metro_data_visualization

1. Web Scrapping
2. One Hot Encoding
3. Machine learning for tweets categorization
4. Sentiment Analysis on article

## 1. Web Scrapping
- Twitter accounts: stm_BLEUE, stm_JAUNE, stm_ORANGE, stm_VERTE and REM_infoservice
- News: Lapresse, 24h, The Gazette

## 2. One Hot encoding
With key words, categorizing when service on the line is stop, slow or has restart. Extracting also other feature like when elevator are out of service.

- Interruption per line
- Duration of the interruption until full service is back
- Ratio of which stations are more impacted
- Elevator for REM

## 3. Machine learning for tweets categorization
- Tokennized tweet
- Word2vec
- Tensorflow model with embedding
- Using stop, slow, restart feature

## 4. Sentiment Analysis on article
Gather all articles related to public transportation in the Montreal region from La Presse and the Gazette. Perform a sentiment analysis on these articles to determine the proportion of negative, neutral, and positive sentiments.


# Project Structure
## Data
### Web Scrapping
- I'm using another [repo](https://github.com/oliLamRou/WebScrapper) to download all tweet from stm and rem twitter handle
- Twitter has a limit of couples hundreds twitter every hour or so. In couple of try my WebScrapper is adding data from where it stopped last time.
- Each line has it's own csv file with raw_date and raw_text capturing everything without filter.
## Categorization Class
### Tweets
- This class will combine all csv and create clean column to help further process.  
Columns: *line*, *tweet*, *preprocessed*, *date*  
- The *preprocessed* column is a simplify str process. Removing short words and changing all line name for just 'line' for exemple.
### OneHotEncoding
- This class inerite Tweets. It will process one hot encoding for: *stop*, *normal*, *slow*, *restart*, *elevator*, *elevator_closed*, *station*, *event*. I'm trying here to get the difference between tweets of when the service restart after an interruption and specifically a part of the line is down.  
- To do that I use REGEX and simple python str operation on the preprocessed column. All the string to compare come from the constant/_lines_stations.py file.
## Dashboard Class
### TimeInterval
- I didn't want to graph intraday data so I'm combining every INT with a **max** function and all FLOAT with a **sum** function. That way I have each day that have at least 1 event but I combine the duration of all interruption throught a day.  
- I can then sum event or duration if I go for higher time frame like month or year.  



- Data processing
- ML