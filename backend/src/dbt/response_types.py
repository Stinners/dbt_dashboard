from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, AliasPath

### These class represent the responses from the dbt API

class APIProject(BaseModel):
    dbt_id: int = Field(validation_alias="id")
    name: str

class APIEnvironment(BaseModel):
    dbt_id: int = Field(validation_alias="id")
    name: str
    type: str
    repo_name: str = Field(validation_alias=AliasPath("repository", "full_name"))
    project_id: int

class APIJob(BaseModel):
    dbt_id: int = Field(validation_alias="id")
    project_id: int
    environment_id: int
    name: str

class APIRun(BaseModel):
    dbt_id: int = Field(validation_alias="id")
    environment_id: int
    project_id: int
    job_id: int
    git_branch: Optional[str]
    git_hash: Optional[str] = Field(validation_alias="git_sha")
    started_at: datetime
    finished_at: Optional[datetime]
    is_error: bool 
    duration: str 
