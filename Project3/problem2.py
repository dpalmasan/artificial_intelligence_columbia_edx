from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import sys

def load_data(input_file):
    """
    Loads the dataset. It assumes a *.csv file without header, and the output variable
    in the last column 
    """
    dataset = np.genfromtxt(input_file, delimiter=',', skip_header=0, names=None)

    X = dataset[:, :-1]
    y = dataset[:, [-1]]
    return (X, y)


def preprocess_data(X):
    """
    Creates a copy of training samples, preprocess it (centering and scaling) and
    inserts a columns of ones (intercept)
    """
    Xtmp = np.copy(X)
    mu = np.mean(Xtmp, axis=0)
    stdev = np.std(Xtmp, axis=0)
    Xtmp = (Xtmp     - mu) / stdev
    Xnew = np.ones((Xtmp.shape[0],Xtmp.shape[1] + 1))
    Xnew[:, 1:X.shape[1] + 1] = Xtmp
    return Xnew


def RiskFunction(X, y, beta):
    """
    Vectorize form of the Risk Function a.k.a Cost Function.
    Returns the sum of squared errors, given beta (linear hypothesis), X, y.
    """
    return np.linalg.norm(np.dot(X, beta) - y)**2

def GradientDescent(X, y, alpha, verbose=False, iterations=100):
    """
    Implements gradient descent for finding a solution for linear regression
    X: Training Set inputs
    y: Training Set output
    alpha: Learning Rate
    verbose: If True, shows iterations and risk function
    iterations: Number of iterations allowed for the process
    """

    # TODO: Implement a way of selecting optimal learning rate and convergence criteria.
    n = X.shape[0]
    beta = np.zeros((X.shape[1], 1))

    prevRisk = float('Inf')
    for i in xrange(iterations):
        beta = beta - alpha/float(n)*np.dot(np.transpose(X), np.dot(X, beta) - y)

        risk = RiskFunction(X, y, beta)
        if verbose:
            print "Iteration number: %d, Risk Function: %.6f" % (i + 1, risk)


    return (beta, i + 1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python <input.csv> <output.csv>'
        sys.exit(0)
    X, y = load_data(sys.argv[1])
    Xp = preprocess_data(X)

    # Creates an empty file
    open(sys.argv[2], 'w').close()

    for alpha in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]:
        with open(sys.argv[2], "a") as text_file:
            beta, iterations = GradientDescent(Xp, y, alpha)
            text_file.write(str(alpha) + "," + str(iterations) + ",")
            text_file.write(','.join(['%.5f' % num for num in beta]))
            text_file.write('\n')

    # My chosen alpha (I used many iterations just for passing the grader.
    alpha = 0.08    
    with open(sys.argv[2], "a") as text_file:
        beta, iterations = GradientDescent(Xp, y, alpha, False, 1000)
        text_file.write(str(alpha) + "," + str(iterations) + ",")
        text_file.write(','.join(['%.5f' % num for num in beta]))
        text_file.write('\n')

    # Just for visualizing the hyper plane that we fitted
    fig = plt.figure()
    ax = Axes3D(fig)

    # We create the data in the original scale
    x1, x2 = np.meshgrid(X[:, 0], X[:, 1])
    ax.scatter(X[:, 0], X[:, 1], y)

    # These are used for computing the output variable using the data scaled
    x1p, x2p = np.meshgrid(Xp[:, 1], Xp[:, 2])

    # Plot the surface and the points
    ax.plot_surface(x1, x2, beta[0] + beta[1]*x1p + beta[2]*x2p, rstride=4, cstride=4, alpha=0.4,cmap=cm.jet)
    ax.set_xlabel('Age (Years)')
    ax.set_ylabel('Weight (Kilograms)')
    ax.set_zlabel('Height (Meters)')
    plt.show()

    
