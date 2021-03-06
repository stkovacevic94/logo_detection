from features import compute_hog_features
from utils import load_data, transform_to_classification_dataset, report_metrics
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
import cv2


if __name__=='__main__':
    np.random.seed(42)
    recompute_vocabulary = False

    clf = LinearSVC(C=0.0005, class_weight="balanced")

    train_images, test_images, train_logos, test_logos = load_data('./data', test_size=0.33)
    train_images_clf, y_train = transform_to_classification_dataset(train_images, train_logos)
    test_images_clf, y_test = transform_to_classification_dataset(test_images, test_logos)
    
    print("Training stage...")
    X_train = compute_hog_features(train_images_clf)
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_train)
    report_metrics(y_train, y_pred, "Train")

    print("Evaluation stage...")
    X_test = compute_hog_features(test_images_clf)
    X_test = scaler.transform(X_test)
    y_pred = clf.predict(X_test)
    report_metrics(y_test, y_pred, "Test")

    s_test = np.ones(len(y_test), np.uint)
    nologo_idx = np.where(y_test == 10)
    s_test[nologo_idx] = 0
    
    s_pred = np.ones(len(y_pred), np.uint)
    nologo_idx = np.where(y_pred == 10)
    s_pred[nologo_idx] = 0
    report_metrics(s_test, s_pred, "Logo/No-Logo results on testset")

    
    

