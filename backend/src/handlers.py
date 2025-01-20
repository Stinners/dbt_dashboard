from datetime import datetime, timezone
import sys

from sqlite3 import Connection

from src.dbt.api import DbtApi
from src.config import get_logger
import src.db.queries as queries

logger = get_logger()

def _get_start_date(conn: Connection, start_date: datetime, use_watermark) -> datetime:
    if use_watermark:
        try:
            last_run_started_row = conn.execute("Select max(started_at) from run;").fetchone()
            last_run_started = DbtApi.parse_timestamp(last_run_started_row[0])
            if last_run_started > start_date:
                start_date = last_run_started
            else:
                logger.warning("Last run was before the start date, you may be missing runs")
        except:
            logger.warning("Failed to load recent run from the database, using default start time")
    else:
        logger.info("Ignoring watermark value")

    return start_date



def load_runs(api: DbtApi, conn: Connection, start_date: datetime, use_watermark=True): 
    start_date = _get_start_date(conn, start_date, use_watermark)
    logger.info(f"Loading runs back to: {start_date}")

    earliest_seen_date = datetime.now(timezone.utc)

    offset = 0
    page_size = 100
    while earliest_seen_date > start_date:
        logger.debug(f"Loading runs from offset: {offset}")
        runs = api.get_runs(limit=page_size, offset=offset)
        earliest_seen_date = min([run.started_at for run in runs])
        logger.debug(f"Earliest date retrived: {earliest_seen_date}")

        queries.insert_runs(conn, runs) 

        if len(runs) < page_size:
            break
        else:
            offset += page_size


def refresh_data(api: DbtApi, conn: Connection, load_runs_from: datetime):
    logger.info("Doing a full refresh of all data")

    projects = api.get_projects() 
    queries.insert_projects(conn, projects)

    environments = api.get_environments() 
    queries.insert_environments(conn, environments)

    jobs = api.get_jobs() 
    queries.insert_jobs(conn, jobs)

    load_runs(api, conn, load_runs_from)
    queries.clean_runs(conn)
