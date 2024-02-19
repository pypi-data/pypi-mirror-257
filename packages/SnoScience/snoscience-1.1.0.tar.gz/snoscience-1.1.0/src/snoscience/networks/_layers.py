"""
Submodule containing the neural network layer classes.
"""

# Default Python packages.
from typing import Optional, Union

# Packages from requirements.
from numpy import sum as numpy_sum
from numpy import array, hstack, ndarray, zeros

# Source package.
from ._neurons import Neuron


class BasicLayer:
    """
    Input or loss layers.
    """
    def __init__(self):
        self.y = array([0.0])
        self.y_prime = array([0.0])

        self.previous: Optional[BasicLayer, Layer] = None
        self.next: Optional[BasicLayer, Layer] = None


class Layer(BasicLayer):
    """
    Hidden or output layers consisting of Neuron instances.
    """
    def __init__(self, activation: str):
        """
        Parameters
        ----------
        activation: str
            Applied activation functions for neurons in this layer.
        """
        super().__init__()

        self.previous: Union[BasicLayer, Layer] = BasicLayer()
        self.next: Union[BasicLayer, Layer] = BasicLayer()

        self.activation = activation
        self.neurons: list[Neuron] = []

    def add_neurons(self, neurons: int, weights: int) -> None:
        """
        Add neurons to this layer.

        Parameters
        ----------
        neurons: int
            Number of neurons to add to this layer.
        weights: int
            Number of weights per neuron.
        """
        self.neurons = [Neuron(weights=weights) for _ in range(neurons)]

        for i, neuron in enumerate(self.neurons):
            neuron.position = i

    def train_neurons(self, optimiser: str, **kwargs) -> None:
        """
        Run the "train" method for each neuron in this layer.

        Parameters
        ----------
        optimiser: str
            Optimiser to train the neurons with.
        kwargs
            Optimiser hyperparameters as keyword arguments.
        """
        if optimiser == "SGD":
            self.calculate_total()

        for neuron in self.neurons:
            neuron.train(optimiser=optimiser, **kwargs)

    def calculate_x(self) -> None:
        """
        Run the "calculate_x" method for each neuron in this layer.
        """
        for neuron in self.neurons:
            neuron.calculate_x(previous=self.previous.y)

    def calculate_y(self) -> None:
        """
        Run the "calculate_y" method for each neuron in this layer.
        Afterward, stack all vectors to create an output array.
        """
        for neuron in self.neurons:
            neuron.calculate_y(activation=self.activation)

        self.y = hstack(tup=[neuron.y for neuron in self.neurons])

    def calculate_y_prime(self) -> None:
        """
        Run the "calculate_y_prime" method for each neuron in this layer.
        """
        for neuron in self.neurons:
            neuron.calculate_y_prime(activation=self.activation)

    def calculate_total(self) -> None:
        """
        Calculate the total derivative vector for the neurons in this layer.
        This is a prerequisite for the SGD optimiser.
        """
        for neuron in self.neurons:
            # Recursively go through subsequent layers to get total derivative vector.
            total = self.calculate_total_neuron(neuron=neuron, start=neuron,
                                                position=neuron.position)

            # Set total derivative vector for neuron weights.
            neuron.total_weights = numpy_sum(total * self.previous.y, axis=0).reshape(-1, 1)
            # Set total derivative float for neuron bias.
            neuron.total_bias = numpy_sum(total)

    def calculate_total_layer(self, start: Neuron, position: int) -> ndarray:
        """
        Calculate the total derivative vector for the layer.
        This is used by the "calculate_total" method to start recursion,
        and by the "calculate_total_neuron" method to continue recursion.
        """
        # Start with zero array and ensure total and input shapes match.
        total = zeros(shape=start.x.shape)

        for neuron in self.neurons:
            total = total + self.calculate_total_neuron(neuron=neuron, start=start,
                                                        position=position)

        return total

    def calculate_total_neuron(self, neuron: Neuron, start: Neuron, position: int) -> ndarray:
        """
        Calculate the total derivative vector for a neuron.
        This is used by the "calculate_total_layer" method to start/continue recursion.
        """
        # Return loss derivative when loss layer is reached.
        if isinstance(self.next, BasicLayer) and not isinstance(self.next, Layer):
            total = neuron.y_prime * self.next.y_prime[:, neuron.position].reshape(-1, 1)

        # For all other layers, start/continue recursion.
        else:
            # Apply chain rule if neuron is not equal to start neuron.
            initial = (neuron.y_prime * neuron.weights[position, 0] if start != neuron
                       else neuron.y_prime)

            # Multiply totals from subsequent recursions and add them to current total.
            middle = self.next.calculate_total_layer(start=start, position=neuron.position)
            total = initial * middle

        return total
