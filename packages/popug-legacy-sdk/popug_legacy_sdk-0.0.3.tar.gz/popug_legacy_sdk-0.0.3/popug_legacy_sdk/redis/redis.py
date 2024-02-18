import redis.asyncio as redis  # noqa

_redis = {}


async def init_redis(redis_pool_name: str, redis_url: str):
    await close_redis(redis_pool_name)
    _redis.clear()
    _redis[redis_pool_name] = await redis.from_url(redis_url)


async def close_redis(redis_pool_name: str):
    if _redis:
        redis_client = _redis.get(redis_pool_name, None)
        await redis_client.close()


def get_redis(redis_pool_name: str):
    def _get_redis():
        if not _redis:
            raise Exception("Need to init redis")
        return _redis[redis_pool_name]

    return _get_redis
