import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin.settings')


# Gunicorn configuration
# https://gist.github.com/kodekracker/6bc6a3a35dcfbc36e2b7

# bind - The server socket to bind
bind = "0.0.0.0:8080"

# workers - The number of worker processes for handling requests.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
workers = 2

# threads - The number of worker threads for handling requests. This will
# run each worker with the specified number of threads.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
threads = 1
