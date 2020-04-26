import numpy as np
import random
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler


def create_sample_data(num_weeks):
    # only for demonstration purposes
    data_set = np.zeros(84 * num_weeks)
    index = 0
    for i in range(num_weeks):
        base = 30
        for j in range(7):
            if j == 4:
                base = random.randint(40, 44)
            elif j == 5:
                base = random.randint(48, 52)  # peaks friday/saturday/sunday
            elif j == 6:
                base = random.randint(37, 39)
            else:
                base = random.randint(28, 32)
            for k in range(12):
                data_set[index] = base + random.randint(-3, 3)
                if k < 6:
                    base += 2
                else:
                    base -= 2
                index += 1
    return data_set
def denormalize(data_set, to_scale):
    data_set = to_scale.inverse_transform(data_set.reshape(-1, 1))
    return data_set

def normalize(data_set):
    to_scale = MinMaxScaler(feature_range=(0, 1))
    data_set = to_scale.fit_transform(data_set.reshape(-1, 1))
    return data_set


def transform_data(data_set, k):
    # looks at k prior values to predict k values ahead
    x = np.zeros([np.size(data_set) - (2 * k) + 1, k])
    y = np.zeros([np.size(data_set) - (2 * k) + 1, k])
    start = 0
    for i in range(np.size(data_set) - (2 * k) + 1):
        index = start
        for j in range(k):
            x[i][j] = data_set[index]
            index += 1
        for j in range(k):
            y[i][j] = data_set[index]
            index += 1
        start += 1
    return x, y

def normalize(data_set, to_scale):
    data_set = to_scale.fit_transform(data_set.reshape(-1, 1))
    return data_set
def train_and_predict(data, num_hours_looked_at=12, show_results=True):
    to_scale = MinMaxScaler(feature_range=(0, 1))
    # trains the model, makes a prediction, graphs the results
    train_data = normalize(data[0:int((np.size(data) * 2) / 3)], to_scale)
    test_data = normalize(data[int((np.size(data) * 2) / 3):], to_scale)

    x_train, y_train = transform_data(train_data, num_hours_looked_at)
    x_test, y_test = transform_data(test_data, num_hours_looked_at)

    x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

    model = Sequential()
    model.add(LSTM(8, input_shape=(1, num_hours_looked_at)))
    model.add(Dense(num_hours_looked_at))
    model.compile(loss="mean_squared_error", optimizer="adam")
    model.fit(x_train, y_train, epochs=50, batch_size=1)

    y_predict = denormalize(model.predict(x_test), to_scale)
    y_predict = y_predict.reshape((y_predict.shape[1], y_predict.shape[0]))
    if show_results:
        plot_results(y_predict[0], test_data[0:168])

    return y_predict


def plot_results(y_predict, y_test):
    # helper method for train_and_predict
    plt.plot(y_test, "-b", label="Actual Data")
    plt.plot(y_predict, "-r", label="RNN Prediction")
    plt.xlabel("Hours")
    plt.ylabel("Number of People (Normalized)")
    plt.legend(loc="upper left")
    plt.show()


