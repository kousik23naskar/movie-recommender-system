import os
from src.mlProject.logging import logger
from src.mlProject.entity.config_entity import DataValidationConfig
import pandas as pd


class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config


        
    
    def validate_all_columns(self)-> bool:
        try:
            validation_status = None
    
            data1 = pd.read_csv(self.config.unzip_data_dir1)
            all_cols1 = list(data1.columns)
    
            all_schema1 = self.config.all_schema1.keys()            
            
            data2 = pd.read_csv(self.config.unzip_data_dir2)
            all_cols2 = list(data2.columns)
    
            all_schema2 = self.config.all_schema2.keys()
            
            validation_results = []  # List to store validation results
            
            with open(self.config.STATUS_FILE, 'w') as f:
                for col1 in all_cols1:
                    if col1 not in all_schema1:
                        validation_status = False
                        f.write(f"Movie [col: {col1}] Validation status: {validation_status}\n")
                    else:
                        validation_status = True
                        f.write(f"Movie [col: {col1}] Validation status: {validation_status}\n")
                    validation_results.append(validation_status)
    
                for col2 in all_cols2:
                    if col2 not in all_schema2:
                        validation_status = False
                        f.write(f"Credit [col: {col2}] Validation status: {validation_status}\n")
                    else:
                        validation_status = True
                        f.write(f"Credit [col: {col2}] Validation status: {validation_status}\n")
                    validation_results.append(validation_status)            
            
            #return validation_status

            # Check if all validation statuses are True
            all_valid = all(validation_results)
            
            # Write the overall validation status to another text file
            with open(self.config.All_STATUS_FILE, 'w') as f_overall:
                f_overall.write(f"Overall validation status: {all_valid}")
            
            return all_valid
        
        except Exception as e:
            raise e