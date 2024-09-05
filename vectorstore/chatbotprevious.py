from llama_index import SimpleDirectoryReader, StorageContext
from llama_index.ingestion import IngestionPipeline
from llama_index.node_parser import TokenTextSplitter
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.retrievers import VectorIndexRetriever
from llama_index import get_response_synthesizer
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
from llama_index.text_splitter import SentenceSplitter
from llama_index.extractors import TitleExtractor
from llama_index.vector_stores import PGVectorStore
from llama_index.ingestion import IngestionPipeline, IngestionCache
from llama_index.embeddings import OpenAIEmbedding
from llama_index import Document
from llama_index.memory import ChatMemoryBuffer
from llama_index.llms  import ChatMessage
import textwrap
import openai
import sys
import os
import json
from datetime import datetime, timedelta,date
import logging
from utils import logger
from config import OPENAI_API_KEY,REGION_NAME,HISTORY_TABLE
# from config import OPENAI_API_KEY,REGION_NAME,HISTORY_TABLE,AWS_ACCESS_KEY,AWS_SECRET_KEY
import asyncio
import boto3
from boto3.dynamodb.conditions import Key,Attr
import random
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class ChatBot:
    def __init__(self,connection): 
        self.vector_store  = PGVectorStore.from_params(
                                database=connection.db_name,
                                host=connection.db_host,
                                password=connection.db_password,
                                port=connection.db_port,
                                user=connection.db_user,
                                table_name=connection.collection_name,
                                embed_dim=1536,  # openai embedding dimension
                            ) 
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store)
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=1536)
        self.chat_engine = self.index.as_chat_engine(
            chat_mode="context",
            memory=self.memory,
        )
        self.clientdynamo = boto3.client(
            'dynamodb',
            region_name=REGION_NAME
        )
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=REGION_NAME
        )
        self.table = self.dynamodb.Table(HISTORY_TABLE)
      
    async def insert_vector_data(self,folderpath):
        try: 
            parent_directory = os.getcwd()
            data_folder_path = os.path.join(parent_directory, folderpath)
            documents = SimpleDirectoryReader(data_folder_path).load_data()
            pipeline = IngestionPipeline(
                transformations=[
                    SentenceSplitter(chunk_size=500, chunk_overlap=50),
                    TitleExtractor(),
                    OpenAIEmbedding(),
                ],
                vector_store=self.vector_store,
            )
            nodes = await pipeline.arun(documents=documents)
           
            if nodes: 
                return True
            return True
        except Exception as e: 
            logger.info(f"An error occurred while Inserting the data:{e}")
            
            return False
   

    def fetch_user_history_from_db(self,userid):

            memory = []
            response = self.table.scan(
                FilterExpression=Attr("userid").eq(userid)
            )
            for item in response['Items']:
                message_user = ChatMessage(role="user", content=item['question'])
                message_system = ChatMessage(role="assistant", content=item['answer'])
                memory.append(message_user)
                memory.append(message_system)
            self.memory.chat_history = memory
           
             

    
    def is_primary_exists(self,id):
        try: 
            response = self.table.scan(
                FilterExpression=Attr("id").eq(id)
            )
            if response['Count']>0: 
                return True
            else: 
                return False
        except Exception as e:
            logger.info(f"Error connecting to Boat:{e}")
            return False
        
         

    def insert_item(self,userid, query, response,status): 
        random_number = random.randint(1, 50)
        while self.is_primary_exists(random_number):
            random_number = random.randint(1, 50)
        ttl_seconds = int(time.time()) + 3600    
        response = self.table.put_item(
            Item={
                'id':random_number,
                'userid': userid,
                'question':query,
                'answer': response,
                'date': f'{date.today()}',
                'status':status,
                'expiration_time':ttl_seconds
            }
        )
        

    def chat_response(self,query,userid):
        #chat_response = ''
        # try: 
        #     status = "active"
        #     self.memory.chat_history.clear()
        #     # self.update_status_for_old_history(connect,userid,'expired')
        #     self.fetch_user_history_from_db(userid)
        prompt = query+"\n first answer from the vector data you have"
        response = self.chat_engine.chat(query)
        print(response)
        #self.insert_item(userid, query, response.response,status)
        chat_response = response.response
        # except Exception as e:
        #     logger.info(f"Error connecting to Boat:{e}")
        return chat_response

