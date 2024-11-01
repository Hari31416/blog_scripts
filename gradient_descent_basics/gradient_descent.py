import numpy as np
from typing import Callable, Optional, Union, Dict, Tuple


class GradientDescent:
    """Implements the gradient descent algorithm.

    Attributes
    ----------
    func : Callable
        The function to be minimized.
    grad_func : Callable
        The gradient of the function. Either `func` or `grad_func` must be provided.

    Methods
    -------
    optimize(start=None, lr=0.1, max_iter=100, eps=1e-6)
        Optimize the function using gradient descent
    """

    def __init__(
        self,
        func: Optional[Callable],
        grad_func: Optional[Callable],
    ):
        if func is None and grad_func is None:
            raise ValueError("Either func or grad_func must be provided")

        self.func = func
        self.grad_func = grad_func

    def _get_gradient(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        if self.grad_func is not None:
            return self.grad_func(x)
        else:
            # use central difference if gradient is not provided
            eps = 1e-5
            return (self.func(x + eps) - self.func(x - eps)) / (2 * eps)

    def optimize(
        self,
        start: Union[float, np.ndarray] = None,
        lr: float = 0.1,
        max_iter: int = 100,
        eps: float = 1e-6,
        shape: Optional[Tuple[int]] = None,
    ) -> Tuple[Union[float, np.ndarray], Dict]:
        """Optimize the function using gradient descent.

        Parameters
        ----------
        start : Union[float, np.ndarray]
            The starting point for the optimization.
        lr : float
            The learning rate.
        max_iter : int
            The maximum number of iterations
        eps : float
            The convergence threshold.
        shape : Tuple[int]
            The shape of the starting point if it is not provided. If start is provided, this is ignored, otherwise a random array with this shape is generated. If neither start nor shape is provided, a random float is generated.

        Returns
        -------
        Union[float, np.ndarray]
            The optimized value of x.
        Dict
            A dictionary containing the history of the optimization.
        """
        history = []

        # generate random starting point if not provided
        if start is None:
            # if shape is provided, generate random array with that shape
            if shape is not None:
                x = np.random.randn(*shape)
            # otherwise, generate random float
            else:
                x = np.random.randn()
        else:
            x = start

        # iterate until convergence
        converged = False
        for i in range(max_iter):
            # get gradient
            grad = self._get_gradient(x)
            # calculate delta that needs to be subtracted from x
            delta = lr * grad

            # convert delta to numpy array if it is not already
            # this is done to allow for both scalar and array inputs
            if not isinstance(delta, np.ndarray):
                delta = np.array([delta])

            # check for convergence, break if converged
            if np.linalg.norm(delta) < eps:
                converged = True
                print(f"Converged in {i} iterations. Breaking...")
                break

            # do the same for x
            if not isinstance(x, np.ndarray):
                x = np.array([x])

            # update x
            x = x - delta

            # save history
            hist = {"x": x, "grad": grad}
            history.append(hist)

        if not converged:
            print(f"Not converged after {max_iter} iterations.")

        return x, history
