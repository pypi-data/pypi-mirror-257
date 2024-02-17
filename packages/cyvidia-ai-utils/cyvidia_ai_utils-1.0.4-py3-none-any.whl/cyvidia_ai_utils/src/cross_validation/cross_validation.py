from typing import  Dict, Mapping, Callable
from datasets import Dataset,concatenate_datasets
from cyvidia_ai_utils.src.cross_validation.cross_validation_model.cross_validation_model import CrossValidationModel
from cyvidia_ai_utils.src.cross_validation.evaluation_result import EvalAverageType, EvaluationResult
import pandas as pd
def cross_validate(
    create_model_instance: Callable[[],CrossValidationModel],
    folds: list[Dataset] | Mapping[str, Dataset],
    target_id_column:str,
    input_text_column:str,
    train_only_folds: list[Dataset]= [],
    average: EvalAverageType= EvalAverageType.WEIGHTED
):
    """Cross validate the model using the given folds and target column.
    Returns a dictionary of validation fold index to evaluation result.
    """
    if isinstance(folds, Mapping):
        fold_list: list[Dataset]=[]
        fold_labels:list[str]=[]
        
        for label, fold in folds.items():
            fold_list.append(fold)
            fold_labels.append(label)
    else:
        fold_list= folds
        fold_labels= [str(i) for i in range(len(folds))]
        
    results: Dict[str, EvaluationResult] = {}
    for i, val_ds in enumerate(fold_list):
        train_folds = fold_list[:i] + fold_list[i+1:]+ train_only_folds
        
        train_ds= concatenate_datasets(train_folds)
        
        model= create_model_instance()
        model.train(train_ds, val_ds)
        result= __evaluate_model(model, val_ds, target_column=target_id_column, input_column=input_text_column, average=average)
        print(f"Fold {fold_labels[i]} result: {result.to_json()}")
        results[fold_labels[i]] = result
    return results

def __evaluate_model(model: 'CrossValidationModel',test_ds_in: Dataset,input_column:str, target_column:str, average: EvalAverageType= EvalAverageType.WEIGHTED)-> EvaluationResult:
    test_df=test_ds_in.to_pandas()
    
    assert(isinstance(test_df, pd.DataFrame))
    test_df= test_df.drop_duplicates(subset=[input_column]).reset_index(drop=True)
    
    test_ds= Dataset.from_pandas(test_df, preserve_index=False)

    predictions_with_scores= model.predict_values(test_ds[input_column])

    predictions= [pred['label'] for pred in predictions_with_scores]
        
    true_values = list(map(lambda x: model.get_label_for_id(x), test_ds[target_column]))
    
    if len(true_values) != len(predictions):
        raise ValueError(f"The number of true values and predictions must be the same: {len(true_values)} != {len(predictions)}")

    if len(true_values)== 0:
        raise ValueError(f"The number of true values and predictions must be greater than 0. Length of test_ds: {len(test_ds)}")
    return EvaluationResult.from_values(true_values, predictions, average)          
        