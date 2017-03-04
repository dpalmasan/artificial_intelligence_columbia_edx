import numpy as np
import matplotlib.pyplot as plt
import sys

def f(x):
    return 1 if x > 0 else -1

def draw(X, y, w):
    """
    This function creates a plot in which the current decision boundary is shown.
    It allows to see which points are misclassified and how the process is done.
    """

    for i in xrange(X.shape[0]):
        if y[i] == 1:
            plt.plot(X[i, 0], X[i, 1], 'ro')
        else:
            plt.plot(X[i, 0], X[i, 1], 'bx')
    
    xmin = X.min(axis=0)
    xmax = X.max(axis=0)
    
    xx = [xmin[0] - 1, xmax[0] + 1]
    yy = -(w[2] + w[0]*xx)/w[1]
    plt.plot(xx, yy, 'k')
    plt.axis([xmin[0] - 1, xmax[0] + 1, xmin[1] - 1, xmax[1] + 1])    
    plt.show()

def PLA(X, y, output_file, animate=False):
    """
    Implements Perceptron Learning Algorithm
    Returns a list of weights, that represent the hyperplane that separates the data
    linearly
    """
    d = X.shape[1]
    w = np.zeros((d + 1, 1))
    conv = False

    open(output_file, 'w').close()
    while not conv:
        conv = True
        for i in xrange(X.shape[0]):
            if y[i]*f(w[-1] + np.dot(X[[i], :], w[:-1, [0]])) <= 0:
                w[-1] = w[-1] + y[i]
                w[:-1, [0]] = w[:-1, [0]] + y[i]*np.transpose(X[[i], :])
                conv = False

        if animate:
            draw(X, y, w)
    
        with open(output_file, "a") as text_file:
            for wi in w:
                if wi[0].is_integer():
                    text_file.write(str(int(wi[0])) + ",")
                else:
                    text_file.write(str(wi[0]) + ",")
            text_file.write("\n")

    return w

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python <input.csv> <output.csv>'
        sys.exit(0)

    dataset = np.genfromtxt(sys.argv[1], delimiter=',', skip_header=0, names=None)

    X = dataset[:, [0, 1]]
    y = dataset[:, [2]]

    # True for debugging and visualizing the decision boundary
    w = PLA(X, y, sys.argv[2], False)
    
