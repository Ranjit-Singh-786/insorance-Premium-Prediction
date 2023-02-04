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
