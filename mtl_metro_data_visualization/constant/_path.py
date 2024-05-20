from pathlib import Path

# Get the absolute path of the current script
script_path = Path(__file__).resolve()

# Get the directory name of the script
root = script_path.parent.parent.parent


TWITTER_STM_REM_PATH = '../../data/twitter_stm_rem.csv'

TWEET_ONE_HOT_PATH = root/'data/tweets_one_hot.csv'

TRAINING_DATA_PATH = '../../data/tweets/'

SCRAP_DIR = root/'data/'

MODEL_PATH = '../../model/categorization.keras'