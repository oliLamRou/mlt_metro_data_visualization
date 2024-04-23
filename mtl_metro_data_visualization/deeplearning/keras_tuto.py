from sentence_transformers import SentenceTransformer
import transformers

from mtl_metro_data_visualization.categorization.tweet import Tweet

path = '../../data/twitter_stm_rem.csv'
tweet = Tweet(path)
tweet.load_preprocess
df_ = tweet.df_.copy()
# df_ = df_.iloc[0:100]

model =  SentenceTransformer("./model_french")#Sahajtomar/french_semantic

def sentence_to_vec(sentence):
    return model.encode(sentence)

df_['embedding'] = df_.tweet.apply(sentence_to_vec)
# print(df_.embedding)
df_[['embedding', 'stop']].to_csv('./temp.csv', index=False)