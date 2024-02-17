from typing import Any, Dict
from cyvidia_ai_utils.src.cross_validation.cross_validation_model.cross_validation_model import CrossValidationModel
from transformers import PreTrainedModel, Trainer,PreTrainedTokenizer, pipeline,PreTrainedTokenizerFast, TrainingArguments,DataCollatorWithPadding

class TransformerCrossValidationModel(CrossValidationModel):
    def __init__(self, model: PreTrainedModel, tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast, training_args: TrainingArguments):
        self.model = model
        self.tokenizer = tokenizer
        self.training_args= training_args
        
    def get_label_for_id(self, id: int)-> str:
        return self.model.config.id2label[id]

    def train(self, train_ds, val_ds):
        def preprocess_function(examples):
            return self.tokenizer(examples["text"], truncation=True)
    
        tokenized_train_ds = train_ds.map(preprocess_function, batched=True)
        tokenized_val_ds = val_ds.map(preprocess_function, batched=True)
        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        
        trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=tokenized_train_ds,
            eval_dataset=tokenized_val_ds,
            tokenizer=self.tokenizer,
            data_collator=data_collator,
        )
        
        trainer.train()
        
        self.model= trainer.model
        

    def predict_values(self, values)-> Dict[str,Any]:
        classifier= pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        
        return classifier(values)
