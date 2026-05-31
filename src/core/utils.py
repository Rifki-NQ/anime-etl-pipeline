import argparse
from pathlib import Path

VALID_FILE_EXTENSION = ".db"


def valid_filepath(filepath: str) -> Path:
    path = Path(filepath)
    if path.suffix.lower() != VALID_FILE_EXTENSION:
        raise argparse.ArgumentTypeError(
            "dataset file must be a db file (example: data.db)"
        )
    return path.with_name(path.stem.replace(" ", "_") + path.suffix.lower())


def validate_years_args(
    parser: argparse.ArgumentParser, args: argparse.Namespace
) -> None:
    if args.start > args.end:
        parser.error("--start year cannot be less than --end year")
