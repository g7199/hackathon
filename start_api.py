from fastapi import FastAPI
from pydantic import BaseModel
from functions.convert_news import convert_news
from functions.question_maker import question_maker
from functions.grading import grading
from functions.link_to_text import link_to_text
from functions.text_to_pic import text_to_pic
from dotenv import load_dotenv
import os
import openai as client

load_dotenv()
client.api_key = os.getenv('OPENAI_API_KEY')

import uvicorn

app = FastAPI()

# 입력 데이터를 위한 Pydantic 모델
class ConvertNewsInput(BaseModel):
    score: int
    text: str

class QuestionMakerInput(BaseModel):
    converted_news: str

class GradingInput(BaseModel):
    ans: list
    qa_list: list
    converted_news: str
    
class LinkToTextInput(BaseModel):
    url: str

@app.post("/convert_news")
async def convert_news_endpoint(input_data: ConvertNewsInput):
    converted_news = convert_news(input_data.score, input_data.text)
    image_url = None
    qa_list = question_maker(converted_news)
    
    if input_data.score < 60:
        image_url = text_to_pic(input_data.text)
        
    return {"converted_news": converted_news, "qa_list": qa_list, "image_url": image_url}

@app.post("/grading")
async def grading_endpoint(input_data: GradingInput):
    result = grading(input_data.ans, input_data.qa_list, input_data.converted_news)
    return {"result": result}

@app.post("/link_to_text")
async def grading_endpoint(input_data: LinkToTextInput):
    result = link_to_text(input_data.url)
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
