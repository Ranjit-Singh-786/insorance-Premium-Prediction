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
    r2_train_score:float
    r2_test_score:float

# to get the output of new model
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float


@dataclass
class ModelPusherArtifact:
    pusher_model_dir:str
    saved_model_dir:str