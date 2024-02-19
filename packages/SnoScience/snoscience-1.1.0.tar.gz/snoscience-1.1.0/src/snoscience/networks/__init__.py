"""
Main module containing the neural network.
"""

# Packages from requirements.
from numpy import round as numpy_round
from numpy import ndarray, random, argmax, arange, zeros

# Source package.
from ._neurons import Neuron
from ._layers import Layer, BasicLayer
from .._loss import mse_prime


class NeuralNetwork:
    """
    Neural network consisting of Layer instances.

    Supported activation functions: sigmoid.
    Supported loss functions: MSE.
    Supported optimisers: SGD.
    """
    _SUPPORTED = {
        "activation": ["sigmoid"],
        "loss": ["MSE"],
        "optimiser": ["SGD"]
    }

    _LOSS = {
        "MSE": mse_prime
    }

    def __init__(self, inputs: int, loss: str = "MSE", optimiser: str = "SGD"):
        self._inputs = inputs
        self._layers: list[Layer] = []
        self._outputs = 0

        # Ensure loss function is supported.
        if loss not in self._SUPPORTED["loss"]:
            raise ValueError(f"unsupported loss function: {loss}")
        else:
            self._loss = self._LOSS[loss]

        # Ensure optimiser is supported.
        if optimiser not in self._SUPPORTED["optimiser"]:
            raise ValueError(f"unsupported optimiser: {optimiser}")
        else:
            self._optimiser = optimiser

    def add_layer(self, neurons: int, activation: str = "sigmoid") -> None:
        """
        Add a layer to the neural network.

        Parameters
        ----------
        neurons: int
            Number of neurons to add to the layer.
        activation: str
            Activation function to use in the layer.
        """
        # Ensure activation function is supported.
        if activation not in self._SUPPORTED["activation"]:
            raise ValueError(f"unsupported activation function: {activation}")

        # Create new layer.
        layer = Layer(activation=activation)

        # Create input layer if no layers exist yet.
        if not self._layers:
            layer.previous = BasicLayer()

            # Neuron weights equal to inputs.
            weights = self._inputs
        else:
            layer.previous = self._layers[-1]

            # Neuron weights equal to neurons in previous layer.
            weights = len(self._layers[-1].neurons)

        layer.previous.next = layer
        layer.add_neurons(neurons=neurons, weights=weights)

        # Add new layer to network.
        self._layers.append(layer)

        # Assign outputs to verify dataset when predicting/training.
        self._outputs = neurons

    def predict(self, x: ndarray, classify: bool) -> ndarray:
        """
        Let the neural network predict the outputs from the given inputs.

        Parameters
        ----------
        x: ndarray
            Inputs for the network.
        classify: bool
            Create classification from output layer, otherwise keep regression.

        Returns
        -------
        ndarray:
            Output predictions from the network.
        """
        if x.shape[-1] != self._inputs:
            raise ValueError(f"expected inputs: {self._inputs}, got: {x.shape[-1]}")
        if not self._layers:
            raise ValueError("no layers present in network")

        # Assign inputs to input layer.
        self._layers[0].previous.y = x

        # Feedforward through network.
        for layer in self._layers:
            layer.calculate_x()
            layer.calculate_y()

        predictions = self._layers[-1].y

        # Create classification from output layer, otherwise keep regression.
        if classify:
            # Select likeliest case per row if multi classification.
            if predictions.shape[-1] > 1:
                # Select index with maximum value per row (if multiple first index is taken).
                maximums = argmax(predictions, axis=1)

                # Create new array with zeros.
                predictions = zeros(shape=predictions.shape)

                # Set indices with maximum elements to one.
                predictions[arange(predictions.shape[0]), maximums] = 1

            # Simply round outputs if binary classification.
            else:
                predictions = numpy_round(predictions)

        return predictions

    def train(self, x: ndarray, y: ndarray, epochs: int, samples: int, **kwargs) -> None:
        """
        Train the neural network with the given parameters.

        Parameters
        ----------
        x: ndarray
            Inputs to train the network with.
        y: ndarray
            Outputs to train the network with.
        epochs: int
            Number of training iterations.
        samples: int:
            Number of samples taken from the dataset per iteration.
        kwargs
            Optimiser hyperparameters as keyword arguments.
        """
        # Ensure method can be run with given inputs.
        if x.shape[-1] != self._inputs:
            raise ValueError(f"expected inputs: {self._inputs}, got: {x.shape[-1]}")
        if not self._layers:
            raise ValueError("no layers present in network")
        if y.shape[-1] != self._outputs:
            raise ValueError(f"expected outputs: {self._outputs}, got: {y.shape[-1]}")
        if samples > len(x):
            raise ValueError(f"number of samples cannot be larger than dataset: {len(x)}")

        # Ensure hyperparameters are given for selected optimiser.
        if self._optimiser == "SGD":
            if "rate" not in kwargs:
                raise KeyError("'rate' parameter required for SGD optimiser")

        # Create loss layer and link output layer to it.
        self._layers[-1].next = BasicLayer()

        for _ in range(epochs):
            # Select random section from dataset based on sample size.
            section = random.choice(a=len(x), size=samples, replace=False)
            section_x = x[section, :]
            section_y = y[section, :]

            # Assign inputs to input layer output.
            self._layers[0].previous.y = section_x

            # Feedforward all outputs for all layers in network.
            for layer in self._layers:
                layer.calculate_x()
                layer.calculate_y()
                layer.calculate_y_prime()

            # Calculate loss and link it to loss layer output derivative.
            self._layers[-1].next.y_prime = self._loss(calc=self._layers[-1].y, true=section_y)

            # Train all layers in network.
            for layer in self._layers:
                layer.train_neurons(optimiser=self._optimiser, **kwargs)
