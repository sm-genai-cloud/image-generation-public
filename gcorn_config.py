bind = '0.0.0.0:80'

# Conservative setup to avoid memory issues
workers = 1           # Only one worker to avoid model duplication
threads = 1           # No threading (use async request queue)
worker_class = 'gthread'
worker_connections = 100
timeout = 30
keepalive = 2
