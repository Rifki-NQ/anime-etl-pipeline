from dataclasses import dataclass


@dataclass
class AnimeDataModel:
    id: int
    id_mal: int | None
    romaji_title: str
    english_title: str | None
    native_title: str | None
    preferred_title: str
    type: str
    format: str | None
    status: str
    description: str | None
    start_date: str | None
    end_date: str | None
    season: str | None
    season_year: int | None
    episodes: int | None
    duration: int | None
    country_of_origin: str
    source: str | None
    hashtag: str | None
    updated_at: str
    genres: str | None
    synonyms: str | None
    average_score: int | None
    mean_score: int | None
    popularity: int
    trending: int
    favourites: int
    animation_studio: str | None
