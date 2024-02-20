from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.svm import SVC
from classifier_model.config.core import config

numerical = config.model_config.numerical_features
categorical = config.model_config.categorical_features
one_hot_encoder = OneHotEncoder()
standar_scaler = StandardScaler()
column_transformer = make_column_transformer((one_hot_encoder, categorical),(standar_scaler, numerical))  
svm = SVC(gamma=config.model_config.gamma)
heart_pipe = make_pipeline(column_transformer, svm)