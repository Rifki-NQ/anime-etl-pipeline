import pytest
import sqlite3
from pathlib import Path
from typing import Any
from dataclasses import fields
from tests.mock_class.mock_extractors import MockAnilistExtractorNormal
from src.core.transformers.transform_anilist import AnilistTransformer
from src.core.loaders.sqlite_loader import LoadToSQLite
from src.core.models.domain_model import AnimeDataModel
from src.core.models.protocols import ExtractorProtocol, TransformerProtocol

@pytest.fixture
def extractor() -> ExtractorProtocol:
    return MockAnilistExtractorNormal()

@pytest.fixture
def transformer(extractor: ExtractorProtocol) -> TransformerProtocol:
    return AnilistTransformer(extractor)

@pytest.fixture
def loader(transformer: TransformerProtocol, tmp_path: Path) -> LoadToSQLite:
    temp_db = tmp_path / "temp_db.db"
    return LoadToSQLite(transformer, temp_db)

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
    data = read_all_rows(loader.filepath)[0]
    assert data[0] == 9488
    assert data[1] == 9488
    assert data[2] == "Cencoroll 2"
    assert data[3] is None
    assert data[4] == "センコロール2"
    assert data[5] == "Cencoroll 2"
    assert data[6] == "ANIME"
    assert data[7] == "MOVIE"
    assert data[8] == "FINISHED"
    assert data[9] == "The second instance of the Cencoroll film series. "
    assert data[10] == "2019-06-29"
    assert data[11] == "2019-06-29"
    assert data[12] == "SPRING"
    assert data[13] == 2019
    assert data[14] == 1
    assert data[15] == 48
    assert data[16] == "JP"
    assert data[17] == "ORIGINAL"
    assert data[18] is None
    assert data[19] == "2026-05-27"
    assert data[20] == "Action,Sci-Fi"
    assert data[21] == "Cencoroll Connect"
    assert data[22] == 70
    assert data[23] == 70
    assert data[24] == 13113
    assert data[25] == 0
    assert data[26] == 137
    assert data[27] is None
