import cv2
import PIL.Image as pilimg
import keras.preprocessing.image
from tensorflow import keras
from tensorflow.keras.optimizers import RMSprop
import numpy as np
import numpy as np #numpy library
np.set_printoptions(threshold=np.inf, linewidth=np.inf) #inf = infinity

import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

class TensorFlow():
    def __init__(self):
        super().__init__()
        self.model = keras

    def test_Learn(self):
        # https://codetorial.net/tensorflow/classifying_the_cats_and_dogs.html
        # 참조
        base_dir = 'D:\\tensor\\'

        train_dir = os.path.join(base_dir, 'train')
        validation_dir = os.path.join(base_dir, 'validation')

        # 훈련에 사용되는 이미지 경로
        train_top_dir = os.path.join(train_dir, 'TOP')
        train_btm_dir = os.path.join(train_dir, 'BTM')
        print(train_top_dir)
        print(train_btm_dir)

        self.model = keras.models.Sequential([
            keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(150, 150, 3)),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(32, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Flatten(),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])

        self.model.summary()

        self.model.compile(optimizer=RMSprop(lr=0.001),
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        train_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.)
        test_datagen =  keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.)

        train_generator = train_datagen.flow_from_directory(train_dir,
                                                            batch_size=20,
                                                            class_mode='binary',
                                                            target_size=(150, 150))
        validation_generator = test_datagen.flow_from_directory(validation_dir,
                                                                batch_size=20,
                                                                class_mode='binary',
                                                                target_size=(150, 150))

        history = self.model.fit(train_generator,
                            validation_data=validation_generator,
                            #steps_per_epoch=10,
                            epochs=2,
                            #validation_steps=50,
                            verbose=2)

        # acc = history.history['accuracy']
        # val_acc = history.history['val_accuracy']
        # loss = history.history['loss']
        # val_loss = history.history['val_loss']
        #
        # epochs = range(len(acc))
        #
        # plt.plot(epochs, acc, 'bo', label='Training accuracy')
        # plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
        # plt.title('Training and validation accuracy')
        # plt.legend()
        #
        # plt.figure()
        #
        # plt.plot(epochs, loss, 'go', label='Training Loss')
        # plt.plot(epochs, val_loss, 'g', label='Validation Loss')
        # plt.title('Training and validation loss')
        # plt.legend()
        #
        # plt.show()

    def Save(self):
        self.test_Learn()
        self.model.save('./TrainModel')
    def Load(self):
        self.model = keras.models.load_model('./TrainModel')

    def Test(self, imgPath):

        img = keras.preprocessing.image.load_img(imgPath, target_size=(150, 150))

        x = keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])

        classes = self.model.predict(images, batch_size=10)

        return classes[0]