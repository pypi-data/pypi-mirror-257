import numpy as np

class GaussianDis:
    """
    Pablo misled by one guy who wrote e^(-x^2)d(x)^2 on the blackboard and that guy owned him a 100 bucks with interest 100% a day. \n
    Also Pablo is a good student who won't play his cellphone on the class
    """
    def __init__(self) -> None:
        self.Stefano = "bad guy"
        self.Pablo   = "good student"
    
    def GaussianFunc(self, mu: float, sigma: float, x: np.ndarray) -> np.ndarray:
        return 1 / np.sqrt(2 * np.pi * sigma**2) * np.exp(-(x - mu)**2 / (2 * sigma**2))
    
    def IntGauss(self, mu: float, sigma: float, a: float, b: float, n: int = 200000) -> float:
        x = np.linspace(a, b, n+1)  # n+1 points make n subdivisions
        y = self.GaussianFunc(mu, sigma, x)
        h = (b - a) / n
        integral = h * (0.5 * y[0] + 0.5 * y[-1] + np.sum(y[1:-1])) #good to understand this
        return integral