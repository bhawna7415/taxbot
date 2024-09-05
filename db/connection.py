
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utils import logger
from config import DATABASE_HOST,DATABASE_NAME,DATABASE_PASSWORD,DATABASE_PORT,COLLECTION_NAME,DATABASE_USER
db_user = os.getenv('DB_USER', 'postgres1')
db_password = os.getenv('DB_PASSWORD', 'testpassword')

class DBConnection:
    def __init__(self,connection=None): 
        self.db_user =  DATABASE_USER
        self.db_password = DATABASE_PASSWORD
        self.db_host = DATABASE_HOST
        self.db_port = DATABASE_PORT
        self.db_name = DATABASE_NAME
        self.collection_name = COLLECTION_NAME
        self.connection = connection
        self.cursor = None
    def connect_db(self): 
        try: 
            self.connection = psycopg2.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()
            if self.cursor: 
                try: 
                    self.cursor.execute("CREATE EXTENSION vector")
                    self.cursor.execute("CREATE TABLE IF NOT EXISTS pgdata (id SERIAL PRIMARY KEY, data_vector vector);")                
                    self.cursor.execute("CREATE TABLE chat_history (id SERIAL PRIMARY KEY, userid SERIAL, question VARCHAR(4096), answer VARCHAR(4096), date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,status varchar(255))")
            
                except Exception as e: 
                    # self.cursor.execute("Drop table chat_history")
                    # self.cursor.execute("CREATE TABLE chat_history (id SERIAL PRIMARY KEY, userid SERIAL, question VARCHAR(4096), answer VARCHAR(4096), date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,status varchar(255))")
                    logger.info(f"Extention vector Already Exist")
        except Exception as e:
            logger.info(f"Error connecting to the database: {e}") 
            raise e 
        return self.cursor

       

