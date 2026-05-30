import argparse
import asyncio
import logging
from httpx import AsyncClient
from src.core.extractors.extract_anilist import AnilistExtractor
from src.core.transformers.transform_anilist import AnilistTransformer
from src.core.loaders.sqlite_loader import LoadToSQLite


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)-40s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anime")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)

    return parser


async def parser_args(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()

    async with AsyncClient() as client:
        extractor = AnilistExtractor(client)
        transformer = AnilistTransformer(extractor)
        loader = LoadToSQLite(transformer)

        await loader.load_data(args.start, args.end)


# package script bootstrap
def main() -> None:
    logger = logging.getLogger(__name__)
    setup_logging()

    logger.info("App started")
    asyncio.run(parser_args(build_parser()))
    logger.info("App finished")
