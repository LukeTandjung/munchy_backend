from abc import ABC, abstractmethod
import pandas as pd

class AbstractMetaFeature(ABC):
    @abstractmethod
    def compute(self, data: pd.DataFrame) -> pd.DataFrame:
        pass