import threading
import requests
import time

# Function to fetch a URL
def fetch_url(url):
    print(f"Starting fetch for {url}")
    response = requests.get(url)
    print(f"Finished fetching {url}: {response.status_code}")

# List of URLs to fetch
urls = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.python.org",
    "https://www.wikipedia.org"
]

# Measure the start time
start_time = time.time()

# Create and start threads for fetching each URL
threads = []
for url in urls:
    thread = threading.Thread(target=fetch_url, args=(url,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Measure the end time
end_time = time.time()

print(f"All fetches completed in {end_time - start_time:.2f} seconds with multithreading.")

# Measure the start time
start_time = time.time()

# Fetch each URL sequentially (one after another)
for url in urls:
    fetch_url(url)

# Measure the end time
end_time = time.time()


print(f"All fetches completed in {end_time - start_time:.2f} seconds without multithreading.")