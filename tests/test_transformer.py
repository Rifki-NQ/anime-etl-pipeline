import pytest
import pytest_asyncio
from tests.mock_class.mock_extractors import MockAnilistExtractorNormal
from src.core.transformers.transform_anilist import AnilistTransformer
from src.core.models.domain_model import AnimeDataModel
from src.core.models.protocols import ExtractorProtocol


@pytest.fixture
def extractor() -> ExtractorProtocol:
    return MockAnilistExtractorNormal()


@pytest.fixture
def transformer(extractor: ExtractorProtocol) -> AnilistTransformer:
    return AnilistTransformer(extractor)


@pytest_asyncio.fixture
async def all_data(transformer: AnilistTransformer) -> list[AnimeDataModel]:
    all_data: list[AnimeDataModel] = []
    async for data in transformer.get_transformed_data(2019, 2019):
        all_data.append(data)
    return all_data


def test_transformed_data_model(all_data: list[AnimeDataModel]) -> None:
    for data in all_data:
        assert isinstance(data, AnimeDataModel)


def test_transformed_first_data_value(all_data: list[AnimeDataModel]) -> None:
    data = all_data[0]
    assert data.id == 9488
    assert data.id_mal == 9488
    assert data.romaji_title == "Cencoroll 2"
    assert data.english_title is None
    assert data.native_title == "センコロール2"
    assert data.preferred_title == "Cencoroll 2"
    assert data.type == "ANIME"
    assert data.format == "MOVIE"
    assert data.status == "FINISHED"
    assert data.description == "The second instance of the Cencoroll film series. "
    assert data.start_date == "2019-06-29"
    assert data.end_date == "2019-06-29"
    assert data.season == "SPRING"
    assert data.season_year == 2019
    assert data.episodes == 1
    assert data.duration == 48
    assert data.country_of_origin == "JP"
    assert data.source == "ORIGINAL"
    assert data.hashtag is None
    assert data.updated_at == "2026-05-27"
    assert data.genres == "Action,Sci-Fi"
    assert data.synonyms == "Cencoroll Connect"
    assert data.average_score == 70
    assert data.mean_score == 70
    assert data.popularity == 13113
    assert data.trending == 0
    assert data.favourites == 137
    assert data.animation_studio is None
