import logging
from datetime import datetime, timezone
from collections.abc import AsyncIterable
from src.core.models.domain_model import AnimeDataModel
from src.core.models.raw_anilist_model import RawAnilistData, AnilistStudiosNodes
from src.core.models.protocols import ExtractorProtocol

logger = logging.getLogger(__name__)


class AnilistTransformer:
    def __init__(self, extractor: ExtractorProtocol) -> None:
        self.extractor = extractor

    async def get_transformed_data(
        self, start_year: int, end_year: int
    ) -> AsyncIterable[AnimeDataModel]:
        years = self._get_year_range(start_year, end_year)
        async for raw_data in self._get_raw_data(years):
            logger.debug(f"Transforming: id {raw_data.id}")
            yield self._transform_data(raw_data)

    async def _get_raw_data(self, years: list[int]) -> AsyncIterable[RawAnilistData]:
        for year in years:
            for i in range(
                1, 100
            ):  # hardcoded max page, since anilist pagination caps at 100
                pages = await self.extractor.get_by_page(i, year)
                if pages is None:
                    break
                logger.info(f"Transforming: page {i}, year {year}")
                for page in pages:
                    yield page

    def _transform_data(self, raw_data: RawAnilistData) -> AnimeDataModel:
        return AnimeDataModel(
            id=raw_data.id,
            id_mal=raw_data.idMal,
            romaji_title=raw_data.title.romaji,
            english_title=raw_data.title.english,
            native_title=raw_data.title.native,
            preferred_title=raw_data.title.userPreferred,
            type=raw_data.type,
            format=raw_data.format,
            status=raw_data.status,
            description=raw_data.description,
            start_date=self._transform_date(**raw_data.startDate.model_dump()),
            end_date=self._transform_date(**raw_data.endDate.model_dump()),
            season=raw_data.season,
            season_year=raw_data.seasonYear,
            episodes=raw_data.episodes,
            duration=raw_data.duration,
            country_of_origin=raw_data.countryOfOrigin,
            source=raw_data.source,
            hashtag=raw_data.hashtag,
            updated_at=self._transform_from_timestamp(raw_data.updatedAt),
            genres=self._join_list(raw_data.genres),
            synonyms=self._join_list(raw_data.synonyms),
            average_score=raw_data.averageScore,
            mean_score=raw_data.meanScore,
            popularity=raw_data.popularity,
            trending=raw_data.trending,
            favourites=raw_data.favourites,
            animation_studio=self._transform_studios(raw_data.studios.nodes),
        )

    def _transform_from_timestamp(self, timestamp: int) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d")

    def _transform_date(
        self,
        year: int | None,
        month: int | None,
        day: int | None,
    ) -> str | None:
        if year is None and month is None and day is None:
            return None

        def resolve_none(value: int | None) -> str:
            return f"{value:02d}" if value is not None else "00"

        return f"{resolve_none(year)}-{resolve_none(month)}-{resolve_none(day)}"

    def _join_list(self, values: list[str]) -> str | None:
        if not values:
            return None
        return ",".join(values)

    def _transform_studios(self, studio_nodes: list[AnilistStudiosNodes]) -> str | None:
        for node in studio_nodes:
            if node.isAnimationStudio:
                return node.name
        return None

    def _get_year_range(self, start: int, end: int) -> list[int]:
        years: list[int] = []
        while start <= end:
            years.append(start)
            start += 1
        return years
