from datetime import datetime
import os
import sys
import json
from typing import Type, TypeVar, List
from urllib.parse import urlencode

import requests
from pydantic import BaseModel, ValidationError
import pytz

from src.dbt.response_types import APIEnvironment, APIProject, APIJob, APIRun
from src.config import get_logger

logger = get_logger()

Model = TypeVar("Model", bound=BaseModel)

class DbtApi():
    def __init__(self, endpoint: str, token: str ):
        self._base_url = endpoint
        self._session = requests.Session()

        self._session.headers.update({
              'Accept': 'application/json',
              'Authorization': f'Token {token}',
        })

    def get_environments(self) -> List[APIEnvironment]:
        data = self._get_json(APIEnvironment, "environments")
        return data

    def get_jobs(self) -> List[APIJob]:
        return self._get_json(APIJob, "jobs")

    def get_projects(self) -> List[APIProject]:
        return self._get_json(APIProject, "projects")

    def get_runs(self, limit=100, project_ids=[], offset=0) -> List[APIRun]:
        args = {"order_by": "-created_at", "limit": limit, "offset": str(offset)}
        if project_ids != []:
            args["project_id__in"] = project_ids

        return self._get_json(APIRun, "runs", args=args)

    def _make_request_url(self, endpoint: str) -> str:
        assert not endpoint.startswith("/")
        return os.path.join(self._base_url, endpoint)

    def _get_json(self, model: Type[Model], endpoint, args={}) -> List[Model]:
        url = self._make_request_url(endpoint)
        logger.info(f"Querying dbt endpoint: {url}")
        response = self._session.get(url, params=urlencode(args))

        if response.status_code != 200:
            logger.error(f"HTTP Error: {response.status_code}")
            logger.error(response.text)
            sys.exit()

        try:
            data = response.json()["data"]
            validated_data = [model(**datum) for datum in data]
            logger.info(f"Got {len(validated_data)} results")
            return validated_data

        except json.decoder.JSONDecodeError:
            logger.error("Response did not contain valid JSON")
            logger.error(response.text)
            sys.exit()

        except ValidationError as e:
            logger.error(f"Invalid data in API response: {e}")
            sys.exit()

    @staticmethod
    def parse_timestamp(timestamp) -> datetime:
        parsable_part = timestamp.split(".")[0]
        naive_datetime = datetime.strptime(parsable_part, "%Y-%m-%d %H:%M:%S")
        utc_datetime = pytz.utc.localize(naive_datetime)
        return utc_datetime

