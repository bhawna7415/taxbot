from os import environ

# DATABASE_URL = environ.get("DATABASE_URL")

# OPENAI_API_KEY = environ.get("OPENAI_API_KEY","sk-test")
# DATABASE_HOST = environ.get("DATABASE_HOST","172.17.0.2")
# DATABASE_PORT = environ.get("DATABASE_PORT","5432")
# DATABASE_NAME = environ.get("DATABASE_NAME","postgres")
# DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD","testpassword")
# COLLECTION_NAME = environ.get("COLLECTION_NAME","pgdata")
# DATABASE_USER = environ.get("DATABASE_USER","postgres")
# REGION_NAME =  environ.get("DATABASE_USER","us-west-2")
# HISTORY_TABLE = environ.get("DATABASE_USER",'dev_chat_history')
# AWS_ACCESS_KEY=environ.get("AWS_ACCESS_KEY","AWS_ACCESS_KEY")
# AWS_SECRET_KEY=environ.get("AWS_SECRET_KEY","AWS_SECRET_KEY")

# AccessKey="ASIAURLWAD7TRGPGNTOE"
# SecretKey= "C/l/zwtrbx02njkLZFtRh/QxrYg9EOYnCVVyrwsT"


# DATABASE_URL = environ.get("DATABASE_URL")
OPENAI_API_KEY = environ.get("OPENAI_API_KEY","sk-test")
DATABASE_HOST = environ.get("DATABASE_HOST","localhost")
DATABASE_PORT = environ.get("DATABASE_PORT","5432")
DATABASE_NAME = environ.get("DATABASE_NAME","taxdatabase")
DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD","testpassword")
COLLECTION_NAME = environ.get("COLLECTION_NAME","pgdata")
DATABASE_USER = environ.get("DATABASE_USER","postgres1")
REGION_NAME =  environ.get("REGION_NAME","us-west-2")
HISTORY_TABLE = environ.get("CHAT_HISTORY_DYNAMODB_TABLE",'dev_chat_history')
BASE_URL = environ.get("BASE_URL",'http://127.0.0.1:8000')
AWS_ACCESS_KEY=environ.get("AWS_ACCESS_KEY","AWS_ACCESS_KEY")
AWS_SECRET_KEY=environ.get("AWS_SECRET_KEY","AWS_SECRET_KEY")
