from typing import Protocol
from collections.abc import AsyncIterator
from src.core.models.raw_anilist_model import RawAnilistData
from src.core.models.domain_model import AnimeDataModel


class ExtractorProtocol(Protocol):
    async def get_by_page(self, page: int, year: int) -> list[RawAnilistData]: ...


class TransformerProtocol(Protocol):
    def get_transformed_data(
        self, start_year: int, end_year: int
    ) -> AsyncIterator[AnimeDataModel]: ...
