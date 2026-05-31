import httpx
import asyncio
import logging
from typing import Callable, Awaitable
from configs import GLOBAL_TIMEOUT, GLOBAL_RATE_LIMIT
from src.core.extractors.anilist_query import QUERY_BY_PAGE
from src.core.models.raw_anilist_model import RawAnilistData
from src.core.exceptions import InvalidYearError, MaxRetryAttemptError

# anilist has limit of when page num is over 100, it will fails
# extract method: per year

logger = logging.getLogger(__name__)


class AnilistExtractor:
    BASE_URL = "https://graphql.anilist.co"
    MAXIMUM_RETRY_ATTEMPT = 3
    RETRY_DELAY = 5.0

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def get_by_page(self, page: int, year: int) -> list[RawAnilistData]:
        if len(str(year)) != 4:
            raise InvalidYearError(year)
        data = await self._request_with_retry(
            self._request,
            QUERY_BY_PAGE,
            {"page": page, "start": int(f"{year:<08d}"), "end": int(f"{year}1231")},
            max_attempt=self.MAXIMUM_RETRY_ATTEMPT,
            retry_delay=self.RETRY_DELAY,
        )
        media_data = data.json()["data"]["Page"]["media"]
        logger.info(f"Extracted: page {page}, year {year}")
        return [RawAnilistData(**r) for r in media_data]

    async def _request_with_retry(
        self,
        requester: Callable[[str, dict[str, int]], Awaitable[httpx.Response]],
        query: str,
        variables: dict[str, int],
        max_attempt: int,
        retry_delay: float,
    ) -> httpx.Response:
        for attempt in range(max_attempt):
            try:
                return await requester(query, variables)
            except httpx.HTTPStatusError as e:
                logger.warning(
                    f"Extractor: http status error occured, code: {e.response.status_code}"
                )
                if e.response.status_code == 429:
                    retry_after = e.response.headers.get("Retry-After")
                    logger.warning(
                        f"Extractor: rate limited, retry after {retry_after} seconds"
                    )
                    if retry_after:
                        await asyncio.sleep(int(retry_after))
            except httpx.HTTPError as e:
                logger.warning(f"Extractor: http error occured: {repr(e)}")
            logger.info(
                f"Extractor: retry attempt: {attempt + 1}, after {retry_delay} seconds"
            )
            await asyncio.sleep(retry_delay)
        logger.error("Extractor: max attempt reached")
        raise MaxRetryAttemptError(max_attempt)

    async def _request(self, query: str, variables: dict[str, int]) -> httpx.Response:
        response = await self.client.post(
            self.BASE_URL,
            json={"query": query, "variables": variables},
            timeout=GLOBAL_TIMEOUT,
        )
        response.raise_for_status()
        await asyncio.sleep(GLOBAL_RATE_LIMIT)
        return response
