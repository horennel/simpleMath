from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import uuid
import uvicorn

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

templates = Jinja2Templates(directory="templates")

exams_db = {}


class ExamQuestion(BaseModel):
    content: str


class ExamData(BaseModel):
    questions: List[ExamQuestion]
    exam_id: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-exam", response_class=HTMLResponse)
async def generate_exam(request: Request, questions: str = Form(...)):
    # 分割问题文本为单独的问题
    question_list = [q.strip() for q in questions.split('\n') if q.strip()]

    # 创建试题数据
    exam_questions = [ExamQuestion(content=q) for q in question_list]
    exam_id = str(uuid.uuid4())
    exam_data = ExamData(questions=exam_questions, exam_id=exam_id)

    # 存储试题 (临时)
    exams_db[exam_id] = exam_data

    # 渲染试题页面
    return templates.TemplateResponse(
        "exam.html",
        {
            "request": request,
            "questions": exam_questions,
            "exam_id": exam_id
        }
    )


@app.get("/exam/{exam_id}", response_class=HTMLResponse)
async def view_exam(request: Request, exam_id: str):
    exam_data = exams_db.get(exam_id)
    if not exam_data:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Exam not found"})

    return templates.TemplateResponse(
        "exam.html",
        {
            "request": request,
            "questions": exam_data.questions,
            "exam_id": exam_id
        }
    )


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=21330)
