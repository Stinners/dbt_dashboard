
from typing import Sequence, List
from sqlite3 import Connection

from pydantic import BaseModel

import src.dbt.response_types as response
from src.db.models import Run, Job
from src.config import get_logger

logger = get_logger()


def insert_logged(conn: Connection, stmt: str, args: Sequence[BaseModel], table):
    arg_dict = [arg.model_dump() for arg in args]
    logger.info(f"Inserting {table}")
    cur = conn.executemany(stmt, arg_dict)
    conn.commit()

    if cur.rowcount != -1:
        logger.info(f"{cur.rowcount} rows updated or inserted")
    else:
        logger.info(f"Rows inserted")


def insert_projects(conn: Connection, projects: Sequence[response.APIProject]): 
    stmt = """
        INSERT INTO project(name, dbt_id)
           VALUES (:name, :dbt_id)
        ON CONFLICT DO UPDATE SET 
           name = excluded.name,
           dbt_id = excluded.dbt_id;
    """
    insert_logged(conn, stmt, projects, "Projects")

def insert_environments(conn: Connection, environments: Sequence[response.APIEnvironment]):
    stmt = """
        WITH new_env(dbt_id, name, type, repo_name, project_id) as (
            VALUES (:dbt_id, :name, :type, :repo_name, :project_id)
        )
        INSERT INTO environment(dbt_id, name, type, repo_name, project_id)
        SELECT
            new_env.dbt_id,
            new_env.name,
            new_env.type, 
            new_env.repo_name,
            project.project_id
        FROM new_env
        JOIN project on new_env.project_id = project.dbt_id
        ON CONFLICT DO UPDATE SET
            dbt_id = excluded.dbt_id,
            name = excluded.name,
            type = excluded.type, 
            repo_name = excluded.repo_name,
            project_id = excluded.project_id;
            
    """
    insert_logged(conn, stmt, environments, "Environments")


def insert_jobs(conn: Connection, jobs: Sequence[response.APIJob]):
    stmt = """
        WITH new_job(dbt_id, name, project_id, environment_id) as (
            VALUES (:dbt_id, :name, :project_id, :environment_id)
        )
        INSERT INTO job(dbt_id, name, project_id, environment_id)
        SELECT
            new_job.dbt_id,
            new_job.name,
            project.project_id, 
            environment.environment_id
        FROM new_job
        JOIN project on new_job.project_id = project.dbt_id
        JOIN environment on new_job.environment_id = environment.dbt_id
        ON CONFLICT DO UPDATE SET
            dbt_id = excluded.dbt_id,
            name = excluded.name,
            project_id = excluded.project_id,
            environment_id = excluded.environment_id
            
    """
    insert_logged(conn, stmt, jobs, "Jobs")


def insert_runs(conn: Connection, runs: Sequence[response.APIRun]):
    stmt = """
        WITH new_run(dbt_id, environment_id, project_id, job_id, git_branch,
                     git_hash, started_at, finished_at, is_error, duration) 
        as (
            VALUES (:dbt_id, :environment_id, :project_id, :job_id, :git_branch, 
                    :git_hash, :started_at, :finished_at, :is_error, :duration)
        )
        INSERT INTO run(dbt_id, environment_id, project_id, job_id, git_branch, 
                        git_hash, started_at, finished_at, is_error, duration)
        SELECT
            new_run.dbt_id, 
            environment.environment_id, 
            project.project_id, 
            job.job_id,
            new_run.git_branch,
            new_run.git_hash,
            new_run.started_at,
            new_run.finished_at,
            new_run.is_error,
            new_run.duration
        FROM new_run
        JOIN project on new_run.project_id = project.dbt_id
        JOIN environment on new_run.environment_id = environment.dbt_id
        JOIN job on new_run.job_id = job.dbt_id
        ON CONFLICT DO UPDATE SET
            dbt_id = excluded.dbt_id,
            environment_id = excluded.environment_id,
            project_id = excluded.project_id,
            job_id = excluded.job_id,
            git_branch = excluded.git_branch,
            git_hash = excluded.git_hash,
            started_at = excluded.started_at,
            finished_at = excluded.finished_at,
            is_error = excluded.is_error,
            duration = excluded.duration
    """
    insert_logged(conn, stmt, runs, "Runs")


def clean_runs(conn: Connection, n_runs=3):
    """ Keep just the most recent runs for every job """
    stmt = """
        with ranked_rows as (
            select 
                run_id, 
                row_number() over (partition by job_id order by started_at desc) as row_no
            from run 
        ),
        old_rows as (
            select run_id 
            from ranked_rows 
            where row_no > :n_runs
        )
        delete from run 
        where run_id in (select run_id from old_rows);
    """

    # Since this uses a CTE, we can't get the number of rows deleted out of this query
    conn.execute(stmt, {"n_runs": n_runs})
    conn.commit()

def get_latest_runs(conn: Connection) -> List[Run]:
    """ Gets the most recent run for each job """
    stmt = """
        with latest_runs as (
            select 
                run_id,
                row_number() over (partition by job_id order by started_at desc) = 1 as latest_run
            from run 
        )
        select 
            run.dbt_id,
            run.git_branch,
            run.git_hash,
            run.started_at,
            run.finished_at,
            run.is_error,
            run.duration,
            environment.name as environment_name,
            project.name     as project_name,
            job.name         as job_name
        from run 
        inner join latest_runs 
           on run.run_id = latest_runs.run_id
          and latest_runs.latest_run
        left join environment 
               on run.environment_id = environment.environment_id
        left join project 
                on run.project_id = project.project_id
        left join job 
               on run.job_id = job.job_id;
    """

    cur = conn.execute(stmt)
    runs = cur.fetchall()
    runs_pydantic = [Run(**run) for run in runs]
    return runs_pydantic

def get_all_jobs(conn: Connection) -> List[Job]:
    stmt = """
        select 
            job.job_id,
            job.dbt_id,
            job.name,
            project.name as project_name,
            environment.name as environment_name
        from job 
        left join project 
          on job.project_id = project.project_id
        left join environment
          on job.environment_id = environment.environment_id;
    """
    cur = conn.execute(stmt)
    jobs = cur.fetchall()
    jobs_pydantic = [Job(**job) for job in jobs]
    return jobs_pydantic
