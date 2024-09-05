import openai
from openai import OpenAI
import json
client = OpenAI()
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import logger
from openai import OpenAI
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

import pandas as pd

class FineTuning:
    def __init__(self,jsonlfile) -> None:
        self.__client = OpenAI()
        self.__jsonlfile = jsonlfile
        self.file_id = None
        self.jobs_id = None
    
    def uploadfile(self):
        file_id = self.__client.files.create(
            file=open(self.__jsonlfile, "rb"),
            purpose="fine-tune"
        ) 
        self.file_id  = file_id  
    def createjobs(self):
        jobs_id = self.__client.fine_tuning.jobs.create(
        training_file= self.file_id.id,
        model= "gpt-3.5-turbo"
        )
        self.jobs_id = jobs_id
    # Retrieve the state of a fine-tune
    def retreivejobs(self):
        # self.jobs_id.id
        jobs_describe = self.__client.fine_tuning.jobs.retrieve(self.jobs_id.id) 
        return jobs_describe

# obj = FineTuning("traningdata.jsonl")
# obj.uploadfile()
# obj.createjobs()
# obj.retreivejobs()