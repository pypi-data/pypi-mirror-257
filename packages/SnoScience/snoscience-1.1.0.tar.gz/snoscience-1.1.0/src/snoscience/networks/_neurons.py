"""
Submodule containing the neural network neuron classes.
"""

# Packages from requirements.
from numpy import array, matmul, ndarray, random

# Source package.
from .._activation import sigmoid, sigmoid_prime


class Neuron:
    """
    Neuron with activation functions.
    """
    def __init__(self, weights: int):
        """
        Parameters
        ----------
        weights: int
            Number of weights to add to the neuron.
        """
        self.x = array([0.0])
        self.y = array([0.0])
        self.y_prime = array([0.0])

        self.weights = 0.01 * random.random(size=(weights, 1))
        self.bias = 0.01 * random.rand()
        self.position = 0

        self.total_weights = array([0.0])
        self.total_bias = 0.0

        self.optimiser = {
            "SGD": self.sgd
        }

        self.activation = {
            "sigmoid": {
                "function": sigmoid,
                "derivative": sigmoid_prime
            }
        }

    def calculate_x(self, previous: ndarray) -> None:
        """
        Calculate the neuron input float based on the output of the previous layer.

        Parameters
        ----------
        previous: ndarray
            Output from the previous layer.
        """
        self.x = matmul(previous, self.weights) + self.bias

    def calculate_y(self, activation: str) -> None:
        """
        Calculate the neuron output vector based on its current input.

        Parameters
        ----------
        activation: str
            Activation function to be used.
        """
        self.y = self.activation[activation]["function"](x=self.x)

    def calculate_y_prime(self, activation: str) -> None:
        """
        Calculate the neuron output derivative vector based on its current input.

        Parameters
        ----------
        activation: str
            Activation function to be used.
            Supported functions: sigmoid.
        """
        self.y_prime = self.activation[activation]["derivative"](x=self.x)

    def train(self, optimiser: str, **kwargs) -> None:
        """
        Train the neuron based on the given optimiser.

        Parameters
        ----------
        optimiser: str
            Optimiser to train the neuron with.
        kwargs
            Optimiser hyperparameters as keyword arguments.
        """
        self.optimiser[optimiser](**kwargs)

    def sgd(self, rate: float) -> None:
        """
        Train the neuron based on the stochastic gradient descent method.

        Parameters
        ----------
        rate: float
            Learning rate.
        """
        self.bias = self.bias - (rate * self.total_bias)
        self.weights = self.weights - (rate * self.total_weights)
