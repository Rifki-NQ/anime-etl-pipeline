QUERY_BY_PAGE = """
    query ($page: Int, $start: FuzzyDateInt, $end: FuzzyDateInt) {
        Page (page: $page, perPage: 50) {
            media (type: ANIME, startDate_greater: $start, startDate_lesser: $end) {
                id
                idMal
                title {
                    romaji
                    english
                    native
                    userPreferred
                }
                type
                format
                status
                description
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                season
                seasonYear
                episodes
                duration
                countryOfOrigin
                source
                hashtag
                updatedAt
                genres
                synonyms
                averageScore
                meanScore
                popularity
                trending
                favourites
                studios {
                    nodes {
                        name
                        isAnimationStudio
                    }
                }
            }
        }
    }
    """
