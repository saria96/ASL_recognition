from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *

def build_model(num_classes):

    model = Sequential()

    # Input layer 
    model.add(Input(shape=(20, 64, 64, 3)))

    # CNN 2D per frame
    model.add(TimeDistributed(Conv2D(32, (3,3), activation='relu')))
    model.add(TimeDistributed(MaxPooling2D(2,2)))

    model.add(TimeDistributed(Conv2D(64, (3,3), activation='relu')))
    model.add(TimeDistributed(MaxPooling2D(2,2)))

    # keep sequence intact
    model.add(TimeDistributed(Flatten()))

    # LSTM gets 3D input 
    model.add(LSTM(128, return_sequences=False))

    model.add(Dropout(0.5))

    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    return model