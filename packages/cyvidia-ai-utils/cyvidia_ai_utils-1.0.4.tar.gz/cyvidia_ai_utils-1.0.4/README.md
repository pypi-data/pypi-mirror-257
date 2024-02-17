## ai-utils

### Installation

```bash
pip install cyvidia-ai-utils
```

### Cross validation

#### Huggingface Trainer API

```python
from cyvidia_ai_utils import TransformerCrossValidationModel, cross_validate, EvaluationResult
from transformers import AutoTokenizer, AutoModelForSequenceClassification,TrainingArguments
from datasets import load_dataset, Dataset
from transformers import DataCollatorWithPadding,Trainer

folds = load_dataset("dipesh/Intent-Classification-small",split=[f"train[{k}%:{k+10}%]" for k in range(0, 100, 10)])
assert(isinstance(folds, list))

def create_model():
    model = AutoModelForSequenceClassification.from_pretrained("prajjwal1/bert-tiny", num_labels=21)
    tokenizer= AutoTokenizer.from_pretrained("prajjwal1/bert-tiny")

    return TransformerCrossValidationModel(
        model= model,
        tokenizer= tokenizer,
        training_args= TrainingArguments(
            output_dir=f'tests/test_models/{uuid.uuid4()}',
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=0.001,
            weight_decay=0.01,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
    )

# folds can either be a list of Dataset's or a dictionary of label to Dataset
folds_dict= {f"train[{k}%:{k+10}%]": fold for k, fold in enumerate(folds)}
results=cross_validate(create_model, folds_dict, target_id_column="label", input_text_column="text")



aggragated_result= EvaluationResult.aggregate(list(results.values()))

```

#### Custom Trainer

```python
from cyvidia_ai_utils import CrossValidationModel

class MyCustomCrossValidationModel(CrossValidationModel):
    def get_label_for_id(self, id: int)-> str:
        # Implement

    def train(self, train_ds, val_ds)-> CrossValidationModel:
        # Implement

    def predict_values(self, values)-> Dict[str,Any]:
        # Implement


def create_model():
    return MyCustomCrossValidationModel()

results= cross_validate(create_model, folds, target_id_column="label", input_text_column="text")
```
