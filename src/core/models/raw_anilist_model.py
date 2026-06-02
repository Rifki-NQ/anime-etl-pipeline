from pydantic import BaseModel


class AnilistTitle(BaseModel):
    romaji: str
    english: str | None
    native: str | None
    userPreferred: str


class AnilistDate(BaseModel):
    year: int | None
    month: int | None
    day: int | None


class AnilistStudiosNodes(BaseModel):
    name: str
    isAnimationStudio: bool


class AnilistStudios(BaseModel):
    nodes: list[AnilistStudiosNodes]


class RawAnilistData(BaseModel):
    id: int
    idMal: int | None
    title: AnilistTitle
    type: str
    format: str | None
    status: str
    description: str | None
    startDate: AnilistDate
    endDate: AnilistDate
    season: str | None
    seasonYear: int | None
    episodes: int | None
    duration: int | None
    countryOfOrigin: str
    source: str | None
    hashtag: str | None
    updatedAt: int
    genres: list[str]
    synonyms: list[str]
    averageScore: int | None
    meanScore: int | None
    popularity: int
    trending: int
    favourites: int
    studios: AnilistStudios
