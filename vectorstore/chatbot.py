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
# from llama_index.core import KeywordTableIndex
from llama_index.llms.openai import OpenAI
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
        self.llm = OpenAI(temperature=0.1, model="gpt-4o",max_tokens=100)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store,llm=self.llm)
        self.memory = ChatMemoryBuffer.from_defaults(token_limit=1536)
        self.chat_engine = self.index.as_chat_engine(
            chat_mode="context",
            memory=self.memory,
            system_prompt=(
        """You are name is Kintsugi sales Tax Bot. Kintsugi is leading company for sales tax solution. Always try to give answer from given context if answer is not present guide user to how you can help instead of providing unrelated user query.you are working as a sales tax advisor,
                    you have a large database of information about sales tax, tax changes, and related topics 
                    now people will ask thier queries about sales tax and you will provide them answer as an advisor
                    your response will not contain any refference about "provided context" or your database, it should be a clear human response based on the provided data
                    you are not responsible to answer users queries in other contexts. Only give responses for the sales tax related query."""
    ),
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
            res=[]
            userids=str(userid)
            response = self.table.scan(
                FilterExpression=Attr("userid").eq(userids)
            )
 
            print("response",response)
            for item in response['Items']:
                message_user = ChatMessage(role="user", content=item['question'])
                message_system = ChatMessage(role="assistant", content=item['answer'])
                memory.append(message_user)
                memory.append(message_system)
                res.append({"userid":userids,"question":item['question'],"answer":item['answer'],"Date":item['date']})
            self.memory.chat_history = memory
            return res
            
             
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
        ttl_seconds = int(time.time()) + 7200   
        print("User Id:",userid) 
        response = self.table.put_item(
            Item={
                'id':random_number,
                'userid': str(userid),
                'question':query,
                'answer': response,
                'date': f'{date.today()}',
                'status':status,
                'expiration_time':ttl_seconds
            }
        )
        
    def chat_response(self,query,userid):
        chat_response = ''
        try: 
            status = "active"
            self.memory.chat_history.clear()
            # self.update_status_for_old_history(connect,userid,'expired')
            self.fetch_user_history_from_db(userid)
            response = self.chat_engine.chat(query)
            self.insert_item(userid, query, response.response,status)
            chat_response = response.response
        except Exception as e:
            logger.info(f"Error connecting to Boat:{e}")
        return chat_response


