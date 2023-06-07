from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()
static_path = "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages
    )
    return response.choices[0].message.content

@app.post("/get")
async def chat(request: Request):
    msg = await request.form()
    input = msg["msg"]
    return get_completion(input)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
