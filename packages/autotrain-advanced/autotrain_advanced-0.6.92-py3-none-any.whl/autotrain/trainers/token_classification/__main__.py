import argparse
import json
from functools import partial

from accelerate.state import PartialState
from datasets import load_dataset, load_from_disk
from huggingface_hub import HfApi
from transformers import (
    AutoConfig,
    AutoModelForTokenClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

from autotrain import logger
from autotrain.trainers.common import monitor, pause_space, remove_autotrain_data, save_training_params
from autotrain.trainers.token_classification import utils
from autotrain.trainers.token_classification.dataset import TokenClassificationDataset
from autotrain.trainers.token_classification.params import TokenClassificationParams


def parse_args():
    # get training_config.json from the end user
    parser = argparse.ArgumentParser()
    parser.add_argument("--training_config", type=str, required=True)
    return parser.parse_args()


@monitor
def train(config):
    if isinstance(config, dict):
        config = TokenClassificationParams(**config)

    if config.repo_id is None and config.username is not None:
        config.repo_id = f"{config.username}/{config.project_name}"

    if PartialState().process_index == 0:
        logger.info("Starting training...")
        logger.info(f"Training config: {config}")

    train_data = None
    valid_data = None
    # check if config.train_split.csv exists in config.data_path
    if config.train_split is not None:
        if config.data_path == f"{config.project_name}/autotrain-data":
            logger.info("loading dataset from disk")
            train_data = load_from_disk(config.data_path)[config.train_split]
        else:
            train_data = load_dataset(
                config.data_path,
                split=config.train_split,
                token=config.token,
            )

    if config.valid_split is not None:
        if config.data_path == f"{config.project_name}/autotrain-data":
            logger.info("loading dataset from disk")
            valid_data = load_from_disk(config.data_path)[config.valid_split]
        else:
            valid_data = load_dataset(
                config.data_path,
                split=config.valid_split,
                token=config.token,
            )

    label_list = train_data.features[config.tags_column].feature.names
    num_classes = len(label_list)

    model_config = AutoConfig.from_pretrained(config.model, num_labels=num_classes)
    model_config._num_labels = num_classes
    model_config.label2id = {l: i for i, l in enumerate(label_list)}
    model_config.id2label = dict(enumerate(label_list))

    try:
        model = AutoModelForTokenClassification.from_pretrained(
            config.model,
            config=model_config,
            trust_remote_code=True,
            token=config.token,
            ignore_mismatched_sizes=True,
        )
    except OSError:
        model = AutoModelForTokenClassification.from_pretrained(
            config.model,
            config=model_config,
            from_tf=True,
            trust_remote_code=True,
            token=config.token,
            ignore_mismatched_sizes=True,
        )

    if model_config.model_type in {"bloom", "gpt2", "roberta"}:
        tokenizer = AutoTokenizer.from_pretrained(
            config.model, token=config.token, trust_remote_code=True, add_prefix_space=True
        )
    else:
        tokenizer = AutoTokenizer.from_pretrained(config.model, token=config.token, trust_remote_code=True)

    train_data = TokenClassificationDataset(data=train_data, tokenizer=tokenizer, config=config)
    if config.valid_split is not None:
        valid_data = TokenClassificationDataset(data=valid_data, tokenizer=tokenizer, config=config)

    if config.logging_steps == -1:
        if config.valid_split is not None:
            logging_steps = int(0.2 * len(valid_data) / config.batch_size)
        else:
            logging_steps = int(0.2 * len(train_data) / config.batch_size)
        if logging_steps == 0:
            logging_steps = 1

    else:
        logging_steps = config.logging_steps

    training_args = dict(
        output_dir=config.project_name,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=2 * config.batch_size,
        learning_rate=config.lr,
        num_train_epochs=config.epochs,
        evaluation_strategy=config.evaluation_strategy if config.valid_split is not None else "no",
        logging_steps=logging_steps,
        save_total_limit=config.save_total_limit,
        save_strategy=config.save_strategy,
        gradient_accumulation_steps=config.gradient_accumulation,
        report_to=config.log,
        auto_find_batch_size=config.auto_find_batch_size,
        lr_scheduler_type=config.scheduler,
        optim=config.optimizer,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        max_grad_norm=config.max_grad_norm,
        push_to_hub=False,
        load_best_model_at_end=True if config.valid_split is not None else False,
        ddp_find_unused_parameters=False,
    )

    if config.mixed_precision == "fp16":
        training_args["fp16"] = True
    if config.mixed_precision == "bf16":
        training_args["bf16"] = True

    if config.valid_split is not None:
        early_stop = EarlyStoppingCallback(early_stopping_patience=3, early_stopping_threshold=0.01)
        callbacks_to_use = [early_stop]
    else:
        callbacks_to_use = []

    args = TrainingArguments(**training_args)
    trainer_args = dict(
        args=args,
        model=model,
        callbacks=callbacks_to_use,
        compute_metrics=partial(utils.token_classification_metrics, label_list=label_list),
    )

    trainer = Trainer(
        **trainer_args,
        train_dataset=train_data,
        eval_dataset=valid_data,
    )
    trainer.train()

    logger.info("Finished training, saving model...")
    trainer.save_model(config.project_name)
    tokenizer.save_pretrained(config.project_name)

    model_card = utils.create_model_card(config, trainer)

    # save model card to output directory as README.md
    with open(f"{config.project_name}/README.md", "w", encoding="utf-8") as f:
        f.write(model_card)

    if config.push_to_hub:
        if PartialState().process_index == 0:
            remove_autotrain_data(config)
            save_training_params(config)
            logger.info("Pushing model to hub...")
            api = HfApi(token=config.token)
            api.create_repo(repo_id=config.repo_id, repo_type="model", private=True)
            api.upload_folder(
                folder_path=config.project_name,
                repo_id=config.repo_id,
                repo_type="model",
            )

    if PartialState().process_index == 0:
        pause_space(config)


if __name__ == "__main__":
    args = parse_args()
    training_config = json.load(open(args.training_config))
    config = TokenClassificationParams(**training_config)
    train(config)
