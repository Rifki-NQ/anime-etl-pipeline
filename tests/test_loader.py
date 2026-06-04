import pytest
import sqlite3
from pathlib import Path
from typing import Any
from dataclasses import fields
from tests.mock_class.mock_extractors import (
    MockAnilistExtractorNormal,
    MockAnilistExtractorUpdated,
)
from src.core.transformers.transform_anilist import AnilistTransformer
from src.core.loaders.sqlite_loader import LoadToSQLite
from src.core.models.domain_model import AnimeDataModel
from src.core.models.protocols import ExtractorProtocol


def make_loader(tmp_path: Path, extractor: ExtractorProtocol) -> LoadToSQLite:
    transformer = AnilistTransformer(extractor)
    temp_db = tmp_path / "temp_db.db"
    return LoadToSQLite(transformer, temp_db)


@pytest.fixture
def loader(tmp_path: Path) -> LoadToSQLite:
    return make_loader(tmp_path, MockAnilistExtractorNormal())


@pytest.fixture
def loader_with_updated_data(tmp_path: Path):
    return make_loader(tmp_path, MockAnilistExtractorUpdated())


def read_all_rows(filepath: Path) -> list[tuple[Any, ...]]:
    with sqlite3.connect(filepath) as conn:
        cur = conn.cursor()
        return cur.execute("SELECT * FROM anime").fetchall()


async def test_loaded_column_names(loader: LoadToSQLite) -> None:
    await loader.load_data(2019, 2019, skip_exists=False)
    with sqlite3.connect(loader.filepath) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM pragma_table_info('anime')")
        for f in fields(AnimeDataModel):
            assert f.name == cur.fetchone()[0]
    conn.close()


async def test_loaded_value_length(loader: LoadToSQLite) -> None:
    await loader.load_data(2019, 2019, skip_exists=False)
    all_data = read_all_rows(loader.filepath)
    assert len(all_data) == 100


async def test_loaded_first_data_value(loader: LoadToSQLite) -> None:
    await loader.load_data(2019, 2019, skip_exists=False)
    first_data = read_all_rows(loader.filepath)[0]
    assert first_data[0] == 9488
    assert first_data[1] == 9488
    assert first_data[2] == "Cencoroll 2"
    assert first_data[3] is None
    assert first_data[4] == "センコロール2"
    assert first_data[5] == "Cencoroll 2"
    assert first_data[6] == "ANIME"
    assert first_data[7] == "MOVIE"
    assert first_data[8] == "FINISHED"
    assert first_data[9] == "The second instance of the Cencoroll film series. "
    assert first_data[10] == "2019-06-29"
    assert first_data[11] == "2019-06-29"
    assert first_data[12] == "SPRING"
    assert first_data[13] == 2019
    assert first_data[14] == 1
    assert first_data[15] == 48
    assert first_data[16] == "JP"
    assert first_data[17] == "ORIGINAL"
    assert first_data[18] is None
    assert first_data[19] == "2026-05-27"
    assert first_data[20] == "Action,Sci-Fi"
    assert first_data[21] == "Cencoroll Connect"
    assert first_data[22] == 70
    assert first_data[23] == 70
    assert first_data[24] == 13113
    assert first_data[25] == 0
    assert first_data[26] == 137
    assert first_data[27] is None


async def test_loading_with_skip_exists(
    loader: LoadToSQLite, loader_with_updated_data: LoadToSQLite
) -> None:
    await loader.load_data(2019, 2019, skip_exists=False)
    first_data = read_all_rows(loader.filepath)[0]
    await loader_with_updated_data.load_data(2019, 2019, skip_exists=True)
    first_data_updated = read_all_rows(loader_with_updated_data.filepath)[0]
    # the only values that is updated, which is romaji title and description
    assert first_data_updated[2] == "Cencoroll 2"
    assert first_data_updated[9] == "The second instance of the Cencoroll film series. "
    assert first_data_updated == first_data


async def test_loading_without_skip_exists(
    loader: LoadToSQLite, loader_with_updated_data: LoadToSQLite
) -> None:
    await loader.load_data(2019, 2019, skip_exists=False)
    first_data = read_all_rows(loader.filepath)[0]
    await loader_with_updated_data.load_data(2019, 2019, skip_exists=False)
    first_data_updated = read_all_rows(loader_with_updated_data.filepath)[0]
    # the only values that is updated, which is romaji title and description
    assert first_data_updated[2] == "Cencoroll 2 mock updated"
    assert (
        first_data_updated[9]
        == "The second instance of the Cencoroll film series. Mock updated for test purpose"
    )
    assert not first_data_updated == first_data
