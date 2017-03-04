import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
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

# Best models obtained using k-fold cross-validation with k = 5
svc = SVC(C=0.1, cache_size=200, class_weight=None, coef0=0.0,
          decision_function_shape=None, degree=3, gamma='auto', kernel='linear',
          max_iter=-1, probability=False, random_state=None, shrinking=True,
          tol=0.001, verbose=False).fit(X_train, y_train)


poly_svc = SVC(C=0.1, cache_size=200, class_weight=None, coef0=0.0,
                decision_function_shape=None, degree=6, gamma=1, kernel='poly',
                max_iter=-1, probability=False, random_state=None, shrinking=True,
                tol=0.001, verbose=False).fit(X_train, y_train)

rbf_svc = SVC(C=10, cache_size=200, class_weight=None, coef0=0.0,
                decision_function_shape=None, degree=3, gamma=10, kernel='rbf',
                max_iter=-1, probability=False, random_state=None, shrinking=True,
                tol=0.001, verbose=False).fit(X_train, y_train)

log_reg = LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False).fit(X_train, y_train)

knn = KNeighborsClassifier(algorithm='auto', leaf_size=5, metric='minkowski',
                           metric_params=None, n_jobs=1, n_neighbors=4, p=2,
                           weights='uniform').fit(X_train, y_train)

dec_trees = DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=7,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best').fit(X_train, y_train)

rf =    RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
        max_depth=22, max_features='auto', max_leaf_nodes=None,
        min_impurity_split=1e-07, min_samples_leaf=1,
        min_samples_split=5, min_weight_fraction_leaf=0.0,
        n_estimators=10, n_jobs=1, oob_score=False, random_state=None,
        verbose=0, warm_start=False).fit(X_train, y_train)

# create a mesh to plot in
h = .02  # step size in the mesh
x_min, x_max = X_test[:, 0].min() - 1, X_test[:, 0].max() + 1
y_min, y_max = X_test[:, 1].min() - 1, X_test[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# title for the plots
titles = ['SVC with linear kernel',
          'SVC with polynomial (degree 6) kernel',
          'SVC with RBF kernel',
          'Logistic Regression',
          'k-Nearest Neighbors (4 neighbors)',
          'Decision Trees']

plt.figure(1)
for i, clf in enumerate((svc, poly_svc, rbf_svc, log_reg, knn, dec_trees)):
    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    plt.subplot(2, 3, i + 1)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot also the training points
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.coolwarm)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())
    plt.title(titles[i])


# Here we plot results obtained with random forests
plt.figure(2)
Z = rf.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

# Plot also the training points
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=plt.cm.coolwarm)
plt.xlabel('X1')
plt.ylabel('X2')
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.xticks(())
plt.yticks(())
plt.title('Random Forests')

plt.show()


