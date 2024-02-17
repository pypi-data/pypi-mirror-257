from abc import abstractmethod
from enum import Enum
from typing import Any, Dict, Mapping, MutableMapping, Optional
from datasets import Dataset
import numpy as np
import json
import sklearn.metrics as metrics


class EvalAverageType(Enum):
    MICRO = "micro"
    MACRO = "macro"
    WEIGHTED = "weighted"
    BINARY= "binary"
    # SAMPLES= "samples"


class EvaluationResult:
    def __init__(
        self, 
        accuracy:float,
        f1_average: float,
        percision_average:float,
        per_label_f1: Mapping[str, float],
        per_label_percision: Mapping[str, float]
    ):
        self.accuracy = accuracy
        self.f1_average = f1_average
        self.percision_average = percision_average
        self.per_label_f1 = per_label_f1
        self.per_label_percision = per_label_percision
        
    @staticmethod
    def from_values(true_values, predictions, average: EvalAverageType):
        labels= list(set(true_values+ predictions))
        
        accuracy = metrics.accuracy_score(true_values, predictions)
        
        f1_average= metrics.f1_score(true_values, predictions, average=average.value)
        
        percision_average= metrics.precision_score(true_values, predictions, average=average.value)
        
        per_label_f1_list = metrics.f1_score(true_values, predictions, average=None, labels=labels)
        assert(isinstance(per_label_f1_list, np.ndarray))
        per_label_f1= dict(zip(labels, per_label_f1_list))
        
        per_label_percision_list = metrics.precision_score(true_values, predictions, average=None, labels=labels)
        assert(isinstance(per_label_percision_list, np.ndarray))
        per_label_percision= dict(zip(labels, per_label_percision_list))

        return EvaluationResult(
            accuracy=float(accuracy),
            f1_average=float(f1_average),
            percision_average=float(percision_average),
            per_label_f1=per_label_f1,
            per_label_percision=per_label_percision
        )
        
    def to_json(self)-> str:
        return json.dumps({
            "accuracy": self.accuracy,
            "f1_average": self.f1_average,
            "percision_average": self.percision_average,
            "per_label_f1": self.per_label_f1,
            "per_label_percision": self.per_label_percision
        })
    
    @staticmethod
    def aggregate(results: list['EvaluationResult'])-> 'EvaluationResult':
        accuracy= np.mean([result.accuracy for result in results])
        f1_average= np.mean([result.f1_average for result in results])
        percision_average= np.mean([result.percision_average for result in results])
        
        per_label_f1= {}
        per_label_percision= {}
        
        for result in results:
            for label, f1 in result.per_label_f1.items():
                if label in per_label_f1:
                    per_label_f1[label] += f1
                else:
                    per_label_f1[label] = f1
            for label, percision in result.per_label_percision.items():
                if label in per_label_percision:
                    per_label_percision[label] += percision
                else:
                    per_label_percision[label] = percision
        
        for label in per_label_f1:
            per_label_f1[label] /= len(results)
        for label in per_label_percision:
            per_label_percision[label] /= len(results)
        
        return EvaluationResult(
            accuracy=float(accuracy),
            f1_average=float(f1_average),
            percision_average=float(percision_average),
            per_label_f1=per_label_f1,
            per_label_percision=per_label_percision
        )

    def __str__(self):
        return f"Accuracy: {self.accuracy}, F1: {self.f1_average}, Percision: {self.percision_average}"
