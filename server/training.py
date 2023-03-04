import numpy as np
import tensorflow as tf
from tensorflow import keras
# import keras
from keras.layers import Dense, Conv2DTranspose, LeakyReLU, Reshape, BatchNormalization, Activation, Conv2D, Flatten, Dropout, Conv1D, Conv1DTranspose
from keras.models import Model, Sequential

x = []
y = []
with open("./data.txt", "r") as f:
  lines = f.readlines()
  for line in lines:
    if line != "":
      board, player, result = line.split('#')

      result = [float(x) for x in result.split(' ')]
      player = int(player)
      
      y.append(np.array(result))
      
      rows = board.split('/')
      sample = np.zeros((65,))
      for i in range(8):
        for k in range(8):
          sample[i*8+k] = int(rows[i][k]) -1
      sample[64] = player
      x.append(sample)

x = np.array(x)
x = x.reshape((x.shape[0], 65, 1))
y = np.array(y)

print(x.shape)
print(y.shape)

def create_model():
  model = Sequential()
  # model.add(Conv2D(32, kernel_size=3, strides = (1,1), padding="same", input_shape=(9, 8, 1)))
  # model.add(LeakyReLU(alpha=0.2))

  # model.add(Conv2D(32, kernel_size=3, strides = (1,1), padding="same"))
  model.add(Dense(32, input_shape=(65, 1)))
  model.add(LeakyReLU(alpha=0.2))

  model.add(Conv1D(32, kernel_size=3, strides = 1, padding="same"))
  model.add(LeakyReLU(alpha=0.2))

  model.add(Conv1D(32, kernel_size=3, strides = 1, padding="same"))
  model.add(LeakyReLU(alpha=0.2))

  model.add(Conv1D(32, kernel_size=3, strides = 1, padding="same"))
  model.add(LeakyReLU(alpha=0.2))

  model.add(Conv1D(32, kernel_size=3, strides = 1, padding="same"))
  model.add(LeakyReLU(alpha=0.2))

  model.add(Flatten())
  model.add(Dense(3, activation="sigmoid"))

  opt = keras.optimizers.Adam(lr=0.0002, beta_1=0.5)
  model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
  return model

model = create_model()
model.summary()

model.fit(
    x = x,
    y = y,
    epochs=100,
    batch_size=64,
)

model.save("saved_model/my_model")