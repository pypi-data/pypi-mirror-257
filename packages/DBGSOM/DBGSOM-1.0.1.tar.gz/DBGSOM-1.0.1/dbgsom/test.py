import cProfile

import pandas as pd

from sklearn.datasets import load_digits
from sklearn.preprocessing import scale
from sklearn.utils.estimator_checks import check_estimator
from dbgsom.dbgsom_ import DBGSOM

# type: ignore
# data = np.load("dbgsom\clusterable_data.npy")
data, _ = load_digits(return_X_y=True)

fashion_mnist = pd.read_csv(
    "F:\\Dokumente\\git\\fashion_mnist\\fashion-mnist_train.csv"
)

fashion_mnist_X = fashion_mnist.drop("label", axis=1)
fashion_mnist_y = fashion_mnist.label

# data = pd.read_csv
# ("F:\\Dokumente\\git\\fashion_mnist\\fashion-mnist_train.csv")
data = scale(data)

som = DBGSOM(
    max_iter=30,
    random_state=32,
    max_neurons=100,
    # decay_function="linear",
)

check_estimator(som)
# cProfile.run("som.fit(fashion_mnist_X)", sort="tottime")

som.fit(fashion_mnist_X, fashion_mnist_y)
# som.fit(data)
# print(len(som.neurons_))
