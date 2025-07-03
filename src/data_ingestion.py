import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_function import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_names = self.config["bucket_file_names"]

        os.makedirs(RAW_DIR,exist_ok=True)
        
        logger.info("Data Ingestion started ...")

    def download_csv_from_gcp(self):
        try:

            client = storage.Client()
            bucket = client.bucket(self.bucket_name)


            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR,file_name)

                if file_name == "animelist.csv":
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    data = pd.read_csv(file_path,nrows=5000000)
                    data.to_csv(file_path,index=False)
                    logger.info("Large file detected only downloding 5M rows")

                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    logger.info("downloading smaller file ie anime and anime with synopsis")


        except Exception as e:
            logger.error("error while downloading the data from gcp")
            raise CustomException("faild to download data from gcp",e)
        

    def run(self):
        try:
            logger.info("starting data ingestion process....")
            self.download_csv_from_gcp()
            logger.info("DATA INGESTION COMPLETED")

        except CustomException as ce:
            logger.error(f"custom Exception: {str(ce)}")

        finally:
            logger.info("data ingestion done...")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()