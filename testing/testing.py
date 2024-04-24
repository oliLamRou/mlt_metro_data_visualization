import pandas as pd
import keras

from mtl_metro_data_visualization.categorization.training_data import TrainingData

loaded_model = keras.saving.load_model('../model/stop.keras')


tweet = 'something'
embedding = TrainingData().sentence_to_vec(tweet)
loaded_model.predict(embedding)