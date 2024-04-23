from sentence_transformers import SentenceTransformer
import transformers

from mtl_metro_data_visualization.categorization.tweet import Tweet

path = '../../data/twitter_stm_rem.csv'
tweet = Tweet(path)
tweet.load_preprocess
df_ = tweet.df_.copy()
# df_ = df_.iloc[0:15]



# model =  SentenceTransformer("Sahajtomar/french_semantic")
# model.save('../../model/french_semantic')
model =  SentenceTransformer('../../model/french_semantic')

def sentence_to_vec(sentence):
    return list(model.encode(sentence))

df_['embedding'] = df_.tweet.apply(sentence_to_vec)
# print((df_['embedding'].iloc[0][0]))



# print(df_.embedding)
df_[['embedding', 'stop', 'tweet']].to_csv('./temp.csv', index=False)