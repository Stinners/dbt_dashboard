from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.dbt.api import DbtApi
from src.config import env
from src.db import connection, queries
import src.db.models as models
import src.handlers as handlers

dbt = DbtApi(env.api_endpoint, env.api_token)
conn = connection.default_db_connection()

routes = FastAPI()

routes.mount("/static", StaticFiles(directory="static"), name="static")

@routes.get("/api/runs")
def recent_runs_endpoint() -> List[models.Run]:
    """ Gets the most recent run for each job """
    runs = queries.get_latest_runs(conn)
    return runs

@routes.get("/api/jobs")
def list_jobs_endpoint() -> List[models.Job]:
    """ Gets the list of all jobs """
    jobs = queries.get_all_jobs(conn)
    return jobs

@routes.post("/api/refresh/runs")
def refresh_runs_endpoint():
    """Refreshes run data from the dbt api"""
    load_from = datetime.now(timezone.utc) - timedelta(weeks=4)
    handlers.load_runs(dbt, conn, start_date=load_from, use_watermark=True)
    return {"status": "success"}

@routes.post("/api/refresh/all")
def refresh_data_endpoint():
    """Refreshes all data from the dbt api"""
    load_from = datetime.now(timezone.utc) - timedelta(weeks=1)
    handlers.refresh_data(dbt, conn, load_runs_from=load_from)
    return {"status": "success"}

