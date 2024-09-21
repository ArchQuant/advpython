import requests
import re
import time
from timeit import timeit

US_WEBSITES = [
    "https://google.com",
    "https://youtube.com",
    "https://facebook.com",
    "https://amazon.com",
    "https://wikipedia.org",
    "https://instagram.com",
    "https://yahoo.com",
    "https://reddit.com",
    "https://microsoft.com",
    "https://instagram.com",
    "https://pinterest.com",
    "https://nytimes.com"
]

def count_https_in_urls():

    htmls = []
    for url in US_WEBSITES:
        # The + operator concat two lists and return a new list
        htmls += [requests.get(url).text]

    count_https = 0
    count_http = 0

    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    time.sleep(2.0)
    print(f"Finished")

def better_count_https_in_urls():
    htmls = []
    for url in US_WEBSITES:
        # list.append adds a single object to the current list
        htmls.append(requests.get(url).text)
    
    count_https = 0
    count_http = 0

    https = re.compile(r"https://")
    http = re.compile(r"http://")

    for html in htmls:
        count_https += len(https.findall(html))
        count_http += len(http.findall(html))

    time.sleep(2.0)
    print(f"Finished")

def profiling():
    import cProfile
    import pstats
    import snakeviz.cli as cli

    with cProfile.Profile() as pr:
        count_https_in_urls()
    
        # cProfile
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats(10)
    
    # snakeviz plot
    profile_output = "../output/count_https.prof"
    stats.dump_stats(filename=profile_output)
    cli.main([profile_output])

def main():
   # print('count_https_in_urls ', timeit(count_https_in_urls, number=1))
   # print('better_count_https_in_urls ', timeit(better_count_https_in_urls, number=1))
    profiling()

if __name__ == '__main__':
    main()