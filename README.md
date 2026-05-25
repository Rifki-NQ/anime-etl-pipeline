# anime-etl-pipeline

anime-etl-pipeline is my first attempt to make automated etl pipeline for anime data, this project is planned to have retry system, logged errors and designed to extract hundreds of anime entries.

---

## Tech Stacks

Below are list of libraries that will be used in this project.

### External libraries

#### [httpx](https://www.python-httpx.org/)

Used to make http request to the api, httpx is used in the extract layer that will fetch the data asynchronously.

#### [pydantic](https://pydantic.dev/docs/validation/)

Used as api data validator that lives in extract layer before sending the data to the tranform layer.

---

### Standard libraries

#### dataclass

Used as the core data model for the anime data, it will lives in the tranform layer as the domain model for the upper layers.

#### sqlite3

Used as the the local data loader, it will receive data from transform layer and save it in the disk / local storage.

---

---
