
## Implementation Steps
1. Initialized project with `uv` and `requirements.txt` (Flask, SQLAlchemy, Flask-SQLAlchemy, pytest).
2. Created `tips.txt` and `.trae/rules/user_rules.md`.
3. Implemented sharding logic in `models.py` using `zlib.crc32(username) % SHARD_COUNT`.
4. Created `createTable.py` to initialize tables.
5. Implemented `app.py` with `/login` route.
6. Created `templates/login.html`.
7. Wrote and passed TDD tests:
   - `tests/test_create_table.py`
   - `tests/test_models.py`
   - `tests/test_app.py`
