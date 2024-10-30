from tensorflow import keras
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras.backend as K


def r2(y_true, y_pred): # Function to calculate R-squared, indicating the network's fit
    SS_res = K.sum(K.square(y_true - y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
    return 1 - SS_res/(SS_tot + K.epsilon())

N = 16
data = np.genfromtxt('dictionary_1.csv', delimiter=',') # Contains dictionary data
print(data.shape)
# Splits dictionary data into score and board data
X = np.array([np.array(i[0:N]) for i in data])
y = data[:, N].reshape(-1, 1)
scaler = StandardScaler()
X = scaler.fit_transform(X)
# Splits the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# Creates the neural network structure
model = keras.models.Sequential()
model.add(keras.layers.Input(shape=(N,)))
model.add(keras.layers.Dense(256, activation='relu'))
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(1, activation='relu'))
model.compile(loss='mean_squared_error', optimizer="adam", metrics=[r2, 'RootMeanSquaredError'])
model.summary()

model.fit(X_train, y_train, epochs=3, batch_size=64, validation_split=0.05) # Trains the neural network
mse_test = model.evaluate(X_test, y_test) # Evaluates the network


# Saves the model
json_model = model.to_json()
with open('fashionmnist_model.json', 'w') as json_file:
    json_file.write(json_model)
model.save_weights('FashionMNIST_weights.h5')
