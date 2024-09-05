from vectorstore.chatbot import ChatBot
from db.connection import DBConnection
import openai 
import os
import time
import asyncio
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
class VStore(ChatBot): 
    def __init__(self): 
        self.connection =  DBConnection(connection=False)
        super().__init__(self.connection)


    async def store_vectors(self):
        tasks = []
        is_connection = self.connection.connect_db()
        if is_connection: 
            current_dir = os.getcwd()
            directories = os.listdir(current_dir)
            for directory in directories: 
                if directory[0:8] == 'data_vec': 
                    files_in_directory = os.listdir(current_dir+'/'+directory)
                    if files_in_directory:
                        tasks.append(self.directory_insertion(directory))
            await asyncio.gather(*tasks) 
                        
    async def directory_insertion(self,directory): 
        await self.insert_vector_data(directory)

        
if __name__ == '__main__': 
    vstore  = VStore()
    asyncio.run(vstore.store_vectors())