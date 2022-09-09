import numpy as np
from abc import ABCMeta, abstractmethod
from scipy.integrate import quad


class __model__(metaclass=ABCMeta):
    def __init__(self, args: dict):
        for key, value in args.items():
            setattr(self, key, value)

        # stores the model output
        self.val = None

    @abstractmethod
    def compute():
        # computation routine of the model
        # can be invoked manually
        return NotImplemented


class gEUD(__model__):
    # main reference: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5768006/
    def __init__(self, volume: np.ndarray, dose: np.ndarray, a: float):
        super().__init__(locals())
        self.val = self.compute()

    def compute(self):
        vol_proportion = self.volume / np.sum(self.volume)
        res = np.sum(np.multiply(vol_proportion, np.power(self.dose, self.a)))**(1/self.a)
        self.val = res
        return res


class LKB(__model__):
    # main reference: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216137/
    def __init__(self, D50: float, m: float, volume: np.ndarray, dose: np.ndarray, a: float):
        super().__init__(locals())
        self.gEUD_model = gEUD(volume=self.volume, dose=self.dose, a=self.a)
        self.val = self.compute()

    def compute(self):
        t = (1 / self.m) * (self.gEUD_model.val / self.D50 - 1) 
        res = quad(lambda u: np.exp(-(u**2)/2)  / ((2*np.pi)**(0.5)) , -np.inf, t)
        self.val = res
        return res
        
class RS(__model__):
    # main reference: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4216137/
    def __init__(self, dose: np.ndarray, volume: np.ndarray, D50: float, gamma: float, seriality: float):
        super().__init__(locals())
        self.PDi_func = np.vectorize(lambda d: 2**(-np.exp(np.exp(1) * self.gamma * (1 - d / self.D50))))
        self.val = self.compute()

    def compute(self):
        self.PDi = self.PDi_func(self.dose)
        vol_proportion = self.volume / np.sum(self.volume)
        prod = np.prod(np.power(1 - np.power(self.PDi, self.seriality), vol_proportion))
        res = (1 - prod)**(1/self.seriality)
        self.val = res
        return res
