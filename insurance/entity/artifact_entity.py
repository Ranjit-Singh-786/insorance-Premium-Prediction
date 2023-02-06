from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    # value of this instance variable we will assign during the object creation time
    feature_store_file_path:str
    train_file_path:str 
    test_file_path:str

@dataclass
class DataValidationArtifact:
    report_file_path:str


@dataclass
class DataTransformationArtifact:
    transformer_object_path:str
    transformed_train_path:str
    transformed_test_path:str
    target_encoder_path:str


@dataclass
class ModelTrainerArtifact:
    model_file_path:str
    r2_train_score:str
    r2_test_score:str
