# irmos Practical Assignment

This project implements a small API that serves structural health data from a real bridge.
For confidentiality reasons, you’ll need to provide the CSV file yourself (`midspan_data.csv`) and place it in the data/ folder before running any scripts.

## Setup

1. Start Docker

```bash
docker compose up --build
```

2. Install Requirements

```bash
pip install -r requirements.txt
```

3. Load Data

```bash
cd data
python load_csv_to_db.py
```

4. Test the API

```bash
python test_script.py
```

## API

Endpoint: `/bridge-data/`
Response:
```json
{
  "_time": [...],
  "stress_cycle": [...],
  "pos_na": [...]
}
```

The API performs simple outlier removal, downsampling, and smoothing before returning results.

## Notes

- The project runs entirely via Docker Compose.
- Data must be located at `data/midspan_data.csv`.