import argparse
import asyncio
from src.core.extractors.extract_anilist import AnilistExtractor
from src.core.transformers.transform_anilist import AnilistTransformer
from src.core.loaders.sqlite_loader import LoadToSQLite

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="anime")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    
    return parser
    
async def parser_args(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    
    extractor = AnilistExtractor()
    transformer = AnilistTransformer(extractor)
    loader = LoadToSQLite(transformer)
    
    await loader.load_data(args.start, args.end)
    
def main() -> None:
    asyncio.run(parser_args(build_parser()))
    
if __name__ == "__main__":
    main()