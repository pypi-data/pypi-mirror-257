import numpy as np
from config.core import config
from pipeline import heart_pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """Train the model."""

    # divide train and test
    if config.app_config.create_validation_data:
        data = load_dataset(file_name=config.app_config.all_data_file)
        X_train, X_test, y_train, y_test = train_test_split(
            data[config.model_config.features],  # predictors
            data[config.model_config.target],
            test_size=config.model_config.test_size,
            # we are setting the random seed here
            # for reproducibility
            random_state=config.model_config.random_state,
        )
    else:
        data = load_dataset(file_name=config.app_config.training_data_file)
        X_train = data[config.model_config.features]
        y_train = data[config.model_config.target]
    # fit model
    heart_pipe.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=heart_pipe)


if __name__ == "__main__":
    run_training()
