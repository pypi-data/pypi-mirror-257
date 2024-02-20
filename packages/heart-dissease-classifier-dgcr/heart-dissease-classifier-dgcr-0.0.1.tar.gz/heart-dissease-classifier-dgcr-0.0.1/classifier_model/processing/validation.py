from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classifier_model.config.core import config

class PatientDataInputSchema(BaseModel):
    Age             : Optional[int]
    Sex             : Optional[str]
    ChestPainType   : Optional[str]
    RestingBP       : Optional[int]
    Cholesterol     : Optional[int]
    FastingBS       : Optional[int]
    RestingECG      : Optional[str]
    MaxHR           : Optional[int]
    ExerciseAngina  : Optional[str]
    Oldpeak         : Optional[float]
    ST_Slope        : Optional[str]

class MultiplePatientDataInputs(BaseModel):
    inputs: List[PatientDataInputSchema]
