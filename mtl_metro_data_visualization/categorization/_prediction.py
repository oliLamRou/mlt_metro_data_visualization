from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from mtl_metro_data_visualization.constant._path import MODEL_PATH
from mtl_metro_data_visualization.constant._categories import MAX_WORDS, MAX_LEN

class Prediction:
	def __init__(self, model_path = None):
		self.model_path = model_path
		if self.model_path == None:
			self.model_path = MODEL_PATH

		self._model = None
		self.tokenizer = Tokenizer(num_words=MAX_WORDS)

	@property
	def model(self):
		if self._model == None:
			self._model = keras.models.load_model(self.model_path)

		return self._model
	

	def predict(self, input_tweet):
		input_sequence = self.tokenizer.texts_to_sequences([input_tweet])
		input_processed = pad_sequences(input_sequence, maxlen=MAX_LEN)

		predictions = self.model.predict(input_processed)

		print("Predicted probabilities:", predictions)
		print(input_tweet)