from fastapi import FastAPI, Request, HTTPException,File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from mangum import Mangum
# from vectorizedata import DocVectorization
from fastapi import Query
import os 
from db.connection import DBConnection
from vectorstore.chatbot import ChatBot
from fastapi.staticfiles import StaticFiles
from utils import logger
from schema import ClassificationResponse,ClassificationRequest
from config import OPENAI_API_KEY
import openai
from productclassification.classifyproduct import CLassfyProduct
app = FastAPI()
# from csvformatter.formatcsv import Formatter
openai.api_key = OPENAI_API_KEY
templates = Jinja2Templates(directory="templates")
db_connection = DBConnection()
connect = db_connection.connect_db()
vectorstore = ChatBot(db_connection)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try: 
        return templates.TemplateResponse("index.html", {"request": request})
       
    except Exception as e: 
        logger.info(f"An error occurred: {e}")
        return f"Error: {e}"


@app.post("/formatcsv")
async def formation_csv(file: UploadFile = File(...)):
    file_path = "raw_data.csv"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # formatter = Formatter()
    # formatter.format_csv()
    return "http://127.0.0.1:8000/static/result.csv"
   

# @app.get(path="/taxbot-vector", description="Help Chat for Kingsugi Platform")
# def chat_documents():
#     try:  
#         data = vectorstore.insert_vector_data()
#         return data
#     except Exception as e: 
#         logger.info(f"An error occurred: {e}")
#         return f"error inserting the vectors {e}"
    


@app.get("/taxbot")
async def chat_app(text: str = Query(..., description="Text to be sent to chat"),user_id: int = Query(..., description="Text to be sent to chat")):
    try: 
        res = vectorstore.chat_response(text,user_id)
        return res
    except Exception as e:
        logger.info(f"Chat function Error : {e}")
        # return "Hello there, how may I help you"
    
@app.get("/get-history")
async def get_user_history(user_id: int = Query(..., description="User ID")):
    try:
        history = vectorstore.fetch_user_history_from_db(user_id)
        return history
    except Exception as e:
        logger.info(f"Get history function Error : {e}")
        raise HTTPException(status_code=500, detail="Error retrieving user history")
    
# @app.post("/classification/", response_model=ClassificationResponse)
# def classify_product(request: ClassificationRequest):
#     # Assuming you have some classification logic here
#     # For simplicity, let's just return the first existing product's category and subcategory
#     if request.existing_products:
#         existing_products = request.existing_products
#         new_product = request.product_to_classify  
#         classify = CLassfyProduct()
#         classified_respose = classify.classify_product_category(existing_products,new_product)
#         return classified_respose
#         #return {"category:"+classified_respose[0],"subcategory:"+classified_respose[1]}
#     else:
#         raise HTTPException(status_code=400, detail="No existing products provided for classification")

# handler = Mangum(app)