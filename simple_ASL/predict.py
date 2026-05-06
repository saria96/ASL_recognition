import numpy as np
from tensorflow.keras.models import load_model
import pickle
from loader import load_video

model = load_model("asl_model.h5")

with open("classes.pkl", "rb") as f:
    classes = pickle.load(f)

video = load_video("test.mp4")

video = np.expand_dims(video, axis=0)

pred = model.predict(video)

print("Prediction:", classes[np.argmax(pred)])