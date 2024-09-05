from fastapi import FastAPI, Request, HTTPException,File, UploadFile
from fastapi.responses import HTMLResponse
from config import OPENAI_API_KEY
from fastapi.staticfiles import StaticFiles
from fastapi import Query
import os 

app = FastAPI()
from csvformatter.formatcsv import Formatter
from csvformatter.formattercsv import CsvFormatter

# client = OpenAI(openai_api_key =OPENAI_API_KEY)
   

# Mount the static files directory as the root directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/formatcsv_old")
async def formation_csv(file: UploadFile = File(...)):
    file_path = "raw_data.csv"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    formatter = Formatter()
    formatter.format_csv()
    return "http://127.0.0.1:8000/static/result.csv"


@app.post("/formatcsv")
async def formation_csv(file: UploadFile = File(...)):  
    file_path = "raw_data.csv"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # formatter = Formatter()
    # formatter.format_csv()

    formatter = CsvFormatter()
    input_file = file.filename  # Replace with the actual file path
   
    input_columns = formatter.read_input_columns(file_path) 

    formatter.match_columns(input_columns)
    return "http://127.0.0.1:8000/static/result.csv"
   

