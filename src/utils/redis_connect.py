from urllib.parse import quote
from typing import Union
import redis
import logging
from src.settings import LoggerSettings
from src.settings import env_settings

logger = logging.getLogger(LoggerSettings().logger_name)


def _get_redis_url(
    redis_host: str = env_settings.REDIS_HOST,
    redis_port: int = env_settings.REDIS_PORT,
    redis_database: str = env_settings.REDIS_DB,
    redis_password: Union[str, None] = None,
) -> str:
    """Create a redis uri from given args
    redis://[username:user_pwd@]name_of_host [:port_number_of_redis_server] [/DB_Name]
    redis://[[username]:[password]]@localhost:6379/0
    """
    if not redis_password:
        redis_url = f"redis://{redis_host}:{redis_port}/{redis_database}"
        logger.debug(f"Redis url is {redis_url}")

    else:
        redis_url = f"redis://default:{quote(redis_password)}@{redis_host}:{redis_port}/{redis_database}"
        logger.debug(f"Redis url is {redis_url}")
    return redis_url


if __name__ == "__main__":
    # r = redis.Redis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
    # print(r)
    # print(r.ping())
    # value = r.set("key2", "value2")
    redis_url = _get_redis_url()
    print(redis_url)
    r = redis.Redis.from_url(redis_url)
    print(r.ping())
