from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Dense, Activation, Dropout, Flatten
from keras import optimizers
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

img_width = 150
img_height = 150
train_data_dir = 'data/train'
valid_data_dir = 'data/validation'

model = Sequential()

model.add(Conv2D(32,(3,3), input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3), input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3), input_shape=(img_width, img_height, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

datagen = ImageDataGenerator(rescale=1./255)

train_generator = datagen.flow_from_directory(directory=train_data_dir,
                                              target_size=(img_width, img_height),
                                              classes=['cats', 'dogs'],
                                              class_mode='binary',
                                              batch_size=16)

validation_generator = datagen.flow_from_directory(directory=valid_data_dir,
                                                   target_size=(img_width,img_height),
                                                   classes=['cats', 'dogs'],
                                                   class_mode='binary',
                                                   batch_size=32)


print('model complied!!')

print('starting training....')
training = model.fit_generator(generator=train_generator, steps_per_epoch=2048 // 16,
                               epochs=20,
                               validation_data=validation_generator,
                               validation_steps=832//16)

print('training finished!!')

print('saving weights to simple_CNN.h5')

model_json = model.to_json()
with open("./model_test_3/model.json", "w") as json_file:
    json_file.write(model_json)

# Save the weights in a separate file
model.save_weights("./model_test_3/model.h5")

print("Classifier trained Successfully!")

print('all weights saved successfully !!')
# models.load_weights('models/simple_CNN.h5')

