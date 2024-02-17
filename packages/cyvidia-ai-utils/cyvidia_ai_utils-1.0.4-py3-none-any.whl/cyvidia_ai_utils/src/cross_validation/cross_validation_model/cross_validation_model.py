from abc import abstractmethod
from typing import Any, Dict
from datasets import Dataset


class CrossValidationModel:
    """Implement this interface to create a model that can be cross-validated."""
    @abstractmethod
    def train(self, train_ds: Dataset, val_ds:Dataset)-> 'CrossValidationModel':
        """Train the model using the given dataset and return the trained model."""
        pass
    
    @abstractmethod
    def predict_values(self, values)-> list[Dict[str,Any]]:
        '''Return the predicted values for the given input values.
        return looks like `[{"label": "POSITIVE", "score": 0.9999}, {"label": "NEGATIVE", "score": 0.7001}]`
        '''
        pass

    @abstractmethod
    def get_label_for_id(self, id: int)-> str:...
        