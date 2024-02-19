# SnoScience

A package optimised for building small neural networks.

![](https://i.postimg.cc/fy4kwbw6/epochs-200.jpg)

The MNIST dataset has been used for validation. Each network is trained by using 64 samples from this dataset per epoch for 200 epochs.
As can be seen from the graph, use Tensorflow or equivalent for networks with more than 3 layers (n>3) and/or more than 20 neurons per layer.
SnoScience networks with one (n=2) or no hidden layers (n=1) are extremely fast.

## Installation

To install the SnoScience package, run the following command:

```shell
pip install snoscience
```

Alternatively, install the package via your IDE.

## Usage

To get started with the SnoScience package, use the code example below:

```Python
from snoscience.networks import NeuralNetwork
from snoscience.metrics import calculate_mse, calculate_accuracy

# Define your dataset here.
x_train, y_train, x_test, y_test = [], [], [], []

# Create model with 1 hidden layer and 1 output layer (n=2).
model = NeuralNetwork(inputs=X, loss="MSE", optimiser="SGD")  # X features per sample
model.add_layer(neurons=2, activation="sigmoid")
model.add_layer(neurons=Y, activation="sigmoid")  # Y outputs per sample

# Define optimizer hyperparameters.
rate = 0.01

# Train model with training updates.
model.train(x=x_train, y=y_train, epochs=1000, samples=32, rate=rate, log=True)
# Or without.
model.train(x=x_train, y=y_train, epochs=1000, samples=32, rate=rate, log=False)

# Make predictions (classification).
y_calc = model.predict(x=x_test, classify=True)
 
# Make predictions (regression).
y_calc = model.predict(x=x_test, classify=False)

# Calculate performance.
mse = calculate_mse(calc=y_calc, true=y_test)
accuracy = calculate_accuracy(calc=y_calc, true=y_test)
```

## Features

#### SnoScience.networks module

1. The user is able to create a neural network capable of being trained and making predictions:
   1. this network is able to process an arbitrary number of inputs.
   2. this network can consist of an arbitrary number of layers.
   3. each layer in this network can consist of an arbitrary number of neurons.
2. The neural network supports the following activation functions:
   1. sigmoid.
3. The neural network supports the following loss functions:
   1. mean squared error (MSE).
4. The neural network supports the following optimisers:
   1. stochastic gradient descent (SGD).
5. The user can train the neural network with a single command:
   1. all inputs are checked for validity before the training proceeds.
6. The user can let the network make predictions with a single command:
   1. all inputs are checked for validity before predictions are given.
   2. these predictions can be regressions of an arbitrary size.
   3. these predictions can be classifications of an arbitrary size.

#### SnoScience.metrics module

1. The user is able to calculate the mean squared error of a regression.
2. The user is able to calculate the accuracy of a classification.

## Changelog

#### v1.1.0

- Build changed from Setuptools to Poetry.
- Revision of project structure.
- Revision of documentation.

#### v1.0.1

- Revision of project structure.
- Revision of documentation.

#### v1.0.0

- SnoScience.networks features 1 through 6 added.
- SnoScience.metrics features 1 and 2 added.

#### v0.1.0

- Initial release.
