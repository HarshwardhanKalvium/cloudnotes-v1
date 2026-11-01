# CloudNotes

CloudNotes uses PostgreSQL and reads runtime configuration from environment
variables. Copy `.env.example` to `.env` for local development, create the
database, then run:

```bash
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 app:app
```

See [deployment.md](deployment.md) for the Ubuntu/systemd setup and
[cloud-mapping.md](cloud-mapping.md) for the Compute Engine mapping.
