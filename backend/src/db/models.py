from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Run(BaseModel):
    dbt_id:int
    environment_name: str
    project_name: str
    job_name: str
    git_branch: Optional[str]
    git_hash: Optional[str]
    started_at: datetime
    finished_at: Optional[datetime]
    is_error: bool
    duration: str

class Job(BaseModel):
    job_id: int
    dbt_id: int
    project_name: str
    environment_name: str
    name: str
