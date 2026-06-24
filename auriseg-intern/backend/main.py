from src.agent.run_agent import run_agent
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Auriseg Code Review API",
    version="1.0.0"
)


class ReviewRequest(BaseModel):
    input_path: str


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "Auriseg Code Review API"
    }


@app.post("/review")
def review_repo(request: ReviewRequest):

    try:
        reports = run_agent(request.input_path)

        return {
            "success": True,
            "reports":reports
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }