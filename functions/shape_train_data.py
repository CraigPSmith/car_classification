import os
import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


def load_training_data(classes, img_size, test=0.2):
    for c, class_label in enumerate(classes):
        for i, img in enumerate(os.listdir('car_images/' + class_label)):

            path = os.path.join('car_images/' + class_label, img)
            img = Image.open(path)
            img = img.convert('L')
            img = img.resize((img_size, img_size), Image.ANTIALIAS)
            img = np.array(img)
            img = np.reshape(img, (1, img_size, img_size, 1))

            if c == 0 and i == 0:
                imgs = img
                labels = np.array(class_label)
            else:
                imgs = np.append(imgs, img, axis=0)
                labels = np.append(labels, np.array(class_label))

    le = LabelEncoder()
    le.fit(labels)
    labels_code = le.transform(labels)
    labels_oh = to_categorical(labels_code)

    x_train, x_test, y_train, y_test = train_test_split(imgs, labels_oh, test_size=test)

    return x_train, x_test, y_train, y_test
