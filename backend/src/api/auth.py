import logging

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    logger.info(f"API KEY: {api_key_header}")
    if api_key_header == "alexisthebestchuckouttherest":
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )