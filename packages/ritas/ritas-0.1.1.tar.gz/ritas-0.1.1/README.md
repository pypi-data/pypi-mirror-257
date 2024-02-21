# PyRitas

How to run

TBD...

## Examples

Sample data

```bash
python src/ritas/main.py data/sample.csv "epsg:26915"
```

UIowa data

```bash
python src/ritas/main.py data/Freddies_2023.csv "+proj=longlat +datum=WGS84 +no_defs"
```

## Run the app

```bash
poetry run streamlit run src/ritas/app/main.py
```
