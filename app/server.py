from http.client import HTTPException
from fastapi import FastAPI
from rq.job import Job
from app.schemas import JobSpec
from app.queues.rqclient import queue, redis_conn
from app.queues.worker import run_agent_job

app = FastAPI(title="Agentic Analysis Platform")

@app.get("/")
def health():
    """Health check endpoint."""
    return {
        "message": "Agentic Analysis API is running",
        "status": "healthy",
    }

@app.post("/jobs", status_code=201)
def submit_job(spec: JobSpec):
    """Enqueue the job to Redis and return the ID immediately."""
    # We pass the dictionary to the worker
    job = queue.enqueue(run_agent_job, spec.dict(), job_timeout='10m') 
    
    return {
        "job_id": job.get_id(),
        "status": "queued",
        "message": "Agent analysis started in the background."
    }

# @app.post("/jobs")
# def submit_job(spec: JobSpec):
#     """Run the job synchronously and print output to console."""
#     print("🔥 Starting job synchronously...")
#     result = run_agent_job(spec.dict())
#     print("🔥 Job finished!")
#     print("Result:", result)
#     return {
#         "message": "Job completed synchronously. Check console logs for details.",
#         "result": result
#     }

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    """Check the status and fetch results of a specific job."""
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404, detail="Job ID not found")

    return {
        "job_id": job_id,
        "status": job.get_status(), # started, finished, failed, queued
        "result": job.result,       # This will be None until status is 'finished'
        "enqueued_at": job.enqueued_at,
        "started_at": job.started_at,
        "ended_at": job.ended_at
    }