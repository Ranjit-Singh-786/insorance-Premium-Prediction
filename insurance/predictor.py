import os,sys
from typing import Optional
from insurance.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME,MODEL_NAME,TARGET_ENCODER_OBJECT_FILE_NAME
from insurance.exception import InsuranceException


class ModelResolver:
    # all are default instance variable name
    def __init__(self, model_registry:str = "saved_models", #main directory for futre training
                transfomer_dir_name = "transfomer", # for keep transformer
                traget_encoder_dir_name = "target_encoder", # for keep labelencoder
                model_dir_name = "model"):  #to keep model 

        self.model_registry = model_registry
        #object of this class will be created in modelEvaluation class
        os.makedirs(self.model_registry, exist_ok=True)
        self.transfomer_dir_name = transfomer_dir_name
        self.traget_encoder_dir_name = traget_encoder_dir_name
        self.model_dir_name = model_dir_name

# 1
    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_name = os.listdir(self.model_registry)
            if len(dir_name) == 0:
                return None
            
            dir_name = list(map(int, dir_name))
            latest_dir_name = max(dir_name)
            return os.path.join(self.model_registry, f"{latest_dir_name}")

        except Exception as e:
            raise InsuranceException(e,sys)
# 2

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Model is Not avaliable")

            return os.path.join(latest_dir, self.model_dir_name, MODEL_NAME)
        except Exception as e:
            raise InsuranceException(e,sys)
# 3

    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transform data is not avaliable")

            return os.path.join(latest_dir, self.transfomer_dir_name,TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise InsuranceException(e,sys)

# 4
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Traget encoder data is not avaliable")

            return os.path.join(latest_dir, self.traget_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise InsuranceException(e,sys)
        
    # if empty then created path for "0" otherwise path for +1
    def get_latest_save_dir_path(self)->str:

        try:
            latest_dir = self.get_latest_dir_path()
            # os.makedirs(latest_dir,exist_ok=True)
            if latest_dir ==  None:
                # return latest_dir

                return os.path.join(self.model_registry, f"{0}")
            # if it is not None
            
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path())) #basename --> last location of this path
            latest_dir  = os.path.join(self.model_registry, f"{latest_dir_num+1}") ## add 1 so that it will increase everytime
            return latest_dir 
        except Exception as e:
            raise InsuranceException(e,sys)
# 6

    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.model_dir_name, MODEL_NAME) # model.pkl
        except Exception as e:
            raise InsuranceException(e,sys)
# 7
    def get_latest_save_transfomer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.transfomer_dir_name, TRANSFORMER_OBJECT_FILE_NAME) # transform.pkl
        except Exception as e:
            raise InsuranceException(e,sys)

# 8
    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.traget_encoder_dir_name, TARGET_ENCODER_OBJECT_FILE_NAME) # encoder.pkl
        except Exception as e:
            raise InsuranceException(e,sys)