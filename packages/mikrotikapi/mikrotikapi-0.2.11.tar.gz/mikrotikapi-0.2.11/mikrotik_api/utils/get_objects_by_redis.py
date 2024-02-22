import json
import logging
from typing import Type, TypeVar

import redis.asyncio as redis

from pydantic import parse_obj_as, BaseModel

from mikrotik_api.schemes import (
    InterfaceScheme,
    MangleScheme,
    PeersScheme,
    SecretScheme,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class RedisObjects:
    def __init__(self, url: str):
        self.url = url

    async def redis_conn(self):
        r = redis.from_url(self.url)
        try:
            return r
        finally:
            await r.close()

    async def set_objects(self, objects: list[Type[T]]):
        r = await self.redis_conn()
        try:
            for index, interface in enumerate(objects):
                json_interface = interface.json()
                await r.set(f"interface_json_model:{index}", json_interface)
            return True

        except redis.RedisError as redis_err:
            logger.exception(f"Redis error: {redis_err}")
            return False

        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            return False

    async def get_objects(self, scheme: Type[T]) -> list[Type[T]] | Type[T]:
        r = await self.redis_conn()
        keys = await r.hgetall(scheme.name)
        objs = []
        for k, v in keys.items():
            objs.append(json.loads(v))

        return parse_obj_as(list[scheme], objs)

    async def get_interfaces_by_logic(self, name: str) -> list[InterfaceScheme] | None:
        try:
            interfaces = await self.get_objects(InterfaceScheme)
            interfaces = list(
                filter(
                    lambda x: x.running is True and x.comment and x.tariffs, interfaces
                )
            )
            interfaces = sorted(interfaces, key=lambda x: x.name)
            interfaces = list(filter(lambda x: name in x.tariffs, interfaces))
            return interfaces

        except IndexError:
            return None

    async def get_peers_by_public_key(self, key: str) -> PeersScheme | None:
        try:
            peers = await self.get_objects(PeersScheme)
            return list(filter(lambda x: x.public_key == key, peers))[0]

        except IndexError:
            return None

    async def get_mangle_by_profile_id(self, profile_id) -> MangleScheme | None:
        try:
            mangles = await self.get_objects(MangleScheme)
            mangles = list(filter(lambda x: x.comment, mangles))
            filtered_mangles = list(
                filter(lambda x: x.profile_id == profile_id, mangles)
            )[0]
            return filtered_mangles

        except IndexError:
            return None
