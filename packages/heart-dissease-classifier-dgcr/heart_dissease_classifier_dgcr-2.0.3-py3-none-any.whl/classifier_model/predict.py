import typing as t

import numpy as np
import pandas as pd

from classifier_model import __version__ as _version
from classifier_model.config.core import config
from classifier_model.processing.data_manager import load_pipeline
# from classifier_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_heart_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction( *, input_data: t.Union[pd.DataFrame, dict], ) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    # validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version}

    # if not errors:
    predictions = _heart_pipe.predict(
        X=data[config.model_config.features]
    )
    results = {
        "predictions": [np.exp(pred) for pred in predictions],  # type: ignore
        "version": _version
    }

    return results
