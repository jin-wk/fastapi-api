name = "fastapi-database-gunicorn"
bind = "0.0.0.0:8000"
workers = 1
reload = True
worker_connections = 1000 * workers
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "info"
accesslog = "logs/gunicorn-access.log"

max_requests = 1000
max_requests_jitter = 50
