#!/usr/bin/env python3

##############
#### Your name: Logan Gillespie
##############

import numpy as np
import re
from sklearn import svm, metrics
from skimage import io, feature, filters, exposure, color


class ImageClassifier:

    def __init__(self):
        self.classifer = None

    def imread_convert(self, f):
        return io.imread(f).astype(np.uint8)

    def load_data_from_folder(self, dir):
        # read all images into an image collection
        ic = io.ImageCollection(dir + "*.bmp", load_func=self.imread_convert)

        # create one large array of image data
        data = io.concatenate_images(ic)

        # extract labels from image names
        labels = np.array(ic.files)
        for i, f in enumerate(labels):
            m = re.search("_", f)
            labels[i] = f[len(dir):m.start()]
        return (data, labels)

    def extract_image_features(self, data):
        # Please do not modify the header above

        # extract feature vector from image data
        ########################
        ######## YOUR CODE HERE
        ########################
        feature_data = []
        # np.zeros((len(data), 240, 320))
        for i in range(0, len(data)):
            image = color.rgb2gray(data[i])

            hog = feature.hog(image, pixels_per_cell=(48, 48), cells_per_block=(4, 4), orientations=9,
                              feature_vector=True, block_norm='L2-Hys')

            feature_data.append(hog)

        # Please do not modify the return type below
        return (feature_data)

    def train_classifier(self, train_data, train_labels):
        # Please do not modify the header above

        # train model and save the trained model to self.classifier

        ########################
        ######## YOUR CODE HERE
        ########################
        clf = svm.LinearSVC()
        clf.fit(train_data, train_labels)
        self.classifer = clf

    def predict_labels(self, data):
        # Please do not modify the header

        # predict labels of test data using trained model in self.classifier
        # the code below expects output to be stored in predicted_labels

        ########################
        ######## YOUR CODE HERE
        ########################
        # Please do not modify the return type below
        predict = self.classifer.predict(data)
        predicted_labels = predict

        return predicted_labels


def main():
    img_clf = ImageClassifier()

    # load images
    (train_raw, train_labels) = img_clf.load_data_from_folder('./train/')
    (test_raw, test_labels) = img_clf.load_data_from_folder('./test/')

    # convert images into features
    train_data = img_clf.extract_image_features(train_raw)
    test_data = img_clf.extract_image_features(test_raw)

    # train model and test on training data
    img_clf.train_classifier(train_data, train_labels)
    predicted_labels = img_clf.predict_labels(train_data)
    print("\nTraining results")
    print("=============================")
    print("Confusion Matrix:\n", metrics.confusion_matrix(train_labels, predicted_labels))
    print("Accuracy: ", metrics.accuracy_score(train_labels, predicted_labels))
    print("F1 score: ", metrics.f1_score(train_labels, predicted_labels, average='micro'))

    # test model
    predicted_labels = img_clf.predict_labels(test_data)
    print("\nTesting results")
    print("=============================")
    print("Confusion Matrix:\n", metrics.confusion_matrix(test_labels, predicted_labels))
    print("Accuracy: ", metrics.accuracy_score(test_labels, predicted_labels))
    print("F1 score: ", metrics.f1_score(test_labels, predicted_labels, average='micro'))


if __name__ == "__main__":
    main()
