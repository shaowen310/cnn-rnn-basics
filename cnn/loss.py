import numpy as np


class Loss(object):

    def __init__(self):
        self.trainable = False  # Whether there are parameters in this layer that can be trained
        self.training = False  # The phrase, if for training then true

    def forward(self, inputs, targets):
        """Forward pass, reture outputs"""
        raise NotImplementedError

    def backward(self, inputs, targets):
        """Backward pass, return gradients to inputs"""
        raise NotImplementedError

    def set_mode(self, training):
        """Set the phrase/mode into training (True) or tesing (False)"""
        self.training = training


class SoftmaxCrossEntropy(Loss):
    def __init__(self, num_class):
        """Initialization

        # Arguments
            num_class: int, the number of category
        """
        super(SoftmaxCrossEntropy, self).__init__()
        self.num_class = num_class

    def forward(self, inputs, targets):
        """Forward pass

        # Arguments
            inputs: numpy array with shape (batch, num_class)
            targets: numpy array with shape (batch,)

        # Returns
            outputs: float, batch loss
            probs: numpy array with shape (batch, num_class), probability to each category with respect to each image
        """
        probs = self.__softmax(inputs)

        batch = inputs.shape[0]
        batch_loss = -np.log(probs[range(batch), targets])
        outputs = np.sum(batch_loss) / batch

        return outputs, probs

    def backward(self, inputs, targets):
        """Backward pass

        # Arguments
            inputs: numpy array with shape (batch, num_class), same with forward inputs
            targets: numpy array with shape (batch,), same eith forward targets

        # Returns
            out_grads: numpy array with shape (batch, num_class), gradients to inputs 
        """
        out_grads = self.__softmax(inputs)

        batch = inputs.shape[0]
        out_grads[range(batch), targets] -= 1
        out_grads /= batch

        return out_grads

    def __softmax(self, inputs):
        exp_inputs = np.exp(inputs.T)
        return (exp_inputs / exp_inputs.sum(axis=0)).T


class L2(Loss):
    def __init__(self, w=0.01):
        """Initialization

        # Arguments
            w: float, weight decay ratio.
        """
        self.w = w

    def forward(self, params):
        """Forward pass

        # Arguments
            params: dictionary, store all weights of the whole model

        # Returns
            outputs: float, L2 regularization loss
        """
        loss = 0
        for _, v in params.items():
            loss += np.sum(v**2)
        outputs = 0.5 * self.w * loss
        return outputs

    def backward(self, params):
        """Backward pass

        # Arguments
            params: dictionary, store all weights of the whole model

        # Returns
            out_grads: dictionary, gradients to each weights in params 
        """
        out_grads = {}
        for k, v in params.items():
            out_grads[k] = self.w * params[k]
        return out_grads
