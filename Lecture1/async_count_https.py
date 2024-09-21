import asyncio
import httpx
import re
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


async def async_count_https_in_urls():
    
    # get URL in async style
    async with httpx.AsyncClient() as client:
        tasks = (client.get(url) for url in US_WEBSITES)
        reqs = await asyncio.gather(*tasks)

    htmls = [req.text for req in reqs]

    count_https = 0
    count_http = 0

    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print(f"Finished")

def profiling():
    import cProfile
    import pstats
    import snakeviz.cli as cli

    with cProfile.Profile() as pr:
        asyncio.run(async_count_https_in_urls())
    
    # cProfile
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(10)
    
    # snakeviz plot
    profile_output = "../output/async_count_https.prof"
    stats.dump_stats(filename=profile_output)
    cli.main([profile_output])

def main():
    profiling()

if __name__ == '__main__':
    main()