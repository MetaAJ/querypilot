"""HTTP boundary for the QueryPilot frontend."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import get_settings
from .models import AnalysisResult, ForecastResult
from .service import run_forecast, run_local_analysis


class AnalysisRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2_000)
    session_id: str | None = None


class AnalysisResponse(BaseModel):
    status: str
    message: str
    session_id: str
    result: AnalysisResult | None = None


app = FastAPI(title="QueryPilot", version="0.1.0")
_frontend_path = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/frontend", StaticFiles(directory=_frontend_path), name="frontend")


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    return FileResponse(_frontend_path / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analysis", response_model=AnalysisResponse)
def create_analysis(request: AnalysisRequest) -> AnalysisResponse:
    session_id = request.session_id or "local-demo"
    if get_settings().database_path.exists():
        result = run_local_analysis(request.question, get_settings().database_path)
        return AnalysisResponse(
            status="ready",
            message="Analysis completed with evidence and a forecast.",
            session_id=session_id,
            result=result,
        )
    return AnalysisResponse(
        status="queued",
        message="Analysis orchestration will run through TrueForge.",
        session_id=session_id,
    )


@app.get("/api/forecast", response_model=ForecastResult)
def get_forecast(horizon: int = 4) -> ForecastResult:
    if not get_settings().database_path.exists():
        raise FileNotFoundError("Generate data/querypilot.db before requesting a forecast")
    if not 1 <= horizon <= 12:
        raise ValueError("horizon must be between 1 and 12")
    return run_forecast(get_settings().database_path, horizon=horizon)
