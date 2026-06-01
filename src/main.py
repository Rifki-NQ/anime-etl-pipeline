import argparse
import asyncio
import logging
from httpx import AsyncClient
from configs import DEFAULT_DB_PATH, DEFAULT_LOGGING_LEVEL
from src.core.utils import valid_filepath, validate_years_args
from src.core.extractors.extract_anilist import AnilistExtractor
from src.core.transformers.transform_anilist import AnilistTransformer
from src.core.loaders.sqlite_loader import LoadToSQLite

logger = logging.getLogger(__name__)


def setup_logging(logging_level: int) -> None:
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s | %(levelname)-8s | %(name)-40s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anime")
    parser.add_argument(
        "--v", action="store_const", const=10, default=DEFAULT_LOGGING_LEVEL
    )
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--sync", action="store_true", default=False)
    parser.add_argument(
        "--path", type=valid_filepath, default=DEFAULT_DB_PATH, required=False
    )

    return parser


async def parse_args(parser: argparse.ArgumentParser) -> None:

    args = parser.parse_args()
    setup_logging(args.v)
    validate_years_args(parser, args)

    logger.info("App started")
    async with AsyncClient() as client:
        extractor = AnilistExtractor(client)
        transformer = AnilistTransformer(extractor)
        loader = LoadToSQLite(transformer, args.path)

        await loader.load_data(args.start, args.end, args.sync)
    logger.info("App finished")


# package script bootstrap
def main() -> None:
    asyncio.run(parse_args(build_parser()))
