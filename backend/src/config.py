# This file contains any code that has to be run before any 
# other internal modules are loaded

import logging
import sys
from typing_extensions import Annotated

from pydantic import BaseModel, Field, AfterValidator, ValidationError
from dotenv import dotenv_values

################ Logging #############

def setup_logging():
    logging.basicConfig(level=logging.DEBUG)

####### Environment Variables #########

DB_PREFIX = r"sqlite:"

def starts_with(prefix: str):
    def _starts_with_inner(value: str):
        if not value.startswith(prefix):
            raise ValueError(f"should start with {prefix}, is {value}")
        return value
    return AfterValidator(_starts_with_inner)

def called(alias):
    return Field(validation_alias=alias)

class EnvironmentVariables(BaseModel):
    api_token:    Annotated[str, called("API_TOKEN")]
    api_endpoint: Annotated[str, called("API_ENDPOINT"), starts_with(r"https://")]
    database_url: Annotated[str, called("DATABASE_URL"), starts_with(DB_PREFIX)]

def load_dotenv():
    config = {
        **dotenv_values(".env"),
        **dotenv_values(".env.secret")
    }
    try:
        return EnvironmentVariables(**config)  # type: ignore
    except ValidationError as e:
        print("Environment variables are not configured correctly")
        print(e)
        sys.exit()

def get_logger():
    return logging.getLogger()

####### Running Code #########

setup_logging()
env = load_dotenv()
