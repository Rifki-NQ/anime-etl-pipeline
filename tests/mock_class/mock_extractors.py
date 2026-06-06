from typing import Any
from src.core.models.raw_anilist_model import RawAnilistData
from tests.mock_data.mock_anilist_data import (
    MOCKED_ANILIST_PAGE_1_UPDATED,
    MOCKED_ANILIST_DATA_PAGE_1,
    MOCKED_ANILIST_DATA_PAGE_2,
)


class MockAnilistExtractorNormal:
    async def get_by_page(self, page: int, year: int) -> list[RawAnilistData] | None:
        mocked_data: list[dict[str, Any]] = []
        match page:
            case 1:
                mocked_data = MOCKED_ANILIST_DATA_PAGE_1
            case 2:
                mocked_data = MOCKED_ANILIST_DATA_PAGE_2
            case _:
                return None
        return [RawAnilistData(**r) for r in mocked_data]


class MockAnilistExtractorUpdated:
    async def get_by_page(self, page: int, year: int) -> list[RawAnilistData] | None:
        mocked_data: list[dict[str, Any]] = []
        match page:
            case 1:
                mocked_data = MOCKED_ANILIST_PAGE_1_UPDATED
            case 2:
                mocked_data = MOCKED_ANILIST_DATA_PAGE_2
            case _:
                return None
        return [RawAnilistData(**r) for r in mocked_data]
