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
- I'm using another [repo](git@github.com:oliLamRou/WebScrapper.git) to download all tweet from stm and rem twitter handle
- Twitter has a limit of couples hundreds twitter every hour or so. In couple of try my WebScrapper is adding data from where it stopped last time.
- Each line has it's own csv file with raw_date and raw_text capturing everything without filter.
## Categorization
### Tweets
This class will combine all csv and create clean column to help further process.  
'line', 'tweet', 'preprocessed', 'date'



- Data processing
- ML