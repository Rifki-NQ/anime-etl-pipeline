import pytest
from unittest.mock import MagicMock, patch
from httpx import HTTPError
from src.core.extractors.extract_anilist import AnilistExtractor
from src.core.exceptions import MaxRetryAttemptError, InvalidYearError

# current max_attempt value = 3


@pytest.fixture
def extractor() -> AnilistExtractor:
    return AnilistExtractor(MagicMock())


async def test_retry_then_fail(extractor: AnilistExtractor) -> None:
    with (
        patch("asyncio.sleep"),
        patch.object(extractor, "_request", side_effect=HTTPError("error")) as mock_req,
    ):
        with pytest.raises(MaxRetryAttemptError):
            await extractor.get_by_page(1, 2019)
        assert mock_req.call_count == extractor.MAXIMUM_RETRY_ATTEMPT


async def test_retry_then_succeed(extractor: AnilistExtractor) -> None:
    with (
        patch("asyncio.sleep"),
        patch.object(
            extractor,
            "_request",
            side_effect=[
                HTTPError("error"),
                MagicMock(),
            ],
        ) as mock_req,
    ):
        await extractor.get_by_page(1, 2019)
        assert mock_req.call_count == 2


async def test_invalid_year_range(extractor: AnilistExtractor) -> None:
    with pytest.raises(InvalidYearError) as exc_info:
        await extractor.get_by_page(1, 20211)
    assert exc_info.value.year == 20211


async def test_request_return_empty_media_data(extractor: AnilistExtractor) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": {"Page": {"media": None}}}
    with patch.object(extractor, "_request", return_value=mock_response):
        data = await extractor.get_by_page(1, 2019)
        assert data is None
