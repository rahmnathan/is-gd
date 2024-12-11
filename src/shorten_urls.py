import argparse
import sys
import os
import requests

from datetime import datetime
from time import sleep
from requests import RequestException

is_gd_api_url = "https://is.gd/create.php"


## is.gd has a 200req/hr rate limit
is_gd_requests_per_hour = 200
is_gd_requests_current = 0
is_gd_chunk_start = datetime.now()
seconds_per_hour = 3600

# Keep track of urls we've processed to avoid duplicates
processed_urls = set()


# Make sure we honor is.gd's rate limit
def honor_rate_limit():
    global is_gd_chunk_start
    global is_gd_requests_current

    if is_gd_requests_per_hour - is_gd_requests_current == 0:
        duration = datetime.now() - is_gd_chunk_start
        if duration.seconds < seconds_per_hour:
            print(f"We've reached is.gd's hourly limit.")
            sleep_time = (seconds_per_hour - duration.seconds) + 2 # 2 second padding just to be safe
            print(f"Sleeping for {sleep_time} seconds before continuing requests.")
            sleep(sleep_time)
            print("Resuming url shortening")

        # Reset rate-limiting params
        is_gd_chunk_start = datetime.now()
        is_gd_requests_current = 0


# call is.gd to shorten the provided URL
def shorten_url(url):
    params = {
        'format': 'simple',
        'url': url
    }

    try:
        response = requests.get(is_gd_api_url, params=params)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Failure shortening url {url}: {e}")


# Shorten the URLs in a given file
def shorten_urls(file_path):
    global is_gd_requests_current
    with open(file_path, 'r') as url_file:
        for line in url_file:
            url = line.strip()
            if url:
                # If we've already shortened this url, skip to the next
                if url in processed_urls:
                    continue

                honor_rate_limit()

                short_url = shorten_url(url)
                is_gd_requests_current += 1
                if short_url:
                    processed_urls.add(url)
                    print(f"{short_url}, {url}")


# Define and parse arguments
parser = argparse.ArgumentParser("python3 shorten_urls.py")
parser.add_argument("path", help="Path to a file (or directory of files) containing urls to shorten.", type=str)
args = parser.parse_args()


# User-supplied path
path = args.path


# Validate that path exists
if not os.path.exists(path):
    print(f"Error: File or directory '{path}' does not exist.")
    sys.exit(1)


# Collect list of url files
url_files = []
if os.path.isfile(path):
    url_files.append(path)
elif os.path.isdir(path):
    for file in os.listdir(path):
        url_files.append(os.path.join(path, file))


url_file_count = len(url_files)

# Useful log statement, but arguably violates the provided requirements
# print(f"Found {url_file_count} files at {path} to process.")


### Single threaded url shortening
for file in url_files:
    shorten_urls(file)


### Multi-threaded url shortening

# is.gd allows 5 concurrent connections
# we'll use one connection per file (up to 5)
## Need to introduce a thread Barrier (or similar) on current request count to avoid overrunning the api limit.
## For now just give ourselves an api-limit buffer
# pool = ThreadPool(url_file_count if url_file_count <= 5 else 5)
# results = pool.map(shorten_urls, url_files)
