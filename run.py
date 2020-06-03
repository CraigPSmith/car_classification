######  SCRAPE IMAGES  ######
from functions.image_scrape_cars import scrape

cars = ['AUDI', 'FORD', 'FORD', 'VOLKSWAGEN', 'JAGUAR', 'NISSAN', 'VAUXHALL'], ['A1', 'FIESTA', 'KUGA', 'GOLF',
                                                                                'F-PACE', 'QASHQAI', 'CORSA']
scrape(cars)

######  SHAPE TRAINING DATA  ######

import os
from functions.shape_train_data import load_training_data

classes = os.listdir('car_images')
classes.sort()
img_size = 150
x_train, x_test, y_train, y_test = load_training_data(classes, img_size, test=0.2)

######  TRAIN MODEL  ######

from functions.conv_model import conv, confusion_plot, save_model, import_model

model_history = conv(x_train, y_train, x_test, y_test, len(classes), img_size, batch=int(x_train.shape[0] / 100),
                     kernel=3, pool=2, drop=0.5, print_epochs=1)

model = model_history.model

confusion_plot(model, x_test, y_test, classes)  # plot confusion matrix

######  SAVE MODEL  ######

save_model(model, classes, model_name='car_class')

######  LOAD MODEL  ######

model, labels = import_model('car_class')
