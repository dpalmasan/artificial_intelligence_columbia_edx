import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def load_data(input_file):
    """
    Loads the dataset. It assumes a *.csv file without header, and the output variable
    in the last column 
    """
    dataset = np.genfromtxt(input_file, delimiter=',', skip_header=1, names=None)

    X = dataset[:, :-1]
    y = dataset[:, -1]
    return (X, y)

X, y = load_data('input3.csv')

# Stratified split test-train data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
estimator_svm = svm.SVC()

##############################
# SVM with linear kernel     #
##############################

# Searching for the best parameters in the model
parameters = {'kernel': ('linear',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
clf = GridSearchCV(estimator_svm, parameters, cv=5)
clf.fit(X_train, y_train)

print clf.best_estimator_
print clf.best_score_

# The chosen model
svc = clf.best_estimator_

# The score obtained using the test set
print svc.score(X_test, y_test)

##############################
# SVM with polynomial kernel #
##############################

# Searching for the best parameters in the model (Takes a while, uncomment for running this)
parameters = {'kernel': ('poly',), 'C': [0.1, 1, 3], 'degree': [4, 5, 6], 'gamma': [0.1, 1]}

clf = GridSearchCV(estimator_svm, parameters, cv=5)
clf.fit(X_train, y_train)

print clf.best_estimator_
print clf.best_score_

# The chosen model
svc_poly = clf.best_estimator_

# The score obtained using the test set
print svc_poly.score(X_test, y_test)

##############################
# SVM with RBF kernel        #
##############################

# Searching for the best parameters in the model
parameters = {'kernel': ('rbf',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}

clf = GridSearchCV(estimator_svm, parameters, cv=5)
clf.fit(X_train, y_train)

print clf.best_estimator_
print clf.best_score_

# The chosen model
svc_rbf = clf.best_estimator_

# The score obtained using the test set
print svc_rbf.score(X_test, y_test)


##############################
# Logistic Regression        #
##############################

# Searching for the best parameters in the model
parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
estimator_lr = LogisticRegression()
clf = GridSearchCV(estimator_lr, parameters, cv=5)
clf.fit(X_train, y_train)

print clf.best_estimator_
print clf.best_score_

# The chosen model
svc_lr = clf.best_estimator_

# The score obtained using the test set
print svc_lr.score(X_test, y_test)

##############################
# k-Nearest Neighbors        #
##############################

# Searching for the best parameters in the model
parameters = {'n_neighbors': xrange(1, 51), 'leaf_size': xrange(5, 61, 5)}
estimator_knn = KNeighborsClassifier()
clf = GridSearchCV(estimator_knn, parameters, cv=5)
clf.fit(X_train, y_train)

print clf.best_estimator_
print clf.best_score_

## The chosen model
svc_knn = clf.best_estimator_

## The score obtained using the test set
print svc_knn.score(X_test, y_test)

##############################
# Decision Trees             #
##############################

# Searching for the best parameters in the model
parameters = {'max_depth': xrange(1, 51), 'min_samples_split': xrange(2, 11)}
estimator_dt = DecisionTreeClassifier()
clf = GridSearchCV(estimator_dt, parameters, cv=5)
clf.fit(X_train, y_train)

print clf.best_estimator_
print clf.best_score_

# The chosen model
dt = clf.best_estimator_

# The score obtained using the test set
print dt.score(X_test, y_test)


##############################
# Random Forests             #
##############################

# Searching for the best parameters in the model
parameters = {'max_depth': xrange(1, 51), 'min_samples_split': xrange(2, 11)}
estimator_rf = RandomForestClassifier()
clf = GridSearchCV(estimator_rf, parameters, cv=5)
clf.fit(X_train, y_train)

print clf.best_estimator_
print clf.best_score_

# The chosen model
rf = clf.best_estimator_

## The score obtained using the test set
print rf.score(X_test, y_test)

