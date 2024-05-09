from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input, Dropout

from mtl_metro_data_visualization.categorization.one_hot_encoding import OneHotEncoding
from mtl_metro_data_visualization.constant._categories import CATEGORIES


oh = OneHotEncoding()
oh.encoding()
df = oh.df
max_words = 60
max_len = 10
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(df.preprocessed.values)
sequences = tokenizer.texts_to_sequences(df.tweet.values)
X_processed = pad_sequences(sequences, maxlen=max_len)


for category in CATEGORIES.keys():
    inputs = 16
    model = Sequential()
    model.add(Embedding(max_words, inputs))
    model.add(LSTM(inputs))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    X_train, X_test, y_train, y_test = train_test_split(X_processed, df[category].values, test_size=0.2, random_state=42)
    model.fit(X_train, y_train, epochs=10, batch_size=inputs, validation_split=0.2, verbose=0)

    model.save(f'../../model/line_{category}.keras')

    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f'Test accuracy for {category}: {accuracy}')