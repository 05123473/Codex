# Universal File Diff Tool (MVP)

## Run API

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

## Compare API

`POST /compare`

```json
{
  "fileA": "path/to/file_or_folder_A",
  "fileB": "path/to/file_or_folder_B"
}
```

## Test

```bash
pytest -q
```
