class DomainError(Exception):
    """Base exception for all business / logic errors"""

    pass


class ExtractorError(DomainError):
    """Base exception for extractor error"""

    pass


class InvalidYearError(ExtractorError):
    """
    Raised when the given year is not valid in length

    invalid example: 123, 90932, 90
    valid example: 2019, 2010, 1992
    """

    def __init__(self, year: int) -> None:
        self.year = year
        super().__init__(
            f"Error: invalid year length for ({year}), expected len: 4, got: {len(str(year))}"
        )
