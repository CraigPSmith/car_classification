import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.optimizers import Adam


def conv(x_train, y_train, x_test, y_test, n_classes, img_size, batch=10, kernel=3, pool=2, drop=0.5, print_epochs=0):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(kernel, kernel), strides=(1, 1), activation='relu',
                     input_shape=(img_size, img_size, 1)))

    model.add(MaxPooling2D(pool_size=(pool, pool)))

    model.add(Conv2D(64, (kernel, kernel), activation='relu'))
    model.add(MaxPooling2D(pool_size=(pool, pool)))

    model.add(Conv2D(128, (kernel, kernel), activation='relu'))
    model.add(MaxPooling2D(pool_size=(pool, pool)))

    model.add(Conv2D(256, (kernel, kernel), activation='relu'))
    model.add(MaxPooling2D(pool_size=(pool, pool)))

    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))
    model.add(BatchNormalization())

    model.add(Dropout(drop))
    model.add(Dense(n_classes, activation='softmax'))

    model.compile(loss=categorical_crossentropy,
                  optimizer=Adam(lr=0.01),
                  metrics=['accuracy'])

    model_history = model.fit(x_train, y_train,
                              batch_size=batch,
                              epochs=20,
                              verbose=print_epochs,
                              validation_data=(x_test, y_test))

    score = model.evaluate(x_test, y_test, batch_size=batch)
    print('Test accuracy:', score[1])

    return model_history


def confusion_plot(model, x_test, y_test, classes):
    predictions = model.predict(x_test)
    predictions = pd.DataFrame(data=predictions, columns=classes)
    preds = predictions.idxmax(axis=1)
    targets = pd.DataFrame(data=y_test, columns=classes)
    tas = targets.idxmax(axis=1)
    cm = confusion_matrix(tas, preds)
    norm_cm = cm / cm.sum(axis=1)[:, None] * 100

    models = []
    for c in classes:
        m = c.split("_")[-1]
        models.append(m)

    plt.figure(figsize=(8, 8))
    plt.title('normalized confusion matrix')
    plt.imshow(norm_cm, interpolation='nearest', cmap=plt.cm.rainbow)
    plt.colorbar()
    tick_marks = np.arange(len(models))
    plt.xticks(tick_marks, models, rotation=90)
    plt.yticks(tick_marks, models)
    plt.ylabel('True')
    plt.xlabel('Predicted')

    return


def save_model(model, labels, model_name='test'):
    np.save('model_params/' + model_name + '_labels', labels)

    model_json = model.to_json()
    with open('model_params/' + model_name + "_model.json", "w") as json_file: json_file.write(model_json)
    model.save_weights('model_params/' + model_name + "_model.h5")


def import_model(model_name):
    labels = np.load('model_params/' + model_name + '_labels.npy', allow_pickle=True)

    json_file = open('model_params/' + model_name + '_model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('model_params/' + model_name + '_model.h5')

    return loaded_model, labels
