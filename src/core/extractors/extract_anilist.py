import httpx
import asyncio
from configs import GLOBAL_TIMEOUT, GLOBAL_RATE_LIMIT
from src.core.extractors.anilist_query import QUERY_BY_PAGE
from src.core.models.raw_anilist_model import RawAnilistData
from src.core.exceptions import InvalidYearError

# anilist has limit of when page num is over 100, it will fails
# extract method: per year


class AnilistExtractor:
    BASE_URL = "https://graphql.anilist.co"

    async def get_by_page(self, page: int, year: int) -> list[RawAnilistData]:
        if len(str(year)) != 4:
            raise InvalidYearError(year)
        data = await self._request(
            QUERY_BY_PAGE,
            {"page": page, "start": int(f"{year:<08d}"), "end": int(f"{year}1231")},
        )
        media_data = data.json()["data"]["Page"]["media"]
        print(f"page {page}, year {year}")
        return [RawAnilistData(**r) for r in media_data]

    async def _request(self, query: str, variables: dict[str, int]) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.BASE_URL,
                json={"query": query, "variables": variables},
                timeout=GLOBAL_TIMEOUT,
            )
        response.raise_for_status()
        await asyncio.sleep(GLOBAL_RATE_LIMIT)
        return response
