from sklearn.model_selection import train_test_split

from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input, Dropout
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding
from mtl_metro_data_visualization.constant._categories import CATEGORIES, MAX_WORDS, MAX_LEN
from mtl_metro_data_visualization.constant._path import MODEL_PATH


oh = OneHotEncoding()
oh.encoding()
df = oh.df

tokenizer = Tokenizer(num_words=MAX_WORDS)
tokenizer.fit_on_texts(df.preprocessed.values)
sequences = tokenizer.texts_to_sequences(df.preprocessed.values)
X_processed = pad_sequences(sequences, maxlen=MAX_LEN)

inputs = 64
model = Sequential()
model.add(Embedding(MAX_WORDS, inputs))
model.add(LSTM(inputs))
model.add(Dense(len(CATEGORIES.keys()), activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

X_train, X_test, y_train, y_test = train_test_split(X_processed, df[CATEGORIES.keys()].values, test_size=0.2, random_state=42)
model.fit(X_train, y_train, epochs=40, batch_size=32, validation_split=0.2, verbose=1)

model.save(MODEL_PATH)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy: {accuracy}')



