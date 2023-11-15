
# Worker

Take PDF pagestreams and turns them into usable documents. Then ingests these
documents into database and search-index.

## Developing

SQLAlchemy models are generated automatically from the database schema:
```
make sqlacodegen
```
