from typing import Protocol
from src.core.models.raw_anilist_model import RawAnilistData


class ExtractorProtocol(Protocol):
    async def get_by_page(self, page: int, year: int) -> list[RawAnilistData]: ...
