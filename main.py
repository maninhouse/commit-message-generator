import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.generator import CommitMessageGenerator

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Commit Message Generator API",
    description="API for generating commit messages from git diff",
    version="1.0.0",
)


class GitDiffRequest(BaseModel):
    git_diff: str


@app.get("/health")
async def health_check():
    logger.info("health check")
    return {"status": "ok"}


@app.post("/generate")
async def generate_commit_message(request: GitDiffRequest):
    try:
        generator = CommitMessageGenerator()
        response = generator.generate(request.git_diff)
        logger.info("success generate commit message")
        return {"response": response}
    except Exception as e:
        logger.error(f"generate commit message error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    logger.info("start api service")
    uvicorn.run(app, host="0.0.0.0", port=8000)
