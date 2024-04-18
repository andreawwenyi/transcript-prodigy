# transcript-prodigy

## Run
### Environment
```sh
conda create -n prodigy python=3.11
pip install -r requirements.txt
```

### Prepare stream
```sh
python3 make_jsonl.py {theme}
```

### Start Prodigy
```sh
python -m prodigy textcat_feedback pilot-parent Parent_fp.jsonl -F recipe.py
```

### Export annotation
```sh
python -m prodigy db-out pilot-parent > ./annotations/Parent_fp.jsonl
```

## References
1. task routing: https://prodi.gy/docs/task-routing
