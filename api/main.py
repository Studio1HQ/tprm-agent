from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import uuid
import sys
sys.path.insert(0, 'src')

from agent import TPRMAgent, InvestigationResult

app = FastAPI(
    title="TPRM Agent API",
    description="Autonomous Third-Party Risk Management Agent",
    version="1.0.0",
)

investigations: dict[str, InvestigationResult] = {}
agent = TPRMAgent()


class InvestigationRequest(BaseModel):
    vendor_name: str
    categories: Optional[list[str]] = None
    generate_monitors: bool = True


class InvestigationResponse(BaseModel):
    investigation_id: str
    status: str
    message: str


@app.post("/investigate", response_model=InvestigationResponse)
def start_investigation(
    request: InvestigationRequest,
    background_tasks: BackgroundTasks,
):
    """Start a new vendor investigation."""
    investigation_id = str(uuid.uuid4())

    def run_investigation():
        result = agent.investigate(
            vendor_name=request.vendor_name,
            categories=request.categories,
            generate_monitors=request.generate_monitors,
        )
        investigations[investigation_id] = result

    background_tasks.add_task(run_investigation)

    return InvestigationResponse(
        investigation_id=investigation_id,
        status="started",
        message=f"Investigation started for {request.vendor_name}",
    )


@app.get("/investigate/{investigation_id}")
def get_investigation(investigation_id: str):
    """Get investigation results."""
    if investigation_id not in investigations:
        raise HTTPException(status_code=404, detail="Investigation not found or still in progress")

    return investigations[investigation_id]


@app.get("/reports/{vendor_name}")
def get_reports(vendor_name: str):
    """Get all reports for a vendor."""
    vendor_reports = [
        result
        for result in investigations.values()
        if result.vendor_name.lower() == vendor_name.lower()
    ]

    if not vendor_reports:
        raise HTTPException(status_code=404, detail="No reports found for this vendor")

    return vendor_reports


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}