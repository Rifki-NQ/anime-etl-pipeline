# anime-etl-pipeline

anime-etl-pipeline is my first attempt to make automated etl pipeline for anime data that extracts data from [Anilist GraphQL](https://docs.anilist.co/guide/graphql/). This project is designed to extract, transform and load hundreds of anime data from the api with its own retry system to minimize failure.

---

## Table of Contents

- [Architecture overview](#architecture-overview)
- [Tech Stacks](#tech-stacks)
- [Usage](#usage)

---

## Architecture overview

This project is split into three distinct layers.

### Extract layer

Extract layer has the responsibility to extract or fetch data from the api, retry system lives in this layer since HTTP request is fragile and tend to fail often.

### Transform layer

Transform layer has the responsibility to transform raw data from the api into the domain model or internal data model.

### Load layer

Load layer has the responsibility to load or save the transformed data into local storage using sqlite3.

---

## Tech Stacks

Below are list of libraries used in this project.

### External libraries

#### [httpx](https://www.python-httpx.org/)

Used to make http request to the api, httpx is used in the extract layer that will fetch the data asynchronously.

#### [pydantic](https://pydantic.dev/docs/validation/)

Used as api data validator that lives in extract layer before sending the data to the transform layer.

### Standard libraries

#### dataclass

Used as the core data model for the anime data, it will live in the transform layer as the domain model for the upper layers.

#### sqlite3

Used as the local data loader, it will receive data from transform layer and save it in the disk / local storage.

---

## Usage

```bash
anime [options]
```

### Command Options

```bash
--start    # type: int, start year of the data to fetch
--end      # type: int, end year of the data to fetch
--path     # type: str, local database filepath destination
--sync     # type: flag, update existing data on database instead of skipping it
```

### Example

```bash
anime --start 2010 --end 2020
```

> run the pipeline, anime from 2010 to 2020

---
